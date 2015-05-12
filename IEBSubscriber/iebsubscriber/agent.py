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

import sys
import logging
import os

sys.path.append(os.getcwd())

from volttron.platform.agent import utils, matching
from volttron.platform.agent import BaseAgent, PublishMixin
from volttron.platform.messaging import headers as headers_mod
from ZMQHelper import zmq_topics
from _utils import page_load_helper




utils.setup_logging()
_log = logging.getLogger(__name__)


class ZMQ_Subscribe(PublishMixin, BaseAgent):
    
    def __init__(self, config_path, **kwargs):
        super(ZMQ_Subscribe, self).__init__(**kwargs)
        self.config = utils.load_config(config_path)

    def setup(self):
        self._agent_id = self.config['agentid']
        # Always call the base class setup()
        super(ZMQ_Subscribe, self).setup()
        print "IEB SUbscrbier"

    #Thermostat device_status response from agent --  handler
    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/thermostat/([0-9a-zA-Z]+)/device_status/response')
    def on_match_device_status_update(self, topic, headers, message, match):
        '''Handle message and send to browser.'''
        print os.path.basename(__file__)+"@on_match_device_status_update"
        print "message:"+str(message)
        device_info = topic.split('/')
        device_id = device_info[6]
        device_type = device_info[5]
        page_load_helper.page_load(device_id, device_type, message[0])
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        topic = topic.split('/')
        topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        print topic_to_tcp
        self.publish(str(topic_to_tcp), headers, str(message))

    #RTU device_status response from agent --  handler
    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/rtu/([0-9a-zA-Z]+)/device_status/response')
    def on_match_device_status_update_rtu(self, topic, headers, message, match):
        '''Handle message and send to browser.'''
        print os.path.basename(__file__)+"@on_match_device_status_update"
        print "message:"+str(message)
        device_info = topic.split('/')
        device_id = device_info[6]
        device_type = device_info[5]
        page_load_helper.page_load(device_id, device_type, message[0])
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        topic = topic.split('/')
        topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        print topic_to_tcp
        self.publish(str(topic_to_tcp), headers, str(message))

    #VAV device_status response from agent --  handler
    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/vav/([0-9a-zA-Z]+)/device_status/response')
    def on_match_device_status_update_vav(self, topic, headers, message, match):
        '''Handle message and send to browser.'''
        print os.path.basename(__file__)+"@on_match_device_status_update"
        print "message:"+str(message)
        device_info = topic.split('/')
        device_id = device_info[6]
        device_type = device_info[5]
        page_load_helper.page_load(device_id, device_type, message[0])
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        topic = topic.split('/')
        topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        print topic_to_tcp
        self.publish(str(topic_to_tcp), headers, str(message))

    #Thermostat update status response from agent --  handler
    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/thermostat/([0-9a-zA-Z]+)/update/response')
    def on_match_status_update(self, topic, headers, message, match):
        print os.path.basename(__file__)+"@on_match_status_update"
        print "message:"+str(message)
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        print 'testing tcp tornado'
        topic = topic.split('/')
        topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        print topic_to_tcp
        self.publish(str(topic_to_tcp), headers, str(message))
        if len(str(message)) != 0:
            print(" Thermostat update status is "+str(message).strip('[]').upper())

    #RTU update status response from agent --  handler
    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/rtu/([0-9a-zA-Z]+)/update/response')
    def on_match_status_update_rtu_response(self, topic, headers, message, match):
        print os.path.basename(__file__)+"RTU UPDATE RESPONSE"
        print "message:"+str(message)
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        topic = topic.split('/')
        topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        print topic_to_tcp
        self.publish(str(topic_to_tcp), headers, str(message))
        if len(str(message)) != 0:
            print(" RTU update status is "+str(message).strip('[]').upper())

    #RTU update status response from agent --  handler
    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/vav/([0-9a-zA-Z]+)/update/response')
    def on_match_status_update_vav_response(self, topic, headers, message, match):
        print os.path.basename(__file__)+"@on_match_status_update"
        print "message:"+str(message)
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        topic = topic.split('/')
        topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        print topic_to_tcp
        self.publish(str(topic_to_tcp), headers, str(message))
        if len(str(message)) != 0:
            print(" VAV update status is "+str(message).strip('[]').upper())

    #Scheduler App - UI Response Handler
    @matching.match_regex('/app/ui/thermostat_scheduler/([0-9a-zA-Z]+)/update/response')
    def on_match_device_scheduleth_response(self, topic, headers, message, match):
        print "inside new method"
        print "message:" + str(message)
        device_id = topic.split('/')
        device_id = device_id[4]
        zmq_topics.set_schedule_update_status(device_id, message)


    @matching.match_regex('/app/ui/plugload_scheduler/([0-9a-zA-Z]+)/update/response')
    def on_match_device_schedulepl_response(self, topic, headers, message, match):
        print "inside new method"
        print "message:" + str(message)
        device_id = topic.split('/')
        device_id = device_id[4]
        zmq_topics.set_schedule_update_status(device_id, message)


    @matching.match_regex('/app/ui/lighting_scheduler/([0-9a-zA-Z]+)/update/response')
    def on_match_device_schedulelt_response(self, topic, headers, message, match):
        print "inside new method"
        print "message:" + str(message)
        device_id = topic.split('/')
        device_id = device_id[4]
        zmq_topics.set_schedule_update_status(device_id, message)


    #Lighting device_status response from agent --  handler
    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/lighting/([0-9a-zA-Z]+)/device_status/response')
    def on_match_hue_page_load(self, topic, headers, message, match):
        print "inside subscribe method for hue page load"
        print "message:"+str(message)
        device_info = topic.split('/')
        device_id = device_info[6]
        device_type = device_info[5]
        page_load_helper.page_load(device_id, device_type, message[0])
        if message:
            print 'success, thermostat updated'+str(message).strip('[]')
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        topic = device_info
        topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        print topic_to_tcp
        self.publish(str(topic_to_tcp), headers, str(message))

    #Lighting update status response from agent --  handler
    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/lighting/([0-9a-zA-Z]+)/update/response')
    def on_match_hue_device_update_status(self, topic, headers, message, match):
        print "inside subscribe method for hue page load"
        print "message:"+str(message)

        if message:
            print 'success, thermostat updated'+str(message).strip('[]')
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        topic = topic.split('/')
        topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        print topic_to_tcp
        self.publish(str(topic_to_tcp), headers, str(message))

    #Plugload update status response from agent --  handler
    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/plugload/([0-9a-zA-Z]+)/update/response')
    def on_match_status_update_plugload(self, topic, headers, message, match):
        print "inside subscribe method"
        print "message:"+str(message)

        if message:
            print 'success, thermostat updated'+str(message).strip('[]')
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        topic = topic.split('/')
        topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        print topic_to_tcp
        self.publish(str(topic_to_tcp), headers, str(message))

    #Plugload device_status response from agent --  handler
    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/plugload/([0-9a-zA-Z]+)/device_status/response')
    def on_match_device_status_update_plugload(self, topic, headers, message, match):
        print "inside subscribe method"
        print "message:"+str(message)
        device_info = topic.split('/')
        device_id = device_info[6]
        device_type = device_info[5]
        page_load_helper.page_load(device_id, device_type, message[0])
        if message:
            print 'success, thermostat updated'+str(message).strip('[]')
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        topic = device_info
        topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        print topic_to_tcp
        self.publish(str(topic_to_tcp), headers, str(message))

    #Occupancy sensor device_status response from agent --  handler
    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/occupancy_sensor/([0-9a-zA-Z]+)/device_status/response')
    def on_match_device_status_occupancy(self, topic, headers, message, match):
        print "inside subscribe method of occupancy sensor"
        print "message:"+str(message)
        device_info = topic.split('/')
        device_id = device_info[6]
        device_type = device_info[5]
        page_load_helper.page_load(device_id, device_type, message[0])
        if message:
            print 'occupancy status received'+str(message).strip('[]')
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        topic = device_info
        topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        print topic_to_tcp
        self.publish(str(topic_to_tcp), headers, str(message))

    #Occupancy sensor device_status response from agent --  handler
    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/ambient_light_sensor/([0-9a-zA-Z]+)/device_status/response')
    def on_match_device_status_daylight_sensor(self, topic, headers, message, match):
        print "inside subscribe method of daylight sensor"
        print "message:"+str(message)
        device_info = topic.split('/')
        device_id = device_info[6]
        device_type = device_info[5]
        page_load_helper.page_load(device_id, device_type, message[0])
        if message:
            print 'daylight_sensor status received'+str(message).strip('[]')
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        topic = device_info
        topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        print topic_to_tcp
        self.publish(str(topic_to_tcp), headers, str(message))

    #Occupancy sensor device_status response from agent --  handler
    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/power_meter/([0-9a-zA-Z]+)/device_status/response')
    def on_match_device_status_powermeter(self, topic, headers, message, match):
        print "inside subscribe method of daylight sensor"
        print "message:"+str(message)
        device_info = topic.split('/')
        device_id = device_info[6]
        device_type = device_info[5]
        page_load_helper.page_load(device_id, device_type, message[0])
        if message:
            print 'powermeter status received'+str(message).strip('[]')
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        topic = device_info
        topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        print topic_to_tcp
        self.publish(str(topic_to_tcp), headers, str(message))

    #Thermostat device identification response from agent --  handler
    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/thermostat/([0-9a-zA-Z]+)/identify/response')
    def on_match_device_identify_thermostat(self, topic, headers, message, match):
        print "inside subscribe method-identify thermostat"
        print "message:"+str(message)
        device_id = topic.split('/')
        device_id = device_id[6]
        print device_id
        update_topic = "identify_device_status_thermostat"
        zmq_topics.identify_device_update(device_id, message, update_topic)
        #zmq_topics.set_wifi_3m50_device_update_status(json.loads(json.dumps(message)))
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        #topic = topic.split('/')
        #topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        #print type(message)
        #self.publish(str(topic_to_tcp), headers, str(message))

    #Lighting device identification response from agent --  handler
    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/lighting/([0-9a-zA-Z]+)/identify/response')
    def on_match_device_identify_lighting(self, topic, headers, message, match):
        print "inside subscribe method-identify lighting"
        print "message:"+str(message)
        device_id = topic.split('/')
        device_id = device_id[6]
        print device_id
        update_topic = "identify_device_status_lighting"
        zmq_topics.identify_device_update(device_id, message, update_topic)
        #zmq_topics.set_plugload_device_update_status(str(message).strip('[]'))
        #zmq_topics.set_wifi_3m50_device_update_status(json.loads(json.dumps(message)))
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        #topic = topic.split('/')
        #topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        #self.publish(str(topic_to_tcp), headers, message)

    #Plugload device identification response from agent --  handler
    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/plugload/([0-9a-zA-Z]+)/identify/response')
    def on_match_device_identify_plugload(self, topic, headers, message, match):
        print "inside subscribe method-identify plugload"
        print "message:"+str(message)
        device_id = topic.split('/')
        device_id = device_id[6]
        print device_id
        update_topic = "identify_device_status_plugload"
        zmq_topics.identify_device_update(device_id, message, update_topic)
        #zmq_topics.set_plugload_device_update_status(str(message).strip('[]'))
        #zmq_topics.set_wifi_3m50_device_update_status(json.loads(json.dumps(message)))
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        #topic = topic.split('/')
        #topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        #self.publish(str(topic_to_tcp), headers, message)


    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/occupancy/([0-9a-zA-Z]+)/identify/response')
    def on_match_device_identify_occupancy(self, topic, headers, message, match):
        print "inside subscribe method-identify plugload"
        print "message:"+str(message)
        device_id = topic.split('/')
        device_id = device_id[6]
        print device_id
        update_topic = "identify_device_status_occupancy_sensor"
        zmq_topics.identify_device_update(device_id, message, update_topic)
        #zmq_topics.set_plugload_device_update_status(str(message).strip('[]'))
        #zmq_topics.set_wifi_3m50_device_update_status(json.loads(json.dumps(message)))
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))

    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/rtu/([0-9a-zA-Z]+)/identify/response')
    def on_match_device_identify_rtu(self, topic, headers, message, match):
        print "inside subscribe method-identify rtu"
        print "message:"+str(message)
        device_id = topic.split('/')
        device_id = device_id[6]
        print device_id
        update_topic = "identify_device_status_rtu"
        zmq_topics.identify_device_update(device_id, message, update_topic)
        #zmq_topics.set_plugload_device_update_status(str(message).strip('[]'))
        #zmq_topics.set_wifi_3m50_device_update_status(json.loads(json.dumps(message)))
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))

    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/vav/([0-9a-zA-Z]+)/identify/response')
    def on_match_device_identify_vav(self, topic, headers, message, match):
        print "inside subscribe method-identify vav"
        print "message:"+str(message)
        device_id = topic.split('/')
        device_id = device_id[6]
        print device_id
        update_topic = "identify_device_status_vav"
        zmq_topics.identify_device_update(device_id, message, update_topic)
        #zmq_topics.set_plugload_device_update_status(str(message).strip('[]'))
        #zmq_topics.set_wifi_3m50_device_update_status(json.loads(json.dumps(message)))
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        #topic = topic.split('/')
        #topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        #self.publish(str(topic_to_tcp), headers, message)


    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/ambient_light_sensor/([0-9a-zA-Z]+)/identify/response')
    def on_match_device_identify_daylight_sensor(self, topic, headers, message, match):
        print "inside subscribe method-identify plugload"
        print "message:"+str(message)
        device_id = topic.split('/')
        device_id = device_id[6]
        print device_id
        update_topic = "identify_device_status_ambient_light_sensor"
        zmq_topics.identify_device_update(device_id, message, update_topic)
        #zmq_topics.set_plugload_device_update_status(str(message).strip('[]'))
        #zmq_topics.set_wifi_3m50_device_update_status(json.loads(json.dumps(message)))
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        #topic = topic.split('/')
        #topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        #self.publish(str(topic_to_tcp), headers, message)


    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/power_meter/([0-9a-zA-Z]+)/identify/response')
    def on_match_device_identify_powermeter(self, topic, headers, message, match):
        print "inside subscribe method-identify plugload"
        print "message:"+str(message)
        device_id = topic.split('/')
        device_id = device_id[6]
        print device_id
        update_topic = "identify_device_status_power_meter"
        zmq_topics.identify_device_update(device_id, message, update_topic)
        #zmq_topics.set_plugload_device_update_status(str(message).strip('[]'))
        #zmq_topics.set_wifi_3m50_device_update_status(json.loads(json.dumps(message)))
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        #topic = topic.split('/')
        #topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        #self.publish(str(topic_to_tcp), headers, message)


    '''
    #Alerts and Notifications Handler - Still being tested.
    @matching.match_exact('/agent/ui/alerts/temperature_exceeds/5')
    def on_match_device_schedule_response(self, topic, headers, message, match):
        print "inside subscribe method"
        print "message:"+str(message)
        _message_id = topic.split('/')
        _msg_len = _message_id.__len__()
        print _msg_len
        notify_handler.handle_ieb_message(_message_id[_msg_len-1])
        #zmq_topics.set_wifi_3m50_schedule(str(message).strip('[]').strip('\'\''))
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        topic = topic.split('/')
        topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        self.publish(str(topic_to_tcp), headers, message)
        '''


def main(argv=sys.argv):
    try:
        utils.default_main(ZMQ_Subscribe,
                           description='ZMQ UI Subscribe',
                           argv=argv)
    except Exception as e:
        _log.exception('unhandled exception', e)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass

