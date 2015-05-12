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


# coding='utf-8'

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
#from thermostat.models import Thermostat
#from smartplug.models import Plugload
#from lighting.models import Lighting
#from sensor.models import AmbientLightSensor, OccupancySensor, MotionSensor
#from powermeter.models import PowerMeter
import re

from django.utils.translation import ugettext_lazy as _
from django.forms import fields
from django.db import models


# Database models for Dashboard page
class Building_Zone(models.Model):
    zone_id = models.AutoField(primary_key=True)
    zone_nickname = models.CharField(max_length=30)

    class Meta:
        db_table = "building_zone"

    def __unicode__(self):
        return str(self.zone_id)
       
    def as_json(self):
        return dict(
            id=self.zone_id,
            zone_nickname=self.zone_nickname.encode('utf-8').title())

    def data_dashboard_global(self):
        gsetting = GlobalSetting.objects.get(zone=self)
        global_setting = GlobalSetting.as_json(gsetting)
        return dict(
            id=self.zone_id,
            zone_nickname=self.zone_nickname.encode('utf-8').title(),
            global_setting=global_setting,
        )

    def data_dashboard(self):
        gsetting = GlobalSetting.objects.get(zone=self)
        global_setting = GlobalSetting.as_json(gsetting)
        return dict(
            id=self.zone_id,
            zone_nickname=self.zone_nickname.encode('utf-8').title(),
            global_setting=global_setting,
            t_count=0,
            pl_count=0,
            lt_count=0,
            ss_count=0,
            pm_count=0
        )

'''
class Current_Status(models.Model):
    
    #0:off, 1:heat, 2:cool
    MODE_CHOICES = (
        ('OFF', 'off'),
        ('HEAT', 'heat'),
        ('COOL', 'cool'))
    FMODE_CHOICES = (
        ('ON', 'on'),
        ('AUTO', 'auto'))
    STATUS_ON_OFF_CHOICES = (
        ('OFF', 'off'),
        ('ON', 'on'))

    MOTION_SENSOR_CHOICES = (
        ('IN', 'occupied'),
        ('OUT', 'unoccupied'))
    id = models.CharField(primary_key=True, max_length=50)
    #device_id = models.ForeignKey(Device_Info, primary_key=True, max_length=50)
    temperature = models.FloatField(
        validators=[MinValueValidator(-30.0), MaxValueValidator(200.0)],
        verbose_name="Temperature (Fahrenheit)", null=True, blank=True)
    setpoint = models.FloatField(
        validators=[MinValueValidator(45.0), MaxValueValidator(95.0)],
        verbose_name="Set Point (Fahrenheit)", null=True, blank=True)
    fmode = models.CharField(max_length=10, choices=FMODE_CHOICES, null=True, blank=True)
    mode = models.CharField(max_length=4, choices=MODE_CHOICES, null=True, blank=True)
    on_off_status = models.CharField(max_length=3, choices=STATUS_ON_OFF_CHOICES, null=True, blank=True)
    dim_percent = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name = "Dim (Percentage)", null=True, blank=True)
    power = models.FloatField(verbose_name="Power (kW)", null=True, blank=True)
    humidity = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name = "Humidity (Percentage)", null=True, blank=True)
    light_intensity = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)],verbose_name = "Light Intensity (lumen)", null=True, blank=True)
    motion = models.CharField(max_length=3, choices=MOTION_SENSOR_CHOICES, null=True, blank=True)
    multiple_on_off = models.CharField(max_length=50, null=True, blank=True)
    light_color = models.CharField(max_length=15, null=True, blank=True)
    ip_address = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.as_json()
    
    def as_json(self):
        return str(dict(
            id=self.id,
            temperature=self.temperature,
            setpoint=self.setpoint,
            fmode=self.fmode,
            mode=self.mode,
            on_off_status=self.on_off_status,
            dim_percent=self.dim_percent,
            power=self.power,
            humidity=self.humidity,
            light_intensity=self.light_intensity,
            motion=self.motion,
            color=self.light_color,
            ip_address=self.ip_address))

    def as_json_dict(self):
        return dict(
            id=self.id,
            temperature=self.temperature,
            setpoint=self.setpoint,
            fmode=self.fmode,
            mode=self.mode,
            on_off_status=self.on_off_status,
            dim_percent=self.dim_percent,
            power=self.power,
            humidity=self.humidity,
            light_intensity=self.light_intensity,
            motion=self.motion,
            color=self.light_color,
            ip_address=self.ip_address)
'''
'''
class Device_Info(models.Model):

    STATUS_CHOICES = (
        ('ON', 'online'),
        ('OFF', 'offline'),
        ('DEL', 'deleted'),
        ('UPD', 'updating'))
    
    DEVICE_TYPE_CHOICES = (
        ('1TH', 'thermostat'),
        ('2DB', 'dimmable ballast'),
        ('2HUE', 'philips hue'),
        ('2SDB','step dim ballast'),
        ('2WL', 'wemo light switch'),
        ('2WSL', 'wattstopper lighting'),
        ('3WSP', 'wemo smart plug'),
        ('3MOD', 'modlet smart plug'),
        ('3WP', 'wattstopper plugload'),
        ('3VTH', 'vt load controller'),
        ('3DSP', 'digi smart plug'),
        ('4DIS', 'digi sensor'),
        ('4WSO', 'wattstopper occupancy sensor'),
        ('4WLS', 'wattstopper daylight sensor'),
        ('4PRM', 'proteus motion sensor'),
        ('5WTN', 'wattnode'),
        ('5DNT', 'dent power meter'))
    
    id = models.CharField(primary_key=True, max_length=50)
    #device_id = models.ForeignKey(Current_Status, primary_key=True, max_length=50)
    current_status = models.ForeignKey(Current_Status, null=True, blank=True)
    nickname = models.CharField(max_length=30)
    device_type = models.CharField(max_length=50)
    device_type_id = models.CharField(max_length=5, choices=DEVICE_TYPE_CHOICES)
    vendor_name = models.CharField(max_length=50)
    device_model = models.CharField(max_length=30)
    zone = models.ForeignKey(Building_Zone)
    mac_address = models.CharField(max_length=50)
    device_status = models.CharField(max_length=3, choices=STATUS_CHOICES)

    #def __unicode__(self):
        #return self.device_name
    def __unicode__(self):
        return self.as_json()
    
    def as_json(self):
        zone_req = Building_Zone.as_json(self.zone)
        #current_status = Current_Status.as_json(self.current_status_id)
        #current_stat = Current_Status.as_json(self.id)
        #current_stat = dict((y, x) for x, y in current_stat)
        #print type(current_stat)
        #print type(zone_req)
        #print self.id.encode('utf-8')
        #print type(self.id.encode('utf-8'))
        return dict(
            #id = self.id.encode('utf-8'),
            id=self.id,
            #current_status = Current_Status.as_json(self.device_id),
            #current_status = current_status,
            current_status=self.current_status,
            nickname=self.nickname.encode('utf-8').title(),
            device_type=self.device_type.encode('utf-8'),
            device_type_id=self.device_type_id.encode('utf-8'),
            device_name=self.vendor_name.encode('utf-8'),
            device_model=self.device_model.encode('utf-8'),
            vendor_name=self.vendor_name.encode('utf-8'),
            zone=zone_req,
            mac_address=self.mac_address.encode('utf-8'),
            device_status=self.device_status.encode('utf-8'))
'''
#-------------------------------------------------------------------------------------------------

class DeviceModel(models.Model):
    device_model_id = models.CharField(primary_key=True, max_length=5)
    device_model_name = models.CharField(max_length=40)

    class Meta:
        db_table = "device_model"

    def __unicode__(self):
        return self.device_model_id

    def as_json(self):
        return dict(
            device_model_id=self.device_model_id,
            device_model_name=self.device_model_name
        )


#Table to store device metadata for all devices in BEMOSS system
class DeviceMetadata(models.Model):

    DEVICE_TYPE_CHOICES = (
        ('1TH', 'thermostat'),
        ('2DB', 'dimmable ballast'),
        ('2HUE', 'philips hue'),
        ('2SDB', 'step dim ballast'),
        ('2WL', 'wemo light switch'),
        ('2WSL', 'wattstopper lighting'),
        ('3WSP', 'wemo smart plug'),
        ('3MOD', 'modlet smart plug'),
        ('3WP', 'wattstopper plugload'),
        ('3VTH', 'vt load controller'),
        ('3DSP', 'digi smart plug'),
        ('4DIS', 'digi sensor'),
        ('4WSO', 'wattstopper occupancy sensor'),
        ('4WLS', 'wattstopper daylight sensor'),
        ('4PRM', 'proteus motion sensor'),
        ('5WTN', 'wattnode'),
        ('5DNT', 'dent power meter'))

    device_id = models.CharField(primary_key=True, max_length=50)
    device_type = models.CharField(max_length=20)
    vendor_name = models.CharField(max_length=50)
    device_model = models.CharField(max_length=30)
    #device_model_id = models.CharField(max_length=5, choices=DEVICE_TYPE_CHOICES)
    device_model_id = models.ForeignKey(DeviceModel, db_column="device_model_id")
    mac_address = models.CharField(max_length=50, null=True, blank=True)
    min_range = models.IntegerField(null=True, blank=True)
    max_range = models.IntegerField(null=True, blank=True)
    identifiable = models.BooleanField()
    communication = models.CharField(max_length=10)
    date_added = models.DateTimeField()
    factory_id = models.CharField(max_length=50, null=True, blank=True)
    bemoss = models.BooleanField()

    class Meta:
        db_table = "device_info"

    def __unicode__(self):
        return self.device_id

    def data_as_json(self):
        return dict(
            device_id=self.device_id,
            device_type=self.device_type.encode('utf-8'),
            vendor_name=self.vendor_name.encode('utf-8'),
            device_model=self.device_model.encode('utf-8'),
            device_model_id=self.device_model_id,
            mac_address=self.mac_address.encode('utf-8'),
            min_range=self.min_range,
            max_range=self.max_range,
            identifiable=self.identifiable,
            date_added=self.date_added,
            bemoss=self.bemoss)

    def data_dashboard(self):

        return dict(
            device_id=self.device_id,
            device_type=self.device_type.encode('utf-8'),
            vendor_name=self.vendor_name.encode('utf-8'),
            device_model=self.device_model.encode('utf-8'),
            device_model_id=self.device_model_id,
            mac_address=self.mac_address.encode('utf-8'),
            min_range=self.min_range,
            max_range=self.max_range,
            identifiable=self.identifiable,
            bemoss=self.bemoss)

    def device_control_page_info(self):
        return dict(
            device_id=self.device_id,
            device_model_id=self.device_model_id,
            mac_address=self.mac_address.encode('utf-8'),
            device_type=self.device_type.encode('utf-8'),
            min_range=self.min_range,
            max_range=self.max_range,
            bemoss=self.bemoss)

    def device_status(self):
        return dict(
            device_model=self.device_model.encode('utf-8').capitalize(),
            date_added=self.date_added)


#Table to store floor-wise setpoints for devices. These setpoints will be overridden by local device settings.
class GlobalSetting(models.Model):
    zone = models.ForeignKey(Building_Zone)
    heat_setpoint = models.IntegerField(null=True, blank=True)
    cool_setpoint = models.IntegerField(null=True, blank=True)
    illuminance = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True,
                                              blank=True)

    class Meta:
        db_table = "global_zone_setting"

    def __unicode__(self):
        return self.id

    def as_json(self):
        return dict(
            zone=self.zone,
            heat_setpoint=self.heat_setpoint,
            cool_setpoint=self.cool_setpoint,
            illumination=self.illuminance
        )





