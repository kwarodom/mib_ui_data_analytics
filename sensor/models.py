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


from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from dashboard.models import Building_Zone, DeviceMetadata


#Occupancy Sensor Data
class OccupancySensor(models.Model):
    occupancy_sensor = models.ForeignKey(DeviceMetadata, max_length=50, primary_key=True)
    space_occupied = models.NullBooleanField(null=True, blank=True)
    ip_address = models.IPAddressField(null=True, blank=True)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    zone = models.ForeignKey(Building_Zone, null=True, blank=True)
    network_status = models.CharField(max_length=7, null=True, blank=True)
    other_parameters = models.CharField(max_length=200, null=True, blank=True)
    last_scanned_time = models.DateTimeField(null=True, blank=True)
    last_offline_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "occupancy_sensor"

    def __unicode__(self):
        return self.occupancy_sensor_id

    def data_as_json(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.occupancy_sensor_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            id=self.occupancy_sensor_id,
            space_occupied=self.space_occupied,
            zone=zone_req,
            nickname=self.nickname.encode('utf-8').title(),
            device_type=metadata['device_type'].encode('utf-8'),
            vendor_name=metadata['vendor_name'].encode('utf-8'),
            device_model=metadata['device_model'].encode('utf-8'),
            device_model_id=metadata['device_model_id'],
            mac_address=metadata['mac_address'].encode('utf-8'),
            identifiable=metadata['identifiable'],
            bemoss=metadata['bemoss'])

    def data_side_nav(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.occupancy_sensor_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            device_id=self.occupancy_sensor_id,
            device_model_id=metadata['device_model_id'],
            mac_address=metadata['mac_address'].encode('utf-8'),
            nickname=self.nickname.encode('utf-8').title(),
            zone_id=zone_req['id'],
            bemoss=metadata['bemoss'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize())

    def device_status(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.occupancy_sensor_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            id=self.occupancy_sensor_id,
            nickname=self.nickname.encode('utf-8').title(),
            device_model=metadata['device_model'],
            date_added=metadata['date_added'],
            zone=zone_req,
            bemoss=metadata['bemoss'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize(),
            last_scanned=self.last_scanned_time,
            last_offline=self.last_offline_time)

    def data_dashboard(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.occupancy_sensor_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            device_id=self.occupancy_sensor_id,
            device_type=metadata['device_type'].encode('utf-8'),
            vendor_name=metadata['vendor_name'].encode('utf-8'),
            device_model=metadata['device_model'].encode('utf-8'),
            device_model_id=metadata['device_model_id'],
            mac_address=metadata['mac_address'].encode('utf-8'),
            nickname=self.nickname.encode('utf-8').title(),
            date_added=metadata['date_added'],
            identifiable=metadata['identifiable'],
            zone_id=zone_req['id'],
            bemoss=metadata['bemoss'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize(),
            last_scanned=self.last_scanned_time)


#Ambient Light Sensor Data
class AmbientLightSensor(models.Model):
    ambient_light_sensor = models.ForeignKey(DeviceMetadata, max_length=50, primary_key=True)
    illuminance = models.IntegerField(null=True, blank=True)
    ip_address = models.IPAddressField(null=True, blank=True)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    zone = models.ForeignKey(Building_Zone, null=True, blank=True)
    network_status = models.CharField(max_length=7, null=True, blank=True)
    other_parameters = models.CharField(max_length=200, null=True, blank=True)
    last_scanned_time = models.DateTimeField(null=True, blank=True)
    last_offline_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "ambient_light_sensor"

    def __unicode__(self):
        return self.ambient_light_sensor_id

    def data_as_json(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.ambient_light_sensor_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            id=self.ambient_light_sensor_id,
            illuminance=self.illuminance,
            zone=zone_req,
            identifiable=metadata['identifiable'],
            nickname=self.nickname.encode('utf-8').title(),
            device_type=metadata['device_type'].encode('utf-8'),
            vendor_name=metadata['vendor_name'].encode('utf-8'),
            device_model=metadata['device_model'].encode('utf-8'),
            device_model_id=metadata['device_model_id'],
            bemoss=metadata['bemoss'],
            mac_address=metadata['mac_address'].encode('utf-8'))

    def device_status(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.ambient_light_sensor_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            id=self.ambient_light_sensor_id,
            nickname=self.nickname.encode('utf-8').title(),
            device_model=metadata['device_model'],
            date_added=metadata['date_added'],
            zone=zone_req,
            zone_nickname=zone_req['zone_nickname'],
            bemoss=metadata['bemoss'],
            network_status=self.network_status.capitalize(),
            last_scanned=self.last_scanned_time,
            last_offline=self.last_offline_time)

    def data_dashboard(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.ambient_light_sensor_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            device_id=self.ambient_light_sensor_id,
            device_type=metadata['device_type'].encode('utf-8'),
            vendor_name=metadata['vendor_name'].encode('utf-8'),
            device_model=metadata['device_model'].encode('utf-8'),
            device_model_id=metadata['device_model_id'],
            mac_address=metadata['mac_address'].encode('utf-8'),
            nickname=self.nickname.encode('utf-8').title(),
            date_added=metadata['date_added'],
            identifiable=metadata['identifiable'],
            zone_id=zone_req['id'],
            bemoss=metadata['bemoss'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize(),
            last_scanned=self.last_scanned_time)

    def data_side_nav(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.ambient_light_sensor_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            device_id=self.ambient_light_sensor_id,
            device_model_id=metadata['device_model_id'],
            mac_address=metadata['mac_address'].encode('utf-8'),
            nickname=self.nickname.encode('utf-8').title(),
            zone_id=zone_req['id'],
            bemoss=metadata['bemoss'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize())


#Motion Sensor Data
class MotionSensor(models.Model):
    motion_sensor = models.ForeignKey(DeviceMetadata, max_length=50, primary_key=True)
    motion = models.BooleanField()
    ip_address = models.IPAddressField()
    nickname = models.CharField(max_length=30)
    zone = models.ForeignKey(Building_Zone)
    network_status = models.CharField(max_length=7)
    other_parameters = models.CharField(max_length=200, null=True, blank=True)
    last_scanned_time = models.DateTimeField(null=True, blank=True)
    last_offline_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "motion_sensor"

    def __unicode__(self):
        return self.motion_sensor_id

    def data_as_json(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.motion_sensor_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            id=self.motion_sensor_id,
            motion=self.motion,
            zone=zone_req,
            identifiable=metadata['identifiable'],
            nickname=self.nickname.encode('utf-8').title(),
            device_type=metadata['device_type'].encode('utf-8'),
            vendor_name=metadata['vendor_name'].encode('utf-8'),
            device_model=metadata['device_model'].encode('utf-8'),
            device_model_id=metadata['device_model_id'],
            bemoss=metadata['bemoss'],
            mac_address=metadata['mac_address'].encode('utf-8'))

    def device_status(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.motion_sensor_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            id=self.motion_sensor_id,
            nickname=self.nickname.encode('utf-8').title(),
            device_model=metadata['device_model'],
            date_added=metadata['date_added'],
            zone=zone_req,
            zone_nickname=zone_req['zone_nickname'],
            bemoss=metadata['bemoss'],
            network_status=self.network_status.capitalize(),
            last_scanned=self.last_scanned_time,
            last_offline=self.last_offline_time)

    def data_dashboard(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.motion_sensor_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            device_id=self.motion_sensor_id,
            device_type=metadata['device_type'].encode('utf-8'),
            vendor_name=metadata['vendor_name'].encode('utf-8'),
            device_model=metadata['device_model'].encode('utf-8'),
            device_model_id=metadata['device_model_id'],
            mac_address=metadata['mac_address'].encode('utf-8'),
            nickname=self.nickname.encode('utf-8').title(),
            date_added=metadata['date_added'],
            identifiable=metadata['identifiable'],
            zone_id=zone_req['id'],
            bemoss=metadata['bemoss'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize(),
            last_scanned=self.last_scanned_time)

    def data_side_nav(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.motion_sensor_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            device_id=self.motion_sensor_id,
            device_model_id=metadata['device_model_id'],
            mac_address=metadata['mac_address'].encode('utf-8'),
            nickname=self.nickname.encode('utf-8').title(),
            zone_id=zone_req['id'],
            bemoss=metadata['bemoss'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize())


class Hub(models.Model):
    hub = models.ForeignKey(DeviceMetadata, max_length=50, primary_key=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    firmware_version = models.CharField(max_length=50, null=True, blank=True)
    factory_id = models.CharField(max_length=50, null=True, blank=True)
    firmware_update_available = models.NullBooleanField(null=True, blank=True)
    battery = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True,
                                          blank=True)
    signal_strength = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True,
                                                  blank=True)
    ip_address = models.IPAddressField()
    nickname = models.CharField(max_length=30)
    zone = models.ForeignKey(Building_Zone)
    network_status = models.CharField(max_length=7)
    other_parameters = models.CharField(max_length=200, null=True, blank=True)
    last_scanned_time = models.DateTimeField(null=True, blank=True)
    last_offline_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "hub"

    def __unicode__(self):
        return self.hub_id

    def data_as_json(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.hub_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            id=self.hub_id,
            location=self.location,
            firmware_version=self.firmware_version,
            factory_id=self.factory_id,
            firmware_update_availabile=self.firmware_update_available,
            battery=self.battery,
            signal_strength=self.signal_strength,
            zone=zone_req,
            bemoss=metadata['bemoss'],
            nickname=self.nickname.encode('utf-8').title(),
            device_type=metadata['device_type'].encode('utf-8'),
            vendor_name=metadata['vendor_name'].encode('utf-8'),
            device_model=metadata['device_model'].encode('utf-8'),
            device_model_id=metadata['device_model_id'],
            mac_address=metadata['mac_address'].encode('utf-8'))

    def device_status(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.hub_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            id=self.hub_id,
            nickname=self.nickname.encode('utf-8').title(),
            device_model=metadata['device_model'],
            date_added=metadata['date_added'],
            zone=zone_req,
            zone_nickname=zone_req['zone_nickname'],
            bemoss=metadata['bemoss'],
            network_status=self.network_status.capitalize(),
            last_scanned=self.last_scanned_time,
            last_offline=self.last_offline_time)

    def data_dashboard(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.hub_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            device_id=self.hub_id,
            device_type=metadata['device_type'].encode('utf-8'),
            vendor_name=metadata['vendor_name'].encode('utf-8'),
            device_model=metadata['device_model'].encode('utf-8'),
            device_model_id=metadata['device_model_id'],
            mac_address=metadata['mac_address'].encode('utf-8'),
            nickname=self.nickname.encode('utf-8').title(),
            date_added=metadata['date_added'],
            zone_id=zone_req['id'],
            bemoss=metadata['bemoss'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize(),
            last_scanned=self.last_scanned_time)

    def data_side_nav(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.hub_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            device_id=self.hub_id,
            device_model_id=metadata['device_model_id'],
            mac_address=metadata['mac_address'].encode('utf-8'),
            nickname=self.nickname.encode('utf-8').title(),
            zone_id=zone_req['id'],
            bemoss=metadata['bemoss'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize())


class MultiSensor(models.Model):
    multi_sensor = models.ForeignKey(DeviceMetadata, max_length=50, primary_key=True)
    acceleration = models.CharField(max_length=10, null=True, blank=True)
    contact = models.CharField(max_length=10, null=True, blank=True)
    battery = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True,
                                          blank=True)
    temperature = models.IntegerField(null=True, blank=True)
    lqi = models.IntegerField(null=True, blank=True)
    rssi = models.IntegerField(null=True, blank=True)
    three_axis = models.CharField(max_length=20, null=True, blank=True)
    ip_address = models.IPAddressField()
    nickname = models.CharField(max_length=30)
    zone = models.ForeignKey(Building_Zone)
    network_status = models.CharField(max_length=7)
    other_parameters = models.CharField(max_length=200, null=True, blank=True)
    last_scanned_time = models.DateTimeField(null=True, blank=True)
    last_offline_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "multi_sensor"

    def __unicode__(self):
        return self.multi_sensor_id

    def data_as_json(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.multi_sensor_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            id=self.multi_sensor_id,
            acceleration=self.acceleration,
            contact=self.contact,
            battery=self.battery,
            temperature=self.temperature,
            lqi=self.lqi,
            rssi=self.rssi,
            three_axis=self.three_axis,
            zone=zone_req,
            nickname=self.nickname.encode('utf-8').title(),
            device_type=metadata['device_type'].encode('utf-8'),
            vendor_name=metadata['vendor_name'].encode('utf-8'),
            device_model=metadata['device_model'].encode('utf-8'),
            device_model_id=metadata['device_model_id'],
            bemoss=metadata['bemoss'],
            mac_address=metadata['factory_id'].encode('utf-8'))

    def device_status(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.multi_sensor_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            id=self.multi_sensor_id,
            nickname=self.nickname.encode('utf-8').title(),
            device_model=metadata['device_model'],
            date_added=metadata['date_added'],
            zone=zone_req,
            bemoss=metadata['bemoss'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize(),
            last_scanned=self.last_scanned_time,
            last_offline=self.last_offline_time)

    def data_dashboard(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.multi_sensor_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            device_id=self.multi_sensor_id,
            device_type=metadata['device_type'].encode('utf-8'),
            vendor_name=metadata['vendor_name'].encode('utf-8'),
            device_model=metadata['device_model'].encode('utf-8'),
            device_model_id=metadata['device_model_id'],
            mac_address=metadata['factory_id'].encode('utf-8'),
            nickname=self.nickname.encode('utf-8').title(),
            date_added=metadata['date_added'],
            zone_id=zone_req['id'],
            bemoss=metadata['bemoss'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize(),
            last_scanned=self.last_scanned_time)

    def data_side_nav(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.multi_sensor_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            device_id=self.multi_sensor_id,
            device_model_id=metadata['device_model_id'],
            mac_address=metadata['mac_address'].encode('utf-8'),
            nickname=self.nickname.encode('utf-8').title(),
            zone_id=zone_req['id'],
            bemoss=metadata['bemoss'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize())


class PresenceSensor(models.Model):
    presence_sensor = models.ForeignKey(DeviceMetadata, max_length=50, primary_key=True)
    presence = models.CharField(max_length=10, null=True, blank=True)
    battery = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True,
                                          blank=True)
    lqi = models.IntegerField(null=True, blank=True)
    rssi = models.IntegerField(null=True, blank=True)
    ip_address = models.IPAddressField()
    nickname = models.CharField(max_length=30)
    zone = models.ForeignKey(Building_Zone)
    network_status = models.CharField(max_length=7)
    other_parameters = models.CharField(max_length=200, null=True, blank=True)
    last_scanned_time = models.DateTimeField(null=True, blank=True)
    last_offline_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "presence_sensor"

    def __unicode__(self):
        return self.presence_sensor_id

    def data_as_json(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.presence_sensor_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            id=self.presence_sensor_id,
            presence=self.presence,
            battery=self.battery,
            lqi=self.lqi,
            rssi=self.rssi,
            zone=zone_req,
            nickname=self.nickname.encode('utf-8').title(),
            device_type=metadata['device_type'].encode('utf-8'),
            vendor_name=metadata['vendor_name'].encode('utf-8'),
            device_model=metadata['device_model'].encode('utf-8'),
            device_model_id=metadata['device_model_id'],
            bemoss=metadata['bemoss'],
            mac_address=metadata['factory_id'].encode('utf-8'))

    def device_status(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.presence_sensor_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            id=self.presence_sensor_id,
            nickname=self.nickname.encode('utf-8').title(),
            device_model=metadata['device_model'],
            date_added=metadata['date_added'],
            zone=zone_req,
            bemoss=metadata['bemoss'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize(),
            last_scanned=self.last_scanned_time,
            last_offline=self.last_offline_time)

    def data_dashboard(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.presence_sensor_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            device_id=self.presence_sensor_id,
            device_type=metadata['device_type'].encode('utf-8'),
            vendor_name=metadata['vendor_name'].encode('utf-8'),
            device_model=metadata['device_model'].encode('utf-8'),
            device_model_id=metadata['device_model_id'],
            mac_address=metadata['factory_id'].encode('utf-8'),
            nickname=self.nickname.encode('utf-8').title(),
            date_added=metadata['date_added'],
            zone_id=zone_req['id'],
            bemoss=metadata['bemoss'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize(),
            last_scanned=self.last_scanned_time)

    def data_side_nav(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.presence_sensor_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            device_id=self.presence_sensor_id,
            device_model_id=metadata['device_model_id'],
            mac_address=metadata['mac_address'].encode('utf-8'),
            nickname=self.nickname.encode('utf-8').title(),
            zone_id=zone_req['id'],
            bemoss=metadata['bemoss'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize())

