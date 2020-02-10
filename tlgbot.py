#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import random
import time
import json
import urllib
import webbrowser
import io

token = '723294153:AAFKnUAet5yQVMEeXV9E9F4vJzPm91lZLlM'
url = 'https://api.telegram.org/bot'
gifKeywords = ['kielbasa', 'колбас', 'кильбас', 'сосис', 'sausage', 'hot dog', 'dodger', 'hotdog', 'хот дог', 'хотдог', 'хот-дог', 'френч-дог', 'френч дог']
recipeKeywords = ['рецепт', 'recipe', 'приготови', 'кулинар', 'cook']

class FoursquareCall:
    def __init__(self, location):
        self.location = location
        self.public = '3SJJZ1S5BBXYCSTPPRV2SQXB2VGOVFPRJMNTYFFWVNZX3BTU'
        self.url = 'https://api.foursquare.com/v2/search/recommendations'
        
    def call(self):
        places=[]
        rad = 1000
        while not places:
            self.params = dict(
                          client_id = self.public,
                          client_secret = 'ADXHOUL2F3X05MJAHMOZUXH2R0FHBJWQSYSPRZYKEUEMZFRY',
                          radius = str(rad),
                          v='20180323',
                          ll = self.location,
                          query='колбаски',
                          limit = 10
                        )
            call = requests.get(url=self.url, params=self.params)
            update = call.json()
            venues = update.get('response').get('group').get('results')
            if venues:
                for venue in venues:    
                    places.append(venue.get('venue').get('id'))
            rad +=1000
            print(places)
        return places
    
class KielbasaBot:
    def __init__(self, ready, token):
        self.ready = False
        self.token = token
        file = open('update_id.txt','r')
        self.offset = int(file.readline())
        file.close()
    
    def update(self):
        call = requests.get('https://api.telegram.org/bot723294153:AAFKnUAet5yQVMEeXV9E9F4vJzPm91lZLlM/getUpdates?offset='+str(self.offset))
        call = call.text.replace('true', 'True')
        call = call.replace('false', 'False')
        update = dict(eval(call)).get('result')
        if update:
            self.offset = int(update[-1].get('update_id'))+1
            file = open('update_id.txt','w')
            file.write(str(self.offset))
            file.close()
            print(update)
        return update
            
    def checkForEvents(self, update):
        for event in update:
            if 'photo' in event.get('message'):
                file_id = event.get('message').get('photo')[-1].get('file_id')
                call = requests.get('https://api.telegram.org/bot723294153:AAFKnUAet5yQVMEeXV9E9F4vJzPm91lZLlM/getFile?file_id='+file_id)
                get = call.json()
                img_url = 'https://api.telegram.org/file/bot723294153:AAFKnUAet5yQVMEeXV9E9F4vJzPm91lZLlM/'+get.get('result').get('file_path')
                image = requests.get(img_url)
                filePath = '/Users/iushkov.a/Desktop/Websocket stuff/file.jpg'
                with open(filePath, 'wb') as f:
                    f.write(image.content)
                searchUrl = 'http://www.google.com/searchbyimage/upload'
                search = requests.post(searchUrl, files={'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''},allow_redirects=False)
                fetchUrl = search.headers['Location']
                head = {
    'accept-language': 'en-US;q=0.8,en;q=0.7',
    'cookie': 'SEARCH_SAMESITE=CgQI1o0B; ANID=AHWqTUk-XCw0Ql59SxTRs2SHI0kcfabDdtS001r1A1jnTZ_xFF6J_54Sx1Y9G2oi; OTZ=5270909_44_44_123780_40_436260; S=billing-ui-v3=Fkq9bjm1wWBPH2UnJ4VjRuHfOCgMDI1O:billing-ui-v3-efe=Fkq9bjm1wWBPH2UnJ4VjRuHfOCgMDI1O; SID=tAcFfTSwY-nSpZvjK7Mt-QBpHrJxtyBH2Z4jVcb3Eg4d9jfvt2xXK5f5UaWLkJjZ89WRXQ.; __Secure-3PSID=tAcFfTSwY-nSpZvjK7Mt-QBpHrJxtyBH2Z4jVcb3Eg4d9jfv4D_DasuiqIwXZSJ5qQ9BRw.; HSID=Av_NpBb0Nkq3EflJ7; SSID=AJWECK-vRFbYiPFu8; APISID=xpFtFPKS3K2q6JTp/A11gexjFsQovDbstc; SAPISID=m2rKibYVBapKhzT_/AiZleEE0dUJTLFuTx; __Secure-HSID=Av_NpBb0Nkq3EflJ7; __Secure-SSID=AJWECK-vRFbYiPFu8; __Secure-APISID=xpFtFPKS3K2q6JTp/A11gexjFsQovDbstc; __Secure-3PAPISID=m2rKibYVBapKhzT_/AiZleEE0dUJTLFuTx; NID=196=NsBYtJGfqayUM3dIwXvWSUQOcOM68nwYm2AbI4bJQCPlLfyWWoRB3fr6WfneF1Xckb6xlShI3Dc-H8JVudtZpMyOETwvibVqUnCqD19g-FaFcBZKR_YDZhKO54E3veHNi4Km5yOPYMFIejKFB7-Y_cvTMD6or9hYE8u8nwPaHShfkK72uSgjYBkXAjumOUpmgfqgbIWiWZ51v3lwpt79_7V22Qu2RiOj9c47GwQvIpqRsQ4j_aNnybNlKZA4aZVACO0RYHuafl_ZXsqvH6cmJO8oTB9yPn4aXughhTbbBw; 1P_JAR=2020-1-27-13; SIDCC=AN0-TYtvQ0rI7L1_3ENYH1WNeeeN0Kw8D2PN_on87viBO67CoPo9CsWied0g21xLykzZ9RR-TqT3',
    'referer': 'https://www.google.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
}
                getcall = requests.get(fetchUrl, headers=head)
                filePath = '/Users/iushkov.a/Desktop/Websocket stuff/file.html'
                with io.open(filePath, 'wb') as f:
                    f.write(getcall.content)

                with io.open(filePath, 'r', encoding='utf-8') as f:
                    for line in f:
                        if 'Possible related search:' in line: 
                            targetLine = 'Possible related search:'
                            newline = line[(line.find(targetLine))+80:(line.find(targetLine))+500]
                        if 'Запрос, который' in line:
                            targetLine = 'Запрос, который'
                            newline = line[(line.find(targetLine))+80:(line.find(targetLine))+500]
                result = newline[newline.find('>')+1:newline.find('<')].lower()
                print(result)
                for keyword in gifKeywords:
                    if keyword in result: 
                        kielbasabool = True
                        break
                    else: kielbasabool = False
                if kielbasabool: 
                    self.sendMessage(event, 'О да! Это изображение кильбасы!')
                else: self.sendMessage(event, 'Нет, это не кильбаса!')
                
            if 'location' in event.get('message'):
                self.sendMessage(event, 'Товарищ! Вот здесь подают колбаски!')
                self.sendMessage(event, 'https://ru.foursquare.com/v/'+self.getVenue(str(event.get('message').get('location').get('latitude'))+','+str(event.get('message').get('location').get('longitude'))))
                
            if 'text' in event.get('message'):
                print(event.get('message').get('from').get('username') + ': ' + event.get('message').get('text'))
                for keyword in gifKeywords:
                    if keyword in event.get('message').get('text').lower():
                        self.sendAnimation(event)
                for keyword in recipeKeywords:
                    if keyword in event.get('message').get('text').lower():
                        self.sendMessage(event, 'Ну, держи колбасный рецептик, дружок!')
                        self.sendMessage(event, self.getRecipe())
                        
            if 'new_chat_participant' in event.get('message'):
                if event.get('message').get('new_chat_participant').get('username') is 'KielbasaBot':
                    self.sendMessage(event, 'Доброе утро! Я Бот-колбасник! Попросите у меня колбасы или сосисок, и я вам заправлю!')
                    self.sendMessage(event, 'Ещё я могу делиться рецептами колбасных блюд! Просто попросите меня о рецепте!')
                    self.sendMessage(event, 'Если ты пришлёшь мне свою геолокацию, укажу тебе куда пойти отведать колбасок!')
                    self.sendMessage(event, 'А ещё я могу определять, что на картинках. Загрузи фоточку, и я скажу, кильбаса ли на ней.')
    
    def getRecipe(self):
        recipes = readFile('recipes.txt')
        targetRecipe = recipes[random.randint(0,len(recipes)-1)]
        return targetRecipe
    
    def getKielbasa(self):
        kielbasas = readFile('gifs.txt')
        targetKielbasa = kielbasas[random.randint(0,len(kielbasas)-1)]
        return targetKielbasa
    
    def getVenue(self, coords):
        forsquareCall = FoursquareCall(coords)
        venues = forsquareCall.call()
        targetVenue = venues[random.randint(0,len(venues)-1)]
        return targetVenue
    
    def getEndpoint(self, endpoint):
        self.endpoint = endpoint
        
    def buildSignature(self):
        self.url = url + self.token + self.endpoint
        
    def getChatId(self, event):
        chatId = str(event.get('message').get('chat').get('id'))
        return chatId
    
    def sendAnimation(self, event):
        self.getEndpoint('/sendAnimation')
        self.buildSignature()
        call = requests.post(self.url, data={'chat_id':self.getChatId(event),'animation':self.getKielbasa()})
        print(call.text)
    
    def sendMessage(self, event, text):
        self.getEndpoint('/sendMessage')
        self.buildSignature()
        call = requests.post(self.url, data={'chat_id':self.getChatId(event),'text':text})
        print(call.text)
        
def readFile(file):
    data = []
    openFile = open(file, 'r')
    for x in openFile: data.append(x[:-1])
    openFile.close()
    return data

if __name__ == '__main__':
    
    kielbasaBot = KielbasaBot(False, token)
    
    while True:
        try:
            time.sleep(1)
            kielbasaBot.checkForEvents(kielbasaBot.update())
        except (TypeError):
            print('TypeError exception occurred')
        


# In[ ]:





# In[ ]:




