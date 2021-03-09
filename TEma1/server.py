import http.server
from socketserver import ThreadingMixIn
import urllib
import requests
import time
import json
PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler
steamapi=open("config.txt",'r').read()
some=76561198057225905
id2=76561198178391634
id3=76561197998387359
id4=76561198084686055
id5=61049916
openapiid=124420327
opendotaapi=1051246927

def actions(type,ID):
    imageurl=0
    c = time.time()
    if type==1 and ID!='0':

        response = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002",
                                params={"key": steamapi, "steamids": ID})
        delay=time.time()-c
        logging(" STEAMPAPI response time: "+ str(delay))
        print(response.json()['response'])
        return response.json()['response']
    if type==2 and ID!=0:
        response = requests.get("https://api.opendota.com/api/players/"+ ID[0])
        delay = time.time() - c
        logging(" DOTAAPI response time: " + str(delay))
        print(response.json())
        return response.json()


class MyHandler(http.server.BaseHTTPRequestHandler):
     def do_HEAD(s):
         s.send_response(200)
         s.send_header("Content-type", "text/html")
         s.end_headers()
     def do_GET(s):
         """Respond to a GET request."""
         s.send_response(200)
         s.send_header("Content-type", "text/html")
         s.end_headers()
         script=['1']
         id='0'
         type='0'
         temp=urllib.parse.parse_qs(s.path)
         if temp!={}:
             script = temp[list(temp)[1]]
             type=temp[list(temp)[0]]
         c=time.time()
         for i in list(temp)[0:1]:
             type=temp[i]

         #print(script)
         for i in temp:
             id=temp[i]
         #print(id)
         #print(type)

         if script[0]=='ok':
             forscript(s,id,type,c)
         else:
             forinterface(s,id,type,c)

def forscript(s,id,type,c):

     if id!='0':
        if type[0]=='STEAMAPI':
            response=actions(1,id)
            avatar = response['players'][0]['avatarfull']
            name=response['players'][0]['personaname']
        elif type[0]=='DOTAAPI':

            response = actions(2, id)
            avatar=response["profile"]['avatarfull']
            name=response['profile']['personaname']
        title = sendrequests2(avatar)
        if title:
            pass
        jsonresponse = json.dumps([avatar, name, title])
        s.wfile.write(jsonresponse.encode('utf-8'))
        delay = time.time() - c
        locallogging( "Request: " + type[0] + " LocalAPI response time:" + str(delay) + " Server response: " + avatar + "\n Avatar's source : " + title + '\n')
def forinterface(s,id,type,c):
    response=''
    title=''
    avatar=' '
    name=''

    if id != '0':
        if type[0] == 'STEAMAPI':
            response = actions(1, id)
            try:
                avatar = response['players'][0]['avatarfull']
                name = response['players'][0]['personaname']
            except:
                pass
        elif type[0] == 'DOTAAPI':

            response = actions(2, id)
            try:
                avatar = response["profile"]['avatarfull']
                name = response['profile']['personaname']
            except:
                pass
        title = sendrequests2(avatar)

    img = "<br>Profile Avatar:<br><img src=\"" + avatar + "\" width=\"200\" height=\"200\"> "
    s.wfile.write(b"<html><head><title>Title goes here.</title></head>")
    s.wfile.write(bytes(open("index.html").read(), 'utf-8'), )
    #s.wfile.write(bytes(str(response), 'UTF-8'))
    s.wfile.write(bytes(img, 'utf-8'))
    s.wfile.write(bytes("<br> Avatar from :" + title, 'utf-8'))
    s.wfile.write(b"</body></html>")
    delay=time.time()-c
    if name!='':
        locallogging("Request: " + type[0] + " LocalAPI response time:" + str(delay) + " Server response: " + avatar + "\n Avatar's source : " + title)


class ThreadingSimpleServer(ThreadingMixIn, http.server.HTTPServer):
    pass

def start():
    server_class=ThreadingSimpleServer
    with server_class(("", PORT), MyHandler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

def sendrequests2(avatar):
    c = time.time()
    response=requests.get("https://trace.moe/api/search",params={"url": avatar})
    delay = time.time() - c
    logging("Trace API response time:" + str(delay) )
    print(response.status_code)
    if response.status_code!=200:
        return " "
    print(response.json())
    if response.json()["docs"][0]['title_english']!=None:
        return response.json()["docs"][0]['title_english']
    else:
        return response.json()["docs"][0]['anime']


def logging(text):
    webserviceslogs=open("webservice.txt",'a')
    webserviceslogs.write(time.asctime())
    webserviceslogs.write(text + '\n')
    webserviceslogs.close()

def locallogging(text):
    local=open("localservice.txt",'a')
    local.write(time.asctime())
    local.write(text +'\n')
    local.close()
def testing():
    c=time.asctime()
    print(c)

#sendrequests3()
#sendrequests()
#sendrequests2("https://cdn.akamai.steamstatic.com/steamcommunity/public/images/avatars/b9/b9f5187b1355cfccdc4352a431de9d45e3c80cc9_full.jpg")
start()
