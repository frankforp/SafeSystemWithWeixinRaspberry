#  -*- coding:utf-8 -*-

import urllib
import urllib2
import json
    

def yeelink_put_datapoints():
    url = 'http://api.yeelink.net/v1.0/device/347567/sensor/388291/datapoints'
    headers = {'U-ApiKey':'25ec08ace6bb4a84f8cbb60a821d42d0'}
    data={
  "timestamp":"2016-05-10T15:13:14",
  "value":12
}
    jdata = json.dumps(data)
    req = urllib2.Request(url,jdata,headers)
    response = urllib2.urlopen(req)       # 发送页面请求
    return response.read()                    # 获取服务器返回的页面信息
print yeelink_put_datapoints()
