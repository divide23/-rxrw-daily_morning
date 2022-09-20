from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

tianqi_url='https://www.yiketianqi.com/free/day?appid=72772742&appsecret=SaL5fYwf&unescape=1&city=石家庄'
def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def qinghua():
    url='http://api.tianapi.com/saylove/index?key=eea0ccd28340872c39f8f0fad8a79e61'
    res = requests.get(url).json()
    return res['newslist'][0]['content']
def tianqi():
    url = 'https://www.yiketianqi.com/free/day?appid=72772742&appsecret=SaL5fYwf&unescape=1&city=石家庄'
    res=requests.get(url).json()
    return res['date'], res['week']
    #return res['city'],res['date'],res['week'],res['wea'],res['tem_day'],res['tem_night'],res['win'],res['win_speed'],res['air'],res['humidity']
def moji():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + '石家庄'
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['city'],weather['weather'],math.floor(weather['temp']),math.floor(weather['high']),math.floor(weather['low']),weather['wind'],weather['airQuality']
def get_random_color():#随机颜色
    return "#%06x" % random.randint(0, 0xFFFFFF)
def one_day():#每日一句
    url='https://open.iciba.com/dsapi/?date='+str(time.strftime('%Y-%m-%d'))
    res = requests.get(url).json()
    return res['note'],res['content']
def zaoan():#早安
    url='http://api.tianapi.com/zaoan/index?key=eea0ccd28340872c39f8f0fad8a79e61'
    res = requests.get(url).json()
    return res['newslist'][0]['content']
if __name__ == '__main__':
    #time.gmtime()
    print(zaoan())
    a,b=tianqi()
    print(a,b)
    print('城市:',moji()[0])
    print('天气:',moji()[1])
    print('温度:',str(moji()[4])+'\\'+str(moji()[3]),'当前温度'+str(moji()[2]))
    print('风向:',moji()[5])
    print('空气质量:',moji()[6])
    print(one_day()[0]+'\n'+one_day()[1])

    client = WeChatClient(app_id, app_secret)
    wm = WeChatMessage(client)
    #wea, temperature = get_weather()
    data= {"date":{"value": a, "color": get_random_color()},"date1":{"value": b,"color": get_random_color()},
           "weather":{"value": moji()[1], "color": get_random_color()},"temperature":{"value": moji()[2], "color": get_random_color()},
           "lowest":{"value": moji()[4], "color": get_random_color()},"highest":{"value": moji()[3], "color": get_random_color()},
           "qinghua":{"value": qinghua(), "color": get_random_color()},"one":{"value": one_day()[0], "color": get_random_color()},
           "one1":{"value": one_day()[1], "color": get_random_color()},"love_days":{"value": get_count(), "color": get_random_color()},
           "birthday_left":{"value": get_birthday(), "color": get_random_color()}}
    res = wm.send_template(user_id, template_id, data)
    print(res)
