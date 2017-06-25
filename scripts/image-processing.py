from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
from azure.storage.blob.models import BlobPermissions

import requests
import shutil
import http.client
import json
import time
import string

# initialise blob service
block_blob_service = BlockBlobService(account_name='nikolas', account_key='b/qWJCuFxdUD4A9Y6erFvXwqMcUBNJz+MAHHADXWN4v+8JRMxMfIW+nqeGKfUFhP1xcb5GJzA2OSuVEs3rVr0Q==')

block_blob_service.create_blob_from_path(
    'addresses',
    'zoom_0.mp4',
    'zoom_0.mp4',
    content_settings=ContentSettings(content_type='video/mp4')
            )

#get url
# block_blob_service.set_container_acl("addresses",{"AccessPolicy": "abc"})
sas_token = block_blob_service.generate_blob_shared_access_signature(
	"addresses",
	"zoom_0.mp4",
	permission= BlobPermissions().READ,
	expiry='2020-10-12',
	start=None)

url = block_blob_service.make_blob_url("addresses", "zoom_0.mp4", sas_token=sas_token, )

conn = http.client.HTTPSConnection("videobreakdown.azure-api.net")

headers = {
    'ocp-apim-subscription-key': "d7739fcadadc4280a02cbd6482f5ef86",
    'content-type': "multipart/form-data",
    'cache-control': "no-cache",
    'postman-token': "329095b8-ea7d-ed09-a01b-95ee437ba7e3"
    }

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
    da = json.loads(data1.decode("utf-8"))
    state = da["state"]
    progress = da["progress"]
    print(state + "\n" + progress)
    time.sleep(14)
    conn1.close()
print(state + "\n" + progress)
conn2 = http.client.HTTPSConnection("videobreakdown.azure-api.net")

headers2 = {
    'ocp-apim-subscription-key': "d7739fcadadc4280a02cbd6482f5ef86",
    'cache-control': "no-cache",
    'postman-token': "71dd16e5-0eb3-cb12-13ac-3c3c37a474b8"
    }

conn2.request("GET", "/Breakdowns/Api/Partner/Breakdowns/" + id + "?language=English", headers=headers2)

res2 = conn2.getresponse()
data2 = res2.read()
d = json.loads(data2.decode("utf-8"))
conn2.close()
print(json.loads(data2.decode("utf-8")))

# with open('data.json') as json_data:
#     d = json.load(json_data)
#     print(d.keys())

insights = d["breakdowns"][0]["insights"]

# returns list of faces given insights dictionary
def getFaceIDs(insights):
    face_ids = []
    for face in insights["faces"]:
        face_ids.append(face["id"])
    return face_ids

t_blocks = d["breakdowns"][0]["insights"]["transcriptBlocks"]

# id_name_dict = {"1729":"Nik", "1598":"Ben", "1492":"Rami"}
id_name_dict = {"1006": "Rami"}
face_ts_list = [] #list of face,ts tuples
for face in t_blocks[2]["faces"]:
    person = (id_name_dict[str(face["id"])])
    print(id_name_dict[str(face["id"])])
    print("------")
    for r in face["ranges"]:
        print("Start: " + r["timeRange"]["start"])
        print("End: " + r["timeRange"]["end"])
        face_ts_list.append((person, r["timeRange"]["start"]))
    print("\n")
print(face_ts_list)
for line in t_blocks[2]["lines"]:
    print(line["text"])
    print("Start: " + line["timeRange"]["start"])
    print("End: " + line["timeRange"]["end"])
    print("-------")

def sort_faces(face_ts_list):
    return sorted(face_ts_list, key=lambda tup: tup[1])
print(sort_faces(face_ts_list))

sum = 0

# get the set of punctuation symbols
invalidChars = set(string.punctuation.replace("_", ""))
f = open("transcript.txt", 'w')

for i in t_blocks[:-6]:
    sum +=len(i["lines"])
    lines = i["lines"]
    faces = i["faces"]
    for face in faces:
        print(id_name_dict[str(face["id"])])
        f.write(id_name_dict[str(face["id"])] + ":")
        break
    for line in lines:
        a = (line["text"])
#         print(line['participantId'])
        if counter:
            print(b + ' ' + a)
            f.write(b + ' ' + a + "\n")
            counter = False
            continue
        if a!= '' and (a[-1]) not in invalidChars:
            counter = True
            b = a
            continue
        print(a)
        f.write(a + "\n")
        print("-----------")
f.close()
