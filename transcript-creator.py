import json
import string

with open('data.json') as json_data:
    d = json.load(json_data)
    print(d.keys())

insights = d["breakdowns"][0]["insights"]

# returns list of faces given insights dictionary
def getFaceIDs(insights):
    face_ids = []
    for face in insights["faces"]:
        face_ids.append(face["id"])
    return face_ids

t_blocks = d["breakdowns"][0]["insights"]["transcriptBlocks"]


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
id_name_dict = {"1729":"Nik", "1598":"Ben", "1492":"Rami"}
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
