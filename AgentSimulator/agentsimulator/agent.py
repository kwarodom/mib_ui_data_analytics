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

from datetime import datetime
import logging
import sys
import json
import time
import volttron.platform.agent

from volttron.platform.agent import BaseAgent, PublishMixin
from volttron.platform.agent import utils, matching
from volttron.platform.messaging import headers as headers_mod


utils.setup_logging()
_log = logging.getLogger(__name__)


class ListenerAgent(PublishMixin, BaseAgent):
    '''Listens to everything and publishes a heartbeat according to the
    heartbeat period specified in the settings module.
    '''
    def __init__(self, config_path, **kwargs):
        super(ListenerAgent, self).__init__(**kwargs)
        self.config = utils.load_config(config_path)

    def setup(self):
        # Demonstrate accessing a value from the config file
        _log.info(self.config['message'])
        self._agent_id = self.config['agentid']
        # Always call the base class setup()
        super(ListenerAgent, self).setup()
        self.topic = 'datalogger/log/bemoss/zone1/thermostat/qaz3m50'

    @matching.match_all
    def on_match(self, topic, headers, message, match):
        #Use match_all to receive all messages and print them out.
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))

   #/ui/bemoss/999/thermostat/WiFiThermostat2/device_status
    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/thermostat/([0-9a-zA-Z]+)/device_status')
    def just_response(self, topic, headers, message, match):
        print "WifiThermostat1Agent got\nTopic: {topic}".format(topic=topic)
        #print "Headers: {headers}".format(headers=headers)
        #print "Message: {message}\n".format(message=message)
        #reply message
        topic = topic.replace('agent/','')
        topic = '/agent'+topic + '/response'
        print topic
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': "agent_id",
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
            headers_mod.DATE: now,
        }
        #_data={'device_id':"WiFiThermostat2",'temp':56,'tmode':1,'fmode':1,'t_heat':75,'t_cool':75}
        _data = {'temperature': 72.5, 'thermostat_mode': 'HEAT', 'fan_mode': 'AUTO', 'heat_setpoint': 75, 'cool_setpoint': 65}
        message = json.dumps(_data)
        message = message.encode(encoding='utf_8')
        print message
        self.publish(topic, headers, message)

    @volttron.platform.agent.periodic(3)
    def test_periodic_thermostat(self):
        topic = '/ui/web/rtu/999/Thermostat4/device_status/response'
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': "agent_id",
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
            headers_mod.DATE: now,
        }
        #_data={'device_id':"WiFiThermostat2",'temp':56,'tmode':1,'fmode':1,'t_heat':75,'t_cool':75}
        _data = {
                "outside_temperature": 55,
                "supply_temperature": 67,
                "return_temperature": 99,
                "pressure": 14,
                "cooling_mode": 'STG1',
                "cooling_status": 'ON',
                "fan_status": 'OFF',
                "heating": 67,
                "heat_setpoint": 65,
                "cool_setpoint": 56,
                "outside_damper_position": 78,
                "bypass_damper_position": 89
            }
        message = json.dumps(_data)
        message = message.encode(encoding='utf_8')
        print message
        print 'periodic message to ui dfsfdsf'
        self.publish(topic, headers, message)
        print "published"

    @volttron.platform.agent.periodic(20)
    def test_periodic_vav(self):
        topic = '/ui/web/vav/999/Thermostat5/device_status/response'
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': "agent_id",
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
            headers_mod.DATE: now,
        }
        #_data={'device_id':"WiFiThermostat2",'temp':56,'tmode':1,'fmode':1,'t_heat':75,'t_cool':75}
        _data = {
                "temperature": 55,
                "supply_temperature": 67,
                "heat_setpoint": 65,
                "cool_setpoint": 56,
                "flap_override": True,
                "flap_position": 89
            }
        message = json.dumps(_data)
        message = message.encode(encoding='utf_8')
        print message
        print 'periodic message to ui'
        self.publish(topic, headers, message)

    @volttron.platform.agent.periodic(30)
    def test_periodic_plugload(self):
        topic = '/ui/web/plugload/2/Plugload2/device_status/response'
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': "agent_id",
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
            headers_mod.DATE: now,
        }
        #_data={'power': '800' ,'status':'off'}
        _data = {'status': 'OFF', 'power': '900'}
        message = json.dumps(_data)
        message = message.encode(encoding='utf_8')
        print message
        print 'periodic message to ui'
        self.publish(topic, headers, message)

    @volttron.platform.agent.periodic(30)
    def test_periodic_lighting(self):
        topic = '/ui/web/lighting/999/WifiLight8/device_status/response'
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': "agent_id",
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
            headers_mod.DATE: now,
        }
        #_data={'power': '800' ,'status':'off'}
        _data={'status':'ON',
                   'brightness':'40','color':'255,136,80',
                   'saturation':'50'}
        message = json.dumps(_data)
        message = message.encode(encoding='utf_8')
        print message
        print 'periodic message to ui'
        self.publish(topic, headers, message)

    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/thermostat/([0-9a-zA-Z]+)/update')
    def deviceControlBehavior_thermostat(self,topic,headers,message,match):
            print "WifiThermostat1Agent got\nTopic: {topic}".format(topic=topic)
            print "Headers: {headers}".format(headers=headers)
            print "Message: {message}\n".format(message=message)
            topic = topic.replace('agent/','')
            topic = '/agent'+topic + '/response'
            print topic
            #topic = '/ui/zone1/wifithermo3m50/qaz3m50/update/wifi_3m50_01/status'
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': 'new agent',
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
                headers_mod.DATE: now,
            }
            message = 'success'
            self.publish(topic, headers, message)

        #4. updateUIBehavior (generic behavior)
        #TODO update topic of the updateUIBehavior
        #@matching.match_exact('/ui/zone1/lighting/lights001/device_status')
    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/lighting/([0-9a-zA-Z]+)/device_status')
    def updateUIBehavior(self,topic,headers,message,match):
            #print "{} agent got\nTopic: {topic}".format(self.get_variable("agent_id"),topic=topic)
            print "Headers: {headers}".format(headers=headers)
            print "Message: {message}\n".format(message=message)
            #reply message
            topic = topic.replace('agent/','')
            topic = '/agent'+topic + '/response'
            print topic
            #topic='/ui/zone1/lighting/lights001/device_status/response'
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': 'test',
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
                headers_mod.DATE: now,
            }
            _data={'status':'on',
                   'brightness':'40%','color':'rgb(255,136,0)',
                   'saturation':'50%'}
            message = json.dumps(_data)
            message = message.encode(encoding='utf_8')
            print message
            self.publish(topic, headers, message)


    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/rtu/([0-9a-zA-Z]+)/device_status')
    def updateUIBehavior_RTU_status(self,topic,headers,message,match):
            #print "{} agent got\nTopic: {topic}".format(self.get_variable("agent_id"),topic=topic)
            print "Headers: {headers}".format(headers=headers)
            print "Message: {message}\n".format(message=message)
            #reply message
            topic = topic.replace('agent/','')
            topic = '/agent'+topic + '/response'
            print topic
            #topic='/ui/zone1/lighting/lights001/device_status/response'
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': 'test',
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
                headers_mod.DATE: now,
            }
            _data = {
                "outside_temperature": 75,
                "supply_temperature": 67,
                "return_temperature": 69,
                "pressure": 24,
                "cooling_mode": 'STG1',
                "cooling_status": 'ON',
                "fan_status": 'OFF',
                "heating": 67,
                "heat_setpoint": 65,
                "cool_setpoint": 56,
                "outside_damper_position": 78,
                "bypass_damper_position": 89
            }
            message = json.dumps(_data)
            message = message.encode(encoding='utf_8')
            print message
            self.publish(topic, headers, message)

    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/vav/([0-9a-zA-Z]+)/device_status')
    def updateUIBehavior_VAV_status(self,topic,headers,message,match):
            #print "{} agent got\nTopic: {topic}".format(self.get_variable("agent_id"),topic=topic)
            print "Headers: {headers}".format(headers=headers)
            print "Message: {message}\n".format(message=message)
            #reply message
            topic = topic.replace('agent/','')
            topic = '/agent'+topic + '/response'
            print topic
            #topic='/ui/zone1/lighting/lights001/device_status/response'
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': 'test',
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
                headers_mod.DATE: now,
            }
            _data = {
                "temperature": 55,
                "supply_temperature": 67,
                "heat_setpoint": 65,
                "cool_setpoint": 56,
                "flap_override": True,
                "flap_position": 89
            }
            message = json.dumps(_data)
            message = message.encode(encoding='utf_8')
            print message
            self.publish(topic, headers, message)

        #5. deviceControlBehavior (generic behavior)
        #TODO update topic of the updateUIBehavior
        #@matching.match_exact('/ui/zone1/lighting/lights001/update/lights001_01')
    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/lighting/([0-9a-zA-Z]+)/update')
    def deviceControlBehavior(self,topic,headers,message,match):
            #print "{} agent got\nTopic: {topic}".format(self.get_variable("agent_id"),topic=topic)
            print "Headers: {headers}".format(headers=headers)
            print "Message: {message}\n".format(message=message)
            #step1: change device status according to the receive message
            #Light.setDeviceStatus(self.get_variable('address'), json.loads(message[0])) #convert received message from string to JSON
            #TODO need to do additional checking whether the device setting is actually success!!!!!!!!
            #step2: update agent's knowledge on this device
            #Light.getDeviceStatus(self.get_variable('address'))
            #step3: send reply message back to the UI
            #topic = '/ui/zone1/lighting/lights001/update/lights001_01/status'
            topic = topic.replace('agent/','')
            topic = '/agent'+topic + '/response'
            print topic
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': 'test',
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
                headers_mod.DATE: now,
            }
            message = 'success'
            self.publish(topic, headers, message)
    '''
    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/plugload/([0-9a-zA-Z]+)/device_status')
    def updateUIBehavior_plugload(self,topic,headers,message,match):
            #print "{} agent got\nTopic: {topic}".format(self.get_variable("agent_id"),topic=topic)
            print "Headers: {headers}".format(headers=headers)
            print "Message: {message}\n".format(message=message)
            #reply message
            topic = topic.replace('agent/','')
            topic = '/agent'+topic + '/response'
            print topic
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': "plug load",
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
                headers_mod.DATE: now,
            }
            _data={'status':'OFF', 'power':670}
            message = json.dumps(_data)
            message = message.encode(encoding='utf_8')
            self.publish(topic, headers, message)

    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/occupancy_sensor/([0-9a-zA-Z]+)/device_status')
    def updateUIBehavior_occupancy(self,topic,headers,message,match):
            #print "{} agent got\nTopic: {topic}".format(self.get_variable("agent_id"),topic=topic)
            print "Headers: {headers}".format(headers=headers)
            print "Message: {message}\n".format(message=message)
            #reply message
            topic = topic.replace('agent/','')
            topic = '/agent'+topic + '/response'
            print topic
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': "occupancy",
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
                headers_mod.DATE: now,
            }
            _data = {'status': 'IN'}
            message = json.dumps(_data)
            message = message.encode(encoding='utf_8')
            self.publish(topic, headers, message)
    '''
    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/ambient_light_sensor/([0-9a-zA-Z]+)/device_status')
    def updateUIBehavior_ambient_lightsensor(self,topic,headers,message,match):
            #print "{} agent got\nTopic: {topic}".format(self.get_variable("agent_id"),topic=topic)
            print "Headers: {headers}".format(headers=headers)
            print "Message: {message}\n".format(message=message)
            #reply message
            topic = topic.replace('agent/','')
            topic = '/agent'+topic + '/response'
            print topic
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': "ambient_light_sensor",
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
                headers_mod.DATE: now,
            }
            _data = {'status': 400}
            message = json.dumps(_data)
            message = message.encode(encoding='utf_8')
            self.publish(topic, headers, message)

        #5. deviceControlBehavior (generic behavior)
    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/plugload/([0-9a-zA-Z]+)/update')
    def deviceControlBehavior_plugload(self,topic,headers,message,match):
            #print "{} agent got\nTopic: {topic}".format(self.get_variable("agent_id"),topic=topic)
            print "Headers: {headers}".format(headers=headers)
            #print "Message: {set_wifi_3m50_update_recv_statusmessage}\n".format(message=message)
            #step1: change device status according to the receive message
            #Plugload.setDeviceStatus(json.loads(message[0]))
            # Plugload.setDeviceStatus(self.get_variable('address'), json.loads(message[0])) #convert received message from string to JSON
            #TODO need to do additional checking whether the device setting is actually success!!!!!!!!
            #step2: update agent's knowledge on this device
            #Plugload.getDeviceStatus()
            # Plugload.getDeviceStatus(self.get_variable('address'))
            #step3: send reply message back to the UI
            topic = topic.replace('agent/','')
            topic = '/agent'+topic + '/response'
            print topic
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': 'plugload',
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
                headers_mod.DATE: now,
            }
            message = 'success'
            self.publish(topic, headers, message)

    @matching.match_exact('/ui/zone1/wifithermo3m50/qaz3m50/get/_schedule')
    def send_initial_update(self, topic, headers, message, match):
        topic = '/ui/zone1/wifithermo3m50/qaz3m50/_schedule/response'
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
                'AgentID': self._agent_id,
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
                headers_mod.DATE: now,
        }
        print headers
        schedule = {
                    'heat':{"0":[360,70,1320,62,1320,62,1320,62],
                         "1":[60,75,120,70,180,65,240,60],
                         "2":[60,75,120,70,180,65,240,60],
                         "3":[360,70,1320,62,1320,62,1320,62],
                         "4":[360,69,1320,62,1320,62,1320,62],
                         "5":[360,70,1320,62,1320,62,1320,62],
                         "6":[240,85,1215,90,1215,95]},
                    'cool':{"0":[244,66,1215,80,1315,80,1415,80],
                         "1":[120,80,240,81,360,82,480,83],
                         "2":[480,75,480,65,480,60,481,77],
                         "3":[480,75,480,80,480,85],
                         "4":[241,76,1215,85,1215,85,1215,90],
                         "5":[240,76,1215,80,1215,80,1215,80],
                         "6":[240,85,1215,90,1215,95]}
                    }
        '''schedule_cool = {"0":[244,66,1215,80,1315,80,1415,80],
                         "1":[120,80,240,81,360,82,480,83],
                         "2":[480,75,480,65,480,60,481,77],
                         "3":[480,75,480,80,480,85],
                         "4":[241,76,1215,85,1215,85,1215,90],
                         "5":[240,76,1215,80,1215,80,1215,80],
                         "6":[240,85,1215,90,1215,95]}
        schedule_heat = {"0":[360,70,1320,62,1320,62,1320,62],
                         "1":[60,75,120,70,180,65,240,60],
                         "2":[60,75,120,70,180,65,240,60],
                         "3":[360,70,1320,62,1320,62,1320,62],
                         "4":[360,69,1320,62,1320,62,1320,62],
                         "5":[360,70,1320,62,1320,62,1320,62],
                         "6":[240,85,1215,90,1215,95]}'''
        message = json.dumps(schedule)
        message = message.encode(encoding='utf_8')
        print message
        self.publish(topic, headers, message)
        #self.publish('/ui/zone1/wifithermo3m50/qaz3m50/device_status/response', headers, str(jsonresult))


    @matching.match_exact('/ui/zone1/wifithermo3m50/qaz3m50/update_schedule/schedule_wifi3m50_01')
    def send_schedule_update_status(self, topic, headers, message, match):
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        self.publish('/ui/zone1/wifithermo3m50/qaz3m50/update_schedule/schedule_wifi3m50_01/status', headers, "success")

    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/thermostat/([0-9a-zA-Z]+)/schedule')
    def send_initial_update_th_schedule(self, topic, headers, message, match):
        topic = topic.replace('agent/','')
        topic = '/agent'+topic + '/response'
        print topic

        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
                'AgentID': self._agent_id,
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
                headers_mod.DATE: now,
        }
        print headers
        schedule = {
                    'heat':{"0":[360,70,1320,62,1320,62,1320,62],
                         "1":[60,75,120,70,180,65,240,60],
                         "2":[60,75,120,70,180,65,240,60],
                         "3":[360,70,1320,62,1320,62,1320,62],
                         "4":[360,69,1320,62,1320,62,1320,62],
                         "5":[360,70,1320,62,1320,62,1320,62],
                         "6":[240,85,1215,90,1215,95]},
                    'cool':{"0":[244,66,1215,80,1315,80,1415,80],
                         "1":[120,80,240,81,360,82,480,83],
                         "2":[480,75,480,65,480,60,481,77],
                         "3":[480,75,480,80,480,85],
                         "4":[241,76,1215,85,1215,85,1215,90],
                         "5":[240,76,1215,80,1215,80,1215,80],
                         "6":[240,85,1215,90,1215,95]}
                    }

        message = json.dumps(schedule)
        message = message.encode(encoding='utf_8')
        message = 'success'
        print message
        self.publish(topic, headers, message)

    @matching.match_exact('/ui/agent/bemoss/([0-9]{3})/thermostat/([0-9a-zA-Z]+)/update_schedule')
    def send_thermostat_schedule_update_status(self, topic, headers, message, match):
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        topic = topic.replace('agent/','')
        topic = '/agent'+topic + '/response'
        print topic
        self.publish(topic, headers, "success")

    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/plugload/([0-9a-zA-Z]+)/schedule')
    def send_initial_update_pll_schedule(self, topic, headers, message, match):
        topic = topic.replace('agent/','')
        topic = '/agent'+topic + '/response'
        print topic

        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
                'AgentID': self._agent_id,
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
                headers_mod.DATE: now,
        }
        print headers
        schedule = {"0":[360,0,600,0,1020,0,1320,0],
            "1":[60,0,120,0,180,0,240,0],
            "2":[60,0,120,0,180,0,240,0],
            "3":[360,0,1320,0,1320,0,1320,0],
            "4":[360,0,1320,0,1320,0,1320,0],
            "5":[360,0,1320,0,1320,0,1320,0],
            "6":[240,0,1215,0,1215,0]}
        message = json.dumps(schedule)
        #message = json.loads(schedule)
        message = message.encode(encoding='utf_8')
        print message
        self.publish(topic, headers, message)

    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/lighting/([0-9a-zA-Z]+)/schedule')
    def send_initial_update_pl_schedule(self, topic, headers, message, match):
        topic = topic.replace('agent/','')
        topic = '/agent'+topic + '/response'
        print topic

        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
                'AgentID': self._agent_id,
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
                headers_mod.DATE: now,
        }
        print headers
        schedule = {"0":[360,0,600,0,1020,0,1320,0],
            "1":[60,0,120,0,180,0,240,0],
            "2":[60,0,120,0,180,0,240,0],
            "3":[360,0,1320,0,1320,0,1320,0],
            "4":[360,0,1320,0,1320,0,1320,0],
            "5":[360,0,1320,0,1320,0,1320,0],
            "6":[240,0,1215,0,1215,0]}
        message = json.dumps(schedule)
        #message = json.loads(schedule)
        message = message.encode(encoding='utf_8')
        print message
        self.publish(topic, headers, message)


    @matching.match_regex('/ui/app/scheduler/([0-9a-zA-Z]+)/update')
    def send_initial_update_sch(self, topic, headers, message, match):
        topic = topic.replace('app/', '')
        topic = '/app' + topic + '/response'
        print topic

        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
            headers_mod.DATE: now,
        }
        print headers
        message = "success"
        message = message.encode(encoding='utf_8')
        print message
        self.publish(topic, headers, message)


    @matching.match_exact('/ui/zone1/wifithermo3m50/qaz3m50/update_schedule/schedule_wifi3m50_01')
    def send_schedule_update_status(self, topic, headers, message, match):
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        self.publish('/ui/zone1/wifithermo3m50/qaz3m50/update_schedule/schedule_wifi3m50_01/status', headers, "success")

    @matching.match_exact('/ui/discover_devices')
    def send_devices_discovered(self, topic, headers, message, match):
        topic = '/ui/discover_devices/response'
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
                'AgentID': self._agent_id,
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
                headers_mod.DATE: now,
        }
        print headers
        devices_discovered = {'devices_on':[{'device_id':'test 1','device_mac_address':'abcd','device_ip':'8.12.236.456'},
                                            {'device_id':'test 2', 'device_mac_address':'abcda13','device_ip':'8.12.246.456'},
                                            {'device_id':'test 3', 'device_mac_address':'aad223kasd','device_ip':'8.12.236.456'}]
                             }

        '''schedule_cool = {"0":[244,66,1215,80,1315,80,1415,80],
                         "1":[120,80,240,81,360,82,480,83],
                         "2":[480,75,480,65,480,60,481,77],
                         "3":[480,75,480,80,480,85],
                         "4":[241,76,1215,85,1215,85,1215,90],
                         "5":[240,76,1215,80,1215,80,1215,80],
                         "6":[240,85,1215,90,1215,95]}
        schedule_heat = {"0":[360,70,1320,62,1320,62,1320,62],
                         "1":[60,75,120,70,180,65,240,60],
                         "2":[60,75,120,70,180,65,240,60],
                         "3":[360,70,1320,62,1320,62,1320,62],
                         "4":[360,69,1320,62,1320,62,1320,62],
                         "5":[360,70,1320,62,1320,62,1320,62],
                         "6":[240,85,1215,90,1215,95]}'''
        message = json.dumps(devices_discovered)
        message = message.encode(encoding='utf_8')
        print message
        self.publish(topic, headers, message)
        
        
    # Demonstrate periodic decorator and settings access
    '''@periodic(settings.HEARTBEAT_PERIOD)
    def publish_heartbeat(self):
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        self.publish('heartbeat/listeneragent', headers, now)'''


     #/ui/bemoss/999/thermostat/WiFiThermostat2/device_status
    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/thermostat/([0-9a-zA-Z]+)/device_status')
    def just_response(self, topic, headers, message, match):
        print "WifiThermostat1Agent got\nTopic: {topic}".format(topic=topic)
        #print "Headers: {headers}".format(headers=headers)
        #print "Message: {message}\n".format(message=message)
        #reply message
        topic = topic.replace('agent/','')
        topic = '/agent'+topic + '/response'
        print topic
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': "agent_id",
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
            headers_mod.DATE: now,
        }
        _data = {'temperature': 73.6, 'thermostat_mode': 'HEAT', 'fan_mode': 'AUTO', 'heat_setpoint': 75.5 , 'cool_setpoint': 65.6}
        message = json.dumps(_data)
        message = message.encode(encoding='utf_8')
        print message
        self.publish(topic, headers, message)

    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/thermostat/([0-9a-zA-Z]+)/update')
    def deviceControlBehavior_thermostat(self,topic,headers,message,match):
            print "WifiThermostat1Agent got\nTopic: {topic}".format(topic=topic)
            print "Headers: {headers}".format(headers=headers)
            print "Message: {message}\n".format(message=message)
            topic = topic.replace('agent/','')
            topic = '/agent'+topic + '/response'
            print topic
            #topic = '/ui/zone1/wifithermo3m50/qaz3m50/update/wifi_3m50_01/status'
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': 'new agent',
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
                headers_mod.DATE: now,
            }
            message = 'success'
            self.publish(topic, headers, message)

    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/vav/([0-9a-zA-Z]+)/update')
    def deviceControlBehavior_vav(self,topic,headers,message,match):
            print "WifiThermostat1Agent got\nTopic: {topic}".format(topic=topic)
            print "Headers: {headers}".format(headers=headers)
            print "Message: {message}\n".format(message=message)
            topic = topic.replace('agent/','')
            topic = '/agent'+topic + '/response'
            print topic
            #topic = '/ui/zone1/wifithermo3m50/qaz3m50/update/wifi_3m50_01/status'
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': 'new agent',
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
                headers_mod.DATE: now,
            }
            message = 'success'
            self.publish(topic, headers, message)


    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/rtu/([0-9a-zA-Z]+)/update')
    def deviceControlBehavior_rtuu(self,topic,headers,message,match):
            print "WifiThermostat1Agent got\nTopic: {topic}".format(topic=topic)
            print "Headers: {headers}".format(headers=headers)
            print "Message: {message}\n".format(message=message)
            topic = topic.replace('agent/','')
            topic = '/agent'+topic + '/response'
            print topic
            #topic = '/ui/zone1/wifithermo3m50/qaz3m50/update/wifi_3m50_01/status'
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': 'new agent',
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
                headers_mod.DATE: now,
            }
            message = 'success'
            self.publish(topic, headers, message)


        #4. updateUIBehavior (generic behavior)
        #TODO update topic of the updateUIBehavior
        #@matching.match_exact('/ui/zone1/lighting/lights001/device_status')
    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/lighting/([0-9a-zA-Z]+)/device_status')
    def updateUIBehavior(self,topic,headers,message,match):
            #print "{} agent got\nTopic: {topic}".format(self.get_variable("agent_id"),topic=topic)
            print "Headers: {headers}".format(headers=headers)
            print "Message: {message}\n".format(message=message)
            #reply message
            topic = topic.replace('agent/','')
            topic = '/agent'+topic + '/response'
            print topic
            #topic='/ui/zone1/lighting/lights001/device_status/response'
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': 'test',
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
                headers_mod.DATE: now,
            }
            _data={'status':'ON',
                   'brightness':49,'color':[34,56,67],
                   'saturation':63}
            message = json.dumps(_data)
            message = message.encode(encoding='utf_8')
            print message
            self.publish(topic, headers, message)

        #5. deviceControlBehavior (generic behavior)
        #TODO update topic of the updateUIBehavior
        #@matching.match_exact('/ui/zone1/lighting/lights001/update/lights001_01')
    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/lighting/([0-9a-zA-Z]+)/update')
    def deviceControlBehavior(self,topic,headers,message,match):
            #print "{} agent got\nTopic: {topic}".format(self.get_variable("agent_id"),topic=topic)
            print "Headers: {headers}".format(headers=headers)
            print "Message: {message}\n".format(message=message)
            #step1: change device status according to the receive message
            #Light.setDeviceStatus(self.get_variable('address'), json.loads(message[0])) #convert received message from string to JSON
            #TODO need to do additional checking whether the device setting is actually success!!!!!!!!
            #step2: update agent's knowledge on this device
            #Light.getDeviceStatus(self.get_variable('address'))
            #step3: send reply message back to the UI
            #topic = '/ui/zone1/lighting/lights001/update/lights001_01/status'
            topic = topic.replace('agent/','')
            topic = '/agent'+topic + '/response'
            print topic
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': 'test',
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
                headers_mod.DATE: now,
            }
            message = 'success'
            self.publish(topic, headers, message)

    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/plugload/([0-9a-zA-Z]+)/device_status')
    def updateUIBehavior_plugload(self,topic,headers,message,match):
            #print "{} agent got\nTopic: {topic}".format(self.get_variable("agent_id"),topic=topic)
            print "Headers: {headers}".format(headers=headers)
            print "Message: {message}\n".format(message=message)
            #reply message
            topic = topic.replace('agent/','')
            topic = '/agent'+topic + '/response'
            print topic
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': "plug load",
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
                headers_mod.DATE: now,
            }
            _data = {'status': 'OFF', 'power':500}
            message = json.dumps(_data)
            message = message.encode(encoding='utf_8')
            self.publish(topic, headers, message)

    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/power_meter/([0-9a-zA-Z]+)/device_status')
    def updateUIBehavior_power_meter(self,topic,headers,message,match):
            #print "{} agent got\nTopic: {topic}".format(self.get_variable("agent_id"),topic=topic)
            print "Headers: {headers}".format(headers=headers)
            print "Message: {message}\n".format(message=message)
            #reply message
            topic = topic.replace('agent/','')
            topic = '/agent'+topic + '/response'
            print topic
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': "plug load",
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
                headers_mod.DATE: now,
            }
            _data = {'real_power': 12, 'apparent_power': 12, 'reactive_power': 10, 'voltage': 14, 'current': 16,
                     'power_factor': 11, 'energy': 12}
            message = json.dumps(_data)
            message = message.encode(encoding='utf_8')
            self.publish(topic, headers, message)

        #5. deviceControlBehavior (generic behavior)
    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/plugload/([0-9a-zA-Z]+)/update')
    def deviceControlBehavior_plugload(self,topic,headers,message,match):
            #print "{} agent got\nTopic: {topic}".format(self.get_variable("agent_id"),topic=topic)
            print "Headers: {headers}".format(headers=headers)
            #print "Message: {set_wifi_3m50_update_recv_statusmessage}\n".format(message=message)
            #step1: change device status according to the receive message
            #Plugload.setDeviceStatus(json.loads(message[0]))
            # Plugload.setDeviceStatus(self.get_variable('address'), json.loads(message[0])) #convert received message from string to JSON
            #TODO need to do additional checking whether the device setting is actually success!!!!!!!!
            #step2: update agent's knowledge on this device
            #Plugload.getDeviceStatus()
            # Plugload.getDeviceStatus(self.get_variable('address'))
            #step3: send reply message back to the UI
            topic = topic.replace('agent/','')
            topic = '/agent'+topic + '/response'
            print topic
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': 'plugload',
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
                headers_mod.DATE: now,
            }
            message = 'success'
            self.publish(topic, headers, message)

    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/thermostat/([0-9a-zA-Z]+)/identify')
    def identify_thermostat(self,topic,headers,message,match):
            #print "{} agent got\nTopic: {topic}".format(self.get_variable("agent_id"),topic=topic)
            print "Headers: {headers}".format(headers=headers)
            #print "Message: {set_wifi_3m50_update_recv_statusmessage}\n".format(message=message)
            #step1: change device status according to the receive message
            #Plugload.setDeviceStatus(json.loads(message[0]))
            # Plugload.setDeviceStatus(self.get_variable('address'), json.loads(message[0])) #convert received message from string to JSON
            #TODO need to do additional checking whether the device setting is actually success!!!!!!!!
            #step2: update agent's knowledge on this device
            #Plugload.getDeviceStatus()
            # Plugload.getDeviceStatus(self.get_variable('address'))
            #step3: send reply message back to the UI
            topic = topic.replace('agent/', '')
            topic = '/agent'+topic + '/response'
            print topic
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': 'plugload',
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
                headers_mod.DATE: now,
            }
            message = 'success'
            time.sleep(10)
            self.publish(topic, headers, message)

    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/lighting/([0-9a-zA-Z]+)/identify')
    def identify_lighting(self,topic,headers,message,match):
            #print "{} agent got\nTopic: {topic}".format(self.get_variable("agent_id"),topic=topic)
            print "Headers: {headers}".format(headers=headers)
            #print "Message: {set_wifi_3m50_update_recv_statusmessage}\n".format(message=message)
            #step1: change device status according to the receive message
            #Plugload.setDeviceStatus(json.loads(message[0]))
            # Plugload.setDeviceStatus(self.get_variable('address'), json.loads(message[0])) #convert received message from string to JSON
            #TODO need to do additional checking whether the device setting is actually success!!!!!!!!
            #step2: update agent's knowledge on this device
            #Plugload.getDeviceStatus()
            # Plugload.getDeviceStatus(self.get_variable('address'))
            #step3: send reply message back to the UI
            topic = topic.replace('agent/', '')
            topic = '/agent'+topic + '/response'
            print topic
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': 'plugload',
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
                headers_mod.DATE: now,
            }
            message = 'success'
            time.sleep(10)
            self.publish(topic, headers, message)

    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/plugload/([0-9a-zA-Z]+)/identify')
    def identify_plugload(self,topic,headers,message,match):
            #print "{} agent got\nTopic: {topic}".format(self.get_variable("agent_id"),topic=topic)
            print "Headers: {headers}".format(headers=headers)
            #print "Message: {set_wifi_3m50_update_recv_statusmessage}\n".format(message=message)
            #step1: change device status according to the receive message
            #Plugload.setDeviceStatus(json.loads(message[0]))
            # Plugload.setDeviceStatus(self.get_variable('address'), json.loads(message[0])) #convert received message from string to JSON
            #TODO need to do additional checking whether the device setting is actually success!!!!!!!!
            #step2: update agent's knowledge on this device
            #Plugload.getDeviceStatus()
            # Plugload.getDeviceStatus(self.get_variable('address'))
            #step3: send reply message back to the UI
            topic = topic.replace('agent/', '')
            topic = '/agent'+topic + '/response'
            print topic
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': 'plugload',
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
                headers_mod.DATE: now,
            }
            message = 'success'
            time.sleep(10)
            self.publish(topic, headers, message)


    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/occupancy_sensor/([0-9a-zA-Z]+)/identify')
    def identify_occupancy(self,topic,headers,message,match):
            #print "{} agent got\nTopic: {topic}".format(self.get_variable("agent_id"),topic=topic)
            print "Headers: {headers}".format(headers=headers)
            #print "Message: {set_wifi_3m50_update_recv_statusmessage}\n".format(message=message)
            #step1: change device status according to the receive message
            #Plugload.setDeviceStatus(json.loads(message[0]))
            # Plugload.setDeviceStatus(self.get_variable('address'), json.loads(message[0])) #convert received message from string to JSON
            #TODO need to do additional checking whether the device setting is actually success!!!!!!!!
            #step2: update agent's knowledge on this device
            #Plugload.getDeviceStatus()
            # Plugload.getDeviceStatus(self.get_variable('address'))
            #step3: send reply message back to the UI
            topic = topic.replace('agent/', '')
            topic = '/agent'+topic + '/response'
            print topic
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': 'plugload',
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
                headers_mod.DATE: now,
            }
            message = 'success'
            time.sleep(10)
            self.publish(topic, headers, message)

    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/ambient_light_sensor/([0-9a-zA-Z]+)/identify')
    def identify_daylight_sensor(self,topic,headers,message,match):
            #print "{} agent got\nTopic: {topic}".format(self.get_variable("agent_id"),topic=topic)
            print "Headers: {headers}".format(headers=headers)
            #print "Message: {set_wifi_3m50_update_recv_statusmessage}\n".format(message=message)
            #step1: change device status according to the receive message
            #Plugload.setDeviceStatus(json.loads(message[0]))
            # Plugload.setDeviceStatus(self.get_variable('address'), json.loads(message[0])) #convert received message from string to JSON
            #TODO need to do additional checking whether the device setting is actually success!!!!!!!!
            #step2: update agent's knowledge on this device
            #Plugload.getDeviceStatus()
            # Plugload.getDeviceStatus(self.get_variable('address'))
            #step3: send reply message back to the UI
            topic = topic.replace('agent/', '')
            topic = '/agent'+topic + '/response'
            print topic
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': 'plugload',
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
                headers_mod.DATE: now,
            }
            message = 'success'
            time.sleep(10)
            self.publish(topic, headers, message)


    @matching.match_regex('/ui/agent/bemoss/([0-9]{3})/power_meter/([0-9a-zA-Z]+)/identify')
    def identify_powermeter(self,topic,headers,message,match):
            #print "{} agent got\nTopic: {topic}".format(self.get_variable("agent_id"),topic=topic)
            print "Headers: {headers}".format(headers=headers)
            #print "Message: {set_wifi_3m50_update_recv_statusmessage}\n".format(message=message)
            #step1: change device status according to the receive message
            #Plugload.setDeviceStatus(json.loads(message[0]))
            # Plugload.setDeviceStatus(self.get_variable('address'), json.loads(message[0])) #convert received message from string to JSON
            #TODO need to do additional checking whether the device setting is actually success!!!!!!!!
            #step2: update agent's knowledge on this device
            #Plugload.getDeviceStatus()
            # Plugload.getDeviceStatus(self.get_variable('address'))
            #step3: send reply message back to the UI
            topic = topic.replace('agent/', '')
            topic = '/agent'+topic + '/response'
            print topic
            now = datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': 'plugload',
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
                headers_mod.DATE: now,
            }
            message = 'success'
            time.sleep(10)
            self.publish(topic, headers, message)


    @matching.match_exact('/ui/zone1/wifithermo3m50/qaz3m50/get/_schedule')
    def send_initial_update(self, topic, headers, message, match):
        topic = '/ui/zone1/wifithermo3m50/qaz3m50/_schedule/response'
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
                'AgentID': self._agent_id,
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
                headers_mod.DATE: now,
        }
        print headers
        schedule = {
                    'heat':{"0":[360,70,1320,62,1320,62,1320,62],
                         "1":[60,75,120,70,180,65,240,60],
                         "2":[60,75,120,70,180,65,240,60],
                         "3":[360,70,1320,62,1320,62,1320,62],
                         "4":[360,69,1320,62,1320,62,1320,62],
                         "5":[360,70,1320,62,1320,62,1320,62],
                         "6":[240,85,1215,90,1215,95]},
                    'cool':{"0":[244,66,1215,80,1315,80,1415,80],
                         "1":[120,80,240,81,360,82,480,83],
                         "2":[480,75,480,65,480,60,481,77],
                         "3":[480,75,480,80,480,85],
                         "4":[241,76,1215,85,1215,85,1215,90],
                         "5":[240,76,1215,80,1215,80,1215,80],
                         "6":[240,85,1215,90,1215,95]}
                    }
        '''schedule_cool = {"0":[244,66,1215,80,1315,80,1415,80],
                         "1":[120,80,240,81,360,82,480,83],
                         "2":[480,75,480,65,480,60,481,77],
                         "3":[480,75,480,80,480,85],
                         "4":[241,76,1215,85,1215,85,1215,90],
                         "5":[240,76,1215,80,1215,80,1215,80],
                         "6":[240,85,1215,90,1215,95]}
        schedule_heat = {"0":[360,70,1320,62,1320,62,1320,62],
                         "1":[60,75,120,70,180,65,240,60],
                         "2":[60,75,120,70,180,65,240,60],
                         "3":[360,70,1320,62,1320,62,1320,62],
                         "4":[360,69,1320,62,1320,62,1320,62],
                         "5":[360,70,1320,62,1320,62,1320,62],
                         "6":[240,85,1215,90,1215,95]}'''
        message = json.dumps(schedule)
        message = message.encode(encoding='utf_8')
        print message
        self.publish(topic, headers, message)
        #self.publish('/ui/zone1/wifithermo3m50/qaz3m50/device_status/response', headers, str(jsonresult))


    @matching.match_exact('/ui/zone1/wifithermo3m50/qaz3m50/update_schedule/schedule_wifi3m50_01')
    def send_schedule_update_status(self, topic, headers, message, match):
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: now,
        }
        self.publish('/ui/zone1/wifithermo3m50/qaz3m50/update_schedule/schedule_wifi3m50_01/status', headers, "success")

    @matching.match_exact('/ui/discover_devices')
    def send_devices_discovered(self, topic, headers, message, match):
        topic = '/ui/discover_devices/response'
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
                'AgentID': self._agent_id,
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
                headers_mod.DATE: now,
        }
        print headers
        devices_discovered = {'devices_on':[{'device_id':'test 1','device_mac_address':'abcd','device_ip':'8.12.236.456'},
                                            {'device_id':'test 2', 'device_mac_address':'abcda13','device_ip':'8.12.246.456'},
                                            {'device_id':'test 3', 'device_mac_address':'aad223kasd','device_ip':'8.12.236.456'}]
                             }

        '''schedule_cool = {"0":[244,66,1215,80,1315,80,1415,80],
                         "1":[120,80,240,81,360,82,480,83],
                         "2":[480,75,480,65,480,60,481,77],
                         "3":[480,75,480,80,480,85],
                         "4":[241,76,1215,85,1215,85,1215,90],
                         "5":[240,76,1215,80,1215,80,1215,80],
                         "6":[240,85,1215,90,1215,95]}
        schedule_heat = {"0":[360,70,1320,62,1320,62,1320,62],
                         "1":[60,75,120,70,180,65,240,60],
                         "2":[60,75,120,70,180,65,240,60],
                         "3":[360,70,1320,62,1320,62,1320,62],
                         "4":[360,69,1320,62,1320,62,1320,62],
                         "5":[360,70,1320,62,1320,62,1320,62],
                         "6":[240,85,1215,90,1215,95]}'''
        message = json.dumps(devices_discovered)
        message = message.encode(encoding='utf_8')
        print message
        self.publish(topic, headers, message)

    '''
    @periodic(120)
    def alert_to_ui(self):
        topic = '/agent/ui/alerts/temperature_exceeds/5'
        now = datetime.utcnow().isoformat(' ') + 'Z'
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.JSON,
            headers_mod.DATE: now,
        }
        print headers

        message = "Send notification"
        #message = message.encode(encoding='utf_8')
        print message
        self.publish(topic, headers, message)'''


def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.default_main(ListenerAgent,
                           description='Example VOLTTRON heartbeat agent',
                           argv=argv)
    except Exception as e:
        _log.exception('unhandled exception')


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
