import query_schema
import json
import matplotlib.pyplot as plt
import time
import sys

def getBasicInformation():
    print("---------------------------------------------------------------------------")
    print("\033[1m" + "Found the following basic information:" + "\033[00m")
    auth = json.loads(q.getUserAuthenticationInfo())
    print("[" + "\033[92m" + "*" + "\033[00m" + "] " + "\033[1m" + "Username: " + "\033[00m" + auth["customerName"])
    print("[" + "\033[92m" + "*" + "\033[00m" + "] " + "\033[1m" + "User email: " + "\033[00m" + auth["customerEmail"])
    print("[" + "\033[92m" + "*" + "\033[00m" + "] " + "\033[1m" + "Has Prime Music: " + "\033[00m" + str(auth["canAccessPrimeMusicContent"]))
    print("[" + "\033[92m" + "*" + "\033[00m" + "] " + "\033[1m" + "User ID: " + "\033[00m" + auth["customerId"])
    print("---------------------------------------------------------------------------")

def getLists():
    print("---------------------------------------------------------------------------")
    print("\033[1m" + "All lists and items:" + "\033[00m")
    data = json.loads(q.getLists())
    for list in data['lists']:
        print("[" + "\033[92m" + "*" + "\033[00m" + "] " + "\033[1m" + "Name: " + "\033[00m" + str(list['name']))
        print("\033[35m" + ">>" + "\033[00m" +  "\033[1m" + "Archived: " + "\033[00m" + str(list['archived']))
        print("\033[35m" + ">>" + "\033[00m" +  "\033[1m" + "Type: " +  "\033[00m" +  list['type'])
        id = list['itemId']
        items = json.loads(q.getItemsFromList(id))['list']
        for item in items:
            print("\033[35m" + ">>>>>>>" + "\033[00m" + item['value'])
        print("\r")
    print("---------------------------------------------------------------------------")

def getMessagesAndContacts(data):
    print("---------------------------------------------------------------------------")
    print("\033[1m" + "Possible sent messages:"+ "\033[00m")
    for act in data:
        info = json.loads(q.getActivityCard(act['id']))
        gotContact = False
        gotMessage = False
        for item in info['activityDialogItems']:
            itemData = json.loads(item['activityItemData'])
            if 'slots' in itemData:
                for sl in itemData['slots']:
                    if sl.get('name') == "ContactName" and sl['value'] != None and not gotContact:
                        gotContact = True
                        print("[" + "\033[92m" + "*" + "\033[00m" + "] " + "\033[1m" + "Contact: "+ "\033[00m" + sl['value'])
                    if sl.get('name') == "MessageContent" and sl['value'] != None and not gotMessage:
                        gotMessage = True
                        print("\033[35m" + ">>>>>>>" + "\033[00m" + "\033[1m" + "Message: "+ "\033[00m" + sl['value'])
        print("\r")
    print("---------------------------------------------------------------------------")


def getBoughtItems(data):
    print("---------------------------------------------------------------------------")
    print("\033[1m" + "Possible purchased items:"+ "\033[00m")
    for act in data:
        info = json.loads(q.getActivityCard(act['id']))
        intents = ["AddToShoppingContainerIntent", "BuyItemIntent", "SearchItemIntent"]
        intent = json.loads(info['activityDialogItems'][1]['activityItemData']).get('intentType')
        if intent in intents:
            for item in info['activityDialogItems']:
                itemData = json.loads(item['activityItemData'])
                t = itemData.get('asrText')
                if t != "" and t != "sí" and t != "no":
                    print("[" + "\033[92m" + "*" + "\033[00m" + "] " + "\033[1m" + "Item: "+ "\033[00m" + t)
    print("---------------------------------------------------------------------------")

def plotActivityByHours(data):
    x = [i for i in range(24)]
    y = data
    plt.figure(1)
    plt.plot(x,y)
    plt.xticks(x)
    plt.ion()
    plt.show()
    plt.pause(0.001)

def plotActivityByWeekdays(data):
    x = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    y = data
    plt.figure(2)
    plt.plot(x,y)
    plt.xticks(x)
    plt.ion()
    plt.show()
    plt.pause(0.001)


def extractHoseholdAccountsInfo():
    print("---------------------------------------------------------------------------")
    print("\033[1m" + "External accounts and calendars:" + "\033[00m")
    data = json.loads(q.getHouseholdAccounts())
    for acc in data['householdAccountList']:
        print("[" + "\033[92m" + "*" + "\033[00m" + "] " + "\033[1m" + "Name: " + "\033[00m" + acc['customerName'])
        if acc['getCalendarAccountsResponse'] != None:
            for i in acc['getCalendarAccountsResponse']['calendarAccountList']:
                print("\033[35m" + ">>>" + "\033[00m" + "[" + "\033[92m" + "*" + "\033[00m" + "] " + "\033[32m" + "Found e-mail: " + "\033[00m" + i['emailId'])
                for cal in i['calendarList']:
                    print("\033[35m" + "-------->" + "\033[00m" + "\033[1m" + "Calendar name: " + "\033[00m" + cal['calendarName'])
                    print("\033[35m" + "----------->" + "\033[00m" + "\033[1m" + "ID: " + "\033[00m"  + cal['calendarId'])
                print("\r")
        else:
            print("\033[31m" + "No more data for this account" + "\033[00m")
        print("\r")
    print("---------------------------------------------------------------------------")

def extractHoseholdInfo():
    print("---------------------------------------------------------------------------")
    print("\033[1m" + "Hosehold:" + "\033[00m")
    data = json.loads(q.getHousehold())
    for usr in data['accounts']:
        print("[" + "\033[92m" + "*" + "\033[00m" + "] " + "\033[1m" + "Name: " + "\033[00m" + usr['fullName'] + "\033[1m" + " Email " + "\033[00m" + usr['email'] + "\033[1m" + " Role: " + "\033[00m" + usr['role'])
    print("---------------------------------------------------------------------------")

def getAllHistory():
    all_act = {'activities': []}
    acts = []
    end = str(round(time.time() * 1000))
    start = "1546297199000"
    h = json.loads(q.getActivities(start, end))
    last = False
    loading = ["_","o","O"]
    i = 0
    while not last:
        sys.stdout.write("[" + "\033[96m" + loading[i%3] + "\033[00m" +  "]" + "\033[1m" +" Getting all actions in history...\r" + "\033[00m")
        h = json.loads(q.getActivities(start, end))
        if end == h['startDate']:
            last = True
        else:
            end = h['startDate']
            acts.append(h['activities'])
        sys.stdout.flush()
        i+=1
    print("[" + "\033[92m" + "*" + "\033[00m" +  "]" + "\033[1m" +" Getting all actions in history...\r" + "\033[00m")
    all_act['activities'] = acts
    return all_act

def extractInfoFromHistory():
    data = getAllHistory()
    hours = [0 for i in range(24)]
    days = [0 for i in range(7)]
    messages = []
    compras = []
    for act_list in data['activities']:
        for act in act_list:
            t = time.localtime(int(act["creationTimestamp"])/1000)
            h = t.tm_hour
            hours[h] += 1
            d = t.tm_wday
            days[d] += 1
            if act['description'] != None:
                desc = json.loads(act['description'])
                if desc['summary'] != None:
                    if "envía un mensaje" in desc['summary']:
                        messages.append(act)
                    elif "compra" in str(desc['summary']) or "cesta" in str(desc['summary']):
                        compras.append(act)
    result = {}
    result['hours'] = hours
    result['days'] = days
    result['messages'] = messages
    result['compras'] = compras
    return result

def createReminder():
    print("---------------------------------------------------------------------------")
    print("\033[1m" + "Create a reminder:" + "\033[00m")
    wakeup = json.loads(q.getWakeUpWord())['wakeWords']
    if wakeup == []:
        print("\033[31m" + "Device currently not connected" + "\033[00m")
    else:
        current_ww = wakeup[0]['wakeWord']
        if current_ww=="ECHO":
            current_ww = "Echo"
        elif current_ww=="ALEXA":
            current_ww = "Alexa"
        else:
            current_ww = "Amazon"
        print("\033[34m" + "==>"  + "\033[00m" + "\033[1m" + "Which wake word do you want to use? Current: " + current_ww + "\033[00m")
        print("\033[1m" + "[1] ALEXA  || [2] AMAZON || [3] ECHO" + "\033[00m")
        w = input()
        r = ""
        if w==str(1):
            r = q.setWakeWord("ALEXA", serial, type, current_ww)
        elif w==str(2):
            r = q.setWakeWord("AMAZON", serial, type, current_ww)
        else:
            r = q.setWakeWord("ECHO", serial, type, current_ww)
        if r.status_code != 200:
            print("\033[31m" + "Something went wrong" + "\033[00m")
        else:
            print("\033[32m" + "Wakeword set successfully." + "\033[00m")
            print("\033[34m" + "==>"  + "\033[00m" + "\033[1m" + "What do you want to be \"remembered\"? ;)" + "\033[00m")
            reminder = input()
            reminder = current_ww + ", " + reminder
            print("\033[34m" + "==>"  + "\033[00m" + "\033[1m" + "At what time do you want to schedule it? - (from 00:00 to 24:00)" + "\033[00m")
            time = input()
            print("\033[34m" + "==>"  + "\033[00m" + "\033[1m" + "What day? - (from 01 to 31)" + "\033[00m")
            day = input()
            print("\033[34m" + "==>"  + "\033[00m" + "\033[1m" + "What month? - (from 01 to 12)" + "\033[00m")
            month = input()
            code = q.createReminder(time, day, month, reminder, serial, type)
            if code.status_code == 200:
                print("\033[32m" + "Reminder created!" + "\033[00m")
            else:
                print("\033[31m" + "Something went wrong" + "\033[00m")
        print("---------------------------------------------------------------------------")

def getLocation():
    print("---------------------------------------------------------------------------")
    print("\033[1m" + "Location:" + "\033[00m")
    device_preferences = json.loads(q.getDevicePreferences())
    for device in device_preferences['devicePreferences']:
        print("[" + "\033[92m" + "*" + "\033[00m" + "] " + "\033[1m" + "Device found: " + "\033[00m")
        if device['deviceSerialNumber'] != None:
            print("\033[35m" + ">>" + "\033[00m" + "\033[1m" + "Serial Number: " + "\033[00m" + device['deviceSerialNumber'])
        if device['deviceType'] != None:
            print("\033[35m" + ">>" + "\033[00m" + "\033[1m" + "Device type: " + "\033[00m" + device['deviceType'])
        if device['postalCode'] != None:
            print("\033[35m" + ">>" + "\033[00m" + "\033[1m" + "Postal code: " + "\033[00m" + str(device['postalCode']))
        for key in device['deviceAddressModel'].keys():
            v = device['deviceAddressModel'][key]
            if v != None:
                print("\033[35m" + ">>" + "\033[00m" + "\033[1m" + key +": " + "\033[00m" + v)
        print("\r")
    print("---------------------------------------------------------------------------")

def usage():
    print("------------------------------------------")
    print("USAGE: python3 PATH_TO_COOKIES.SQLITE_FILE")
    print("------------------------------------------")

def main(argv):
    global serial
    global type
    global q

    if len(argv) != 2:
        usage()
        return

    print("""\
     \033[94m$$$$$$\  $$\                                                                  $$\       $$\                 $$\ \r
    $$  __$$\ $$ |                                                                 $$ |      \__|                $$ |
    $$ /  $$ |$$ | $$$$$$\  $$\   $$\ $$$$$$\         $$$$$$$\  $$$$$$\   $$$$$$\  $$ |  $$\ $$\  $$$$$$\   $$$$$$$ |
    $$$$$$$$ |$$ |$$  __$$\ \$$\ $$  |\____$$\       $$  _____|$$  __$$\ $$  __$$\ $$ | $$  |$$ |$$  __$$\ $$  __$$ |
    $$  __$$ |$$ |$$$$$$$$ | \$$$$  / $$$$$$$ |      $$ /      $$ /  $$ |$$ /  $$ |$$$$$$  / $$ |$$$$$$$$ |$$ /  $$ |
    $$ |  $$ |$$ |$$   ____| $$  $$< $$  __$$ |      $$ |      $$ |  $$ |$$ |  $$ |$$  _$$<  $$ |$$   ____|$$ |  $$ |
    $$ |  $$ |$$ |\$$$$$$$\ $$  /\$$\\$$$$$$$ |      \$$$$$$$\ \$$$$$$  |\$$$$$$  |$$ | \$$\ $$ |\$$$$$$$\ \$$$$$$$ |
    \__|  \__|\__| \_______|\__/  \__|\_______|       \_______| \______/  \______/ \__|  \__|\__| \_______| \_______| \033[00m

    """)

    extracted_data = ""
    q = query_schema.Query(argv[1])
    dev = json.loads(q.getDevices())['devices'][0]
    print("---------------------------------------------------------------------------")
    print("[" + "\033[92m" + "*" + "\033[00m" + "] " + "\033[1m" + "ACCOUNT NAME: " + "\033[00m" + dev['accountName'])
    serial = dev['serialNumber']
    type = dev['deviceType']

    c = True
    while(c):

        print("--------------------------------")
        print("\033[1m" + "What do you want to see?" + "\033[00m")
        print("[1] Basic user information")
        print("[2] Hosehold")
        print("[3] Additional e-mails and calendars")
        print("[4] Location")
        print("[5] Lists")
        print("[6] Contacts and messages")
        print("[7] Bought items")
        print("[8] Plot activity diagram")
        print("[9] Create Reminder")
        print("[10] Print all the information")
        print("--------------------------------")


        action = input()
        if (action=='1'):
            getBasicInformation()
        elif (action=='2'):
            extractHoseholdInfo()
        elif (action=='3'):
            extractHoseholdAccountsInfo()
        elif (action=='4'):
            getLocation()
        elif (action=='5'):
            getLists()
        elif (action=='6'):
            if extracted_data == "":
                extracted_data = extractInfoFromHistory()
            getMessagesAndContacts(extracted_data['messages'])
        elif (action=='7'):
            if extracted_data == "":
                extracted_data = extractInfoFromHistory()
            getBoughtItems(extracted_data['compras'])
        elif (action=='8'):
            if extracted_data == "":
                extracted_data = extractInfoFromHistory()
            plotActivityByHours(extracted_data["hours"])
            plotActivityByWeekdays(extracted_data["days"])
            print("\033[32m" + "Plots done" + "\033[00m \r")
        elif (action=='9'):
            createReminder()
        elif (action=='10'):
            getBasicInformation()
            extractHoseholdInfo()
            extractHoseholdAccountsInfo()
            getLocation()
            getLists()
            if extracted_data == "":
                extracted_data = extractInfoFromHistory()
            getMessagesAndContacts(extracted_data['messages'])
            getBoughtItems(extracted_data['compras'])
            plotActivityByHours(extracted_data["hours"])
            plotActivityByWeekdays(extracted_data["days"])
        else:
            print("Incorrect number")

        more = input("Another action? [y/n]")
        if (more =='y'):
             c = True
        else:
             c = False


q = ""
serial = ""
type = ""
main(sys.argv)
