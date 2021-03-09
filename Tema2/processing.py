import requests
import json
def testpost():
    url="http://localhost:8080"
    something={'foo':'somthing'}
    response=json.dumps(something)
    res=requests.post(url,data=response)
    print(res.text)

testpost()