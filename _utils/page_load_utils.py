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

__author__ = 'kruthika'

from RTU.models import RTU
from VAV.models import VAV
from thermostat.models import Thermostat
from lighting.models import Lighting
from smartplug.models import Plugload
from sensor.models import OccupancySensor, AmbientLightSensor, MotionSensor
from powermeter.models import PowerMeter
import json
import os
import settings

'''
def get_page_load_data(device_id, device_type, device_type_id):
    try:
        json_file = open(os.path.join(settings.PROJECT_DIR, 'resources/page_load/page_load.json'), "r")
        _json_data = json.load(json_file)
        device_page_load_data = _json_data[device_type][device_id]['page_load']
        json_file.close()
        if device_page_load_data != "{empty_string}":
            return device_page_load_data
        else:
            get_page_load_data(device_id, device_type, device_type_id)
    except RuntimeError:
        print 'Exception in loading page..... Depth Exceeded'
        print 'Accessing database....'
        _status = access_database_page_load(device_id, device_type_id)
        return _status
'''


def get_page_load_data(device_id, device_type, device_type_id):
    #json_file = open(os.path.join(settings.PROJECT_DIR, 'resources/page_load/page_load.json'), "r")
    #_json_data = json.load(json_file)
    #device_page_load_data = _json_data[device_type][device_id]['page_load']
    #json_file.close()
    #if device_page_load_data != "{empty_string}":
        #return device_page_load_data
    #else:
        #print 'Accessing database....'
        #_status = access_database_page_load(device_id, device_type_id)
        #return _status
    print 'Accessing database....'
    _status = access_database_page_load(device_id, device_type_id)
    return _status


def access_database_page_load(device_id, device_type_id):
    #current_status = [ob.as_json_dict() for ob in Current_Status.objects.filter(id=device_id)]
    #print current_status
    _status = {}
    if device_type_id == '1TH':
        status = [ob.data_as_json() for ob in Thermostat.objects.filter(thermostat_id=device_id)]
        _status = {
            'temperature': status[0]['temperature'],
            'thermostat_mode': status[0]['thermostat_mode'],
            'heat_setpoint': status[0]['heat_setpoint'],
            'cool_setpoint': status[0]['cool_setpoint'],
            'fan_mode': status[0]['fan_mode'],
            'override': status[0]['override']
        }
    elif device_type_id == '1NST':
        status = [ob.data_as_json() for ob in Thermostat.objects.filter(thermostat_id=device_id)]

        _status = {
            'temperature': status[0]['temperature'],
            'thermostat_mode': status[0]['thermostat_mode'],
            'heat_setpoint': status[0]['heat_setpoint'],
            'cool_setpoint': status[0]['cool_setpoint'],
            'fan_mode': status[0]['fan_mode'],
            'battery': status[0]['battery'],
            'override': status[0]['override']
        }
    elif device_type_id == '1RTU':
        status = [ob.as_json() for ob in RTU.objects.filter(rtu_id=device_id)]
        cooling_mode = status[0]['cooling_mode']
        if cooling_mode == 'NONE':
            cooling_mode = 'None'
        elif cooling_mode == 'STG1':
            cooling_mode = 'Stage 1 Cooling'
        elif cooling_mode == 'STG2':
            cooling_mode = 'Stage 2 Cooling'
        elif cooling_mode == 'STG3':
            cooling_mode = 'Stage 3 Cooling'
        elif cooling_mode == 'STG4':
            cooling_mode = 'Stage 4 Cooling'
        _status = {
            "outside_temperature": status[0]['outside_temp'],
            "supply_temperature": status[0]['supply_temp'],
            "return_temperature": status[0]['return_temp'],
            "pressure": status[0]['pressure'],
            "cooling_mode": cooling_mode,
            "cooling_status": status[0]['cooling_status'],
            "fan_status": status[0]['fan_status'],
            "heating": status[0]['heating'],
            "heat_setpoint": status[0]['heat_setpoint'],
            "cool_setpoint": status[0]['cool_setpoint'],
            "outside_damper_position": status[0]['outside_damper_pos'],
            "bypass_damper_position": status[0]['bypass_damper_pos']
        }
    elif device_type_id == '1VAV':
        status = [ob.as_json() for ob in VAV.objects.filter(vav_id=device_id)]
        _status = {
            "temperature": status[0]['temperature'],
            "supply_temperature": status[0]['supply_temp'],
            "heat_setpoint": status[0]['heat_setpoint'],
            "cool_setpoint": status[0]['cool_setpoint'],
            "flap_override": status[0]['flap_override'],
            "flap_position": status[0]['flap_position']
        }
        print _status
    elif device_type_id == '2SDB' or device_type_id == '2DB' or device_type_id == '2WSL':
        status = [ob.data_as_json() for ob in Lighting.objects.filter(lighting_id=device_id)]
        _status = {
            "brightness": status[0]['brightness'],
            "saturation": 63,
            "status": status[0]['status']
        }
    elif device_type_id == '2WL':
        status = [ob.data_as_json() for ob in Lighting.objects.filter(lighting_id=device_id)]
        _status = {
            "status": status[0]['status']
        }
    elif device_type_id == '3WSP':
        status = [ob.data_as_json() for ob in Plugload.objects.filter(plugload_id=device_id)]
        _status = {
            "status": status[0]['status']
        }
    elif device_type_id == '3WP':
        status = [ob.data_as_json() for ob in Plugload.objects.filter(plugload_id=device_id)]
        _status = {
            "status": status[0]['status'],
            "power": status[0]['power']
        }
    elif device_type_id == '2HUE':
        status = [ob.data_as_json() for ob in Lighting.objects.filter(lighting_id=device_id)]
        _status = {
            "brightness": status[0]['brightness'],
            "color": status[0]['color'],
            "saturation": 63,
            "status": status[0]['status']
        }
    elif device_type_id == '4WSO':
        status = [ob.data_as_json() for ob in OccupancySensor.objects.filter(occupancy_sensor_id=device_id)]
        _status = {
            "status": status[0]['space_occupied']
        }
    elif device_type_id == '4WLS':
        status = [ob.data_as_json() for ob in AmbientLightSensor.objects.filter(ambient_light_sensor_id=device_id)]
        _status = {
            "illuminance": status[0]['illuminance']
        }
    elif device_type_id == '5DNT' or device_type_id == '5WTN':
        status = [ob.data_as_json() for ob in PowerMeter.objects.filter(power_meter_id=device_id)]
        _status = {
            "real_power": status[0]['real_power'],
            "apparent_power": status[0]['apparent_power'],
            "reactive_power": status[0]['reactive_power'],
            "energy": status[0]['energy'],
            "voltage": status[0]['voltage'],
            "power_factor": status[0]['power_factor'],
            "current": status[0]['current'],
        }

    return _status

'''
#Old database access
def _access_database_page_load(device_id, device_type_id):
    current_status = [ob.as_json_dict() for ob in Current_Status.objects.filter(id=device_id)]
    print current_status
    _status = {}
    if device_type_id == '1TH':
        if current_status[0]['mode'] == 'HEAT':
            _status = {
                'temperature': current_status[0]['temperature'],
                'thermostat_mode': current_status[0]['mode'],
                'heat_setpoint': current_status[0]['setpoint'],
                'cool_setpoint': 0,
                'fan_mode': current_status[0]['fmode']
            }
        elif current_status[0]['mode'] == 'COOL':
            _status = {
                'temperature': current_status[0]['temperature'],
                'thermostat_mode': current_status[0]['mode'],
                'heat_setpoint': 0,
                'cool_setpoint': current_status[0]['setpoint'],
                'fan_mode': current_status[0]['fmode']
            }
    elif device_type_id == '2SDB' or device_type_id == '2DB' or device_type_id == '2WSL':
        _status = {
            "brightness": current_status[0]['dim_percent'],
            "saturation": 63,
            "status": current_status[0]['on_off_status']
        }
    elif device_type_id == '2WL':
        _status = {
            "status": current_status[0]['on_off_status']
        }

    elif device_type_id == '3WSP':
        status = [ob.data_as_json() for ob in Plugload.objects.filter(plugload_id=device_id)]
        _status = {
            "status": status[0]['status']
        }
    elif device_type_id == '3WP':
        _status = {
            "status": current_status[0]['on_off_status'],
            "power": current_status[0]['power']
        }
    elif device_type_id == '2HUE':
        _status = {
            "brightness": current_status[0]['dim_percent'],
            "color": current_status[0]['color'],
            "saturation": 63,
            "status": current_status[0]['on_off_status']
        }
    elif device_type_id == '4WSO':
        _status = {
            "status": current_status[0]['motion']
        }
    elif device_type_id == '4WLS':
        _status = {
            "status": current_status[0]['light_intensity']
        }
    elif device_type_id == '5DNT':
        _status = {
            "power": current_status[0]['power']
        }

    return _status
'''


def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv


def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv