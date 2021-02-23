import threading
from _thread import *
import requests
import time

count=0
def sendrequests(number):
    print(number)
    c=time.time()
    response=requests.get("http://localhost:8080/index.html?something=STEAMAPI&SCRIPT=ok&ID=76561198084686055")
    delay=time.time()-c
    global count
    count+=delay
    print(response.json())
    print("I am done :" + str(number))


def multithreaded(batch,number):
    for j in range(int(batch)):
        for i in range(int(number)):
            threading.Thread(target=sendrequests,args=(i,)).start()
        time.sleep(1)
def start():
    batch=input('Batch')
    number=input('number')

    multithreaded(batch,number)
    time.sleep(15)
    global count
    avg=count/(int(batch)*int(number))
    print(avg)
#multithreaded()
start()