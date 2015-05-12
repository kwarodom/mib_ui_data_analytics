# -*- coding: utf-8 -*-
# Authors: Kruthika Rathinavel
# Version: 2.0
# Email: kruthika@vt.edu
# Created: "2014-10-13 18:45:40"
# Updated: "2015-02-13 15:06:41"


# Copyright © 2014 by Virginia Polytechnic Institute and State University
# All rights reserved
#
# Virginia Polytechnic Institute and State University (Virginia Tech) owns the copyright for the BEMOSS software and
# and its associated documentation ("Software") and retains rights to grant research rights under patents related to
# the BEMOSS software to other academic institutions or non-profit research institutions.
# You should carefully read the following terms and conditions before using this software.
# Your use of this Software indicates your acceptance of this license agreement and all terms and conditions.
#
# You are hereby licensed to use the Software for Non-Commercial Purpose only.  Non-Commercial Purpose means the
# use of the Software solely for research.  Non-Commercial Purpose excludes, without limitation, any use of
# the Software, as part of, or in any way in connection with a product or service which is sold, offered for sale,
# licensed, leased, loaned, or rented.  Permission to use, copy, modify, and distribute this compilation
# for Non-Commercial Purpose to other academic institutions or non-profit research institutions is hereby granted
# without fee, subject to the following terms of this license.
#
# Commercial Use: If you desire to use the software for profit-making or commercial purposes,
# you agree to negotiate in good faith a license with Virginia Tech prior to such profit-making or commercial use.
# Virginia Tech shall have no obligation to grant such license to you, and may grant exclusive or non-exclusive
# licenses to others. You may contact the following by email to discuss commercial use:: vtippatents@vtip.org
#
# Limitation of Liability: IN NO EVENT WILL VIRGINIA TECH, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR REDISTRIBUTE
# THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR
# CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO
# LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE
# OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF VIRGINIA TECH OR OTHER PARTY HAS BEEN ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGES.
#
# For full terms and conditions, please visit https://bitbucket.org/bemoss/bemoss_os.
#
# Address all correspondence regarding this license to Virginia Tech's electronic mail address: vtippatents@vtip.org

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from datetime import datetime
from alerts.views import get_notifications
from dashboard.models import DeviceMetadata, Building_Zone
from powermeter.models import PowerMeter
from thermostat.models import Thermostat
from lighting.models import Lighting
from smartplug.models import Plugload
from sensor.models import AmbientLightSensor, MotionSensor, OccupancySensor
from VAV.models import VAV
from RTU.models import RTU
from ZMQHelper.zmq_pub import ZMQ_PUB
from _utils import page_load_utils as _helper
import logging
import os
import settings
import json
import time

logger = logging.getLogger("views")

import _utils.defaults as __

kwargs = {'subscribe_address': __.SUB_SOCKET,
                    'publish_address': __.PUSH_SOCKET}

zmq_pub = ZMQ_PUB(**kwargs)


@login_required(login_url='/login/')
def rtu_view(request, mac):
    print 'RTU pageload'
    context = RequestContext(request)
    mac = mac.encode('ascii', 'ignore')
    #username = request.session.get('user')
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


    device_metadata = [ob.device_control_page_info() for ob in DeviceMetadata.objects.filter(mac_address=mac)]
    print device_metadata
    device_id = device_metadata[0]['device_id']
    device_type = device_metadata[0]['device_type']
    device_type_id = device_metadata[0]['device_model_id']
    device_type_id = device_type_id.device_model_id

    device_status = [ob.as_json() for ob in RTU.objects.filter(rtu_id=device_id)]
    device_zone = device_status[0]['zone']['id']
    device_nickname = device_status[0]['nickname']
    zone_nickname = device_status[0]['zone']['zone_nickname']

    info_required = "Update RTU data"
    ieb_topic = '/ui/agent/bemoss/' + str(device_zone) + '/' + device_type + '/' + device_id + '/device_status'
    zmq_pub.requestAgent(ieb_topic, info_required, "text/plain", "UI")
    '''
    json_file = open(os.path.join(settings.PROJECT_DIR, 'resources/page_load/page_load.json'), "r+")
    _json_data = json.load(json_file)
    if device_id not in _json_data['rtu']:
        _json_data['rtu'][device_id] = {"page_load": "{empty_string}"}

    json_file.seek(0)
    json_file.write(json.dumps(_json_data, indent=4, sort_keys=True))
    json_file.truncate()
    json_file.close()

    time.sleep(3)'''
    #Using page_load.json
    vals = _helper.get_page_load_data(device_id, device_type, device_type_id)

    if vals['cooling_mode'] == 'NONE':
        vals['cooling_mode'] = "None"
    elif vals['cooling_mode'] == 'STG1':
        vals['cooling_mode'] = "Stage 1 Cooling"
    elif vals['cooling_mode'] == 'STG2':
        vals['cooling_mode'] = "Stage 2 Cooling"
    elif vals['cooling_mode'] == 'STG3':
        vals['cooling_mode'] = "Stage 3 Cooling"
    elif vals['cooling_mode'] == 'STG4':
        vals['cooling_mode'] = "Stage 4 Cooling"

    zones = [ob.as_json() for ob in Building_Zone.objects.all()]
    thermostats_sn = [ob.data_side_nav() for ob in Thermostat.objects.filter(network_status='ONLINE')]
    vav_sn = [ob.data_side_nav() for ob in VAV.objects.filter(network_status='ONLINE')]
    rtu_sn = [ob.data_side_nav() for ob in RTU.objects.filter(network_status='ONLINE')]
    lighting_sn = [ob.data_side_nav() for ob in Lighting.objects.filter(network_status='ONLINE')]
    plugload_sn = [ob.data_side_nav() for ob in Plugload.objects.filter(network_status='ONLINE')]
    occ_sensors_sn = [ob.data_side_nav() for ob in OccupancySensor.objects.filter(network_status='ONLINE')]
    lt_sensors_sn = [ob.data_side_nav() for ob in AmbientLightSensor.objects.filter(network_status='ONLINE')]
    mtn_sensors_sn = [ob.data_side_nav() for ob in MotionSensor.objects.filter(network_status='ONLINE')]
    powermeters_sn = [ob.data_side_nav() for ob in PowerMeter.objects.filter(network_status='ONLINE')]

    active_al = get_notifications()
    context.update({'active_al':active_al})
    context.update({
        'zones': zones, 'thermostat_sn': thermostats_sn,
         'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn, 'occ_sensors_sn': occ_sensors_sn,
         'lt_sensors_sn': lt_sensors_sn, 'mtn_sensors_sn': mtn_sensors_sn,  'powermeters_sn': powermeters_sn,
         'vav_sn': vav_sn, 'rtu_sn': rtu_sn
    })

    return render_to_response(
        'thermostat/rtu.html',
        {'device_id': device_id, 'device_zone': device_zone, 'zone_nickname': zone_nickname, 'mac_address': mac,
         'device_nickname': device_nickname, 'device_status': vals, 'zones': zones, 'thermostat_sn': thermostats_sn,
         'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn, 'occ_sensors_sn': occ_sensors_sn,
         'lt_sensors_sn': lt_sensors_sn, 'mtn_sensors_sn': mtn_sensors_sn,  'powermeters_sn': powermeters_sn,
         'vav_sn': vav_sn, 'rtu_sn': rtu_sn, 'mac': mac},
        context)


@login_required(login_url='/login/')
def submit_rtu_data(request):
    if request.POST:
        _data = request.body
        json_data = json.loads(_data)

        update_number = "Test1"

        device_info = json_data['device_info']
        print device_info

        json_data.pop('device_info')
        print json_data

        ieb_topic = '/ui/agent/bemoss/'+device_info+'/update'
        print ieb_topic
        content_type = "application/json"
        fromUI = "UI"
        print "entering in sending message to agent"

        zmq_pub.sendToAgent(ieb_topic, json_data, content_type, fromUI)
        print "success in sending message to agent"

        a_dict = {'update_number': update_number}
        json_data.update(a_dict)
        print json_data

        if request.is_ajax():
            return HttpResponse(json.dumps(json_data), mimetype='application/json')

