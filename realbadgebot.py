import requests, os, config, time
from bs4 import BeautifulSoup

session = requests.Session()
session.cookies[".ROBLOSECURITY"] = config.cookie
session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"

def make_badge(placeid, groupid, name, description, decalid):
    response = session.get("https://www.roblox.com/build/upload")
    try:
        soup = BeautifulSoup(response.text, "lxml")
        veri = soup.find("input", {"name" : "__RequestVerificationToken"}).attrs["value"]
    except NameError:
        print(NameError)
        return False

    data = {
        '__RequestVerificationToken': veri,
        'assetTypeId': '21',
        'isOggUploadEnabled': 'True',
        'isTgaUploadEnabled': 'True',
        'groupId': f'{groupid}',
        'assetImageId': f'{decalid}',
        'expectedCost': f'{config.expectedCost}',
        'targetPlaceId': f'{placeid}',
        'UseGroupFunds': f'{config.UseGroupFunds}',
        'onVerificationPage': "False",
        "captchaEnabled": "True",
        'name': name,
        'description': description
    }
    try:
        response = session.post('https://www.roblox.com/build/doverifiedupload', data=data)
        soup = BeautifulSoup(response.text, 'html.parser')
        element = soup.find('div', id='upload-result')
        result = element.text.strip()
        print(result)
        if result == "No free badges left":
            return False
    except:
        print("error is making request")
        time.sleep(15)
        make_badge(placeid, groupid, name, decalid)
        

i = 0
badgedecals = config.badgedecals

for place in config.placeslist:
    for _ in range(5):
        decal = badgedecals[i]
        if i == len(badgedecals)-1:
            i = 0
        else:
            i += 1
        h = make_badge(place, config.groupid, config.name,config.description, decal)
        if h == False:
            break