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

from django.core.management import setup_environ
import settings
import datetime

setup_environ(settings)

from dashboard.models import DeviceMetadata, DeviceModel, Building_Zone
from thermostat.models import Thermostat
from VAV.models import VAV
from RTU.models import RTU
from lighting.models import Lighting
from smartplug.models import Plugload
from powermeter.models import PowerMeter
from sensor.models import OccupancySensor, AmbientLightSensor, MultiSensor, PresenceSensor
from admin.models import NetworkStatus

print "Adding database records for device_info table."

zone_999 = Building_Zone.objects.get(zone_id=999)

#Thermostat device_model objects
device_model_nest = DeviceModel.objects.get(device_model_id='1NST')
device_model_radio_th = DeviceModel.objects.get(device_model_id='1TH')
device_model_vav = DeviceModel.objects.get(device_model_id='1VAV')
device_model_rtu = DeviceModel.objects.get(device_model_id='1RTU')


#Thermostats
device_info_th1 = DeviceMetadata(device_id="Thermostat1", device_type="thermostat", vendor_name="Google",
                                 device_model="Nest", device_model_id=device_model_nest, mac_address="ASDKJH1310",
                                 min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                 date_added=datetime.datetime.now(), bemoss=True)
device_info_th1.save()

device_info_th2 = DeviceMetadata(device_id="Thermostat2", device_type="thermostat", vendor_name="Radio",
                                 device_model="CT30", device_model_id=device_model_radio_th, mac_address="ASASJH1310",
                                 min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                 date_added=datetime.datetime.now(), bemoss=True)
device_info_th2.save()

device_info_th3 = DeviceMetadata(device_id="Thermostat3", device_type="vav", vendor_name="VAV",
                                 device_model="VAV", device_model_id=device_model_vav, mac_address="DFASJH1310",
                                 min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                 date_added=datetime.datetime.now(), bemoss=True)
device_info_th3.save()

device_info_th4 = DeviceMetadata(device_id="Thermostat4", device_type="rtu", vendor_name="RTU",
                                 device_model="RTU", device_model_id=device_model_rtu, mac_address="DFADFH1310",
                                 min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                 date_added=datetime.datetime.now(), bemoss=True)
device_info_th4.save()

#Lighting Controllers' Device Models
device_model_db = DeviceModel.objects.get(device_model_id='2DB')
device_model_sdb = DeviceModel.objects.get(device_model_id='2SDB')
device_model_hue = DeviceModel.objects.get(device_model_id='2HUE')
device_model_wl = DeviceModel.objects.get(device_model_id='2WL')
device_model_wsl = DeviceModel.objects.get(device_model_id='2WSL')

#Lighting Controllers
device_info_lt1 = DeviceMetadata(device_id="Lighting1", device_type="lighting", vendor_name="Dimmable Ballast",
                                 device_model="Dimmable ballast", device_model_id=device_model_db,
                                 mac_address="AASKJH1310", min_range=20, max_range=95, identifiable=True,
                                 communication="Wifi", date_added=datetime.datetime.now(), bemoss=True)
device_info_lt1.save()

device_info_lt2 = DeviceMetadata(device_id="Lighting2", device_type="lighting", vendor_name="StepDim",
                                 device_model="StepDim Ballast", device_model_id=device_model_sdb,
                                 mac_address="LKASJH1310", min_range=20, max_range=95, identifiable=True,
                                 communication="Wifi", date_added=datetime.datetime.now(), bemoss=True)
device_info_lt2.save()

device_info_lt3 = DeviceMetadata(device_id="Lighting3", device_type="lighting", vendor_name="Philips",
                                 device_model="Philips Hue", device_model_id=device_model_hue, mac_address="DFASDH1310",
                                 min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                 date_added=datetime.datetime.now(), bemoss=True)
device_info_lt3.save()

device_info_lt4 = DeviceMetadata(device_id="Lighting4", device_type="lighting", vendor_name="Belkin",
                                 device_model="Wemo", device_model_id=device_model_wl, mac_address="DFADL918A0",
                                 min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                 date_added=datetime.datetime.now(), bemoss=True)
device_info_lt4.save()

device_info_lt5 = DeviceMetadata(device_id="Lighting5", device_type="lighting", vendor_name="Wattstopper",
                                 device_model="Wattstopper", device_model_id=device_model_wsl, mac_address="LKADL918A0",
                                 min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                 date_added=datetime.datetime.now(), bemoss=True)
device_info_lt5.save()


#Plugload Device Model Objects
device_model_wsp = DeviceModel.objects.get(device_model_id='3WSP')
device_model_wp = DeviceModel.objects.get(device_model_id='3WP')
device_model_dsp = DeviceModel.objects.get(device_model_id='3DSP')

#Plugload controllers
device_info_pl1 = DeviceMetadata(device_id="Plugload1", device_type="plugload", vendor_name="Belkin",
                                 device_model="Wemo SPlug", device_model_id=device_model_wsp, mac_address="DZASDH1310",
                                 min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                 date_added=datetime.datetime.now(), bemoss=True)
device_info_pl1.save()

device_info_pl2 = DeviceMetadata(device_id="Plugload2", device_type="plugload", vendor_name="Wattstopper",
                                 device_model="Wastt Splug", device_model_id=device_model_wp, mac_address="IKHJL918A0",
                                 min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                 date_added=datetime.datetime.now(), bemoss=True)
device_info_pl2.save()

device_info_pl3 = DeviceMetadata(device_id="Plugload3", device_type="plugload", vendor_name="Digi",
                                 device_model="Digi SPlug", device_model_id=device_model_dsp, mac_address="THADL918A0",
                                 min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                 date_added=datetime.datetime.now(), bemoss=True)
device_info_pl3.save()


#Sensor Device Model Objects
device_model_wso = DeviceModel.objects.get(device_model_id='4WSO')
device_model_wls = DeviceModel.objects.get(device_model_id='4WLS')
device_model_stp = DeviceModel.objects.get(device_model_id='4STP')
device_model_stm = DeviceModel.objects.get(device_model_id='4STM')

#Sensors
device_info_s1 = DeviceMetadata(device_id="Sensor1", device_type="occupancy_sensor", vendor_name="Wattstopper",
                                device_model="Wattstopper", device_model_id=device_model_wso, mac_address="DZA78H1310",
                                min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                date_added=datetime.datetime.now(), bemoss=True)
device_info_s1.save()

device_info_s2 = DeviceMetadata(device_id="Sensor2", device_type="ambient_light_sensor", vendor_name="Wattstopper",
                                device_model="Watt LtSens", device_model_id=device_model_wls, mac_address="PQHJL918A0",
                                min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                date_added=datetime.datetime.now(), bemoss=True)
device_info_s2.save()

device_info_s3 = DeviceMetadata(device_id="Sensor3", device_type="occupancy_sensor", vendor_name="Smartthings",
                                device_model="SmartPresence", device_model_id=device_model_stp, mac_address="09ADL918A0",
                                min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                date_added=datetime.datetime.now(), bemoss=True)
device_info_s3.save()

device_info_s4 = DeviceMetadata(device_id="Sensor4", device_type="occupancy_sensor", vendor_name="Smartthings",
                                device_model="SmartMulti", device_model_id=device_model_stm, mac_address="NMADL918A0",
                                min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                date_added=datetime.datetime.now(), bemoss=True)
device_info_s4.save()

#Powermeter device model objects
device_model_wtn = DeviceModel.objects.get(device_model_id='5WTN')
device_model_dnt = DeviceModel.objects.get(device_model_id='5DNT')

device_info_pm1 = DeviceMetadata(device_id="Powermeter1", device_type="power_meter", vendor_name="Wattnode",
                                 device_model="Wattnode", device_model_id=device_model_wtn, mac_address="ZAADL918A0",
                                 min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                 date_added=datetime.datetime.now(), bemoss=True)
device_info_pm1.save()

device_info_pm2 = DeviceMetadata(device_id="Powermeter2", device_type="power_meter", vendor_name="Dent",
                                 device_model="Dent", device_model_id=device_model_dnt, mac_address="NMAHG918A0",
                                 min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                 date_added=datetime.datetime.now(), bemoss=True)
device_info_pm2.save()


print "Devices added to device_info table"
#-----------------------------------------------------------------------------------------------------------------------

#Adding thermostat status to thermostat tables.
thermostat1 = Thermostat(thermostat_id=device_info_th1, temperature=70, thermostat_mode="HEAT", fan_mode="AUTO",
                         heat_setpoint=75, cool_setpoint=65.5, thermostat_state="HEAT", fan_state="AUTO",
                         ip_address='34.23.12.76', zone_id=zone_999.zone_id, nickname="Thermostat1", network_status='ONLINE',
                         last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
thermostat1.save()

thermostat2 = Thermostat(thermostat_id=device_info_th2, temperature=70, thermostat_mode="HEAT", fan_mode="AUTO",
                         heat_setpoint=75, cool_setpoint=65.5, thermostat_state="HEAT", fan_state="AUTO",
                         ip_address='34.73.12.76', zone_id=zone_999.zone_id, nickname="Thermostat2", network_status='ONLINE',
                         last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
thermostat2.save()

print "Thermostats added to thermostat table"
#-----------------------------------------------------------------------------------------------------------------------

#Adding VAV
vav = VAV(vav_id=device_info_th3, temperature=70, supply_temperature=75, heat_setpoint=75, cool_setpoint=65.5,
          flap_override="ON", flap_position=50, zone_id=zone_999.zone_id, ip_address='34.73.67.76', nickname="Thermostat2",
          network_status='ONLINE', last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
vav.save()

print "VAV added to vav table"
#-----------------------------------------------------------------------------------------------------------------------

#Adding RTU
rtu = RTU(rtu_id=device_info_th4, outside_temperature=70, supply_temperature=75, return_temperature=64,
          pressure=34.5, cooling_mode='STG1', cooling_status='ON', fan_status='ON', heating=57, heat_setpoint=75,
          cool_setpoint=65.5, outside_damper_position=45, bypass_damper_position=87, zone_id=zone_999.zone_id,
          ip_address='34.73.67.96', nickname="RTU", network_status='ONLINE', last_scanned_time=datetime.datetime.now(),
          last_offline_time=datetime.datetime.now())
rtu.save()

print "RTU added to rtu table"
#-----------------------------------------------------------------------------------------------------------------------

#Adding Lighting Controllers
lighting1 = Lighting(lighting_id=device_info_lt1, status='ON', brightness=34, color=(45,23,56), multiple_on_off='101',
                     ip_address='34.54.23.64', nickname="Lighting1", zone_id=zone_999.zone_id, network_status='ONLINE',
                     last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
lighting1.save()

lighting2 = Lighting(lighting_id=device_info_lt2, status='ON', brightness=94, color=(45,29,56), multiple_on_off='111',
                     ip_address='76.54.73.64', nickname="Lighting2", zone_id=zone_999.zone_id, network_status='ONLINE',
                     last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
lighting2.save()

lighting3 = Lighting(lighting_id=device_info_lt3, status='ON', brightness=54, color=(45,23,56), multiple_on_off='101',
                     ip_address='34.54.233.64', nickname="Lighting3", zone_id=zone_999.zone_id, network_status='ONLINE',
                     last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
lighting3.save()

lighting4 = Lighting(lighting_id=device_info_lt4, status='ON', brightness=84, color=(85,29,56), multiple_on_off='111',
                     ip_address='76.54.71.64', nickname="Lighting4", zone_id=zone_999.zone_id, network_status='ONLINE',
                     last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
lighting4.save()

print "Lighting controllers added to Lighting table"
#-----------------------------------------------------------------------------------------------------------------------

#Adding Plugload Controllers
plugload1 = Plugload(plugload_id=device_info_pl1, status='ON', power=3, energy=5, ip_address='34.98.23.64',
                     nickname="Plugload1", zone_id=zone_999.zone_id, network_status='ONLINE',
                     last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
plugload1.save()

plugload2 = Plugload(plugload_id=device_info_pl2, status='ON', power=3, energy=5, ip_address='34.89.23.64',
                     nickname="Plugload2", zone_id=zone_999.zone_id, network_status='ONLINE',
                     last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
plugload2.save()

plugload3 = Plugload(plugload_id=device_info_pl3, status='ON', power=3, energy=5, ip_address='9.89.23.64',
                     nickname="Plugload3", zone_id=zone_999.zone_id, network_status='ONLINE',
                     last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
plugload3.save()

print "Plugload controllers added to plugload table"
#-----------------------------------------------------------------------------------------------------------------------

#Adding Powermeters
powermeter1 = PowerMeter(power_meter_id=device_info_pm1, real_power=12.0, reactive_power=1.3, apparent_power=1.5, energy=2.3, voltage=8.1, current=1.4,
                         power_factor=1.2, ip_address='12.43.23.67', network_status='ONLINE', nickname="Powermeter1", zone_id=zone_999.zone_id,
                         last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
powermeter1.save()

powermeter2 = PowerMeter(power_meter_id=device_info_pm2, real_power=1.2, reactive_power=3.4, apparent_power=1.5, energy=2.3, voltage=8.1, current=1.4,
                         power_factor=1.5, ip_address='12.43.20.67', network_status='ONLINE', nickname="Powermeter2", zone_id=zone_999.zone_id,
                         last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
powermeter2.save()

print "Powermeter controllers added to powermeter table"
#-----------------------------------------------------------------------------------------------------------------------

#Adding Sensors
sensor1 = OccupancySensor(occupancy_sensor_id=device_info_s1, space_occupied=True, ip_address='12.65.34.87',
                          nickname="OccSensor", zone_id=zone_999.zone_id, network_status='ONLINE',
                          last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
sensor1.save()

sensor2 = AmbientLightSensor(ambient_light_sensor_id=device_info_s2, illuminance=678, ip_address='12.65.34.87',
                             nickname="OccSensor", zone_id=zone_999.zone_id, network_status='ONLINE',
                             last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
sensor2.save()

sensor3 = MultiSensor(multi_sensor_id=device_info_s3, acceleration="YES", contact="Some", battery=34, temperature=76,
                      lqi=12, rssi=56, three_axis="Somevalue", ip_address='12.65.34.87', nickname="OccSensor",
                      zone_id=zone_999.zone_id, network_status='ONLINE', last_scanned_time=datetime.datetime.now(),
                      last_offline_time=datetime.datetime.now())
sensor3.save()

sensor4 = PresenceSensor(presence_sensor_id=device_info_s4, presence="PRESENT", battery=89, lqi=34, rssi=45,
                         ip_address='12.65.34.87', nickname="OccSensor", zone_id=zone_999.zone_id, network_status='ONLINE',
                         last_scanned_time=datetime.datetime.now(),  last_offline_time=datetime.datetime.now())
sensor4.save()

print "Sensors added to sensor table"
#-----------------------------------------------------------------------------------------------------------------------

#Network Status table.
nw1 = NetworkStatus(node_name="Beaglebone", node_type="EmdSys", node_model="Black", node_status="ONLINE", building_name="bemoss",
                    associated_zone=zone_999, ip_address='12.65.34.97', mac_address='234adjkhf', date_added=datetime.datetime.now(), communication="MQTCP")
nw1.save()

nw2 = NetworkStatus(node_name="Pandaboard", node_type="EmdSys", node_model="Bigg",  mac_address='234adjkhf',node_status="ONLINE", building_name="bemoss",
                    associated_zone=zone_999, ip_address='12.65.34.77', date_added=datetime.datetime.now(), communication="MQTCP")
nw2.save()

nw3 = NetworkStatus(node_name="BananaPi", node_type="EmdSys", node_model="China",  mac_address='234adjkhf',node_status="ONLINE", building_name="bemoss",
                    associated_zone=zone_999, ip_address='12.12.34.87', date_added=datetime.datetime.now(), communication="MQTCP")
nw3.save()

