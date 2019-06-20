import requests
import json
import sqlite3

class Query:

    def __init__(self, file):
        conn = sqlite3.connect(file)
        c = conn.cursor()
        self.cookie = {
            'session-id': None,
            'session-id-time': None,
            'ubid-acbes': None,
            'session-token': None,
            'x-acbes': None,
            'at-acbes': None,
            'sess-at-acbes': None,
            'sst-acbes': None,
            'csrf': None,
            'x-wl-uid': None,
        }
        for key in self.cookie.keys():
            query = "select value from moz_cookies where baseDomain=? and name=?;"
            c.execute(query, ("amazon.es",key))
            self.cookie[key] = c.fetchone()[0]

        self.headers = {
            'Host': 'alexa.amazon.es',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'https://alexa.amazon.es/spa/index.html',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'close',
            'Cookie': 'at-acbes=' + self.cookie['at-acbes']+ '; csrf=' + self.cookie['csrf']+ '; sess-at-acbes=' + self.cookie['sess-at-acbes']+ '; session-id=' + self.cookie['session-id']+ '; session-id-time=' + self.cookie['session-id-time']+ '; session-token=' + self.cookie['session-token']+ '; sst-acbes=' + self.cookie['sst-acbes']+ '; ubid-acbes=' + self.cookie['ubid-acbes']+ '; x-acbes=' + self.cookie['x-acbes']+ '; x-wl-uid=' + self.cookie['x-wl-uid'],
        }
        conn.close()

    #List all devices and some user information
    def getDevices(self):
        url = "https://alexa.amazon.es/api/devices-v2/device"
        r = requests.get(url, headers=self.headers, cookies=self.cookie)
        return r.text


    #History of actions done
    def getActivities(self, start, end):
        url = "https://alexa.amazon.es/api/activities-with-range"
        p = {'startTime': start, 'endTime': end, 'size': "50"}
        r = requests.get(url, headers=self.headers, cookies=self.cookie, params=p)
        return r.text

    def getActivityCard(self, id):
        url = "https://alexa.amazon.es/api/activity-dialog-items"
        r = requests.get(url, headers=self.headers, cookies=self.cookie, params={'activityKey': id})
        return r.text

    def getActivityInfo(self, id):
        url = "https://alexa.amazon.es/api/activities/" + id
        r = requests.get(url, headers=self.headers, cookies=self.cookie)
        return r.text

    #Email, name and customerID
    def getUserAuthenticationInfo(self):
        url = "https://alexa.amazon.es/api/authentication"
        r = requests.get(url, headers=self.headers, cookies=self.cookie)
        return r.text

    def getHomeCards(self):
        url = "https://alexa.amazon.es/api/cards"
        r = requests.get(url, headers=self.headers, cookies=self.cookie)
        return r.text

    def getDevicePreferences(self):
        url = "https://alexa.amazon.es/api/device-preferences"
        r = requests.get(url, headers=self.headers, cookies=self.cookie)
        return r.text

    def getUserMarketPlace(self):
        url = "https://alexa.amazon.es/api/get-customer-pfm"
        r = requests.get(url, headers=self.headers, cookies=self.cookie)
        return r.text

    def getHousehold(self):
        url = "https://alexa.amazon.es/api/household"
        r = requests.get(url, headers=self.headers, cookies=self.cookie)
        return r.text

    def getHouseholdAccounts(self):
        url = "https://alexa.amazon.es/api/eon/householdaccounts"
        r = requests.get(url, headers=self.headers, cookies=self.cookie)
        return r.text

    def getWakeUpWord(self):
        url = "https://alexa.amazon.es/api/wake-word"
        r = requests.get(url, headers=self.headers, cookies=self.cookie)
        return r.text

    def getGoogleCalendarToken(self):
        url = "https://alexa.amazon.es/api/external-auth/link-url?provider=Google&service=Eon"
        r = requests.get(url, headers=self.headers, cookies=self.cookie)
        return r.text

    def getLists(self):
        url = "https://alexa.amazon.es/api/namedLists"
        r = requests.get(url, headers=self.headers, cookies=self.cookie)
        return r.text

    def getItemsFromList(self, id):
        url = "https://alexa.amazon.es/api/namedLists/" + id+ "/items"
        r = requests.get(url, headers=self.headers, cookies=self.cookie)
        return r.text

    def getNotifications(self):
        url = "https://alexa.amazon.es/api/notifications"
        r = requests.get(url, headers=self.headers, cookies=self.cookie)
        return r.text

    def setWakeWord(self, word, serial, type, currentww):
        url = "https://alexa.amazon.es/api/wake-word/" + serial
        p = {"active":True,
            "deviceSerialNumber":serial,
            "deviceType":type,
            "midFieldState":None,
            "wakeWord":word,
            "displayName":currentww}
        h = self.headers
        h['Content-Type'] = 'application/json'
        h['csrf'] = '-1224666430'
        r = requests.put(url, headers=h, cookies=self.cookie, data=json.dumps(p))
        return r

    def createReminder(self, time, day, month, reminder, deviceSerialNumber, deviceType):
        url = "https://alexa.amazon.es/api/notifications/createReminder"
        custom_headers = self.headers
        custom_headers['Content-type'] = 'application/json'
        custom_headers['csrf'] = self.cookie['csrf']
        payload = {
            "type":"Reminder",
            "status":"ON",
            "alarmTime":1556979420000,
            "originalTime":time + ":00.000",
            "originalDate":"2019-" + month + "-" + day,
            "timeZoneId":None,
            "reminderIndex":None,
            "skillInfo":None,
            "sound":None,
            "deviceSerialNumber":deviceSerialNumber,
            "deviceType":deviceType,
            "recurringPattern":None,
            "reminderLabel":reminder,
            "isSaveInFlight":True,
            "id":"createReminder",
            "isRecurring":False,
            "createdDate":1556979236162
        }
        p = json.dumps(payload)
        r = requests.put(url, headers=custom_headers, cookies=self.cookie, data=p)
        return r


    def getAudioFromUtteranceId(self, id):
        url = "https://alexa.amazon.es/api/utterance/audio/data?id=" + id
        custom_headers = {
            'Host': 'alexa.amazon.es',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept': 'audio/webm, audio/ogg, audio/wav, audio/*; q=0.9, application/ogg; q=0.7, video/*;q=0.6,*/*;q=0.5',
            'Referer': 'https://alexa.amazon.es/spa/index.html',
            'Connection': 'close',
            'Range': 'bytes=0-',
            'Cookie': 'at-acbes=' + self.cookie['at-acbes']+ '; csrf=' + self.cookie['csrf'] + '; sess-at-acbes=' + self.cookie['sess-at-acbes']+ '; session-id=' + self.cookie['session-id']+ '; session-id-time=' + self.cookie['session-id-time']+ '; session-token=' + self.cookie['session-token']+ '; sst-acbes=' + self.cookie['sst-acbes']+ '; ubid-acbes=' + self.cookie['ubid-acbes']+ '; x-acbes=' + self.cookie['x-acbes']+ '; x-wl-uid=' + self.cookie['x-wl-uid'],
        }
        r = requests.get(url, headers=custom_headers, cookies=self.cookie, stream=True)
        f = open("out_audio.wav", "wb")
        f.write(r.content)
        f.close()
        return r
