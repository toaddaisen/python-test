# -*- coding: utf-8 -*-

"""Not Bugs !

 code is far away from bugs with the god animal protecting
 :佛主保佑,永无BUG！ by 蛤蟆


"""

#encoding=utf8  #编码
import os
import json
import urllib2
import urllib
import demjson


#基于百度地图API下的名称来解析地理位置信息
def getLatFromAddress(addr):
    #地址格式化
    addr=urllib.quote(addr)
    #print(type(addr))
    #百度API的访问URL
    #ak=TfSEOtYFtNRnoEUYwsqwl67Kq7GYZMPe  这个必须是有效的KEY，没有就需要去百度开发者平台申请。
    url2 = 'http://api.map.baidu.com/geocoder/v2/?address='+addr+'&output=json&pois=1&ak=TfSEOtYFtNRnoEUYwsqwl67Kq7GYZMPe'
    #
    req = urllib2.urlopen(url2)  # json格式的返回数据
    res = req.read().decode("utf-8")  # 将其他编码的字符串解码成unicode
    return json.loads(res)

#本函数或者百度的经纬度后，返回datav需要的呼吸层数据、飞线层数据格式。(lat:纬度，lng:经度)
def dictFormatReturnLatlng(addr):
    #获取百度API的经纬度
    str = getLatFromAddress(addr)
    """
    百度API返回格式
    {"status":0,"result":
      {  "location":
            {
              "lng":113.30764967515182,
              "lat":23.12004910207623
            },
         "precise":0,
         "confidence":12,
         "level":"城市"
      }
    }
    """
    #dictjson={}#声明一个字典
    #get()获取json里面的数据
    jsonResult = str.get('result')
    location = jsonResult.get('location')
    #经度-百度API，
    lng = location.get('lng')
    #纬度-百度API，
    lat = location.get('lat')
    #
    #呼吸层数据格式
    dict1 = {"lat": 23.130360497828082,"lng": 113.26100320235732,"value": 10,"type": 1}
    #飞线层数据格式
    dict2 = {"from":"113.3191755474854,23.255090955408278","to":"113.334265,23.157334"}
    #
    # 按格式组合新的值，更新呼吸层数据dict1的经纬度
    dict1['lng']=lng
    dict1['lat']=lat
    #更新飞线层数据dict2的“from”值
    dict2['from']=repr(lng)+","+repr(lat)
    #
    #返回
    return dict1,dict2

#文件操作函数
def fileWrite(strs,filename):
    f=open(filename,'a')
    f.write(strs)
    f.close()




if __name__ == '__main__':
    #定义门店的GPS位置，默认default的gps表示其他门店。
    dict_shops_gps ={
        "xx店2":"113.24695546576301,23.12937604358692",
        "xx店2":"113.26100320235732,23.130360497828082",
        "xx店3":"113.34505943922106,23.018467091030313",
        "xx店4":"113.30277295228619,23.21658147677828",
        "xx店5":"113.47330611064973,23.172410051540965",
        "xx店6":"113.37943874090762,23.198925950189885",
        "xx店7":"113.52257363237052,23.256272300342058",
        "店8":"116.21737220036687,23.254287288524624",
        "店9":"114.09021387291316,22.54371575307169",
        "10店":"113.58096421896627,22.24845636319041",
        "11店":"113.08990050943565,22.623981973194355",
        "12店":"121.46130252083329,31.234464485454479",
        "13店":"113.21249727039506,23.180851306520429",
        "default":"113.334265,23.157334"
            }
    

    dictjson2={ "from": "113.3191755474854,23.255090955408278", "to": "113.246,23.129"}

    #获取ERP系统实际用户与地址文件
    file_obj2 = open("org2.txt")
    #读取文件内容
    all_users_addrs = file_obj2.readlines()
    #逐行遍历文件内容
    #广东省广州市荔湾区芳村,xx店
    for users_addrs in all_users_addrs:
        #用,分割成2个部分
        users=users_addrs.replace("\n","").split(",")

        # 调用百度API的函数，返回经纬度。
        # 用地址users[0]做参数，
        # 返回二个值：均为dict格式
        #  第一返回值，呼吸层数据，格式：{"lat": 23.130360497828082,"lng": 113.26100320235732,"value": 10,"type": 1}
        #  第二返回值，飞线层数据，格式：{"from": "113.3191755474854,23.255090955408278", "to": "113.334265,23.157334"}
        # 返回GPS[23.256272300342058, 113.52257363237052]
        #
        dictdata1,dictdata2= dictFormatReturnLatlng(users[0])
        # 写入txt，该txt用于数据可视化的datav的浮点层
        fileWrite(json.dumps(dictdata1),"lat.txt")
        fileWrite(",\n","lat.txt")


        #获取默认的GPS值
        strto=dict_shops_gps['default']

        #如果是指定范围的门店，获取该门店的精准GPS值
        for(k,v) in dict_shops_gps.items():
            if k==users[1]:
                strto=v
        #组合飞线数据，更新loc12的to值。
        dictdata2["to"]=strto


        print users[0].decode('utf-8')
        print dictdata1
        #print shops[shopsname]
        print dictdata2
        #保存到txt
        fileWrite(json.dumps(dictdata2),"fei.txt")
        fileWrite(",\n","fei.txt")
    file_obj2.close()


