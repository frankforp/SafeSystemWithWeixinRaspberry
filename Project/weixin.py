# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree

    
#my_appid = '你的appid' #填写你的appid
#my_secret = '你的app secret' #填写你的app secret
#my_yeekey = '你的yeekey'#填写你的 yeekey


 
def _check_hash(data):
    signature=data.signature
    timestamp=data.timestamp
    nonce=data.nonce
    #自己的token
    token="wangxu" #这里改写你在微信公众平台里输入的token
    #字典序排序
    list=[token,timestamp,nonce]
    list.sort()
    sha1=hashlib.sha1()
    map(sha1.update,list)
    hashcode=sha1.hexdigest()
    #sha1加密算法        
 
    #如果是来自微信的请求，则回复echostr
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
	return server.render.reply_text(fromUser, toUser,int(time.time()), u'欢迎关注此微信号，具体功能请点击下方菜单')

def handle_event_unsubscribe(server, fromUser, toUser, xml):
	return server.render.reply_text(fromUser, toUser,int(time.time()), u'我还不想离开你')

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
        return self.render.reply_text(fromUser, toUser,int(time.time()), u'我还不能理解你说的话:' + reply_msg)
        
    def weixin_receive_event(self, fromUser, toUser, xml):
        event = xml.find('Event').text
		try:
			return weixin_even_table[event](self, fromUser, toUser, xml)
        except:
			return self.render.reply_text(fromUser, toUser,int(time.time()), u'我还不能理解你说的话:' + event)

    def GET(self):
        data = web.input()
        if	_check_hash(data):
            return	data.echostr      

    def	POST(self):        
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text

        if msgType == 'text':
            return self.weixin_receive_text(fromUser, toUser, xml)
        
        elif msgType == 'event':
            return self.weixin_receive_event(fromUser, toUser, xml)
	    


        