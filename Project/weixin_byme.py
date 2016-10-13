# -*- coding: utf-8 -*-

import hashlib
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree

    

 
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

def yeelink_get_picture():
    url = 'http://api.yeelink.net/v1.0/device/347567/sensor/388292/photo/content'
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    return response.read()
	
def yeelink_get_temperature(self):
    url = 'http://api.yeelink.net/v1.0/device/347567/sensor/388291/datapoints'
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)       # ����ҳ������
    data = response.read()                    # ��ȡ���������ص�ҳ����Ϣ
    ddata=json.loads(data)
    return str(ddata['value'])


def yeelink_post_door_open(self):
    url = 'http://api.yeelink.net/v1.0/device/347567/sensor/388397/datapoints'
    headers = {'U-ApiKey':'25ec08ace6bb4a84f8cbb60a821d42d0'}
    data={
  "value":1
}
    jdata = json.dumps(data)
    req = urllib2.Request(url,jdata,headers)
    response = urllib2.urlopen(req)       # ����ҳ������
    return response.read()


def yeelink_post_door_close(self):
    url = 'http://api.yeelink.net/v1.0/device/347567/sensor/388397/datapoints'
    headers = {'U-ApiKey':'25ec08ace6bb4a84f8cbb60a821d42d0'}
    data={
  "value":0
}
    jdata = json.dumps(data)
    req = urllib2.Request(url,jdata,headers)
    response = urllib2.urlopen(req)       # ����ҳ������
    return response.read()
	
    
def	handle_click_door_open(server, fromUser, toUser, xml):
    yeelink_post_door_open(server)
    return server.render.reply_text(fromUser,toUser,int(time.time()),u'���Ѵ�')
	
    
def	handle_click_door_close(server, fromUser, toUser, xml):
	yeelink_post_door_close(server)
 	return server.render.reply_text(fromUser,toUser,int(time.time()),u'���ѹر�')

def	handle_click_detection(server,fromUser,toUser,xml):
    value=yeelink_get_temperature(server)
    tem= str(value)
    return server.render.reply_text(fromUser,toUser,int(time.time()),u'�¶ȣ�'+tem)


	
def	handle_click_help(server, fromUser, toUser, xml):
	return server.render.reply_image(fromUser,toUser,int(time.time()))
	
	
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
	
def handle_event_click(server,fromUser,toUser,xml):
    key=xml.find('EventKey').text
    try:
        return weixin_click_table[key](server,fromUser,toUser,xml)
    except KeyError,e:
        print 'weixin_click_table:%s'%e
        return server.render.reply_text(fromUser,toUser,int(time.time()),u'Unknow click'+key)

		


weixin_event_table = {
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
        	return weixin_event_table[event](self,fromUser,toUser,xml)
        except KeyError,e:
            print 'weixin_event_table:%s'%e
            return server.render.reply_text(fromUser,toUser,int(time.time()),u'�Ҳ����'+event)

        
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
	    


        