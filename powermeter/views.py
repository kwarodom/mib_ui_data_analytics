'''
__author__ = "Kruthika Rathinavel"
__copyright__ = "Copyright 2014, BEMOSS"
__credits__ = []
__license__ = "...."  # Pending
__version__ = "1.0.1"
__maintainer__ = "Kruthika Rathinavel"
__email__ = "kruthika@vt.edu"
__status__ = "Prototype"
__created__ = "2014-10-13 18:45:40"
'''


from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from datetime import datetime
from django.shortcuts import render_to_response
from alerts.views import get_notifications
from dashboard.models import Building_Zone, DeviceMetadata
from ZMQHelper.zmq_pub import ZMQ_PUB
from _utils import page_load_utils as _helper
import json
import os
import settings
import time

from lighting.models import Lighting
from powermeter.models import PowerMeter
from sensor.models import OccupancySensor, AmbientLightSensor, MotionSensor
from VAV.models import VAV
from RTU.models import RTU
from smartplug.models import Plugload
from thermostat.models import Thermostat

import _utils.defaults as __

kwargs = {'subscribe_address': __.SUB_SOCKET,
                    'publish_address': __.PUSH_SOCKET}

zmq_pub = ZMQ_PUB(**kwargs)


@login_required(login_url='/login/')
def powermeter(request, mac):
    print 'inside powermeter view method'
    context = RequestContext(request)
    username = request.session.get('user')
    print username
    if request.session.get('last_visit'):
    # The session has a value for the last visit
        last_visit_time = request.session.get('last_visit')

        visits = request.session.get('visits', 0)

        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] = visits + 1
    else:
        # The get returns None, and the session does not have a value for the last visit.
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1

    print type(mac)
    mac = mac.encode('ascii', 'ignore')
    print type(mac)

    device_metadata = [ob.device_control_page_info() for ob in DeviceMetadata.objects.filter(mac_address=mac)]
    print device_metadata
    device_id = device_metadata[0]['device_id']
    device_type_id = device_metadata[0]['device_model_id']
    device_type_id = device_type_id.device_model_id
    device_type = device_metadata[0]['device_type']

    device_status = [ob.data_as_json() for ob in PowerMeter.objects.filter(power_meter_id=device_id)]
    device_zone = device_status[0]['zone']['id']
    device_nickname = device_status[0]['nickname']
    zone_nickname = device_status[0]['zone']['zone_nickname']

    '''
    device_info = [ob.as_json() for ob in Device_Info.objects.filter(mac_address=mac)]
    device_id = device_info[0]['id']
    device_zone = device_info[0]['zone']['id']
    device_nickname = device_info[0]['nickname']
    zone_nickname = device_info[0]['zone']['zone_nickname']
    device_type_id = device_info[0]['device_type_id']
    print device_type_id
    print device_zone 
    '''

    info_required = "Update Hue data"
    powermeter_update_send_topic = '/ui/agent/bemoss/' + str(device_zone) + '/' + device_type + '/' + device_id + '/device_status'
    zmq_pub.requestAgent(powermeter_update_send_topic, info_required, "text/plain", "UI")
    '''
    json_file = open(os.path.join(settings.PROJECT_DIR, 'resources/page_load/page_load.json'), "r+")
    _json_data = json.load(json_file)
    if device_id not in _json_data[device_type]:
        _json_data[device_type][device_id] = {"page_load": "{empty_string}"}

    json_file.seek(0)
    json_file.write(json.dumps(_json_data, indent=4, sort_keys=True))
    json_file.truncate()
    json_file.close()

    time.sleep(3)'''

    _data = _helper.get_page_load_data(device_id, device_type, device_type_id)

    zones = [ob.as_json() for ob in Building_Zone.objects.all()]
    thermostats_sn = [ob.data_side_nav() for ob in Thermostat.objects.filter(network_status='ONLINE', thermostat_id__bemoss=True)]
    vav_sn = [ob.data_side_nav() for ob in VAV.objects.filter(network_status='ONLINE', vav_id__bemoss=True)]
    rtu_sn = [ob.data_side_nav() for ob in RTU.objects.filter(network_status='ONLINE', rtu_id__bemoss=True)]
    lighting_sn = [ob.data_side_nav() for ob in Lighting.objects.filter(network_status='ONLINE', lighting_id__bemoss=True)]
    plugload_sn = [ob.data_side_nav() for ob in Plugload.objects.filter(network_status='ONLINE', plugload_id__bemoss=True)]
    occ_sensors_sn = [ob.data_side_nav() for ob in OccupancySensor.objects.filter(network_status='ONLINE', occupancy_sensor_id__bemoss=True)]
    lt_sensors_sn = [ob.data_side_nav() for ob in AmbientLightSensor.objects.filter(network_status='ONLINE', ambient_light_sensor_id__bemoss=True)]
    mtn_sensors_sn = [ob.data_side_nav() for ob in MotionSensor.objects.filter(network_status='ONLINE', motion_sensor_id__bemoss=True)]
    powermeters_sn = [ob.data_side_nav() for ob in PowerMeter.objects.filter(network_status='ONLINE', power_meter_id__bemoss=True)]
    active_al = get_notifications()
    context.update({'active_al':active_al})
    context.update({
            'zones': zones, 'thermostat_sn': thermostats_sn,
             'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn, 'occ_sensors_sn': occ_sensors_sn,
             'lt_sensors_sn': lt_sensors_sn, 'mtn_sensors_sn': mtn_sensors_sn,  'powermeters_sn': powermeters_sn,
             'vav_sn': vav_sn, 'rtu_sn': rtu_sn
            })

    return render_to_response(
        'powermeter/powermeter.html',
        {'device_data': _data, 'device_id': device_id, 'device_zone': device_zone, 'zone_nickname': zone_nickname,
         'mac_address': mac, 'device_nickname': device_nickname, 'zones': zones, 'thermostat_sn': thermostats_sn,
         'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn, 'occ_sensors_sn': occ_sensors_sn,
         'lt_sensors_sn': lt_sensors_sn, 'mtn_sensors_sn': mtn_sensors_sn,  'powermeters_sn': powermeters_sn,
         'vav_sn': vav_sn, 'rtu_sn': rtu_sn, 'device_type_id': device_type_id},
        context)
