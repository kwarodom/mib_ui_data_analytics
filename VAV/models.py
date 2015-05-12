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
from dashboard.models import DeviceMetadata, Building_Zone


class VAV(models.Model):

    STATUS_CHOICES = (
        ('ON', 'On'),
        ('OFF', 'Off'))

    vav = models.ForeignKey(DeviceMetadata, max_length=50, primary_key=True)
    temperature = models.FloatField(null=True, blank=True)
    supply_temperature = models.FloatField(null=True, blank=True)
    heat_setpoint = models.FloatField(null=True, blank=True)
    cool_setpoint = models.FloatField(null=True, blank=True)
    flap_override = models.CharField(max_length=3, choices=STATUS_CHOICES, null=True, blank=True)
    flap_position = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True,
                                                blank=True)
    ip_address = models.IPAddressField(null=True, blank=True)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    zone = models.ForeignKey(Building_Zone, null=True, blank=True)
    network_status = models.CharField(max_length=7, null=True, blank=True)
    other_parameters = models.CharField(max_length=200, null=True, blank=True)
    last_scanned_time = models.DateTimeField(null=True, blank=True)
    last_offline_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'vav'

    def __str__(self):
        return self.as_json()

    def __unicode__(self):
        return self.vav_id

    def as_json(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.vav_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            id=self.vav_id,
            temperature=self.temperature,
            supply_temp=self.supply_temperature,
            heat_setpoint=self.heat_setpoint,
            cool_setpoint=self.cool_setpoint,
            flap_override=self.flap_override,
            identifiable=metadata['identifiable'],
            flap_position=self.flap_position,
            zone=zone_req,
            nickname=self.nickname.encode('utf-8'),
            device_model_id=metadata['device_model_id'],
            mac_address=metadata['mac_address'].encode('utf-8'),
            device_type=metadata['device_type'].encode('utf-8'),
            vendor_name=metadata['vendor_name'].encode('utf-8'),
            bemoss=metadata['bemoss'],
            device_model=metadata['device_model'].encode('utf-8'),
        )

    def device_status(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.vav_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            id=self.vav_id,
            nickname=self.nickname.encode('utf-8').title(),
            device_model=metadata['device_model'],
            date_added=metadata['date_added'],
            zone_id=zone_req['id'],
            bemoss=metadata['bemoss'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize(),
            last_scanned=self.last_scanned_time,
            last_offline=self.last_offline_time)

    def data_dashboard(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.vav_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            device_id=self.vav_id,
            device_type=metadata['device_type'].encode('utf-8'),
            vendor_name=metadata['vendor_name'].encode('utf-8'),
            device_model=metadata['device_model'].encode('utf-8'),
            device_model_id=metadata['device_model_id'],
            mac_address=metadata['mac_address'].encode('utf-8'),
            nickname=self.nickname.encode('utf-8').title(),
            date_added=metadata['date_added'],
            zone_id=zone_req['id'],
            bemoss=metadata['bemoss'],
            identifiable=metadata['identifiable'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize(),
            last_scanned=self.last_scanned_time)

    def data_side_nav(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.vav_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            device_id=self.vav_id,
            device_model_id=metadata['device_model_id'],
            mac_address=metadata['mac_address'].encode('utf-8'),
            nickname=self.nickname.encode('utf-8').title(),
            zone_id=zone_req['id'],
            bemoss=metadata['bemoss'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize())