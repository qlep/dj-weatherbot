from itertools import chain
from django.shortcuts import render
from django.http import HttpResponse
import requests, json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

weatherappid = ""
botid = ""

message = ""
chatid = ""
city = ""
temp = ""

# send bot message
def sendBotMessage(chatid, message):
    url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&parse_mode=HTML&text={}'.format(botid, chatid, message)
    m = requests.post(url)
    #print(m.content)

# get weather update
def getWeather(units, city):
    city = city
    units = units
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units={}&appid={}'.format(city, units, weatherappid)

    response = requests.get(url)
    data = json.loads(response.text)

    print(data)

    return data
# get cat url
def getCatURL():
    url = 'https://api.thecatapi.com/v1/images/search'
    response = requests.get(url)
    data = json.loads(response.text)

    print(data)

    return data[0]['url']

# index webpage
def index(request):
    city = "Helsinki"
    weather = getWeather("metric", "Helsinki")
    temp = weather['main']['temp']
    responsestr = '<h1>{}</h1><p>ilmat meillä nyt: {}</p>'.format(city, temp)

    return HttpResponse(responsestr)

# tele webhook happens here
# REMEMBER set webook in tele: 
# curl -F "url=https://weatherboat.azurewebsites.net/bot/" https://api.telegram.org/bot382694174:AAHZeoMmAJQ6C5oLQfoNax11deTbSC2gKvA/setWebhook
@require_POST
def bot(request):
    jsondata = request.body
    data = json.loads(jsondata)

    print(data)

    if 'message' in data:
        chatid = data['message']['chat']['id']
        message = data['message']['text']

        try:
            temp = getWeather('metric', message)['main']['temp']
            sendBotMessage(chatid, 'Its {} degrees in {}'.format(temp, message))

        except:
            sendBotMessage(chatid, "nope")
            sendBotMessage(chatid, getCatURL())

    else:
        print("----traffic other than messages---------->")
        print(data)

    return HttpResponse(status = 200)