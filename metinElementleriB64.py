import base64
from PIL import Image
from io import BytesIO
import pymongo
import os

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["antalyaningundemi"]#dbname

haberler=db["haberler"]
videoHaberler=db["videoHaberler"]
galeriler=db["galeriler"]
koseYazilari=db["koseYazilari"]
resimler=db["resimler"]


PREFIX="data:image/jpeg;base64,"

cursor=haberler.find()
for document in cursor:
    #thumbnail güncelle
    thumbnailResimUrl=document["thumbnailResimURL"]
    if thumbnailResimUrl is not None and thumbnailResimUrl[0]=="h":#url ise
        document["thumbnailResimURL"]=PREFIX+resimler.find_one({"href":thumbnailResimUrl})["base64img"]
    if document["metinGovde"] is not None:
        for element in document["metinGovde"]:
            if len(element)==2:#resim demektir
                resimURL=element["resim"]
                if resimURL[0]=="h":#url ise
                    element["resim"]=PREFIX+resimler.find_one({"href":resimURL})["base64img"]

    haberler.replace_one({'_id':document["_id"]}, document, upsert=False)

cursor=videoHaberler.find()
for document in cursor:
    if document["metinGovde"] is not None:
        for element in document["metinGovde"]:
            if len(element)==2:#resim demektir
                resimURL=element["resim"]
                if resimURL[0]=="h":#url ise
                        element["resim"]=PREFIX+resimler.find_one({"href":resimURL})["base64img"]

        videoHaberler.replace_one({'_id':document["_id"]}, document, upsert=False)

cursor=koseYazilari.find()
for document in cursor:
    if document["metinGovde"] is not None:
        for element in document["metinGovde"]:
            if len(element)==2:#resim demektir
                resimURL=element["resim"]
                if resimURL[0]=="h":#url ise
                        element["resim"]=PREFIX+resimler.find_one({"href":resimURL})["base64img"]

        koseYazilari.replace_one({'_id':document["_id"]}, document, upsert=False)

cursor=galeriler.find()
for document in cursor:
    if document["metinGovde"] is not None:
        for element in document["metinGovde"]:
            if len(element)==2:#resim demektir
                resimURL=element["resim"]
                if resimURL[0]=="h":#url ise
                        element["resim"]=PREFIX+resimler.find_one({"href":resimURL})["base64img"]

        galeriler.replace_one({'_id':document["_id"]}, document, upsert=False)