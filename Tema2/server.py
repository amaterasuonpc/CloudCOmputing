import http.server
from socketserver import ThreadingMixIn
import urllib
import requests
import time
import json
import cgi
PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler
import main

def processGet(s,path,request):
   # print(request)
    #print(path)
    if request=={}:
        print("No Parameters")
    paths=path.split('/')
    path=paths[1]
   # print(len(paths))
    if path=="Shows":
        if len(paths)==2:
            s.send_response(200)
            s.send_header("Content-type", "text/html")
            s.end_headers()
            shows=main.getShowsNames()
            response=json.dumps(shows)
            print(response)
            s.wfile.write(response.encode('UTF-8'))
        elif len(paths)==3:  # process different shows
            entry=paths[2]
            if entry.isdecimal():
                show=main.getshowinfo(entry)
                if len(show.items())==1:
                    s.send_response(404)
                    s.send_header("Content-type", "text/html")
                    s.end_headers()
                else:
                    s.send_response(200)
                    s.send_header("Content-type", "text/html")
                    s.end_headers()
                    response=json.dumps(show)
                    s.wfile.write(response.encode('UTF-8'))
            else:
                s.send_response(404)
                s.send_header("Content-type", "text/html")
                s.end_headers()
        elif len(paths)==4: #Actors
            entry = paths[2]
            if entry.isdecimal():
                actors=main.getActorsInfoFromShow(entry)
                if len(actors.items())==1:
                    s.send_response(404)
                    s.send_header("Content-type", "text/html")
                    s.end_headers()
                else:
                    s.send_response(200)
                    s.send_header("Content-type", "text/html")
                    s.end_headers()
                    response=json.dumps(actors)
                    s.wfile.write(response.encode('UTF-8'))
        elif len(paths)==5: #Specific actor of a show
            entry = paths[2]
            if entry.isdecimal():
                actors = main.getActorsInfoFromShow(entry)
                entry=paths[4]
                print(actors.keys())
                print("In specificactor from show")

                if entry.isdecimal() and len(actors.items())!=1:
                    try:
                        actor=actors[int(entry)]

                    except Exception:
                        s.send_response(404)
                        s.send_header("Content-type", "text/html")
                        s.end_headers()
                        print("in except")

                        return
                    s.send_response(200)
                    s.send_header("Content-type", "text/html")
                    s.end_headers()
                    response = json.dumps(actor)
                    s.wfile.write(response.encode('UTF-8'))
                else:
                    s.send_response(404)
                    s.send_header("Content-type", "text/html")
                    s.end_headers()
        else:
            s.send_response(404)
            s.send_header("Content-type", "text/html")
            s.end_headers()
    elif path=="Actors":
        if len(paths)==2:
            actors=main.getActors()
            s.send_response(200)
            s.send_header("Content-type", "text/html")
            s.end_headers()
            response = json.dumps(actors)
            s.wfile.write(response.encode('UTF-8'))
        elif len(paths)==3:
            entry = paths[2]
            if entry.isdecimal():
                actor=main.getActorInfo(entry)
                if len(actor.items())==1:
                    s.send_response(404)
                    s.send_header("Content-type", "text/html")
                    s.end_headers()
                else:
                    s.send_response(200)
                    s.send_header("Content-type", "text/html")
                    s.end_headers()
                    response=json.dumps(actor)
                    s.wfile.write(response.encode('UTF-8'))
        else:
            s.send_response(404)
            s.send_header("Content-type", "text/html")
            s.end_headers()

    else:
        s.send_response(404)
        s.send_header("Content-type", "text/html")
        s.end_headers()


def processPOST(self,path,request):
    ctype, pdict = cgi.parse_header(self.headers['content-type'])
    if request=={}:
        print("No Parameters")
    paths=path.split('/')
    path=paths[1]

    if ctype == 'text/plain':
       # print(self.headers['content-length'])
        something = self.rfile.read(int(self.headers['content-length']))
        #print(something.decode())
        jsonfile = json.loads(something.decode())
        if path=="Shows":
            if len(paths)==2: #Shows
                try:
                    main.insertIntoShows(jsonfile)
                except:
                    self.send_response(409)
                    self.send_header("Content-type","text/html")
                    self.end_headers()
                    return
                self.send_response(201)
                self.send_header("Location","/Shows/{0}".format(jsonfile['ID']))
                self.end_headers()
            if len(paths)==3: #specific show
                if paths[2]!=jsonfile['ID']:
                    self.send_response(404)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    return

                try:
                    main.insertIntoShows(jsonfile)
                except:
                    self.send_response(409)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    return
                self.send_response(201)
                self.send_header("Location", "/Shows/{0}".format(jsonfile['ID']))
                self.end_headers()
            if len(paths)==4: # add Actors
                show=paths[2]
                print("addActorstoShow")
                try:
                    main.addActorstoShow(jsonfile,show)
                except (Exception) as e:
                    print(e)
                    self.send_response(409)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    return
                self.send_response(201)
                self.send_header("Location", "/Shows/{0}/Actors".format(paths[2]))
                self.end_headers()
                pass
        elif path=="Actors": # for all Actors
            print(jsonfile)
            print("In actors POST")
            try:
                main.insertIntoActors(jsonfile)
            except (Exception) as e :
                print(e)
                self.send_response(409)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                return
            self.send_response(201)
            self.send_header("Location", "/Actors/{0}".format(jsonfile['ID']))
            self.end_headers()
    else:
        self.send_response(404)





def processPUT(self,path,request):
    ctype, pdict = cgi.parse_header(self.headers['content-type'])
    if request == {}:
        print("No Parameters")
    paths = path.split('/')
    path = paths[1]

    if ctype == 'text/plain':
        # print(self.headers['content-length'])
        something = self.rfile.read(int(self.headers['content-length']))
        jsonfile = json.loads(something.decode())
        print(jsonfile)
        if path == "Shows":
            if len(paths) == 2:  # Shows

                self.send_response(405)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                return

            if len(paths) == 3:  # specific show
                print("In specific show")
                if int(paths[2]) != jsonfile['ID']:
                    self.send_response(404)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    return
                try:
                    main.updateShowInfo(jsonfile)
                except:
                    self.send_response(409)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    return
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
            if len(paths) == 4:  # add Actors
                pass
        elif path == "Actors":  # for all Actors
            print(jsonfile)
            if len(paths) == 2:

                self.send_response(405)
                self.send_header("Location", "/Actors/{0}".format(jsonfile['ID']))
                self.end_headers()
            elif len(paths)==3: #specific actor
               # print("In PUT actors/{ID}")
                print(type(jsonfile['ID']),type(paths[2]))
                if jsonfile['ID']!=int(paths[2]):
                    self.send_response(404)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()

                try:
                    main.updateActorInfo(jsonfile)
                except (Exception) as e:
                    print(e)
                    self.send_response(404)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    return
                self.send_response(200)
                self.send_header("Location", "/Actors/{0}".format(jsonfile['ID']))
                self.end_headers()
    else:
        self.send_response(404)




def processDELETE(self,path,request):
    ctype, pdict = cgi.parse_header(self.headers['content-type'])
    if request == {}:
        print("No Parameters")
    paths = path.split('/')
    path = paths[1]

    if ctype == 'text/plain':
        # print(self.headers['content-length'])
        something = self.rfile.read(int(self.headers['content-length']))
        jsonfile = json.loads(something.decode())
        print(jsonfile)
        if path == "Shows":
            if len(paths) == 2:  # Shows
                self.send_response(405)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                return

            if len(paths) == 3:  # specific show
                print("In specific show DELETE")
                if int(paths[2]) != jsonfile['ID']:
                    self.send_response(404)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    return
                try:
                    main.deleteShow(jsonfile)
                except (Exception) as e:
                    print(e)
                    self.send_response(404)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    return
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
            if len(paths) == 4:  # add Actors
                pass
        elif path == "Actors":  # for all Actors
            print(jsonfile)
            if len(paths) == 2:

                self.send_response(405)
                self.send_header("Content-type", "text/html")
                self.end_headers()
            elif len(paths) == 3:  # specific actor

                if jsonfile['ID'] != int(paths[2]):
                    self.send_response(404)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                try:
                    main.deleteActor(jsonfile)
                except (Exception) as e:
                    print(e)
                    self.send_response(404)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    return
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
    else:
        self.send_response(404)


class MyHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        """Respond to a GET request."""
        #s.send_response(200)
        #s.send_header("Content-type", "text/html")
        #s.end_headers()
        temp = urllib.parse.parse_qs(s.path)

        processGet(s,s.path,temp)
    def do_POST(self):
        temp = urllib.parse.parse_qs(self.path)
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        processPOST(self,self.path,temp)
    def do_PUT(self):
        temp = urllib.parse.parse_qs(self.path)
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        processPUT(self,self.path,temp)

    def do_DELETE(self):
        temp = urllib.parse.parse_qs(self.path)
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        processDELETE(self,self.path,temp)




class ThreadingSimpleServer(ThreadingMixIn, http.server.HTTPServer):
    pass

def start():
    server_class=ThreadingSimpleServer
    with server_class(("", PORT), MyHandler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
start()