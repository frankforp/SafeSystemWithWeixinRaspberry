# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree

    
#my_appid = '���appid' #��д���appid
#my_secret = '���app secret' #��д���app secret
#my_yeekey = '���yeekey'#��д��� yeekey


 
def _check_hash(data):
    signature=data.signature
    timestamp=data.timestamp
    nonce=data.nonce
    #�Լ���token
    token="wangxu" #�����д����΢�Ź���ƽ̨�������token
    #�ֵ�������
    list=[token,timestamp,nonce]
    list.sort()
    sha1=hashlib.sha1()
    map(sha1.update,list)
    hashcode=sha1.hexdigest()
    #sha1�����㷨        
 
    #���������΢�ŵ�������ظ�echostr
    if hashcode == signature:
        return True
    return False
	

#def yeelink_get_temperature():
	
def	handle_click_door_open(server, fromUser, toUser, xml):
	pass
	
def	handle_click_door_close(server, fromUser, toUser, xml):
	pass

def	handle_click_detection(server, fromUser, toUser, xml):
	pass
	
def	handle_click_help(server, fromUser, toUser, xml):
	pass
	
	
weixin_click_table = {
    'V1001_DOOROPEN'        :   handle_click_door_open,
    'V1001_DOORCLOSE'       :   handle_click_door_close,
    'V1001_DETECTION'       :   handle_click_detection,
    'V1001_HELP'            :   handle_click_help
}


def handle_event_subscribe(server, fromUser, toUser, xml):
	return server.render.reply_text(fromUser, toUser,int(time.time()), u'��ӭ��ע��΢�źţ����幦�������·��˵�')

def handle_event_unsubscribe(server, fromUser, toUser, xml):
	return server.render.reply_text(fromUser, toUser,int(time.time()), u'�һ������뿪��')

def handle_event_scan(server, fromUser, toUser, xml):
	pass
	
def handle_event_location(server, fromUser, toUser, xml):
	pass
	
def handle_event_click(server, fromUser, toUser, xml):
	key = xml.find('EventKey').text
	try:
		return weixin_click_table[key](server, fromUser, toUser, xml)
	except:
		return server.render.reply_text(fromUser, toUser,int(time.time()), u'Unknow click: '+key)

		


weixin_even_table = {
	'subscribe'     :   handle_event_subscribe,
    'unsbscribe'    :   handle_event_unsubscribe,
    'SCAN'          :   handle_event_scan,
    'LOCATION'      :   handle_event_location,
    'CLICK'         :   handle_event_click,
}
	

class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
#        self.client = WeiXinClient(my_appid, my_secret, fc=True, path='/tmp')
#        self.client.request_access_token()


    def weixin_receive_text(self, fromUser, toUser, xml):
        content = xml.find('Content').text
        reply_msg = content
        return self.render.reply_text(fromUser, toUser,int(time.time()), u'�һ����������˵�Ļ�:' + reply_msg)
        
    def weixin_receive_event(self, fromUser, toUser, xml):
        event = xml.find('Event').text
		try:
			return weixin_even_table[event](self, fromUser, toUser, xml)
        except:
			return self.render.reply_text(fromUser, toUser,int(time.time()), u'�һ����������˵�Ļ�:' + event)

    def GET(self):
        data = web.input()
        if	_check_hash(data):
            return	data.echostr      

    def	POST(self):        
        str_xml = web.data() #���post��������
        xml = etree.fromstring(str_xml)#����XML����
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text

        if msgType == 'text':
            return self.weixin_receive_text(fromUser, toUser, xml)
        
        elif msgType == 'event':
            return self.weixin_receive_event(fromUser, toUser, xml)
	    


        