import os
import sys
sys.path = ['/home/kruthika/workspace']+sys.path
sys.path.insert(3, '/home/kruthika/workspace/bemoss_web_ui/rtunetwork/')
sys.path.insert(2, '/home/kruthika/workspace/bemoss_web_ui/rtunetwork/lib/clock')
sys.path.insert(0, '/home/kruthika/workspace/bemoss_web_ui/helper/')
sys.path.insert(1, '/home/kruthika/workspace/bemoss_web_ui/ZMQHelper/')
#print sys.path
os.environ['DJANGO_SETTINGS_MODULE']='bemoss_web_ui.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

