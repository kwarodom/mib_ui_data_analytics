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


from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
import json
import ast
import re
import time
from alerts.views import get_notifications

from .models import Building_Zone
from ZMQHelper.zmq_pub import ZMQ_PUB
from helper import config_helper
from ZMQHelper import zmq_topics

from .models import DeviceMetadata, Building_Zone, GlobalSetting
from thermostat.models import Thermostat
from VAV.models import VAV
from RTU.models import RTU
from smartplug.models import Plugload
from lighting.models import Lighting
from sensor.models import AmbientLightSensor, OccupancySensor, MotionSensor
from powermeter.models import PowerMeter
from VAV.models import VAV
from RTU.models import RTU
from admin.models import NetworkStatus
from django.contrib.auth.models import User

import _utils.defaults as __

kwargs = {'subscribe_address': __.SUB_SOCKET,
                    'publish_address': __.PUSH_SOCKET}

zmq_pub = ZMQ_PUB(**kwargs)


'''
@login_required(login_url='/login/')
def dashboard(request):
    #print 'inside dashboard view method'
    context = RequestContext(request)
    username = request.user
    
    devices = [ob.as_json() for ob in Device_Info.objects.filter(device_status='ON').order_by('device_type_id')]
    #print devices
    
    zones = [ob.as_json() for ob in Building_Zone.objects.all()]
    #print zones

    current_status = [ob.as_json() for ob in Current_Status.objects.all()]
    #print current_status
    
    devices_in_zones_count = {}
    for zone in zones:
        dict_zone = {zone['id']: 0}
        count = 0
        for device in devices:
            if device['zone']['id'] == zone['id']:
                dict_zone[zone['id']] += 1
                count += 1

        devices_in_zones_count[zone['id']] = count

    #print devices_in_zones_count

    context = RequestContext(request)
    request.zones = zones
    request.devices = devices
    request.device_count = devices_in_zones_count

    return render_to_response(
        'dashboard.html',
        {'devices': devices, 'zones':zones, 'dcount':devices_in_zones_count },
        context)
'''


@login_required(login_url='/login/')
def add_new_zone(request):
    if request.POST:
        _data = request.raw_post_data
        #print _data
        zone_id = ""
        a = re.compile("^[A-Za-z0-9_ ]*[A-Za-z0-9 ][A-Za-z0-9_ ]*$")
        if (a.match(_data)):
            p = Building_Zone.objects.get_or_create(zone_nickname=str(_data))
            zone_id = Building_Zone.objects.get(zone_nickname=str(_data)).zone_id
            global_settings = GlobalSetting(id=zone_id, heat_setpoint=70, cool_setpoint=72, illuminance=67, zone_id=zone_id)
            global_settings.save()
            message = "success"
            if request.is_ajax():
                return HttpResponse(str(zone_id), mimetype='text/plain')
        else:
            message = "invalid"
            if request.is_ajax():
                return HttpResponse("invalid", mimetype='text/plain')
    

@login_required(login_url='/login/')
def save_changes_modal(request):
    if request.POST:
        _data = request.raw_post_data
        #print type(_data)
        a = re.compile("^[A-Za-z0-9_]*[A-Za-z0-9][A-Za-z0-9_]*$")
        _data = ast.literal_eval(_data)
        if a.match(_data['nickname']):
            device_id = _data['id']
            nickname = _data['nickname']
            #device = Device_Info.objects.get(id=device_id)
            device_type_id = _data['device_type']
            if device_type_id == '1TH' or device_type_id == '1NST':
                device = Thermostat.objects.get(thermostat_id=device_id)
                device.nickname = nickname
                device.save()
            elif device_type_id == '1VAV':
                device = VAV.objects.get(vav_id=device_id)
                device.nickname = nickname
                device.save()
            elif device_type_id == '1RTU':
                device = RTU.objects.get(rtu_id=device_id)
                device.nickname = nickname
                device.save()
            elif device_type_id == '2DB' or device_type_id == '2SDB' or device_type_id =='2HUE' or device_type_id =='2WL' or device_type_id == '2WSL':
                device = Lighting.objects.get(lighting_id=device_id)
                device.nickname = nickname
                device.save()
            elif device_type_id == '3WSP' or device_type_id =='3MOD' or device_type_id =='3VTH' or device_type_id =='3DSP' or device_type_id == '3WP':
                device = Plugload.objects.get(plugload_id=device_id)
                device.nickname = nickname
                device.save()
            elif device_type_id == '4WSO':
                device = OccupancySensor.objects.get(occupancy_sensor_id=device_id)
                device.nickname = nickname
                device.save()
            elif device_type_id == '4WLS':
                device = AmbientLightSensor.objects.get(ambient_light_sensor_id=device_id)
                device.nickname = nickname
                device.save()
            elif device_type_id == '5DNT' or device_type_id == '5WTN':
                device = PowerMeter.objects.get(powermeter_id=device_id)
                device.nickname = nickname
                device.save()

            message = {'status':'success',
                       'device_id':device_id,
                       'nickname':nickname}
            if request.is_ajax():
                return HttpResponse(json.dumps(message), mimetype='application/json')
        else:
            message = "invalid"
            if request.is_ajax():
                return HttpResponse(json.dumps(message), mimetype='application/json')


@login_required(login_url='/login/')
def save_zone_nickname_changes(request):
    context = RequestContext(request)
    if request.POST:
        _data = request.raw_post_data
        a = re.compile("^[A-Za-z0-9_]*[A-Za-z0-9][A-Za-z0-9_]*$")
        _data = ast.literal_eval(_data)
        if a.match(_data['nickname']):
            zone_id = _data['id']
            nickname = _data['nickname']
            zone = Building_Zone.objects.get(zone_id=zone_id)
            zone.zone_nickname = nickname  # change field
            zone.save()
            message = {'status':'success',
                       'zone_id':zone_id,
                       'nickname':nickname}
            if request.is_ajax():
                return HttpResponse(json.dumps(message),mimetype='application/json')
        else:
            message = "invalid"
            if request.is_ajax():
                return HttpResponse(json.dumps(message),mimetype='application/json')

'''
def get_data_from_model():
    devices = [ob.as_json() for ob in Device_Info.objects.filter(device_status='ON')]
    #print devices
    zones = [ob.as_json() for ob in Building_Zone.objects.all()]
    #print zones
    devices_in_zones_count = []
    for zone in zones:
        dict_zone = {zone['id']:0}
        for device in devices:
            if device['zone']['id'] == zone['id']:
                dict_zone[zone['id']] = dict_zone[zone['id']]+1

        devices_in_zones_count.append(dict_zone)
    #print devices_in_zones_count
    req_data = {
                'devices': devices, 
                'zones': zones,
                'dcount': devices_in_zones_count}
    
    return req_data
'''

@login_required(login_url='/login/')
def identify_device(request):
    '''if request.POST:
        _data = request.raw_post_data
        _data = json.loads(_data)
        device_info = [ob.as_json() for ob in De.objects.filter(id=_data['id'])]
        device_id = device_info[0]['id']
        device_zone = device_info[0]['zone']['id']
        device_nickname = device_info[0]['nickname']
        zone_nickname = device_info[0]['zone']['zone_nickname']
        device_type_id = device_info[0]['device_type_id']

        if device_type_id == '1TH' or :
            device_type = 'thermostat'
        elif device_type_id == '2DB' or device_type_id == '2SDB' or device_type_id =='2HUE' or device_type_id =='2WL' or device_type_id == '2WSL':
            device_type = 'lighting'
        elif device_type_id == '3WSP' or device_type_id =='3MOD' or device_type_id =='3VTH' or device_type_id =='3DSP' or device_type_id == '3WP':
            device_type = 'plugload'
        elif device_type_id == '4WSO':
            device_type = 'occupancy'
        elif device_type_id == '4WLS':
            device_type = 'daylight_sensor'
        elif device_type_id == '5DNT':
            device_type = 'powermeter'

        info_required = "Identify device"
        ieb_topic = '/ui/agent/bemoss/' + str(device_zone) + '/' + device_type + '/' + device_id + '/identify'
        #wifi_3m50_update_send_topic = 'ui/agent/bemoss/zone1/thermostat/' + device_id + '/device_status'
        zmq_pub.requestAgent(ieb_topic, info_required, "text/plain", "UI")
        zmq_topics.reset_update_topic('identify_device_status_' + device_type)
        #print "Reset old device status"'''
    if request.POST:
        _data = request.raw_post_data
        _data = json.loads(_data)
        #print _data
        #print "Identify device"
        device_info = [ob.data_as_json() for ob in DeviceMetadata.objects.filter(device_id=_data['id'])]
        device_id = device_info[0]['device_id']
        if 'zone_id' in _data:
            device_zone = _data['zone_id']
        device_model = device_info[0]['device_model_id']
        device_type_id = device_model.device_model_id

        if device_type_id == '1TH' or device_type_id == '1NST':
            device_zone = Thermostat.objects.get(thermostat_id=device_id).zone_id
            #print device_zone
            device_type = 'thermostat'
        elif device_type_id == '1RTU':
            device_zone = RTU.objects.get(rtu_id=device_id).zone_id
            #print device_zone
            device_type = 'rtu'
        elif device_type_id == '1VAV':
            device_zone = VAV.objects.get(vav_id=device_id).zone_id
            #print device_zone
            device_type = 'vav'
        elif device_type_id == '2DB' or device_type_id == '2SDB' or device_type_id =='2HUE' or device_type_id =='2WL' or device_type_id == '2WSL':
            device_zone = Lighting.objects.get(lighting_id=device_id).zone_id
            #print device_zone
            device_type = 'lighting'
        elif device_type_id == '3WSP' or device_type_id =='3MOD' or device_type_id =='3VTH' or device_type_id =='3DSP' or device_type_id == '3WP':
            device_zone = Plugload.objects.get(plugload_id=device_id).zone_id
            #print device_zone
            device_type = 'plugload'
        elif device_type_id == '4WSO':
            device_zone = OccupancySensor.objects.get(occupancy_sensor_id=device_id).zone_id
            #print device_zone
            device_type = 'occupancy_sensor'
        elif device_type_id == '4WLS':
            device_zone = AmbientLightSensor.objects.get(ambient_light_sensor_id=device_id).zone_id
            #print device_zone
            device_type = 'ambient_light_sensor'
        elif device_type_id == '5DNT' or device_type_id == '5WTN':
            device_zone = PowerMeter.objects.get(power_meter_id=device_id).zone_id
            #print device_zone
            device_type = 'power_meter'

        info_required = "Identify device"
        ieb_topic = '/ui/agent/bemoss/' + str(device_zone) + '/' + device_type + '/' + device_id + '/identify'
        #wifi_3m50_update_send_topic = 'ui/agent/bemoss/zone1/thermostat/' + device_id + '/device_status'
        zmq_pub.requestAgent(ieb_topic, info_required, "text/plain", "UI")
        zmq_topics.reset_update_topic('identify_device_status_' + device_type)
        #print "Reset old device status"

    if request.is_ajax():
        return HttpResponse(json.dumps("success"), mimetype='application/json')


@login_required(login_url='/login/')
def identify_status(request):
    if request.POST:
        _data = request.raw_post_data
        device_info = [ob.data_as_json() for ob in DeviceMetadata.objects.filter(device_id=_data)]
        device_type_id = device_info[0]['device_model_id']
        device_type_id = device_type_id.device_model_id
        if device_type_id == '1TH' or device_type_id == '1NST':
            device_type = 'thermostat'
        elif device_type_id == '1RTU':
            device_type = 'rtu'
        elif device_type_id == '1VAV':
            device_type = 'vav'
        elif device_type_id == '2DB' or device_type_id == '2SDB' or device_type_id =='2HUE' or device_type_id =='2WL' or device_type_id == '2WSL':
            device_type = 'lighting'
        elif device_type_id == '3WSP' or device_type_id =='3MOD' or device_type_id =='3VTH' or device_type_id =='3DSP' or device_type_id == '3WP':
            device_type = 'plugload'
        elif device_type_id == '4WSO':
            device_type = 'occupancy_sensor'
        elif device_type_id == '4WLS':
            device_type = 'ambient_light_sensor'
        elif device_type_id == '5DNT' or device_type_id == '5WTN':
            device_type = 'power_meter'

        #print device_type
        #identify_status_message = recursive_get_device_update('identify_device_status_' + device_type)
        identify_status_message = config_helper.get_device_update_message('identify_device_status_' + device_type)

        data_split = identify_status_message.split("/")
        if data_split[0] == _data:
            result = data_split[1]

        json_result = {'status': result}
        zmq_topics.reset_update_topic('identify_device_status_' + device_type)

    if request.is_ajax():
        return HttpResponse(json.dumps(json_result), mimetype='application/json')


def recursive_get_device_update(update_variable):
    #wifi_3m50_device_initial_update = SessionHelper.get_device_update_message(update_variable)
    wifi_3m50_device_initial_update = config_helper.get_device_update_message(update_variable)
    vals = ""
    if wifi_3m50_device_initial_update != '{update_number}/{status}':
        vals = wifi_3m50_device_initial_update
        return vals
    else:
        time.sleep(5)
        recursive_get_device_update(update_variable)


@login_required(login_url='/login/')
def discover_nodes(request):
    #print 'inside dashboard - node discovery page method'
    context = RequestContext(request)

    username = request.user
    #print username

    if request.user.get_profile().group.name.lower() == 'admin':
        zones = [ob.as_json() for ob in Building_Zone.objects.all()]
        thermostats_sn = [ob.data_side_nav() for ob in Thermostat.objects.filter(network_status='ONLINE',
                                                                                 thermostat_id__bemoss=True)]
        vav_sn = [ob.data_side_nav() for ob in VAV.objects.filter(network_status='ONLINE', vav_id__bemoss=True)]
        rtu_sn = [ob.data_side_nav() for ob in RTU.objects.filter(network_status='ONLINE', rtu_id__bemoss=True)]
        lighting_sn = [ob.data_side_nav() for ob in Lighting.objects.filter(network_status='ONLINE',
                                                                            lighting_id__bemoss=True)]
        plugload_sn = [ob.data_side_nav() for ob in Plugload.objects.filter(network_status='ONLINE',
                                                                            plugload_id__bemoss=True)]
        occ_sensors_sn = [ob.data_side_nav() for ob in OccupancySensor.objects.filter(network_status='ONLINE',
                                                                                      occupancy_sensor_id__bemoss=True)]
        lt_sensors_sn = [ob.data_side_nav() for ob in AmbientLightSensor.objects.filter(network_status='ONLINE',
                                                                                        ambient_light_sensor_id__bemoss=True)]
        mtn_sensors_sn = [ob.data_side_nav() for ob in MotionSensor.objects.filter(network_status='ONLINE',
                                                                                   motion_sensor_id__bemoss=True)]
        powermeters_sn = [ob.data_side_nav() for ob in PowerMeter.objects.filter(network_status='ONLINE',
                                                                                 power_meter_id__bemoss=True)]
        bemoss_lite = [ob.data_dashboard() for ob in NetworkStatus.objects.filter(node_status='ONLINE')]
        active_al = get_notifications()
        context.update({'active_al':active_al})
        context.update({
            'zones': zones, 'thermostat_sn': thermostats_sn,
             'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn, 'occ_sensors_sn': occ_sensors_sn,
             'lt_sensors_sn': lt_sensors_sn, 'mtn_sensors_sn': mtn_sensors_sn,  'powermeters_sn': powermeters_sn,
             'vav_sn': vav_sn, 'rtu_sn': rtu_sn
        })

        return render_to_response(
            'dashboard/node_discovery.html',
            {'lites': bemoss_lite}, context)
    else:
        return HttpResponseRedirect('/home/')


@login_required(login_url='/login/')
def discover(request):
    #print 'inside dashboard - device discovery page method'
    context = RequestContext(request)

    username = request.user
    #print username

    zones = [ob.as_json() for ob in Building_Zone.objects.all()]
    thermostats_sn = [ob.data_side_nav() for ob in Thermostat.objects.filter(network_status='ONLINE',
                                                                             thermostat_id__bemoss=True)]
    vav_sn = [ob.data_side_nav() for ob in VAV.objects.filter(network_status='ONLINE', vav_id__bemoss=True)]
    rtu_sn = [ob.data_side_nav() for ob in RTU.objects.filter(network_status='ONLINE', rtu_id__bemoss=True)]
    lighting_sn = [ob.data_side_nav() for ob in Lighting.objects.filter(network_status='ONLINE',
                                                                        lighting_id__bemoss=True)]
    plugload_sn = [ob.data_side_nav() for ob in Plugload.objects.filter(network_status='ONLINE',
                                                                        plugload_id__bemoss=True)]
    occ_sensors_sn = [ob.data_side_nav() for ob in OccupancySensor.objects.filter(network_status='ONLINE',
                                                                                  occupancy_sensor_id__bemoss=True)]
    lt_sensors_sn = [ob.data_side_nav() for ob in AmbientLightSensor.objects.filter(network_status='ONLINE',
                                                                                    ambient_light_sensor_id__bemoss=True)]
    mtn_sensors_sn = [ob.data_side_nav() for ob in MotionSensor.objects.filter(network_status='ONLINE',
                                                                               motion_sensor_id__bemoss=True)]
    powermeters_sn = [ob.data_side_nav() for ob in PowerMeter.objects.filter(network_status='ONLINE',
                                                                             power_meter_id__bemoss=True)]

    if request.user.get_profile().group.name.lower() == 'admin':
        thermostats = [ob.data_dashboard() for ob in Thermostat.objects.filter(network_status='ONLINE', thermostat_id__bemoss=True)]
        vav = [ob.data_dashboard() for ob in VAV.objects.filter(network_status='ONLINE', vav_id__bemoss=True)]
        rtu = [ob.data_dashboard() for ob in RTU.objects.filter(network_status='ONLINE', rtu_id__bemoss=True)]
        plugloads = [ob.data_dashboard() for ob in Plugload.objects.filter(network_status='ONLINE', plugload_id__bemoss=True)]
        lighting_loads = [ob.data_dashboard() for ob in Lighting.objects.filter(network_status='ONLINE', lighting_id__bemoss=True)]
        occupancy_sensors = [ob.data_dashboard() for ob in OccupancySensor.objects.filter(network_status='ONLINE',
                                                                                          occupancy_sensor_id__bemoss=True)]
        light_sensors = [ob.data_dashboard() for ob in AmbientLightSensor.objects.filter(network_status='ONLINE',
                                                                                         ambient_light_sensor_id__bemoss=True)]
        motion_sensors = [ob.data_dashboard() for ob in MotionSensor.objects.filter(network_status='ONLINE', motion_sensor_id__bemoss=True)]
        powermeters = [ob.data_dashboard() for ob in PowerMeter.objects.filter(network_status='ONLINE', power_meter_id__bemoss=True)]
        bemoss_lite = [ob.data_dashboard() for ob in NetworkStatus.objects.filter(node_status='ONLINE')]
        context.update({
            'zones': zones, 'thermostat_sn': thermostats_sn,
             'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn, 'occ_sensors_sn': occ_sensors_sn,
             'lt_sensors_sn': lt_sensors_sn, 'mtn_sensors_sn': mtn_sensors_sn,  'powermeters_sn': powermeters_sn,
             'vav_sn': vav_sn, 'rtu_sn': rtu_sn
        })
        active_al = get_notifications()
        context.update({'active_al':active_al})
        '''return render_to_response(
            'dashboard/discovery.html',
            {'thermostats': thermostats, 'plugloads':plugloads, 'lighting_loads':lighting_loads,
             'occupancy_sensors': occupancy_sensors, 'light_sensors': light_sensors, 'powermeters': powermeters, 'rtu': rtu,
             'vav': vav, 'lites': bemoss_lite,
             'zones': zones, 'thermostat_sn': thermostats_sn,
             'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn, 'occ_sensors_sn': occ_sensors_sn,
             'lt_sensors_sn': lt_sensors_sn, 'mtn_sensors_sn': mtn_sensors_sn,  'powermeters_sn': powermeters_sn,
             'vav_sn': vav_sn, 'rtu_sn': rtu_sn}, context)'''
        return render_to_response(
            'dashboard/discovery.html',
            {'thermostats': thermostats, 'plugloads':plugloads, 'lighting_loads':lighting_loads,
             'occupancy_sensors': occupancy_sensors, 'light_sensors': light_sensors, 'powermeters': powermeters, 'rtu': rtu,
             'vav': vav, 'lites': bemoss_lite}, context)
    else:
        return HttpResponseRedirect('/home/')


@login_required(login_url='/login/')
def change_zones_thermostats(request):
    #print "Inside change zones for hvac controllers"
    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        #print _data

        for thermostat in _data['thermostats']:
            if thermostat[1] != "Assign a New Zone":
                zone = Building_Zone.objects.get(zone_nickname__iexact=thermostat[1])
                th_instance = Thermostat.objects.get(thermostat_id=thermostat[0])
                #/ui/networkagent/device_id/old_zone_id/new_zone_id/change
                if zone.zone_id != th_instance.zone_id:
                    zone_update_send_topic = '/ui/networkagent/' + str(thermostat[0]) + '/' + str(th_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")

                th_instance.zone = zone  # change field
                th_instance.nickname = thermostat[2]
                if thermostat[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(thermostat[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    d_info = DeviceMetadata.objects.get(device_id=thermostat[0])
                    d_info.bemoss = False
                    d_info.save()
                    #th_instance.network_status = 'NBD'
                th_instance.save()
            else:
                zone = Building_Zone.objects.get(zone_id=999)
                th_instance = Thermostat.objects.get(thermostat_id=thermostat[0])
                th_instance.zone = zone  # change field
                th_instance.nickname = thermostat[2]
                if thermostat[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(thermostat[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    d_info = DeviceMetadata.objects.get(device_id=thermostat[0])
                    d_info.bemoss = False
                    d_info.save()
                    #th_instance.network_status = 'NBD'
                th_instance.save()

        for vav in _data['vav']:
            if vav[1] != "Assign a New Zone":
                zone = Building_Zone.objects.get(zone_nickname__iexact=vav[1])
                vav_instance = VAV.objects.get(vav_id=vav[0])
                if zone.zone_id != vav_instance.zone_id:
                    zone_update_send_topic = '/ui/networkagent/' + str(vav[0]) + '/' + str(vav_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                vav_instance.zone = zone  # change field
                vav_instance.nickname = vav[2]
                if vav[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(vav[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    #vav_instance.network_status = 'NBD'
                    d_info = DeviceMetadata.objects.get(device_id=vav[0])
                    d_info.bemoss = False
                    d_info.save()
                vav_instance.save()
            else:
                zone = Building_Zone.objects.get(zone_id=999)
                vav_instance = VAV.objects.get(vav_id=vav[0])
                vav_instance.zone = zone  # change field
                vav_instance.nickname = vav[2]
                if vav[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(vav[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    #vav_instance.network_status = 'NBD'
                    d_info = DeviceMetadata.objects.get(device_id=vav[0])
                    d_info.bemoss = False
                    d_info.save()
                vav_instance.save()

        for rtu in _data['rtu']:
            if rtu[1] != "Assign a New Zone":
                zone = Building_Zone.objects.get(zone_nickname__iexact=rtu[1])
                rtu_instance = RTU.objects.get(rtu_id=rtu[0])
                if zone.zone_id != rtu_instance.zone_id:
                    zone_update_send_topic = '/ui/networkagent/' + str(rtu[0]) + '/' + str(rtu_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                rtu_instance.zone = zone  # change field
                rtu_instance.nickname = rtu[2]
                if rtu[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(rtu[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    #rtu_instance.network_status = 'NBD'
                    d_info = DeviceMetadata.objects.get(device_id=rtu[0])
                    d_info.bemoss = False
                    d_info.save()
                rtu_instance.save()
            else:
                zone = Building_Zone.objects.get(zone_id=999)
                rtu_instance = RTU.objects.get(rtu_id=rtu[0])
                rtu_instance.zone = zone  # change field
                rtu_instance.nickname = rtu[2]
                if rtu[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(rtu[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    #rtu_instance.network_status = 'NBD'
                    d_info = DeviceMetadata.objects.get(device_id=rtu[0])
                    d_info.bemoss = False
                    d_info.save()
                rtu_instance.save()

    if request.is_ajax():
        return HttpResponse(json.dumps("success"), mimetype='application/json')


@login_required(login_url='/login/')
def change_zones_plugloads(request):
    #print "Inside change zones for plugloads"
    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        #print _data

        for plugload in _data['data']:
            if plugload[1] != "Assign a New Zone":
                zone = Building_Zone.objects.get(zone_nickname__iexact=plugload[1])
                pl_instance = Plugload.objects.get(plugload_id=plugload[0])
                if zone.zone_id != pl_instance.zone_id:
                    zone_update_send_topic = '/ui/networkagent/' + str(plugload[0]) + '/' + str(pl_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                pl_instance.zone = zone  # change field
                pl_instance.nickname = plugload[2]
                if plugload[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(plugload[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    #pl_instance.network_status = 'NBD'
                    d_info = DeviceMetadata.objects.get(device_id=plugload[0])
                    d_info.bemoss = False
                    d_info.save()
                pl_instance.save()
            else:
                zone = Building_Zone.objects.get(zone_id=999)
                pl_instance = Plugload.objects.get(plugload_id=plugload[0])
                pl_instance.zone = zone  # change field
                pl_instance.nickname = plugload[2]
                if plugload[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(plugload[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    #pl_instance.network_status = 'NBD'
                    d_info = DeviceMetadata.objects.get(device_id=plugload[0])
                    d_info.bemoss = False
                    d_info.save()
                pl_instance.save()

    if request.is_ajax():
        return HttpResponse(json.dumps("success"), mimetype='application/json')


@login_required(login_url='/login/')
def change_zones_lighting_loads(request):
    #print "Inside change zones for lighting loads"
    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        #print _data

        for lt_load in _data['data']:
            if lt_load[1] != "Assign a New Zone":
                zone = Building_Zone.objects.get(zone_nickname__iexact=lt_load[1])
                lt_instance = Lighting.objects.get(lighting_id=lt_load[0])
                if zone.zone_id != lt_instance.zone_id:
                    zone_update_send_topic = '/ui/networkagent/' + str(lt_load[0]) + '/' + str(lt_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                lt_instance.zone = zone  # change field
                lt_instance.nickname = lt_load[2]
                if lt_load[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(lt_load[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    #lt_instance.network_status = 'NBD'
                    d_info = DeviceMetadata.objects.get(device_id=lt_load[0])
                    d_info.bemoss = False
                    d_info.save()
                lt_instance.save()
            else:
                zone = Building_Zone.objects.get(zone_id=999)
                lt_instance = Lighting.objects.get(lighting_id=lt_load[0])
                lt_instance.zone = zone  # change field
                lt_instance.nickname = lt_load[2]
                if lt_load[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(lt_load[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    #lt_instance.network_status = 'NBD'
                    d_info = DeviceMetadata.objects.get(device_id=lt_load[0])
                    d_info.bemoss = False
                    d_info.save()
                lt_instance.save()

    if request.is_ajax():
        return HttpResponse(json.dumps("success"), mimetype='application/json')


@login_required(login_url='/login/')
def change_zones_powermeters(request):
    #print "Inside change zones for powermeters"
    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        #print _data

        for pm in _data['data']:
            if pm[1] != "Assign a New Zone":
                zone = Building_Zone.objects.get(zone_nickname__iexact=pm[1])
                pm_instance = PowerMeter.objects.get(power_meter_id=pm[0])
                if zone.zone_id != pm_instance.zone_id:
                    zone_update_send_topic = '/ui/networkagent/' + str(pm[0]) + '/' + str(pm_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                pm_instance.zone = zone  # change field
                pm_instance.nickname = pm[2]
                if pm[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(pm[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    #pm_instance.network_status = 'NBD'
                    d_info = DeviceMetadata.objects.get(device_id=pm[0])
                    d_info.bemoss = False
                    d_info.save()
                pm_instance.save()
            else:
                zone = Building_Zone.objects.get(zone_id=999)
                pm_instance = PowerMeter.objects.get(power_meter_id=pm[0])
                pm_instance.zone = zone  # change field
                pm_instance.nickname = pm[2]
                if pm[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(pm[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    #pm_instance.network_status = 'NBD'
                    d_info = DeviceMetadata.objects.get(device_id=pm[0])
                    d_info.bemoss = False
                    d_info.save()
                pm_instance.save()

    if request.is_ajax():
        return HttpResponse(json.dumps("success"), mimetype='application/json')


@login_required(login_url='/login/')
def change_zones_sensors(request):
    #print "Inside change zones for sensors"
    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        #print _data

        for occs in _data['occupancy']:
            if occs[1] != "Assign a New Zone":
                zone = Building_Zone.objects.get(zone_nickname__iexact=occs[1])
                occ_instance = OccupancySensor.objects.get(occupancy_sensor_id=occs[0])
                if zone.zone_id != occ_instance.zone_id:
                    zone_update_send_topic = '/ui/networkagent/' + str(occs[0]) + '/' + str(occ_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                occ_instance.zone = zone  # change field
                occ_instance.nickname = occs[2]
                if occs[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(occs[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    #occ_instance.network_status = 'NBD'
                    d_info = DeviceMetadata.objects.get(device_id=occs[0])
                    d_info.bemoss = False
                    d_info.save()
                occ_instance.save()
            else:
                zone = Building_Zone.objects.get(zone_id=999)
                occ_instance = OccupancySensor.objects.get(occupancy_sensor_id=occs[0])
                occ_instance.zone = zone  # change field
                occ_instance.nickname = occs[2]
                if occs[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(occs[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    #occ_instance.network_status = 'NBD'
                    d_info = DeviceMetadata.objects.get(device_id=occs[0])
                    d_info.bemoss = False
                    d_info.save()
                occ_instance.save()

        for lts in _data['light']:
            if lts[1] != "Assign a New Zone":
                zone = Building_Zone.objects.get(zone_nickname__iexact=lts[1])
                lts_instance = AmbientLightSensor.objects.get(ambient_light_sensor_id=lts[0])
                if zone.zone_id != lts_instance.zone_id:
                    zone_update_send_topic = '/ui/networkagent/' + str(lts[0]) + '/' + str(lts_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                lts_instance.zone = zone  # change field
                lts_instance.nickname = lts[2]
                if lts[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(lts[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic,'{"auth_token": "bemoss"}', "text/plain", "UI")
                    #lts_instance.network_status = 'NBD'
                    d_info = DeviceMetadata.objects.get(device_id=lts[0])
                    d_info.bemoss = False
                    d_info.save()
                lts_instance.save()
            else:
                zone = Building_Zone.objects.get(zone_id=999)
                lts_instance = AmbientLightSensor.objects.get(ambient_light_sensor_id=lts[0])
                lts_instance.zone = zone  # change field
                lts_instance.nickname = lts[2]
                if lts[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(lts[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    #lts_instance.network_status = 'NBD'
                    d_info = DeviceMetadata.objects.get(device_id=lts[0])
                    d_info.bemoss = False
                    d_info.save()
                lts_instance.save()

        for ms in _data['motion']:
            if ms[1] != "Assign a New Zone":
                zone = Building_Zone.objects.get(zone_nickname__iexact=ms[1])
                ms_instance = MotionSensor.objects.get(motion_sensor_id=ms[0])
                if zone.zone_id != ms_instance.zone_id:
                    zone_update_send_topic = '/ui/networkagent/' + str(ms[0]) + '/' + str(ms_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                ms_instance.zone = zone  # change field
                ms_instance.nickname = ms[2]
                if ms[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(ms[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    #ms_instance.network_status = 'NBD'
                    d_info = DeviceMetadata.objects.get(device_id=ms[0])
                    d_info.bemoss = False
                    d_info.save()
                ms_instance.save()
            else:
                zone = Building_Zone.objects.get(zone_id=999)
                ms_instance = MotionSensor.objects.get(motion_sensor_id=ms[0])
                ms_instance.zone = zone  # change field
                ms_instance.nickname = ms[2]
                if ms[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(ms[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    #ms_instance.network_status = 'NBD'
                    d_info = DeviceMetadata.objects.get(device_id=ms[0])
                    d_info.bemoss = False
                    d_info.save()
                ms_instance.save()

    if request.is_ajax():
        return HttpResponse(json.dumps("success"), mimetype='application/json')


@login_required(login_url='/login/')
def change_zones_lite(request):
    #print "Inside change zones for bemoss lite"
    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        #print _data

        for lite in _data['data']:
            if lite[1] != "Associate with Zone":
                zone = Building_Zone.objects.get(zone_nickname__iexact=lite[1])
                lite_instance = NetworkStatus.objects.get(node_id=lite[0])
                lite_instance.associated_zone = zone  # change field
                lite_instance.save()

    if request.is_ajax():
        return HttpResponse(json.dumps("success"), mimetype='application/json')


@login_required(login_url='/login/')
def bemoss_home(request):
    context = RequestContext(request)
    username = request.user

    zones = [ob.as_json() for ob in Building_Zone.objects.all()]
    thermostats_sn = [ob.data_side_nav() for ob in Thermostat.objects.filter(network_status='ONLINE',
                                                                             thermostat_id__bemoss=True)]
    vav_sn = [ob.data_side_nav() for ob in VAV.objects.filter(network_status='ONLINE', vav_id__bemoss=True)]
    rtu_sn = [ob.data_side_nav() for ob in RTU.objects.filter(network_status='ONLINE', rtu_id__bemoss=True)]
    lighting_sn = [ob.data_side_nav() for ob in Lighting.objects.filter(network_status='ONLINE',
                                                                        lighting_id__bemoss=True)]
    plugload_sn = [ob.data_side_nav() for ob in Plugload.objects.filter(network_status='ONLINE',
                                                                        plugload_id__bemoss=True)]
    occ_sensors_sn = [ob.data_side_nav() for ob in OccupancySensor.objects.filter(network_status='ONLINE',
                                                                                  occupancy_sensor_id__bemoss=True)]
    lt_sensors_sn = [ob.data_side_nav() for ob in AmbientLightSensor.objects.filter(network_status='ONLINE',
                                                                                    ambient_light_sensor_id__bemoss=True)]
    mtn_sensors_sn = [ob.data_side_nav() for ob in MotionSensor.objects.filter(network_status='ONLINE',
                                                                               motion_sensor_id__bemoss=True)]
    powermeters_sn = [ob.data_side_nav() for ob in PowerMeter.objects.filter(network_status='ONLINE',
                                                                             power_meter_id__bemoss=True)]

    device_count ={
                    "devices": {
                    }
                    }

    all_zones = Building_Zone.objects.all()
    for zone in all_zones:
        th_count = Thermostat.objects.filter(network_status='ONLINE', zone_id=zone.zone_id,
                                             thermostat_id__bemoss=True).count()
        vav_count = VAV.objects.filter(network_status='ONLINE', zone_id=zone.zone_id, vav_id__bemoss=True).count()
        rtu_count = RTU.objects.filter(network_status='ONLINE', zone_id=zone.zone_id, rtu_id__bemoss=True).count()
        t_count = th_count + vav_count + rtu_count

        pl_count = Plugload.objects.filter(network_status='ONLINE', zone_id=zone.zone_id, plugload_id__bemoss=True).count()
        lt_count = Lighting.objects.filter(network_status='ONLINE', zone_id=zone.zone_id, lighting_id__bemoss=True).count()
        occ_count = OccupancySensor.objects.filter(network_status='ONLINE', zone_id=zone.zone_id,
                                                   occupancy_sensor_id__bemoss=True).count()
        lt_sens_count = AmbientLightSensor.objects.filter(network_status='ONLINE', zone_id=zone.zone_id,
                                                          ambient_light_sensor_id__bemoss=True).count()
        msens_count = MotionSensor.objects.filter(network_status='ONLINE', zone_id=zone.zone_id,
                                                  motion_sensor_id__bemoss=True).count()
        ss_count = occ_count + lt_sens_count + msens_count

        pm_count = PowerMeter.objects.filter(network_status='ONLINE', zone_id=zone.zone_id, power_meter_id__bemoss=True).count()

        device_count['devices'][zone.zone_id] = {'th': 0, 'pl': 0, 'lt': 0, 'ss': 0, 'pm': 0}
        device_count['devices'][zone.zone_id]['th'] = t_count
        device_count['devices'][zone.zone_id]['pl'] = pl_count
        device_count['devices'][zone.zone_id]['lt'] = lt_count
        device_count['devices'][zone.zone_id]['ss'] = ss_count
        device_count['devices'][zone.zone_id]['pm'] = pm_count

    #print device_count

    zones_p = [ob.data_dashboard() for ob in Building_Zone.objects.all().order_by('zone_nickname')]
    #print zones_p

    for zone in zones_p:
        z_id = zone['id']
        zone['t_count'] = device_count['devices'][z_id]['th']
        zone['pl_count'] = device_count['devices'][z_id]['pl']
        zone['lt_count'] = device_count['devices'][z_id]['lt']
        zone['ss_count'] = device_count['devices'][z_id]['ss']
        zone['pm_count'] = device_count['devices'][z_id]['pm']
    active_al = get_notifications()
    context.update({'active_al':active_al})
    context.update({
            'zones': zones, 'thermostat_sn': thermostats_sn,
             'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn, 'occ_sensors_sn': occ_sensors_sn,
             'lt_sensors_sn': lt_sensors_sn, 'mtn_sensors_sn': mtn_sensors_sn,  'powermeters_sn': powermeters_sn,
             'vav_sn': vav_sn, 'rtu_sn': rtu_sn
    })

    return render_to_response(
        'dashboard/dashboard.html',
        {'zones_p': zones_p}, context)


@login_required(login_url='/login/')
def change_global_settings(request):
    #context = RequestContext(request)
    #username = request.user

    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        #print _data

        zone_id = _data['zone_id']
        zone = Building_Zone.objects.get(zone_id=zone_id)
        gsettings = GlobalSetting.objects.get(zone_id=zone)
        gsettings.heat_setpoint = _data['heat_setpoint']
        gsettings.cool_setpoint = _data['cool_setpoint']
        gsettings.illuminance = _data['illumination']
        gsettings.save()

        if request.is_ajax():
            return HttpResponse(json.dumps("success"), mimetype='application/json')


@login_required(login_url='/login/')
def zone_device_listing(request, zone_dev):
    context = RequestContext(request)
    username = request.user

    zone_dev = zone_dev.encode('ascii', 'ignore')
    zone_info = zone_dev.split("_")
    zone_id = zone_info[0]
    device_type = zone_info[1]

    #Side navigation bar
    zones = [ob.as_json() for ob in Building_Zone.objects.all()]
    thermostats_sn = [ob.data_side_nav() for ob in Thermostat.objects.filter(network_status='ONLINE',
                                                                             thermostat_id__bemoss=True)]
    vav_sn = [ob.data_side_nav() for ob in VAV.objects.filter(network_status='ONLINE', vav_id__bemoss=True)]
    rtu_sn = [ob.data_side_nav() for ob in RTU.objects.filter(network_status='ONLINE', rtu_id__bemoss=True)]
    lighting_sn = [ob.data_side_nav() for ob in Lighting.objects.filter(network_status='ONLINE',
                                                                        lighting_id__bemoss=True)]
    plugload_sn = [ob.data_side_nav() for ob in Plugload.objects.filter(network_status='ONLINE',
                                                                        plugload_id__bemoss=True)]
    occ_sensors_sn = [ob.data_side_nav() for ob in OccupancySensor.objects.filter(network_status='ONLINE',
                                                                                  occupancy_sensor_id__bemoss=True)]
    lt_sensors_sn = [ob.data_side_nav() for ob in AmbientLightSensor.objects.filter(network_status='ONLINE',
                                                                                    ambient_light_sensor_id__bemoss=True)]
    mtn_sensors_sn = [ob.data_side_nav() for ob in MotionSensor.objects.filter(network_status='ONLINE',
                                                                               motion_sensor_id__bemoss=True)]
    powermeters_sn = [ob.data_side_nav() for ob in PowerMeter.objects.filter(network_status='ONLINE',
                                                                             power_meter_id__bemoss=True)]

    context.update({
        'zones': zones, 'thermostat_sn': thermostats_sn,
         'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn, 'occ_sensors_sn': occ_sensors_sn,
         'lt_sensors_sn': lt_sensors_sn, 'mtn_sensors_sn': mtn_sensors_sn,  'powermeters_sn': powermeters_sn,
         'vav_sn': vav_sn, 'rtu_sn': rtu_sn
    })

    #For the page
    if device_type == 'th':
        thermostats = [ob.data_as_json() for ob in Thermostat.objects.filter(zone_id=zone_id, thermostat_id__bemoss=True)]
        if len(thermostats) != 0:
            zone_nickname = thermostats[0]['zone']['zone_nickname']
        #print thermostats

        rtu = [ob.as_json() for ob in RTU.objects.filter(zone_id=zone_id, rtu_id__bemoss=True)]
        if len(rtu) != 0:
            zone_nickname = rtu[0]['zone']['zone_nickname']
        #print rtu

        vav = [ob.as_json() for ob in VAV.objects.filter(zone_id=zone_id, vav_id__bemoss=True)]
        if len(vav) != 0:
            zone_nickname = vav[0]['zone']['zone_nickname']
        #print vav
        active_al = get_notifications()
        context.update({'active_al':active_al})
        return render_to_response(
            'dashboard/thermostats.html',
            {'thermostats': thermostats, 'rtu': rtu, 'vav': vav, 'zone_id': zone_id, 'zone_nickname': zone_nickname,
             'zones': zones, 'thermostat_sn': thermostats_sn, 'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn,
             'occ_sensors_sn': occ_sensors_sn, 'lt_sensors_sn': lt_sensors_sn, 'mtn_sensors_sn': mtn_sensors_sn,
             'powermeters_sn': powermeters_sn, 'vav_sn': vav_sn, 'rtu_sn': rtu_sn}, context)

    elif device_type == 'lt':
        lighting = [ob.data_as_json() for ob in Lighting.objects.filter(zone_id=zone_id, lighting_id__bemoss=True)]
        zone_nickname = lighting[0]['zone']['zone_nickname']
        #print lighting

        return render_to_response(
            'dashboard/lighting_loads.html',
            {'lighting_loads': lighting, 'zone_id': zone_id, 'zone_nickname': zone_nickname,
             'zones': zones, 'thermostat_sn': thermostats_sn, 'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn,
             'occ_sensors_sn': occ_sensors_sn, 'lt_sensors_sn': lt_sensors_sn, 'mtn_sensors_sn': mtn_sensors_sn,
             'powermeters_sn': powermeters_sn, 'vav_sn': vav_sn, 'rtu_sn': rtu_sn}, context)

    elif device_type == 'pl':
        plugloads = [ob.data_as_json() for ob in Plugload.objects.filter(zone_id=zone_id, plugload_id__bemoss=True)]
        zone_nickname = plugloads[0]['zone']['zone_nickname']
        #print plugloads

        return render_to_response(
            'dashboard/plugloads.html',
            {'plugloads': plugloads, 'zone_id': zone_id, 'zone_nickname': zone_nickname,
             'zones': zones, 'thermostat_sn': thermostats_sn, 'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn,
             'occ_sensors_sn': occ_sensors_sn, 'lt_sensors_sn': lt_sensors_sn, 'mtn_sensors_sn': mtn_sensors_sn,
             'powermeters_sn': powermeters_sn, 'vav_sn': vav_sn, 'rtu_sn': rtu_sn}, context)

    elif device_type == 'ss':
        occ_sensors = [ob.data_as_json() for ob in OccupancySensor.objects.filter(zone_id=zone_id, occupancy_sensor_id__bemoss=True)]
        if len(occ_sensors) != 0:
            zone_nickname = occ_sensors[0]['zone']['zone_nickname']
        #print occ_sensors

        lt_sensors = [ob.data_as_json() for ob in AmbientLightSensor.objects.filter(zone_id=zone_id, ambient_light_sensor_id__bemoss=True)]
        if len(lt_sensors) != 0:
            zone_nickname = lt_sensors[0]['zone']['zone_nickname']
        #print lt_sensors

        m_sensors = [ob.data_as_json() for ob in MotionSensor.objects.filter(zone_id=zone_id, motion_sensor_id__bemoss=True)]
        if len(m_sensors) != 0:
            zone_nickname = m_sensors[0]['zone']['zone_nickname']
        #print m_sensors

        return render_to_response(
            'dashboard/sensors.html',
            {'occ_sensors': occ_sensors, 'lt_sensors': lt_sensors, 'm_sensors': m_sensors, 'zone_id': zone_id,
            'zone_nickname': zone_nickname,
             'zones': zones, 'thermostat_sn': thermostats_sn, 'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn,
             'occ_sensors_sn': occ_sensors_sn, 'lt_sensors_sn': lt_sensors_sn, 'mtn_sensors_sn': mtn_sensors_sn,
             'powermeters_sn': powermeters_sn, 'vav_sn': vav_sn, 'rtu_sn': rtu_sn}, context)

    elif device_type == 'pm':
        pm = [ob.data_as_json() for ob in PowerMeter.objects.filter(zone_id=zone_id, power_meter_id__bemoss=True)]
        zone_nickname = pm[0]['zone']['zone_nickname']
        #print pm

        return render_to_response(
            'dashboard/powermeters.html',
            {'powermeters': pm, 'zone_id': zone_id, 'zone_nickname': zone_nickname,
             'zones': zones, 'thermostat_sn': thermostats_sn, 'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn,
             'occ_sensors_sn': occ_sensors_sn, 'lt_sensors_sn': lt_sensors_sn, 'mtn_sensors_sn': mtn_sensors_sn,
             'powermeters_sn': powermeters_sn, 'vav_sn': vav_sn, 'rtu_sn': rtu_sn}, context)


@login_required(login_url='/login/')
def zone_device_all_listing(request, zone_dev):
    context = RequestContext(request)
    username = request.user

    zone_id = zone_dev.encode('ascii', 'ignore')

    #Side navigation bar
    zones = [ob.as_json() for ob in Building_Zone.objects.all()]
    thermostats_sn = [ob.data_side_nav() for ob in Thermostat.objects.filter(network_status='ONLINE',
                                                                             thermostat_id__bemoss=True)]
    vav_sn = [ob.data_side_nav() for ob in VAV.objects.filter(network_status='ONLINE', vav_id__bemoss=True)]
    rtu_sn = [ob.data_side_nav() for ob in RTU.objects.filter(network_status='ONLINE', rtu_id__bemoss=True)]
    lighting_sn = [ob.data_side_nav() for ob in Lighting.objects.filter(network_status='ONLINE',
                                                                        lighting_id__bemoss=True)]
    plugload_sn = [ob.data_side_nav() for ob in Plugload.objects.filter(network_status='ONLINE',
                                                                        plugload_id__bemoss=True)]
    occ_sensors_sn = [ob.data_side_nav() for ob in OccupancySensor.objects.filter(network_status='ONLINE',
                                                                                  occupancy_sensor_id__bemoss=True)]
    lt_sensors_sn = [ob.data_side_nav() for ob in AmbientLightSensor.objects.filter(network_status='ONLINE',
                                                                                    ambient_light_sensor_id__bemoss=True)]
    mtn_sensors_sn = [ob.data_side_nav() for ob in MotionSensor.objects.filter(network_status='ONLINE',
                                                                               motion_sensor_id__bemoss=True)]
    powermeters_sn = [ob.data_side_nav() for ob in PowerMeter.objects.filter(network_status='ONLINE',
                                                                             power_meter_id__bemoss=True)]
    active_al = get_notifications()
    context.update({'active_al':active_al})
    context.update({
        'zones': zones, 'thermostat_sn': thermostats_sn,
         'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn, 'occ_sensors_sn': occ_sensors_sn,
         'lt_sensors_sn': lt_sensors_sn, 'mtn_sensors_sn': mtn_sensors_sn,  'powermeters_sn': powermeters_sn,
         'vav_sn': vav_sn, 'rtu_sn': rtu_sn
    })

    #For the page

    thermostats = [ob.data_as_json() for ob in Thermostat.objects.filter(zone_id=zone_id, thermostat_id__bemoss=True)]
    if len(thermostats) != 0:
        zone_nickname = thermostats[0]['zone']['zone_nickname']
    #print thermostats

    rtu = [ob.as_json() for ob in RTU.objects.filter(zone_id=zone_id, rtu_id__bemoss=True)]
    if len(rtu) != 0:
        zone_nickname = rtu[0]['zone']['zone_nickname']
    #print rtu

    vav = [ob.as_json() for ob in VAV.objects.filter(zone_id=zone_id, vav_id__bemoss=True)]
    if len(vav) != 0:
        zone_nickname = vav[0]['zone']['zone_nickname']
    #print vav

    lighting = [ob.data_as_json() for ob in Lighting.objects.filter(zone_id=zone_id, lighting_id__bemoss=True)]
    if len(lighting) != 0:
        zone_nickname = lighting[0]['zone']['zone_nickname']
    #print lighting

    plugloads = [ob.data_as_json() for ob in Plugload.objects.filter(zone_id=zone_id, plugload_id__bemoss=True)]
    if len(plugloads) != 0:
        zone_nickname = plugloads[0]['zone']['zone_nickname']
    #print plugloads

    occ_sensors = [ob.data_as_json() for ob in OccupancySensor.objects.filter(zone_id=zone_id, occupancy_sensor_id__bemoss=True)]
    if len(occ_sensors) != 0:
        zone_nickname = occ_sensors[0]['zone']['zone_nickname']
    #print occ_sensors

    lt_sensors = [ob.data_as_json() for ob in AmbientLightSensor.objects.filter(zone_id=zone_id, ambient_light_sensor_id__bemoss=True)]
    if len(lt_sensors) != 0:
        zone_nickname = lt_sensors[0]['zone']['zone_nickname']
    #print lt_sensors

    m_sensors = [ob.data_as_json() for ob in MotionSensor.objects.filter(zone_id=zone_id, motion_sensor_id__bemoss=True)]
    if len(m_sensors) != 0:
        zone_nickname = m_sensors[0]['zone']['zone_nickname']
    #print m_sensors

    pm = [ob.data_as_json() for ob in PowerMeter.objects.filter(zone_id=zone_id, power_meter_id__bemoss=True)]
    if len(pm) != 0:
        zone_nickname = pm[0]['zone']['zone_nickname']
    #print pm

    return render_to_response(
        'dashboard/zone_devices_all.html',
        {'thermostats': thermostats, 'vav': vav, 'rtu': rtu, 'lighting_loads': lighting,
         'plugloads': plugloads, 'occ_sensors':occ_sensors, 'lt_sensors': lt_sensors,
         'm_sensors': m_sensors, 'powermeters': pm, 'zone_id': zone_id, 'zone_nickname': zone_nickname,
         }, context)

@login_required(login_url='/login/')
def modify_thermostats(request):
    #print "Inside modify hvac controllers"
    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        #print _data

        for thermostat in _data['thermostats']:
            zone = Building_Zone.objects.get(zone_nickname__iexact=thermostat[2])
            th_instance = Thermostat.objects.get(thermostat_id=thermostat[0])
            if zone.zone_id != th_instance.zone_id:
                zone_update_send_topic = '/ui/networkagent/' + str(thermostat[0]) + '/' + str(th_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
            th_instance.zone = zone  # change field
            th_instance.nickname = thermostat[1]
            th_instance.save()

        for vav in _data['vav']:
            zone = Building_Zone.objects.get(zone_nickname__iexact=vav[2])
            vav_instance = VAV.objects.get(vav_id=vav[0])
            if zone.zone_id != vav_instance.zone_id:
                zone_update_send_topic = '/ui/networkagent/' + str(vav[0]) + '/' + str(vav_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
            vav_instance.zone = zone  # change field
            vav_instance.nickname = vav[1]
            vav_instance.save()

        for rtu in _data['rtu']:
            zone = Building_Zone.objects.get(zone_nickname__iexact=rtu[2])
            rtu_instance = RTU.objects.get(rtu_id=rtu[0])
            if zone.zone_id != rtu_instance.zone_id:
                zone_update_send_topic = '/ui/networkagent/' + str(rtu[0]) + '/' + str(rtu_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
            rtu_instance.zone = zone  # change field
            rtu_instance.nickname = rtu[1]
            rtu_instance.save()

    if request.is_ajax():
        return HttpResponse(json.dumps("success"), mimetype='application/json')


@login_required(login_url='/login/')
def modify_plugloads(request):
    #print "Inside modify plugloads"
    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        #print _data

        for plugload in _data:
            zone = Building_Zone.objects.get(zone_nickname__iexact=plugload[2])
            pl_instance = Plugload.objects.get(plugload_id=plugload[0])
            if zone.zone_id != pl_instance.zone_id:
                zone_update_send_topic = '/ui/networkagent/' + str(plugload[0]) + '/' + str(pl_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
            pl_instance.zone = zone  # change field
            pl_instance.nickname = plugload[1]
            pl_instance.save()

    if request.is_ajax():
        return HttpResponse(json.dumps("success"), mimetype='application/json')


@login_required(login_url='/login/')
def modify_lighting_loads(request):
    #print "Inside modify lighting loads"
    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        #print _data

        for lt_load in _data:
            zone = Building_Zone.objects.get(zone_nickname__iexact=lt_load[2])
            lt_instance = Lighting.objects.get(lighting_id=lt_load[0])
            if zone.zone_id != lt_instance.zone_id:
                zone_update_send_topic = '/ui/networkagent/' + str(lt_load[0]) + '/' + str(lt_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
            lt_instance.zone = zone  # change field
            lt_instance.nickname = lt_load[1]
            lt_instance.save()

    if request.is_ajax():
        return HttpResponse(json.dumps("success"), mimetype='application/json')


@login_required(login_url='/login/')
def modify_powermeters(request):
    #print "Inside modify powermeters"
    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        #print _data

        for pm in _data:
            zone = Building_Zone.objects.get(zone_nickname__iexact=pm[2])
            pm_instance = PowerMeter.objects.get(power_meter_id=pm[0])
            if zone.zone_id != pm_instance.zone_id:
                zone_update_send_topic = '/ui/networkagent/' + str(pm[0]) + '/' + str(pm_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
            pm_instance.zone = zone  # change field
            pm_instance.nickname = pm[1]
            pm_instance.save()

    if request.is_ajax():
        return HttpResponse(json.dumps("success"), mimetype='application/json')


@login_required(login_url='/login/')
def modify_sensors(request):
    #print "Inside change zones for sensors"
    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        #print _data

        for occs in _data['occupancy']:
            zone = Building_Zone.objects.get(zone_nickname__iexact=occs[2])
            occ_instance = OccupancySensor.objects.get(occupancy_sensor_id=occs[0])
            if zone.zone_id != occ_instance.zone_id:
                zone_update_send_topic = '/ui/networkagent/' + str(occs[0]) + '/' + str(occ_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
            occ_instance.zone = zone  # change field
            occ_instance.nickname = occs[1]
            occ_instance.save()

        for lts in _data['light']:
            zone = Building_Zone.objects.get(zone_nickname__iexact=lts[2])
            lts_instance = AmbientLightSensor.objects.get(ambient_light_sensor_id=lts[0])
            if zone.zone_id != lts_instance.zone_id:
                zone_update_send_topic = '/ui/networkagent/' + str(lts[0]) + '/' + str(lts_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
            lts_instance.zone = zone  # change field
            lts_instance.nickname = lts[1]
            lts_instance.save()

        for ms in _data['motion']:
            zone = Building_Zone.objects.get(zone_nickname__iexact=ms[2])
            ms_instance = MotionSensor.objects.get(motion_sensor_id=ms[0])
            if zone.zone_id != ms_instance.zone_id:
                zone_update_send_topic = '/ui/networkagent/' + str(ms[0]) + '/' + str(ms_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
            ms_instance.zone = zone  # change field
            ms_instance.nickname = ms[1]
            ms_instance.save()

    if request.is_ajax():
        return HttpResponse(json.dumps("success"), mimetype='application/json')












