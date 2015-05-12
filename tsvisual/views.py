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

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponse
from alerts.views import get_notifications
from dashboard.models import Building_Zone, DeviceMetadata
from powerdb2.smap.models import Stream, Subscription, Metadata2
from thermostat.models import Thermostat
from lighting.models import Lighting
from smartplug.models import Plugload
from sensor.models import AmbientLightSensor, MotionSensor, OccupancySensor
from VAV.models import VAV
from RTU.models import RTU
from powermeter.models import PowerMeter
import json
import urllib2


@login_required(login_url='/login/')
def smap_plot_thermostat(request, mac):
    """Page load definition for thermostat statistics."""
    print "inside smap view method"
    context = RequestContext(request)
    if request.method == 'GET':

        device_metadata = [ob.device_control_page_info() for ob in DeviceMetadata.objects.filter(mac_address=mac)]
        print device_metadata
        device_id = device_metadata[0]['device_id']
        device_type_id = device_metadata[0]['device_model_id']
        mac_address = device_metadata[0]['mac_address']
        device_type_id = device_type_id.device_model_id
        print device_type_id

        device_status = [ob.data_as_json() for ob in Thermostat.objects.filter(thermostat_id=device_id)]
        device_zone = device_status[0]['zone']['id']
        device_nickname = device_status[0]['nickname']
        zone_nickname = device_status[0]['zone']['zone_nickname']

        device_info = str(device_zone) + '/thermostat/' + device_id
        device_info = device_info.encode('ascii', 'ignore')
        device_smap_tag = '/bemoss/' + str(device_zone) + '/thermostat/' + device_id
        device_smap_tag = device_smap_tag.encode('ascii', 'ignore')
        temperature = device_smap_tag + '/temperature'
        heat_setpoint = device_smap_tag + '/heat_setpoint'
        cool_setpoint = device_smap_tag + '/cool_setpoint'
        print temperature

        _uuid_temperature = get_uuid_for_data_point(temperature)
        _uuid_heat_setpoint = get_uuid_for_data_point(heat_setpoint)
        _uuid_cool_setpoint = get_uuid_for_data_point(cool_setpoint)

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

        rs_temperature = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_temperature)
        rs_heat_setpoint = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_heat_setpoint)
        rs_cool_setpoint = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_cool_setpoint)

        return render_to_response(
            'statistics/statistics_thermostat.html',
            {'temperature': rs_temperature, 'heat_setpoint': rs_heat_setpoint, 'cool_setpoint': rs_cool_setpoint,
              'device_info': device_info, 'mac': mac_address,
             'nickname': device_nickname,
             'zone_nickname': zone_nickname},
            context)


@login_required(login_url='/login/')
def auto_update_smap_thermostat(request):
    if request.method == 'POST':
        print 'inside smap auto update thermostat'
        _data = request.body
        _data = json.loads(_data)
        device_info = _data['device_info']

        device_smap_tag = '/bemoss/' + device_info.encode('ascii', 'ignore')
        device_smap_tag = device_smap_tag.encode('ascii', 'ignore')
        temperature = device_smap_tag + '/temperature'
        heat_setpoint = device_smap_tag + '/heat_setpoint'
        cool_setpoint = device_smap_tag + '/cool_setpoint'

        _uuid_temperature = get_uuid_for_data_point(temperature)
        _uuid_heat_setpoint = get_uuid_for_data_point(heat_setpoint)
        _uuid_cool_setpoint = get_uuid_for_data_point(cool_setpoint)

        rs_temperature = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_temperature)
        rs_heat_setpoint = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_heat_setpoint)
        rs_cool_setpoint = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_cool_setpoint)

        json_result = {
            'temperature': rs_temperature,
            'heat_setpoint': rs_heat_setpoint,
            'cool_setpoint': rs_cool_setpoint
        }

        print 'test'
        if request.is_ajax():
                return HttpResponse(json.dumps(json_result), mimetype='application/json')


@login_required(login_url='/login/')
def auto_update_smap_lighting(request):
    if request.method == 'POST':
        print 'inside smap auto update lighting'
        _data = request.body
        _data = json.loads(_data)
        device_info = _data['device_info']

        device_smap_tag = '/bemoss/' + device_info.encode('ascii', 'ignore')
        device_smap_tag = device_smap_tag.encode('ascii', 'ignore')

        status = device_smap_tag + '/status'
        brightness = device_smap_tag + '/brightness'

        _uuid_status = get_uuid_for_data_point(status)
        _uuid_brightness = get_uuid_for_data_point(brightness)

        rs_status = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_status)
        rs_brightness = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_brightness)

        json_result = {
            'status': rs_status,
            'brightness': rs_brightness
        }

        print 'test'
        if request.is_ajax():
            return HttpResponse(json.dumps(json_result), mimetype='application/json')


@login_required(login_url='/login/')
def smap_plot_lighting(request, mac):
    print "inside smap view method for lighting"
    context = RequestContext(request)
    if request.method == 'GET':

        device_metadata = [ob.device_control_page_info() for ob in DeviceMetadata.objects.filter(mac_address=mac)]
        print device_metadata
        device_id = device_metadata[0]['device_id']
        device_type_id = device_metadata[0]['device_model_id']
        device_type_id = device_type_id.device_model_id
        print device_type_id

        device_status = [ob.data_as_json() for ob in Lighting.objects.filter(lighting_id=device_id)]
        device_zone = device_status[0]['zone']['id']
        device_nickname = device_status[0]['nickname']
        zone_nickname = device_status[0]['zone']['zone_nickname']

        device_info = str(device_zone) + '/lighting/' + device_id
        device_info = device_info.encode('ascii', 'ignore')
        device_smap_tag = '/bemoss/' + str(device_zone) + '/lighting/' + device_id
        device_smap_tag = device_smap_tag.encode('ascii', 'ignore')
        status = device_smap_tag + '/status'
        brightness = device_smap_tag + '/brightness'
        print status

        _uuid_status = get_uuid_for_data_point(status)
        _uuid_brightness = get_uuid_for_data_point(brightness)

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

        rs_status = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_status)
        rs_brightness = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_brightness)

        return render_to_response(
            'statistics/statistics_lighting.html',
            {'status': rs_status, 'brightness': rs_brightness,
             'device_info': device_info, 'nickname': device_nickname, 'zone_nickname': zone_nickname,
            'device_type_id': device_type_id, 'zones': zones, 'mac': mac}, context)


@login_required(login_url='/login/')
def smap_plot_plugload(request, mac):
    print "inside smap view method for plugload"
    context = RequestContext(request)
    if request.method == 'GET':
        '''
        device_info = [ob.as_json() for ob in Device_Info.objects.filter(mac_address=mac)]
        print device_info
        device_id = device_info[0]['id']
        device_zone = device_info[0]['zone']['id']
        device_nickname = device_info[0]['nickname']
        device_zone_nickname = device_info[0]['zone']['zone_nickname']
        device_type_id = device_info[0]['device_type_id']
        '''

        device_metadata = [ob.device_control_page_info() for ob in DeviceMetadata.objects.filter(mac_address=mac)]
        print device_metadata
        device_id = device_metadata[0]['device_id']
        device_type_id = device_metadata[0]['device_model_id']
        device_type_id = device_type_id.device_model_id

        if device_type_id == '2WL':
            device_status = [ob.data_as_json() for ob in Lighting.objects.filter(lighting_id=device_id)]
            device_zone = device_status[0]['zone']['id']
            device_nickname = device_status[0]['nickname']
            zone_nickname = device_status[0]['zone']['zone_nickname']

            device_info = str(device_zone) + '/lighting/' + device_id
            device_info = device_info.encode('ascii', 'ignore')
            device_smap_tag = '/bemoss/' + str(device_zone) + '/lighting/' + device_id
        else:
            device_status = [ob.data_as_json() for ob in Plugload.objects.filter(plugload_id=device_id)]
            device_zone = device_status[0]['zone']['id']
            device_nickname = device_status[0]['nickname']
            zone_nickname = device_status[0]['zone']['zone_nickname']

            device_info = str(device_zone) + '/plugload/' + device_id
            device_info = device_info.encode('ascii', 'ignore')
            device_smap_tag = '/bemoss/' + str(device_zone) + '/plugload/' + device_id


        device_smap_tag = device_smap_tag.encode('ascii', 'ignore')
        status = device_smap_tag + '/status'
        print status

        _uuid_status = get_uuid_for_data_point(status)

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

        rs_status = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_status)

        return render_to_response(
            'statistics/statistics_plugload.html',
            {'status': rs_status, 'zones': zones, 'mac': mac,
             'device_info': device_info, 'nickname': device_nickname, 'zone_nickname': zone_nickname,
             'device_type_id': device_type_id}, context)


@login_required(login_url='/login/')
def auto_update_smap_plugload(request):
    if request.method == 'POST':
        print 'inside smap auto update plugload'
        _data = request.body
        _data = json.loads(_data)
        device_info = _data['device_info']

        device_smap_tag = '/bemoss/' + device_info.encode('ascii', 'ignore')
        device_smap_tag = device_smap_tag.encode('ascii', 'ignore')

        status = device_smap_tag + '/status'

        _uuid_status = get_uuid_for_data_point(status)

        rs_status = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_status)

        json_result = {
            'status': rs_status
        }

        print 'test'
        if request.is_ajax():
            return HttpResponse(json.dumps(json_result), mimetype='application/json')


def get_uuid_for_data_point(tagval):
    metadata = Metadata2.objects.using('smap').filter(tagval=tagval)
    stream_id = metadata[0].stream_id
    print stream_id
    stream_object = Stream.objects.using('smap').filter(id=stream_id)
    _uuid = stream_object[0].uuid
    print _uuid
    return _uuid.encode('ascii', 'ignore')


@login_required(login_url='/login/')
def smap_plot_occupancy(request, mac):
    print "inside smap view method for occupancy"
    context = RequestContext(request)
    if request.method == 'GET':


        device_metadata = [ob.device_control_page_info() for ob in DeviceMetadata.objects.filter(mac_address=mac)]
        print device_metadata
        device_id = device_metadata[0]['device_id']
        device_type_id = device_metadata[0]['device_model_id']
        device_type_id = device_type_id.device_model_id
        print device_type_id

        device_status = [ob.data_as_json() for ob in OccupancySensor.objects.filter(occupancy_sensor_id=device_id)]
        device_zone = device_status[0]['zone']['id']
        device_nickname = device_status[0]['nickname']
        zone_nickname = device_status[0]['zone']['zone_nickname']

        device_info = str(device_zone) + '/occupancy_sensor/' + device_id
        device_info = device_info.encode('ascii', 'ignore')
        device_smap_tag = '/bemoss/' + str(device_zone) + '/occupancy_sensor/' + device_id

        device_smap_tag = device_smap_tag.encode('ascii', 'ignore')
        status = device_smap_tag + '/space_occupied'
        print status

        _uuid_status = get_uuid_for_data_point(status)

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

        rs_status = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_status)

        return render_to_response(
            'statistics/statistics_occupancy.html',
            {'status': rs_status, 'mac': mac,
             'device_info': device_info, 'nickname': device_nickname, 'zone_nickname': zone_nickname,
             'device_type_id': device_type_id}, context)


@login_required(login_url='/login/')
def auto_update_smap_occupancy(request):
    if request.method == 'POST':
        print 'inside smap auto update occupancy sensor'
        _data = request.body
        _data = json.loads(_data)
        device_info = _data['device_info']

        device_smap_tag = '/bemoss/' + device_info.encode('ascii', 'ignore')
        device_smap_tag = device_smap_tag.encode('ascii', 'ignore')

        status = device_smap_tag + '/space_occupied'

        _uuid_status = get_uuid_for_data_point(status)

        rs_status = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_status)

        json_result = {
            'status': rs_status
        }

        print 'test'
        if request.is_ajax():
            return HttpResponse(json.dumps(json_result), mimetype='application/json')


@login_required(login_url='/login/')
def smap_plot_daylight_sensor(request, mac):
    print "inside smap view method for day light sensor"
    context = RequestContext(request)
    if request.method == 'GET':

        device_metadata = [ob.device_control_page_info() for ob in DeviceMetadata.objects.filter(mac_address=mac)]
        print device_metadata
        device_id = device_metadata[0]['device_id']
        device_type_id = device_metadata[0]['device_model_id']
        device_type_id = device_type_id.device_model_id
        print device_type_id

        device_status = [ob.data_as_json() for ob in AmbientLightSensor.objects.filter(ambient_light_sensor_id=device_id)]
        device_zone = device_status[0]['zone']['id']
        device_nickname = device_status[0]['nickname']
        zone_nickname = device_status[0]['zone']['zone_nickname']

        device_info = str(device_zone) + '/ambient_light_sensor/' + device_id
        device_info = device_info.encode('ascii', 'ignore')
        device_smap_tag = '/bemoss/' + str(device_zone) + '/ambient_light_sensor/' + device_id

        device_smap_tag = device_smap_tag.encode('ascii', 'ignore')
        status = device_smap_tag + '/illuminance'
        print status

        _uuid_status = get_uuid_for_data_point(status)

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

        rs_status = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_status)

        #parsed_json = [[1406349525000.0, 74.0], [1406349581000.0, 74.0], [1406349641000.0, 74.0], [1406349701000.0, 74.0], [1406349762000.0, 74.0], [1406349822000.0, 74.0], [1406349882000.0, 74.0], [1406349942000.0, 74.0], [1406350002000.0, 74.0], [1406350065000.0, 74.0], [1406350122000.0, 74.0], [1406350181000.0, 74.0], [1406350240000.0, 74.0], [1406350302000.0, 74.5], [1406350363000.0, 74.5], [1406350422000.0, 74.5], [1406350481000.0, 74.5], [1406350543000.0, 74.5], [1406350602000.0, 74.5], [1406350662000.0, 74.5], [1406350721000.0, 74.5], [1406350782000.0, 74.5], [1406350843000.0, 74.5], [1406350902000.0, 74.5], [1406350961000.0, 74.5], [1406351024000.0, 74.5], [1406351083000.0, 74.5], [1406351141000.0, 74.5], [1406351202000.0, 74.5], [1406351263000.0, 74.5], [1406351321000.0, 74.5], [1406351384000.0, 74.5], [1406351441000.0, 74.5], [1406351502000.0, 76.0], [1406351561000.0, 76.0], [1406351621000.0, 76.0], [1406351682000.0, 76.0], [1406351742000.0, 76.0], [1406351802000.0, 76.0], [1406351862000.0, 76.0], [1406351922000.0, 76.0], [1406351982000.0, 76.0], [1406352041000.0, 76.0], [1406352102000.0, 76.0], [1406352161000.0, 76.0], [1406352222000.0, 76.0], [1406352282000.0, 76.0], [1406352342000.0, 76.0], [1406352402000.0, 76.0], [1406352461000.0, 76.0], [1406352522000.0, 76.0], [1406352582000.0, 76.0], [1406352642000.0, 76.0], [1406352702000.0, 76.0], [1406352761000.0, 76.0], [1406352822000.0, 76.0], [1406352882000.0, 76.0], [1406352942000.0, 76.0], [1406353001000.0, 76.0], [1406353063000.0, 76.0], [1406353122000.0, 76.0], [1406353182000.0, 76.0], [1406353241000.0, 76.0], [1406353302000.0, 76.0], [1406353362000.0, 76.0], [1406353422000.0, 76.0], [1406353481000.0, 76.0], [1406353541000.0, 76.0], [1406353601000.0, 76.0], [1406353662000.0, 76.0], [1406353722000.0, 76.0], [1406353786000.0, 76.0], [1406353841000.0, 76.0], [1406353901000.0, 76.0], [1406353962000.0, 76.0], [1406354024000.0, 76.0], [1406354081000.0, 76.0], [1406354141000.0, 76.0], [1406354202000.0, 76.0], [1406354263000.0, 76.0], [1406354322000.0, 76.0], [1406354382000.0, 76.0], [1406354442000.0, 76.0], [1406354503000.0, 76.0], [1406354562000.0, 76.0], [1406354625000.0, 76.0], [1406354681000.0, 76.0], [1406354743000.0, 76.0], [1406354803000.0, 76.0], [1406354861000.0, 76.0], [1406354921000.0, 76.0], [1406354981000.0, 76.0], [1406355042000.0, 76.0], [1406355103000.0, 76.0], [1406355161000.0, 76.0], [1406355223000.0, 76.0], [1406355282000.0, 76.0], [1406355343000.0, 76.0], [1406355402000.0, 76.0], [1406355464000.0, 76.0], [1406355522000.0, 76.0], [1406355582000.0, 76.0], [1406355642000.0, 76.0], [1406355701000.0, 76.0], [1406355763000.0, 76.0], [1406355822000.0, 76.0], [1406355887000.0, 76.0], [1406355942000.0, 76.0], [1406356001000.0, 76.0], [1406356062000.0, 76.0], [1406356122000.0, 76.0], [1406356183000.0, 76.0], [1406356241000.0, 76.0], [1406356302000.0, 76.0], [1406356362000.0, 76.0], [1406356425000.0, 76.0], [1406356481000.0, 76.0], [1406356542000.0, 76.0], [1406356602000.0, 76.0], [1406356664000.0, 76.0], [1406356722000.0, 76.0], [1406356780000.0, 76.0], [1406356842000.0, 76.0], [1406356903000.0, 76.0], [1406356963000.0, 76.0], [1406357022000.0, 76.0], [1406357081000.0, 76.0], [1406357142000.0, 76.0], [1406357202000.0, 76.0], [1406357261000.0, 76.0], [1406357322000.0, 76.0], [1406357383000.0, 76.0], [1406357442000.0, 76.0], [1406357505000.0, 76.0], [1406357561000.0, 76.0], [1406357621000.0, 76.0], [1406357682000.0, 76.0], [1406357742000.0, 76.0], [1406357802000.0, 76.0], [1406357862000.0, 76.0], [1406357921000.0, 76.0], [1406357982000.0, 76.0], [1406358041000.0, 76.0], [1406358101000.0, 76.0], [1406358161000.0, 76.0], [1406358222000.0, 76.0], [1406358283000.0, 76.0], [1406358340000.0, 76.0], [1406358401000.0, 76.0], [1406358462000.0, 76.0], [1406358522000.0, 76.0], [1406358582000.0, 76.0], [1406358643000.0, 76.0], [1406358702000.0, 76.0], [1406358761000.0, 76.0], [1406358824000.0, 76.0], [1406358882000.0, 76.0], [1406358942000.0, 76.0], [1406359002000.0, 76.0], [1406359063000.0, 76.0], [1406359122000.0, 76.0], [1406359182000.0, 76.0], [1406359243000.0, 76.0], [1406359300000.0, 76.0], [1406359363000.0, 76.0], [1406359422000.0, 76.0], [1406359481000.0, 76.0], [1406359542000.0, 76.0], [1406359601000.0, 76.0], [1406359661000.0, 76.0], [1406359722000.0, 76.0], [1406359782000.0, 76.0], [1406359842000.0, 76.0], [1406359901000.0, 76.0], [1406359962000.0, 76.0], [1406360021000.0, 76.0], [1406360081000.0, 76.0], [1406360141000.0, 76.0], [1406360202000.0, 76.0], [1406360261000.0, 76.0], [1406360322000.0, 76.0], [1406360385000.0, 76.0], [1406360443000.0, 76.0], [1406360502000.0, 76.0], [1406360565000.0, 76.0], [1406360623000.0, 76.0], [1406360681000.0, 76.0], [1406360742000.0, 76.0], [1406360801000.0, 76.0], [1406360861000.0, 76.0], [1406360923000.0, 76.0], [1406360981000.0, 76.0], [1406361041000.0, 76.0], [1406361102000.0, 76.0], [1406361161000.0, 76.0], [1406361224000.0, 76.0], [1406361281000.0, 76.0], [1406361342000.0, 76.0], [1406361403000.0, 76.0], [1406361462000.0, 76.0], [1406361521000.0, 76.0], [1406361582000.0, 76.0], [1406361645000.0, 76.0], [1406361702000.0, 76.0], [1406361761000.0, 76.0], [1406361826000.0, 76.0], [1406361883000.0, 76.0], [1406361942000.0, 76.0], [1406362002000.0, 76.0], [1406362061000.0, 76.0], [1406362123000.0, 76.0], [1406362184000.0, 76.0], [1406362246000.0, 76.0], [1406362302000.0, 76.0], [1406362363000.0, 76.0], [1406362423000.0, 76.0], [1406362483000.0, 76.0], [1406362543000.0, 76.0], [1406362602000.0, 76.0], [1406362661000.0, 76.0], [1406362722000.0, 76.0], [1406362782000.0, 76.0], [1406362843000.0, 76.0], [1406362901000.0, 76.0], [1406362962000.0, 76.0], [1406363023000.0, 76.0], [1406363085000.0, 76.0], [1406363141000.0, 76.0], [1406363201000.0, 76.0], [1406363262000.0, 76.0], [1406363323000.0, 76.0], [1406363382000.0, 76.0], [1406363443000.0, 76.0], [1406363503000.0, 76.0], [1406363562000.0, 76.0], [1406363623000.0, 76.0], [1406363682000.0, 76.0], [1406363742000.0, 76.0], [1406363802000.0, 76.0], [1406363861000.0, 76.0], [1406363923000.0, 76.0], [1406363982000.0, 76.0], [1406364044000.0, 76.0], [1406364101000.0, 76.0], [1406364162000.0, 76.0], [1406364225000.0, 76.0], [1406364283000.0, 76.0], [1406364340000.0, 76.0], [1406364403000.0, 76.0], [1406364462000.0, 76.0], [1406364522000.0, 76.0], [1406364582000.0, 76.0], [1406364643000.0, 76.0], [1406364702000.0, 76.0], [1406364761000.0, 76.0], [1406364822000.0, 76.0], [1406364882000.0, 76.0], [1406364943000.0, 76.0], [1406365003000.0, 76.0], [1406365061000.0, 76.0], [1406365123000.0, 76.0], [1406365181000.0, 76.0], [1406365242000.0, 76.0], [1406365302000.0, 76.0], [1406365361000.0, 76.0], [1406365423000.0, 76.0], [1406365482000.0, 76.0], [1406365546000.0, 76.0], [1406365602000.0, 76.0], [1406365662000.0, 76.0], [1406365723000.0, 76.0], [1406365782000.0, 76.0], [1406365842000.0, 76.0], [1406365902000.0, 76.0], [1406365962000.0, 76.0], [1406366023000.0, 76.0], [1406366086000.0, 76.0], [1406366142000.0, 76.0], [1406366202000.0, 76.0], [1406366261000.0, 76.0], [1406366323000.0, 76.0], [1406366382000.0, 76.0], [1406366445000.0, 76.0], [1406366503000.0, 76.0], [1406366562000.0, 76.0], [1406366625000.0, 76.0], [1406366681000.0, 76.0], [1406366741000.0, 76.0], [1406366802000.0, 76.0], [1406366863000.0, 76.0], [1406366921000.0, 76.0], [1406366982000.0, 76.0], [1406367043000.0, 76.0], [1406367101000.0, 76.0], [1406367164000.0, 76.0], [1406367222000.0, 76.0], [1406367283000.0, 76.0], [1406367342000.0, 76.0], [1406367403000.0, 76.0], [1406367461000.0, 76.0], [1406367523000.0, 76.0], [1406367582000.0, 76.0], [1406367640000.0, 76.0], [1406367702000.0, 76.0], [1406367762000.0, 76.0], [1406367822000.0, 76.0], [1406367885000.0, 76.0], [1406367941000.0, 76.0], [1406368002000.0, 76.0], [1406368063000.0, 76.0], [1406368122000.0, 76.0], [1406368182000.0, 76.0], [1406368241000.0, 76.0], [1406368302000.0, 76.0], [1406368362000.0, 76.0], [1406368422000.0, 76.0], [1406368484000.0, 76.0], [1406368542000.0, 76.0], [1406368602000.0, 76.0], [1406368662000.0, 76.0], [1406368722000.0, 76.0], [1406368782000.0, 76.0], [1406368843000.0, 76.0], [1406368902000.0, 76.0], [1406368962000.0, 76.0], [1406369022000.0, 76.0], [1406369082000.0, 76.0], [1406369141000.0, 76.0], [1406369202000.0, 76.0], [1406369262000.0, 76.0], [1406369323000.0, 76.0], [1406369382000.0, 76.0], [1406369442000.0, 76.0], [1406369489000.0, 76.0], [1406369563000.0, 76.0], [1406369625000.0, 76.0], [1406369672000.0, 76.0], [1406369742000.0, 76.0], [1406369802000.0, 76.0], [1406369857000.0, 76.0], [1406369923000.0, 76.0], [1406369979000.0, 76.0], [1406370027000.0, 76.0], [1406370101000.0, 76.0], [1406370155000.0, 76.0], [1406370214000.0, 76.0], [1406370283000.0, 76.0], [1406370342000.0, 76.0], [1406370401000.0, 76.0], [1406370462000.0, 76.0], [1406370525000.0, 76.0], [1406370581000.0, 76.0], [1406370642000.0, 76.0], [1406370702000.0, 76.0], [1406370763000.0, 76.0], [1406370822000.0, 76.0], [1406370882000.0, 76.0], [1406370943000.0, 76.0], [1406371002000.0, 76.0], [1406371062000.0, 76.0], [1406371120000.0, 76.0], [1406371183000.0, 76.0], [1406371242000.0, 76.0], [1406371302000.0, 76.0], [1406371363000.0, 76.0], [1406371422000.0, 76.0], [1406371483000.0, 76.0], [1406371542000.0, 76.0], [1406371603000.0, 76.0], [1406371662000.0, 76.0], [1406371722000.0, 76.0], [1406371782000.0, 76.0], [1406371842000.0, 76.0], [1406371903000.0, 76.0], [1406371962000.0, 76.0], [1406372021000.0, 76.0], [1406372082000.0, 76.0], [1406372142000.0, 76.0], [1406372206000.0, 76.0], [1406372261000.0, 76.0], [1406372321000.0, 76.0], [1406372383000.0, 76.0], [1406372442000.0, 76.0], [1406372504000.0, 76.0], [1406372563000.0, 76.0], [1406372609000.0, 76.0], [1406372684000.0, 76.0], [1406372741000.0, 76.0], [1406372804000.0, 76.0], [1406372863000.0, 76.0], [1406372922000.0, 76.0], [1406372982000.0, 76.0], [1406373041000.0, 76.0], [1406373105000.0, 76.0], [1406373163000.0, 76.0], [1406373222000.0, 76.0], [1406373282000.0, 76.0], [1406373342000.0, 76.0], [1406373401000.0, 76.0], [1406373463000.0, 76.0], [1406373522000.0, 76.0], [1406373583000.0, 76.0], [1406373641000.0, 76.0], [1406373703000.0, 76.0], [1406373761000.0, 76.0], [1406373822000.0, 76.0], [1406373881000.0, 76.0], [1406373942000.0, 76.0], [1406374002000.0, 76.0], [1406374062000.0, 76.0], [1406374121000.0, 76.0], [1406374182000.0, 76.0], [1406374242000.0, 76.0], [1406374308000.0, 76.0], [1406374362000.0, 76.0], [1406374422000.0, 76.0], [1406374482000.0, 76.0], [1406374542000.0, 76.0], [1406374603000.0, 76.0], [1406374662000.0, 76.0], [1406374722000.0, 76.0], [1406374781000.0, 76.0], [1406374843000.0, 76.0], [1406374888000.0, 76.0], [1406374963000.0, 76.0], [1406375022000.0, 76.0], [1406375081000.0, 76.0], [1406375141000.0, 76.0], [1406375201000.0, 76.0], [1406375262000.0, 76.0], [1406375314000.0, 76.0], [1406375382000.0, 76.0], [1406375442000.0, 76.0], [1406375503000.0, 76.0], [1406375563000.0, 76.0], [1406375622000.0, 76.0], [1406375684000.0, 76.0], [1406375743000.0, 76.0], [1406375802000.0, 76.0], [1406375862000.0, 76.0], [1406375924000.0, 76.0], [1406375982000.0, 76.0], [1406376043000.0, 76.0], [1406376102000.0, 76.0], [1406376162000.0, 76.0], [1406376222000.0, 76.0], [1406376283000.0, 76.0], [1406376342000.0, 76.0], [1406376402000.0, 76.0], [1406376461000.0, 76.0], [1406376522000.0, 76.0], [1406376580000.0, 76.0], [1406376636000.0, 76.0], [1406376702000.0, 76.0], [1406376763000.0, 76.0], [1406376821000.0, 76.0], [1406376885000.0, 76.0], [1406376942000.0, 76.0], [1406377003000.0, 76.0], [1406377061000.0, 76.0], [1406377123000.0, 76.0], [1406377182000.0, 76.0], [1406377243000.0, 76.0], [1406377301000.0, 76.0], [1406377360000.0, 76.0], [1406377428000.0, 76.0], [1406377483000.0, 76.0], [1406377542000.0, 76.0], [1406377603000.0, 76.0], [1406377663000.0, 76.0], [1406377722000.0, 76.0], [1406377782000.0, 76.0], [1406377842000.0, 76.0], [1406377902000.0, 76.0], [1406377962000.0, 76.0], [1406378022000.0, 76.0], [1406378082000.0, 76.0], [1406378143000.0, 76.0], [1406378199000.0, 76.0], [1406378264000.0, 76.0], [1406378325000.0, 76.0], [1406378382000.0, 76.0], [1406378442000.0, 76.0], [1406378502000.0, 76.0], [1406378563000.0, 76.0], [1406378621000.0, 76.0], [1406378683000.0, 76.0], [1406378742000.0, 76.0], [1406378802000.0, 76.0], [1406378862000.0, 76.0], [1406378923000.0, 76.0], [1406378985000.0, 76.0], [1406379043000.0, 76.0], [1406379101000.0, 76.0], [1406379163000.0, 76.0], [1406379223000.0, 76.0], [1406379282000.0, 76.0], [1406379342000.0, 76.0], [1406379402000.0, 76.0], [1406379463000.0, 76.0], [1406379521000.0, 76.0], [1406379583000.0, 76.0], [1406379642000.0, 76.0], [1406379702000.0, 76.0], [1406379763000.0, 76.0], [1406379822000.0, 76.0], [1406379884000.0, 76.0], [1406379943000.0, 76.0], [1406380002000.0, 76.0], [1406380061000.0, 76.0], [1406380123000.0, 76.0], [1406380182000.0, 76.0], [1406380242000.0, 76.0], [1406380302000.0, 76.0], [1406380363000.0, 76.0], [1406380422000.0, 76.0], [1406380485000.0, 76.0], [1406380542000.0, 76.0], [1406380602000.0, 76.0], [1406380661000.0, 76.0], [1406380723000.0, 76.0], [1406380782000.0, 76.0], [1406380842000.0, 76.0], [1406380902000.0, 76.0], [1406380963000.0, 76.0], [1406381024000.0, 76.0], [1406381083000.0, 76.0], [1406381143000.0, 76.0], [1406381202000.0, 76.0], [1406381261000.0, 76.0], [1406381326000.0, 76.0], [1406381388000.0, 76.0], [1406381457000.0, 76.0], [1406381501000.0, 76.0], [1406381563000.0, 76.0], [1406381622000.0, 76.0], [1406381682000.0, 76.0], [1406381740000.0, 76.0], [1406381803000.0, 76.0], [1406381863000.0, 76.0], [1406381923000.0, 76.0], [1406381982000.0, 76.0], [1406382043000.0, 76.0], [1406382102000.0, 76.0], [1406382160000.0, 76.0], [1406382223000.0, 76.0], [1406382282000.0, 76.0], [1406382342000.0, 76.0], [1406382402000.0, 76.0], [1406382462000.0, 76.0], [1406382521000.0, 76.0], [1406382582000.0, 76.0], [1406382641000.0, 76.0], [1406382702000.0, 76.0], [1406382762000.0, 76.0], [1406382823000.0, 76.0], [1406382885000.0, 76.0], [1406382942000.0, 76.0], [1406383001000.0, 76.0], [1406383062000.0, 76.0], [1406383123000.0, 76.0], [1406383182000.0, 76.0], [1406383242000.0, 76.0], [1406383302000.0, 76.0], [1406383362000.0, 76.0], [1406383426000.0, 76.0], [1406383482000.0, 76.0], [1406383545000.0, 76.0], [1406383603000.0, 76.0], [1406383663000.0, 76.0], [1406383723000.0, 76.0], [1406383780000.0, 76.0], [1406383843000.0, 76.0], [1406383903000.0, 76.0], [1406383963000.0, 76.0], [1406384022000.0, 76.0], [1406384081000.0, 76.0], [1406384143000.0, 76.0], [1406384203000.0, 76.0], [1406384262000.0, 76.0], [1406384322000.0, 76.0], [1406384382000.0, 76.0], [1406384446000.0, 76.0], [1406384501000.0, 76.0], [1406384562000.0, 76.0], [1406384622000.0, 76.0], [1406384685000.0, 76.0], [1406384743000.0, 76.0], [1406384803000.0, 76.0], [1406384862000.0, 76.0], [1406384922000.0, 76.0], [1406384983000.0, 76.0], [1406385043000.0, 76.0], [1406385102000.0, 76.0], [1406385163000.0, 76.0], [1406385223000.0, 76.0], [1406385281000.0, 76.0], [1406385342000.0, 76.0], [1406385401000.0, 76.0], [1406385462000.0, 76.0], [1406385523000.0, 76.0], [1406385583000.0, 76.0], [1406385642000.0, 76.0], [1406385701000.0, 76.0], [1406385763000.0, 76.0], [1406385823000.0, 76.0], [1406385882000.0, 76.0], [1406385942000.0, 76.0], [1406386002000.0, 76.0], [1406386063000.0, 76.0], [1406386122000.0, 76.0], [1406386183000.0, 76.0], [1406386241000.0, 76.0], [1406386306000.0, 76.0], [1406386363000.0, 76.0], [1406386420000.0, 76.0], [1406386482000.0, 76.0], [1406386543000.0, 76.0], [1406386603000.0, 76.0], [1406386662000.0, 76.0], [1406386722000.0, 76.0], [1406386782000.0, 76.0], [1406386842000.0, 76.0], [1406386903000.0, 76.0], [1406386955000.0, 76.0], [1406387025000.0, 76.0], [1406387082000.0, 76.0], [1406387143000.0, 76.0], [1406387203000.0, 76.0], [1406387262000.0, 76.0], [1406387322000.0, 76.0], [1406387382000.0, 76.0], [1406387443000.0, 76.0], [1406387502000.0, 76.0], [1406387563000.0, 76.0], [1406387623000.0, 76.0], [1406387682000.0, 76.0], [1406387746000.0, 76.0], [1406387805000.0, 76.0], [1406387865000.0, 76.0], [1406387923000.0, 76.0], [1406387982000.0, 76.0], [1406388043000.0, 76.0], [1406388101000.0, 76.0], [1406388163000.0, 76.0], [1406388222000.0, 76.0], [1406388287000.0, 76.0], [1406388343000.0, 76.0], [1406388402000.0, 76.0], [1406388462000.0, 76.0], [1406388523000.0, 76.0], [1406388580000.0, 76.0], [1406388642000.0, 76.0], [1406388705000.0, 76.0], [1406388762000.0, 76.0], [1406388821000.0, 76.0], [1406388882000.0, 76.0], [1406388945000.0, 76.0], [1406389005000.0, 76.0], [1406389062000.0, 76.0], [1406389122000.0, 76.0], [1406389181000.0, 76.0], [1406389241000.0, 76.0], [1406389302000.0, 76.0], [1406389363000.0, 76.0], [1406389421000.0, 76.0], [1406389485000.0, 76.0], [1406389542000.0, 76.0], [1406389605000.0, 76.0], [1406389661000.0, 76.0], [1406389721000.0, 76.0]]
        return render_to_response(
            'statistics/statistics_light_sensor.html',
            {'status': rs_status,
             'device_info': device_info, 'nickname': device_nickname, 'zone_nickname': zone_nickname,
             'device_type_id': device_type_id, 'mac': mac}, context)


@login_required(login_url='/login/')
def auto_update_smap_daylight_sensor(request):
    if request.method == 'POST':
        print 'inside smap auto update day light sensor'
        _data = request.body
        _data = json.loads(_data)
        device_info = _data['device_info']

        device_smap_tag = '/bemoss/' + device_info.encode('ascii', 'ignore')
        device_smap_tag = device_smap_tag.encode('ascii', 'ignore')

        status = device_smap_tag + '/illuminance'

        _uuid_status = get_uuid_for_data_point(status)

        rs_status = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_status)

        json_result = {
            'status': rs_status
        }

        print 'test'
        if request.is_ajax():
            return HttpResponse(json.dumps(json_result), mimetype='application/json')


@login_required(login_url='/login/')
def smap_plot_wattstopper_plugload(request, mac):
    print "inside smap view method for day light sensor"
    context = RequestContext(request)
    if request.method == 'GET':

        device_metadata = [ob.device_control_page_info() for ob in DeviceMetadata.objects.filter(mac_address=mac)]
        print device_metadata
        device_id = device_metadata[0]['device_id']
        device_type_id = device_metadata[0]['device_model_id']
        device_type_id = device_type_id.device_model_id
        print device_type_id

        device_status = [ob.data_as_json() for ob in Plugload.objects.filter(plugload_id=device_id)]
        device_zone = device_status[0]['zone']['id']
        device_nickname = device_status[0]['nickname']
        zone_nickname = device_status[0]['zone']['zone_nickname']

        device_info = str(device_zone) + '/plugload/' + device_id
        device_info = device_info.encode('ascii', 'ignore')
        device_smap_tag = '/bemoss/' + str(device_zone) + '/plugload/' + device_id

        device_smap_tag = device_smap_tag.encode('ascii', 'ignore')
        status = device_smap_tag + '/status'
        power = device_smap_tag + '/power'
        print status

        _uuid_status = get_uuid_for_data_point(status)
        _uuid_power = get_uuid_for_data_point(power)

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

        rs_status = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_status)
        rs_power = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_power)

        return render_to_response(
            'statistics/statistics_wtplug.html',
            {'status': rs_status, 'power': rs_power,
             'device_info': device_info, 'nickname': device_nickname, 'zone_nickname': zone_nickname,
             'device_type_id': device_type_id, 'mac': mac}, context)


@login_required(login_url='/login/')
def auto_update_smap_wattstopper_plugload(request):
    if request.method == 'POST':
        print 'inside smap auto update wattstopper plugload'
        _data = request.body
        _data = json.loads(_data)
        device_info = _data['device_info']

        device_smap_tag = '/bemoss/' + device_info.encode('ascii', 'ignore')
        device_smap_tag = device_smap_tag.encode('ascii', 'ignore')

        status = device_smap_tag + '/status'
        power = device_smap_tag + '/power'

        _uuid_status = get_uuid_for_data_point(status)
        _uuid_power = get_uuid_for_data_point(power)

        rs_status = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_status)
        rs_power = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_power)

        json_result = {
            'status': rs_status,
            'power': rs_power
        }

        print 'test'
        if request.is_ajax():
            return HttpResponse(json.dumps(json_result), mimetype='application/json')


@login_required(login_url='/login/')
def smap_plot_powermeter(request, mac):
    print "inside smap view method for powermeter"
    context = RequestContext(request)
    if request.method == 'GET':

        device_metadata = [ob.device_control_page_info() for ob in DeviceMetadata.objects.filter(mac_address=mac)]
        print device_metadata
        device_id = device_metadata[0]['device_id']
        device_type_id = device_metadata[0]['device_model_id']
        device_type_id = device_type_id.device_model_id
        print device_type_id

        device_status = [ob.data_as_json() for ob in PowerMeter.objects.filter(power_meter_id=device_id)]
        device_zone = device_status[0]['zone']['id']
        device_nickname = device_status[0]['nickname']
        zone_nickname = device_status[0]['zone']['zone_nickname']

        device_info = str(device_zone) + '/power_meter/' + device_id
        device_info = device_info.encode('ascii', 'ignore')
        device_smap_tag = '/bemoss/' + str(device_zone) + '/power_meter/' + device_id

        device_smap_tag = device_smap_tag.encode('ascii', 'ignore')
        real_power = device_smap_tag + '/real_power'
        power_factor = device_smap_tag + '/power_factor'

        _uuid_real_power = get_uuid_for_data_point(real_power)
        _uuid_power_factor = get_uuid_for_data_point(power_factor)

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

        rs_real_power = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_real_power)
        rs_power_factor = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_power_factor)

        return render_to_response(
            'statistics/statistics_powermeter.html',
            {'real_power': rs_real_power, 'power_factor': rs_power_factor, 'mac': mac,
             'device_info': device_info, 'nickname': device_nickname, 'zone_nickname': zone_nickname,
             'device_type_id': device_type_id, 'zones': zones}, context)


@login_required(login_url='/login/')
def auto_update_smap_powermeter(request):
    if request.method == 'POST':
        print 'inside smap auto update wattstopper plugload'
        _data = request.body
        _data = json.loads(_data)
        device_info = _data['device_info']

        device_smap_tag = '/bemoss/' + device_info.encode('ascii', 'ignore')
        device_smap_tag = device_smap_tag.encode('ascii', 'ignore')
        real_power = device_smap_tag + '/real_power'
        power_factor = device_smap_tag + '/power_factor'

        _uuid_real_power = get_uuid_for_data_point(real_power)
        _uuid_power_factor = get_uuid_for_data_point(power_factor)

        rs_real_power = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_real_power)
        rs_power_factor = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_power_factor)

        json_result = {'real_power': rs_real_power,
                       'power_factor': rs_power_factor}

        print 'test'
        if request.is_ajax():
            return HttpResponse(json.dumps(json_result), mimetype='application/json')


@login_required(login_url='/login/')
def smap_plot_vav(request, mac):
    """Page load definition for VAV statistics."""
    print "inside smap view method"
    context = RequestContext(request)
    if request.method == 'GET':

        device_metadata = [ob.device_control_page_info() for ob in DeviceMetadata.objects.filter(mac_address=mac)]
        print device_metadata
        device_id = device_metadata[0]['device_id']
        device_type_id = device_metadata[0]['device_model_id']
        device_type = device_metadata[0]['device_type']
        device_type_id = device_type_id.device_model_id
        print device_type_id

        device_status = [ob.as_json() for ob in VAV.objects.filter(vav_id=device_id)]
        device_zone = device_status[0]['zone']['id']
        device_nickname = device_status[0]['nickname']
        zone_nickname = device_status[0]['zone']['zone_nickname']

        device_info = str(device_zone) + '/' + device_type + '/' + device_id
        device_info = device_info.encode('ascii', 'ignore')
        device_smap_tag = '/bemoss/' + str(device_zone) + '/' + device_type + '/' + device_id
        device_smap_tag = device_smap_tag.encode('ascii', 'ignore')
        temperature = device_smap_tag + '/temperature'
        supply_temperature = device_smap_tag + '/supply_temperature'
        heat_setpoint = device_smap_tag + '/heat_setpoint'
        cool_setpoint = device_smap_tag + '/cool_setpoint'
        flap_position = device_smap_tag + '/flap_position'
        print temperature

        _uuid_temperature = get_uuid_for_data_point(temperature)
        _uuid_supply_temperature = get_uuid_for_data_point(supply_temperature)
        _uuid_heat_setpoint = get_uuid_for_data_point(heat_setpoint)
        _uuid_cool_setpoint = get_uuid_for_data_point(cool_setpoint)
        _uuid_flap_position = get_uuid_for_data_point(flap_position)

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

        rs_temperature = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_temperature)
        rs_supply_temperature = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_supply_temperature)
        rs_heat_setpoint = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_heat_setpoint)
        rs_cool_setpoint = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_cool_setpoint)
        rs_flap_position = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_flap_position)

        return render_to_response(
            'statistics/statistics_vav.html',
            {'temperature': rs_temperature, 'supply_temperature': rs_supply_temperature,
             'flap_position': rs_flap_position, 'heat_setpoint': rs_heat_setpoint, 'cool_setpoint': rs_cool_setpoint,
             'zones': zones, 'mac': mac, 'device_info': device_info,
             'nickname': device_nickname,
             'zone_nickname': zone_nickname},
            context)


@login_required(login_url='/login/')
def auto_update_smap_vav(request):
    """Statistics page load for VAV"""
    if request.method == 'POST':
        print 'inside smap auto update VAV'
        _data = request.body
        _data = json.loads(_data)
        device_info = _data['device_info']

        device_smap_tag = '/bemoss/' + device_info.encode('ascii', 'ignore')
        device_smap_tag = device_smap_tag.encode('ascii', 'ignore')
        temperature = device_smap_tag + '/temperature'
        supply_temperature = device_smap_tag + '/supply_temperature'
        heat_setpoint = device_smap_tag + '/heat_setpoint'
        cool_setpoint = device_smap_tag + '/cool_setpoint'
        flap_position = device_smap_tag + '/flap_position'

        _uuid_temperature = get_uuid_for_data_point(temperature)
        _uuid_supply_temperature = get_uuid_for_data_point(supply_temperature)
        _uuid_heat_setpoint = get_uuid_for_data_point(heat_setpoint)
        _uuid_cool_setpoint = get_uuid_for_data_point(cool_setpoint)
        _uuid_flap_position = get_uuid_for_data_point(flap_position)

        rs_temperature = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_temperature)
        rs_supply_temperature = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_supply_temperature)
        rs_heat_setpoint = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_heat_setpoint)
        rs_cool_setpoint = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_cool_setpoint)
        rs_flap_position = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_flap_position)


        json_result = {'temperature': rs_temperature,
                       'supply_temperature': rs_supply_temperature,
                        'flap_position': rs_flap_position,
                        'heat_setpoint': rs_heat_setpoint,
                        'cool_setpoint': rs_cool_setpoint}

        if request.is_ajax():
                return HttpResponse(json.dumps(json_result), mimetype='application/json')


@login_required(login_url='/login/')
def smap_plot_rtu(request, mac):
    """Page load definition for RTU statistics."""
    print "inside smap view method"
    context = RequestContext(request)
    if request.method == 'GET':

        device_metadata = [ob.device_control_page_info() for ob in DeviceMetadata.objects.filter(mac_address=mac)]
        print device_metadata
        device_id = device_metadata[0]['device_id']
        device_type_id = device_metadata[0]['device_model_id']
        device_type = device_metadata[0]['device_type']
        device_type_id = device_type_id.device_model_id
        print device_type_id

        device_status = [ob.as_json() for ob in RTU.objects.filter(rtu_id=device_id)]
        device_zone = device_status[0]['zone']['id']
        device_nickname = device_status[0]['nickname']
        zone_nickname = device_status[0]['zone']['zone_nickname']

        device_info = str(device_zone) + '/' + device_type + '/' + device_id
        device_info = device_info.encode('ascii', 'ignore')
        device_smap_tag = '/bemoss/' + str(device_zone) + '/' + device_type + '/' + device_id
        device_smap_tag = device_smap_tag.encode('ascii', 'ignore')
        outside_temperature = device_smap_tag + '/outside_temperature'
        return_temperature = device_smap_tag + '/return_temperature'
        supply_temperature = device_smap_tag + '/supply_temperature'
        heat_setpoint = device_smap_tag + '/heat_setpoint'
        cool_setpoint = device_smap_tag + '/cool_setpoint'
        cooling_mode = device_smap_tag + '/cooling_mode'
        heating = device_smap_tag + '/heating'
        outside_damper_position = device_smap_tag + '/outside_damper_position'
        bypass_damper_position = device_smap_tag + '/bypass_damper_position'

        _uuid_outside_temperature = get_uuid_for_data_point(outside_temperature)
        _uuid_return_temperature = get_uuid_for_data_point(return_temperature)
        _uuid_supply_temperature = get_uuid_for_data_point(supply_temperature)
        _uuid_heat_setpoint = get_uuid_for_data_point(heat_setpoint)
        _uuid_cool_setpoint = get_uuid_for_data_point(cool_setpoint)
        _uuid_cooling_mode = get_uuid_for_data_point(cooling_mode)
        _uuid_heating = get_uuid_for_data_point(heating)
        _uuid_outside_damper_position = get_uuid_for_data_point(outside_damper_position)
        _uuid_bypass_damper_position = get_uuid_for_data_point(bypass_damper_position)

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

        rs_outside_temperature = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_outside_temperature)
        rs_return_temperature = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_return_temperature)
        rs_supply_temperature = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_supply_temperature)
        rs_heat_setpoint = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_heat_setpoint)
        rs_cool_setpoint = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_cool_setpoint)
        rs_cooling_mode = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_cooling_mode)
        rs_heating = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_heating)
        rs_outside_damper_position = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_outside_damper_position)
        rs_bypass_damper_position = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_bypass_damper_position)

        #parsed_json = [[1406349525000.0, 74.0], [1406349581000.0, 74.0], [1406349641000.0, 74.0], [1406349701000.0, 74.0], [1406349762000.0, 74.0], [1406349822000.0, 74.0], [1406349882000.0, 74.0], [1406349942000.0, 74.0], [1406350002000.0, 74.0], [1406350065000.0, 74.0], [1406350122000.0, 74.0], [1406350181000.0, 74.0], [1406350240000.0, 74.0], [1406350302000.0, 74.5], [1406350363000.0, 74.5], [1406350422000.0, 74.5], [1406350481000.0, 74.5], [1406350543000.0, 74.5], [1406350602000.0, 74.5], [1406350662000.0, 74.5], [1406350721000.0, 74.5], [1406350782000.0, 74.5], [1406350843000.0, 74.5], [1406350902000.0, 74.5], [1406350961000.0, 74.5], [1406351024000.0, 74.5], [1406351083000.0, 74.5], [1406351141000.0, 74.5], [1406351202000.0, 74.5], [1406351263000.0, 74.5], [1406351321000.0, 74.5], [1406351384000.0, 74.5], [1406351441000.0, 74.5], [1406351502000.0, 76.0], [1406351561000.0, 76.0], [1406351621000.0, 76.0], [1406351682000.0, 76.0], [1406351742000.0, 76.0], [1406351802000.0, 76.0], [1406351862000.0, 76.0], [1406351922000.0, 76.0], [1406351982000.0, 76.0], [1406352041000.0, 76.0], [1406352102000.0, 76.0], [1406352161000.0, 76.0], [1406352222000.0, 76.0], [1406352282000.0, 76.0], [1406352342000.0, 76.0], [1406352402000.0, 76.0], [1406352461000.0, 76.0], [1406352522000.0, 76.0], [1406352582000.0, 76.0], [1406352642000.0, 76.0], [1406352702000.0, 76.0], [1406352761000.0, 76.0], [1406352822000.0, 76.0], [1406352882000.0, 76.0], [1406352942000.0, 76.0], [1406353001000.0, 76.0], [1406353063000.0, 76.0], [1406353122000.0, 76.0], [1406353182000.0, 76.0], [1406353241000.0, 76.0], [1406353302000.0, 76.0], [1406353362000.0, 76.0], [1406353422000.0, 76.0], [1406353481000.0, 76.0], [1406353541000.0, 76.0], [1406353601000.0, 76.0], [1406353662000.0, 76.0], [1406353722000.0, 76.0], [1406353786000.0, 76.0], [1406353841000.0, 76.0], [1406353901000.0, 76.0], [1406353962000.0, 76.0], [1406354024000.0, 76.0], [1406354081000.0, 76.0], [1406354141000.0, 76.0], [1406354202000.0, 76.0], [1406354263000.0, 76.0], [1406354322000.0, 76.0], [1406354382000.0, 76.0], [1406354442000.0, 76.0], [1406354503000.0, 76.0], [1406354562000.0, 76.0], [1406354625000.0, 76.0], [1406354681000.0, 76.0], [1406354743000.0, 76.0], [1406354803000.0, 76.0], [1406354861000.0, 76.0], [1406354921000.0, 76.0], [1406354981000.0, 76.0], [1406355042000.0, 76.0], [1406355103000.0, 76.0], [1406355161000.0, 76.0], [1406355223000.0, 76.0], [1406355282000.0, 76.0], [1406355343000.0, 76.0], [1406355402000.0, 76.0], [1406355464000.0, 76.0], [1406355522000.0, 76.0], [1406355582000.0, 76.0], [1406355642000.0, 76.0], [1406355701000.0, 76.0], [1406355763000.0, 76.0], [1406355822000.0, 76.0], [1406355887000.0, 76.0], [1406355942000.0, 76.0], [1406356001000.0, 76.0], [1406356062000.0, 76.0], [1406356122000.0, 76.0], [1406356183000.0, 76.0], [1406356241000.0, 76.0], [1406356302000.0, 76.0], [1406356362000.0, 76.0], [1406356425000.0, 76.0], [1406356481000.0, 76.0], [1406356542000.0, 76.0], [1406356602000.0, 76.0], [1406356664000.0, 76.0], [1406356722000.0, 76.0], [1406356780000.0, 76.0], [1406356842000.0, 76.0], [1406356903000.0, 76.0], [1406356963000.0, 76.0], [1406357022000.0, 76.0], [1406357081000.0, 76.0], [1406357142000.0, 76.0], [1406357202000.0, 76.0], [1406357261000.0, 76.0], [1406357322000.0, 76.0], [1406357383000.0, 76.0], [1406357442000.0, 76.0], [1406357505000.0, 76.0], [1406357561000.0, 76.0], [1406357621000.0, 76.0], [1406357682000.0, 76.0], [1406357742000.0, 76.0], [1406357802000.0, 76.0], [1406357862000.0, 76.0], [1406357921000.0, 76.0], [1406357982000.0, 76.0], [1406358041000.0, 76.0], [1406358101000.0, 76.0], [1406358161000.0, 76.0], [1406358222000.0, 76.0], [1406358283000.0, 76.0], [1406358340000.0, 76.0], [1406358401000.0, 76.0], [1406358462000.0, 76.0], [1406358522000.0, 76.0], [1406358582000.0, 76.0], [1406358643000.0, 76.0], [1406358702000.0, 76.0], [1406358761000.0, 76.0], [1406358824000.0, 76.0], [1406358882000.0, 76.0], [1406358942000.0, 76.0], [1406359002000.0, 76.0], [1406359063000.0, 76.0], [1406359122000.0, 76.0], [1406359182000.0, 76.0], [1406359243000.0, 76.0], [1406359300000.0, 76.0], [1406359363000.0, 76.0], [1406359422000.0, 76.0], [1406359481000.0, 76.0], [1406359542000.0, 76.0], [1406359601000.0, 76.0], [1406359661000.0, 76.0], [1406359722000.0, 76.0], [1406359782000.0, 76.0], [1406359842000.0, 76.0], [1406359901000.0, 76.0], [1406359962000.0, 76.0], [1406360021000.0, 76.0], [1406360081000.0, 76.0], [1406360141000.0, 76.0], [1406360202000.0, 76.0], [1406360261000.0, 76.0], [1406360322000.0, 76.0], [1406360385000.0, 76.0], [1406360443000.0, 76.0], [1406360502000.0, 76.0], [1406360565000.0, 76.0], [1406360623000.0, 76.0], [1406360681000.0, 76.0], [1406360742000.0, 76.0], [1406360801000.0, 76.0], [1406360861000.0, 76.0], [1406360923000.0, 76.0], [1406360981000.0, 76.0], [1406361041000.0, 76.0], [1406361102000.0, 76.0], [1406361161000.0, 76.0], [1406361224000.0, 76.0], [1406361281000.0, 76.0], [1406361342000.0, 76.0], [1406361403000.0, 76.0], [1406361462000.0, 76.0], [1406361521000.0, 76.0], [1406361582000.0, 76.0], [1406361645000.0, 76.0], [1406361702000.0, 76.0], [1406361761000.0, 76.0], [1406361826000.0, 76.0], [1406361883000.0, 76.0], [1406361942000.0, 76.0], [1406362002000.0, 76.0], [1406362061000.0, 76.0], [1406362123000.0, 76.0], [1406362184000.0, 76.0], [1406362246000.0, 76.0], [1406362302000.0, 76.0], [1406362363000.0, 76.0], [1406362423000.0, 76.0], [1406362483000.0, 76.0], [1406362543000.0, 76.0], [1406362602000.0, 76.0], [1406362661000.0, 76.0], [1406362722000.0, 76.0], [1406362782000.0, 76.0], [1406362843000.0, 76.0], [1406362901000.0, 76.0], [1406362962000.0, 76.0], [1406363023000.0, 76.0], [1406363085000.0, 76.0], [1406363141000.0, 76.0], [1406363201000.0, 76.0], [1406363262000.0, 76.0], [1406363323000.0, 76.0], [1406363382000.0, 76.0], [1406363443000.0, 76.0], [1406363503000.0, 76.0], [1406363562000.0, 76.0], [1406363623000.0, 76.0], [1406363682000.0, 76.0], [1406363742000.0, 76.0], [1406363802000.0, 76.0], [1406363861000.0, 76.0], [1406363923000.0, 76.0], [1406363982000.0, 76.0], [1406364044000.0, 76.0], [1406364101000.0, 76.0], [1406364162000.0, 76.0], [1406364225000.0, 76.0], [1406364283000.0, 76.0], [1406364340000.0, 76.0], [1406364403000.0, 76.0], [1406364462000.0, 76.0], [1406364522000.0, 76.0], [1406364582000.0, 76.0], [1406364643000.0, 76.0], [1406364702000.0, 76.0], [1406364761000.0, 76.0], [1406364822000.0, 76.0], [1406364882000.0, 76.0], [1406364943000.0, 76.0], [1406365003000.0, 76.0], [1406365061000.0, 76.0], [1406365123000.0, 76.0], [1406365181000.0, 76.0], [1406365242000.0, 76.0], [1406365302000.0, 76.0], [1406365361000.0, 76.0], [1406365423000.0, 76.0], [1406365482000.0, 76.0], [1406365546000.0, 76.0], [1406365602000.0, 76.0], [1406365662000.0, 76.0], [1406365723000.0, 76.0], [1406365782000.0, 76.0], [1406365842000.0, 76.0], [1406365902000.0, 76.0], [1406365962000.0, 76.0], [1406366023000.0, 76.0], [1406366086000.0, 76.0], [1406366142000.0, 76.0], [1406366202000.0, 76.0], [1406366261000.0, 76.0], [1406366323000.0, 76.0], [1406366382000.0, 76.0], [1406366445000.0, 76.0], [1406366503000.0, 76.0], [1406366562000.0, 76.0], [1406366625000.0, 76.0], [1406366681000.0, 76.0], [1406366741000.0, 76.0], [1406366802000.0, 76.0], [1406366863000.0, 76.0], [1406366921000.0, 76.0], [1406366982000.0, 76.0], [1406367043000.0, 76.0], [1406367101000.0, 76.0], [1406367164000.0, 76.0], [1406367222000.0, 76.0], [1406367283000.0, 76.0], [1406367342000.0, 76.0], [1406367403000.0, 76.0], [1406367461000.0, 76.0], [1406367523000.0, 76.0], [1406367582000.0, 76.0], [1406367640000.0, 76.0], [1406367702000.0, 76.0], [1406367762000.0, 76.0], [1406367822000.0, 76.0], [1406367885000.0, 76.0], [1406367941000.0, 76.0], [1406368002000.0, 76.0], [1406368063000.0, 76.0], [1406368122000.0, 76.0], [1406368182000.0, 76.0], [1406368241000.0, 76.0], [1406368302000.0, 76.0], [1406368362000.0, 76.0], [1406368422000.0, 76.0], [1406368484000.0, 76.0], [1406368542000.0, 76.0], [1406368602000.0, 76.0], [1406368662000.0, 76.0], [1406368722000.0, 76.0], [1406368782000.0, 76.0], [1406368843000.0, 76.0], [1406368902000.0, 76.0], [1406368962000.0, 76.0], [1406369022000.0, 76.0], [1406369082000.0, 76.0], [1406369141000.0, 76.0], [1406369202000.0, 76.0], [1406369262000.0, 76.0], [1406369323000.0, 76.0], [1406369382000.0, 76.0], [1406369442000.0, 76.0], [1406369489000.0, 76.0], [1406369563000.0, 76.0], [1406369625000.0, 76.0], [1406369672000.0, 76.0], [1406369742000.0, 76.0], [1406369802000.0, 76.0], [1406369857000.0, 76.0], [1406369923000.0, 76.0], [1406369979000.0, 76.0], [1406370027000.0, 76.0], [1406370101000.0, 76.0], [1406370155000.0, 76.0], [1406370214000.0, 76.0], [1406370283000.0, 76.0], [1406370342000.0, 76.0], [1406370401000.0, 76.0], [1406370462000.0, 76.0], [1406370525000.0, 76.0], [1406370581000.0, 76.0], [1406370642000.0, 76.0], [1406370702000.0, 76.0], [1406370763000.0, 76.0], [1406370822000.0, 76.0], [1406370882000.0, 76.0], [1406370943000.0, 76.0], [1406371002000.0, 76.0], [1406371062000.0, 76.0], [1406371120000.0, 76.0], [1406371183000.0, 76.0], [1406371242000.0, 76.0], [1406371302000.0, 76.0], [1406371363000.0, 76.0], [1406371422000.0, 76.0], [1406371483000.0, 76.0], [1406371542000.0, 76.0], [1406371603000.0, 76.0], [1406371662000.0, 76.0], [1406371722000.0, 76.0], [1406371782000.0, 76.0], [1406371842000.0, 76.0], [1406371903000.0, 76.0], [1406371962000.0, 76.0], [1406372021000.0, 76.0], [1406372082000.0, 76.0], [1406372142000.0, 76.0], [1406372206000.0, 76.0], [1406372261000.0, 76.0], [1406372321000.0, 76.0], [1406372383000.0, 76.0], [1406372442000.0, 76.0], [1406372504000.0, 76.0], [1406372563000.0, 76.0], [1406372609000.0, 76.0], [1406372684000.0, 76.0], [1406372741000.0, 76.0], [1406372804000.0, 76.0], [1406372863000.0, 76.0], [1406372922000.0, 76.0], [1406372982000.0, 76.0], [1406373041000.0, 76.0], [1406373105000.0, 76.0], [1406373163000.0, 76.0], [1406373222000.0, 76.0], [1406373282000.0, 76.0], [1406373342000.0, 76.0], [1406373401000.0, 76.0], [1406373463000.0, 76.0], [1406373522000.0, 76.0], [1406373583000.0, 76.0], [1406373641000.0, 76.0], [1406373703000.0, 76.0], [1406373761000.0, 76.0], [1406373822000.0, 76.0], [1406373881000.0, 76.0], [1406373942000.0, 76.0], [1406374002000.0, 76.0], [1406374062000.0, 76.0], [1406374121000.0, 76.0], [1406374182000.0, 76.0], [1406374242000.0, 76.0], [1406374308000.0, 76.0], [1406374362000.0, 76.0], [1406374422000.0, 76.0], [1406374482000.0, 76.0], [1406374542000.0, 76.0], [1406374603000.0, 76.0], [1406374662000.0, 76.0], [1406374722000.0, 76.0], [1406374781000.0, 76.0], [1406374843000.0, 76.0], [1406374888000.0, 76.0], [1406374963000.0, 76.0], [1406375022000.0, 76.0], [1406375081000.0, 76.0], [1406375141000.0, 76.0], [1406375201000.0, 76.0], [1406375262000.0, 76.0], [1406375314000.0, 76.0], [1406375382000.0, 76.0], [1406375442000.0, 76.0], [1406375503000.0, 76.0], [1406375563000.0, 76.0], [1406375622000.0, 76.0], [1406375684000.0, 76.0], [1406375743000.0, 76.0], [1406375802000.0, 76.0], [1406375862000.0, 76.0], [1406375924000.0, 76.0], [1406375982000.0, 76.0], [1406376043000.0, 76.0], [1406376102000.0, 76.0], [1406376162000.0, 76.0], [1406376222000.0, 76.0], [1406376283000.0, 76.0], [1406376342000.0, 76.0], [1406376402000.0, 76.0], [1406376461000.0, 76.0], [1406376522000.0, 76.0], [1406376580000.0, 76.0], [1406376636000.0, 76.0], [1406376702000.0, 76.0], [1406376763000.0, 76.0], [1406376821000.0, 76.0], [1406376885000.0, 76.0], [1406376942000.0, 76.0], [1406377003000.0, 76.0], [1406377061000.0, 76.0], [1406377123000.0, 76.0], [1406377182000.0, 76.0], [1406377243000.0, 76.0], [1406377301000.0, 76.0], [1406377360000.0, 76.0], [1406377428000.0, 76.0], [1406377483000.0, 76.0], [1406377542000.0, 76.0], [1406377603000.0, 76.0], [1406377663000.0, 76.0], [1406377722000.0, 76.0], [1406377782000.0, 76.0], [1406377842000.0, 76.0], [1406377902000.0, 76.0], [1406377962000.0, 76.0], [1406378022000.0, 76.0], [1406378082000.0, 76.0], [1406378143000.0, 76.0], [1406378199000.0, 76.0], [1406378264000.0, 76.0], [1406378325000.0, 76.0], [1406378382000.0, 76.0], [1406378442000.0, 76.0], [1406378502000.0, 76.0], [1406378563000.0, 76.0], [1406378621000.0, 76.0], [1406378683000.0, 76.0], [1406378742000.0, 76.0], [1406378802000.0, 76.0], [1406378862000.0, 76.0], [1406378923000.0, 76.0], [1406378985000.0, 76.0], [1406379043000.0, 76.0], [1406379101000.0, 76.0], [1406379163000.0, 76.0], [1406379223000.0, 76.0], [1406379282000.0, 76.0], [1406379342000.0, 76.0], [1406379402000.0, 76.0], [1406379463000.0, 76.0], [1406379521000.0, 76.0], [1406379583000.0, 76.0], [1406379642000.0, 76.0], [1406379702000.0, 76.0], [1406379763000.0, 76.0], [1406379822000.0, 76.0], [1406379884000.0, 76.0], [1406379943000.0, 76.0], [1406380002000.0, 76.0], [1406380061000.0, 76.0], [1406380123000.0, 76.0], [1406380182000.0, 76.0], [1406380242000.0, 76.0], [1406380302000.0, 76.0], [1406380363000.0, 76.0], [1406380422000.0, 76.0], [1406380485000.0, 76.0], [1406380542000.0, 76.0], [1406380602000.0, 76.0], [1406380661000.0, 76.0], [1406380723000.0, 76.0], [1406380782000.0, 76.0], [1406380842000.0, 76.0], [1406380902000.0, 76.0], [1406380963000.0, 76.0], [1406381024000.0, 76.0], [1406381083000.0, 76.0], [1406381143000.0, 76.0], [1406381202000.0, 76.0], [1406381261000.0, 76.0], [1406381326000.0, 76.0], [1406381388000.0, 76.0], [1406381457000.0, 76.0], [1406381501000.0, 76.0], [1406381563000.0, 76.0], [1406381622000.0, 76.0], [1406381682000.0, 76.0], [1406381740000.0, 76.0], [1406381803000.0, 76.0], [1406381863000.0, 76.0], [1406381923000.0, 76.0], [1406381982000.0, 76.0], [1406382043000.0, 76.0], [1406382102000.0, 76.0], [1406382160000.0, 76.0], [1406382223000.0, 76.0], [1406382282000.0, 76.0], [1406382342000.0, 76.0], [1406382402000.0, 76.0], [1406382462000.0, 76.0], [1406382521000.0, 76.0], [1406382582000.0, 76.0], [1406382641000.0, 76.0], [1406382702000.0, 76.0], [1406382762000.0, 76.0], [1406382823000.0, 76.0], [1406382885000.0, 76.0], [1406382942000.0, 76.0], [1406383001000.0, 76.0], [1406383062000.0, 76.0], [1406383123000.0, 76.0], [1406383182000.0, 76.0], [1406383242000.0, 76.0], [1406383302000.0, 76.0], [1406383362000.0, 76.0], [1406383426000.0, 76.0], [1406383482000.0, 76.0], [1406383545000.0, 76.0], [1406383603000.0, 76.0], [1406383663000.0, 76.0], [1406383723000.0, 76.0], [1406383780000.0, 76.0], [1406383843000.0, 76.0], [1406383903000.0, 76.0], [1406383963000.0, 76.0], [1406384022000.0, 76.0], [1406384081000.0, 76.0], [1406384143000.0, 76.0], [1406384203000.0, 76.0], [1406384262000.0, 76.0], [1406384322000.0, 76.0], [1406384382000.0, 76.0], [1406384446000.0, 76.0], [1406384501000.0, 76.0], [1406384562000.0, 76.0], [1406384622000.0, 76.0], [1406384685000.0, 76.0], [1406384743000.0, 76.0], [1406384803000.0, 76.0], [1406384862000.0, 76.0], [1406384922000.0, 76.0], [1406384983000.0, 76.0], [1406385043000.0, 76.0], [1406385102000.0, 76.0], [1406385163000.0, 76.0], [1406385223000.0, 76.0], [1406385281000.0, 76.0], [1406385342000.0, 76.0], [1406385401000.0, 76.0], [1406385462000.0, 76.0], [1406385523000.0, 76.0], [1406385583000.0, 76.0], [1406385642000.0, 76.0], [1406385701000.0, 76.0], [1406385763000.0, 76.0], [1406385823000.0, 76.0], [1406385882000.0, 76.0], [1406385942000.0, 76.0], [1406386002000.0, 76.0], [1406386063000.0, 76.0], [1406386122000.0, 76.0], [1406386183000.0, 76.0], [1406386241000.0, 76.0], [1406386306000.0, 76.0], [1406386363000.0, 76.0], [1406386420000.0, 76.0], [1406386482000.0, 76.0], [1406386543000.0, 76.0], [1406386603000.0, 76.0], [1406386662000.0, 76.0], [1406386722000.0, 76.0], [1406386782000.0, 76.0], [1406386842000.0, 76.0], [1406386903000.0, 76.0], [1406386955000.0, 76.0], [1406387025000.0, 76.0], [1406387082000.0, 76.0], [1406387143000.0, 76.0], [1406387203000.0, 76.0], [1406387262000.0, 76.0], [1406387322000.0, 76.0], [1406387382000.0, 76.0], [1406387443000.0, 76.0], [1406387502000.0, 76.0], [1406387563000.0, 76.0], [1406387623000.0, 76.0], [1406387682000.0, 76.0], [1406387746000.0, 76.0], [1406387805000.0, 76.0], [1406387865000.0, 76.0], [1406387923000.0, 76.0], [1406387982000.0, 76.0], [1406388043000.0, 76.0], [1406388101000.0, 76.0], [1406388163000.0, 76.0], [1406388222000.0, 76.0], [1406388287000.0, 76.0], [1406388343000.0, 76.0], [1406388402000.0, 76.0], [1406388462000.0, 76.0], [1406388523000.0, 76.0], [1406388580000.0, 76.0], [1406388642000.0, 76.0], [1406388705000.0, 76.0], [1406388762000.0, 76.0], [1406388821000.0, 76.0], [1406388882000.0, 76.0], [1406388945000.0, 76.0], [1406389005000.0, 76.0], [1406389062000.0, 76.0], [1406389122000.0, 76.0], [1406389181000.0, 76.0], [1406389241000.0, 76.0], [1406389302000.0, 76.0], [1406389363000.0, 76.0], [1406389421000.0, 76.0], [1406389485000.0, 76.0], [1406389542000.0, 76.0], [1406389605000.0, 76.0], [1406389661000.0, 76.0], [1406389721000.0, 76.0]]
        return render_to_response(
            'statistics/statistics_rtu.html',
            {'outside_temperature': rs_outside_temperature, 'supply_temperature': rs_supply_temperature,
             'return_temperature': rs_return_temperature, 'heating': rs_heating,
             'outside_damper_position': rs_outside_damper_position,
             'bypass_damper_position': rs_bypass_damper_position, 'cooling_mode': rs_cooling_mode,
             'heat_setpoint': rs_heat_setpoint, 'cool_setpoint': rs_cool_setpoint,
             'zones': zones, 'mac': mac, 'device_info': device_info,
             'nickname': device_nickname,
             'zone_nickname': zone_nickname},
            context)


@login_required(login_url='/login/')
def auto_update_smap_rtu(request):
    """Statistics page update for RTU"""
    if request.method == 'POST':
        print 'inside smap auto update RTU'
        _data = request.body
        _data = json.loads(_data)
        device_info = _data['device_info']

        device_smap_tag = '/bemoss/' + device_info.encode('ascii', 'ignore')
        device_smap_tag = device_smap_tag.encode('ascii', 'ignore')
        outside_temperature = device_smap_tag + '/outside_temperature'
        return_temperature = device_smap_tag + '/return_temperature'
        supply_temperature = device_smap_tag + '/supply_temperature'
        heat_setpoint = device_smap_tag + '/heat_setpoint'
        cool_setpoint = device_smap_tag + '/cool_setpoint'
        cooling_mode = device_smap_tag + '/cooling_mode'
        heating = device_smap_tag + '/heating'
        outside_damper_position = device_smap_tag + '/outside_damper_position'
        bypass_damper_position = device_smap_tag + '/bypass_damper_position'

        _uuid_outside_temperature = get_uuid_for_data_point(outside_temperature)
        _uuid_return_temperature = get_uuid_for_data_point(return_temperature)
        _uuid_supply_temperature = get_uuid_for_data_point(supply_temperature)
        _uuid_heat_setpoint = get_uuid_for_data_point(heat_setpoint)
        _uuid_cool_setpoint = get_uuid_for_data_point(cool_setpoint)
        _uuid_cooling_mode = get_uuid_for_data_point(cooling_mode)
        _uuid_heating = get_uuid_for_data_point(heating)
        _uuid_outside_damper_position = get_uuid_for_data_point(outside_damper_position)
        _uuid_bypass_damper_position = get_uuid_for_data_point(bypass_damper_position)

        rs_outside_temperature = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_outside_temperature)
        rs_return_temperature = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_return_temperature)
        rs_supply_temperature = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_supply_temperature)
        rs_heat_setpoint = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_heat_setpoint)
        rs_cool_setpoint = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_cool_setpoint)
        rs_cooling_mode = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_cooling_mode)
        rs_heating = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_heating)
        rs_outside_damper_position = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_outside_damper_position)
        rs_bypass_damper_position = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_bypass_damper_position)

        json_result = {'outside_temperature': rs_outside_temperature,
                       'supply_temperature': rs_supply_temperature,
                        'return_temperature': rs_return_temperature,
                        'heating': rs_heating,
                        'outside_damper_position': rs_outside_damper_position,
                        'bypass_damper_position': rs_bypass_damper_position,
                        'cooling_mode': rs_cooling_mode,
                        'heat_setpoint': rs_heat_setpoint,
                        'cool_setpoint': rs_cool_setpoint}

        print 'test'
        if request.is_ajax():
                return HttpResponse(json.dumps(json_result), mimetype='application/json')


def get_data_from_smap(url):
    rs = urllib2.urlopen(url)

    json_string = rs.read()
    parsed_json = json.loads(json_string)
    parsed_json = parsed_json[0]['Readings']
    return parsed_json