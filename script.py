import threading
from _thread import *
import requests
import time
def sendrequests(number):
    print(number)
    response=requests.get("http://localhost:8080/index.html?something=STEAMAPI&SCRIPT=ok&ID=76561198084686055")
    print(response.json())
    print("I am done :" + str(number))

def multithreaded():
    for j in range(3):
        for i in range(25):
            threading.Thread(target=sendrequests,args=(i,)).start()
        time.sleep(1)
sendrequests(1)
#multithreaded()