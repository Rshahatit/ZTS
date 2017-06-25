from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
from azure.storage.blob.models import BlobPermissions

import requests
import shutil
import http.client
import json
import time

# initialise blob service
block_blob_service = BlockBlobService(account_name='nikolas', account_key='b/qWJCuFxdUD4A9Y6erFvXwqMcUBNJz+MAHHADXWN4v+8JRMxMfIW+nqeGKfUFhP1xcb5GJzA2OSuVEs3rVr0Q==')

print("1")
block_blob_service.create_blob_from_path(
    'addresses',
    'zoom_0.mp4',
    'zoom_0.mp4',
    content_settings=ContentSettings(content_type='video/mp4')
            )
print("2")
#get url
# block_blob_service.set_container_acl("addresses",{"AccessPolicy": "abc"})
sas_token = block_blob_service.generate_blob_shared_access_signature(
	"addresses",
	"zoom_0.mp4",
	permission= BlobPermissions().READ,
	expiry='2020-10-12',
	start=None)
print("3")

url = block_blob_service.make_blob_url("addresses", "zoom_0.mp4", sas_token=sas_token, )

conn = http.client.HTTPSConnection("videobreakdown.azure-api.net")

headers = {
    'ocp-apim-subscription-key': "d7739fcadadc4280a02cbd6482f5ef86",
    'content-type': "multipart/form-data",
    'cache-control': "no-cache",
    'postman-token': "329095b8-ea7d-ed09-a01b-95ee437ba7e3"
    }
print("4")
conn.request("POST", "/Breakdowns/Api/Partner/Breakdowns?name=test&privacy=Private&videoUrl=" + url + "&language=English", headers=headers)

res = conn.getresponse()
data = res.read()

id = data.decode("utf-8")
id = id[1:len(id) - 1]
conn.close()

state = "nothing"
while(state != "Processed"):
    conn1 = http.client.HTTPSConnection("videobreakdown.azure-api.net")

    headers1 = {
        'ocp-apim-subscription-key': "d7739fcadadc4280a02cbd6482f5ef86",
        'cache-control': "no-cache",
        'postman-token': "089b4ce7-bbdc-314c-374d-45762450ac63"
        }

    conn1.request("GET", "/Breakdowns/Api/Partner/Breakdowns/" + id + "/State", headers=headers1)

    res1 = conn1.getresponse()
    data1 = res1.read()
    d = json.loads(data1.decode("utf-8"))
    state = d["state"]
    time.sleep(7)
    conn1.close()

conn2 = http.client.HTTPSConnection("videobreakdown.azure-api.net")

headers2 = {
    'ocp-apim-subscription-key': "d7739fcadadc4280a02cbd6482f5ef86",
    'cache-control': "no-cache",
    'postman-token': "71dd16e5-0eb3-cb12-13ac-3c3c37a474b8"
    }

conn2.request("GET", "/Breakdowns/Api/Partner/Breakdowns/" + id + "?language=English", headers=headers2)

res2 = conn2.getresponse()
data2 = res2.read()

print(json.loads(data2.decode("utf-8")))
conn2.close()
