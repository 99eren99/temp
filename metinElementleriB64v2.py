import base64
from PIL import Image
from io import BytesIO
import pymongo
import os

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["antalyangundemgazetesiDB"]#dbname

haberler=db["haberler"]
videoHaberler=db["videoHaberler"]
galeriler=db["galeriler"]
koseYazilari=db["koseYazilari"]
resimler=db["resimler"]

def getB64image(path):
    img=Image.open(path).convert("RGB")
    buff = BytesIO()
    img.save(buff, format="JPEG")
    base64img = base64.b64encode(buff.getvalue()).decode("utf-8")
    return base64img

#örnek url : ./wp-content/uploads/2023/07/BOLUDA-BUGUN-ELEKTRIK-KESINTISI.jpg
PREFIX="data:image/jpeg;base64,"

cursor=haberler.find()
for document in cursor:
    #thumbnail güncelle
    thumbnailResimUrl=document["thumbnailResimURL"]

    if thumbnailResimUrl is not None and thumbnailResimUrl[0]=="h":#url ise
        path="./"+("/").join(thumbnailResimUrl.split("/")[3:])
        document["thumbnailResimURL"]=PREFIX+getB64image(path)
    if document["metinGovde"] is not None:
        for element in document["metinGovde"]:
            if len(element)==2:#resim demektir
                resimURL=element["resim"]
                if resimURL is not None and resimURL[0]=="h":#url ise
                    path="./"+("/").join(resimURL.split("/")[3:])
                    element["resim"]=PREFIX+getB64image(path)

    haberler.replace_one({'_id':document["_id"]}, document, upsert=False)

cursor=videoHaberler.find()
for document in cursor:
    if document["metinGovde"] is not None:
        for element in document["metinGovde"]:
            if len(element)==2:#resim demektir
                resimURL=element["resim"]
                if resimURL is not None and resimURL[0]=="h":#url ise
                    path="./"+("/").join(resimURL.split("/")[3:])
                    element["resim"]=PREFIX+getB64image(path)

        videoHaberler.replace_one({'_id':document["_id"]}, document, upsert=False)

cursor=koseYazilari.find()
for document in cursor:
    if document["metinGovde"] is not None:
        for element in document["metinGovde"]:
            if len(element)==2:#resim demektir
                resimURL=element["resim"]
                if resimURL is not None and resimURL[0]=="h":#url ise
                    path="./"+("/").join(resimURL.split("/")[3:])
                    element["resim"]=PREFIX+getB64image(path)

        koseYazilari.replace_one({'_id':document["_id"]}, document, upsert=False)

cursor=galeriler.find()
for document in cursor:
    if document["metinGovde"] is not None:
        for element in document["metinGovde"]:
            if len(element)==2:#resim demektir
                resimURL=element["resim"]
                if resimURL is not None and resimURL[0]=="h":#url ise
                    path="./"+("/").join(resimURL.split("/")[3:])
                    element["resim"]=PREFIX+getB64image(path)

        galeriler.replace_one({'_id':document["_id"]}, document, upsert=False)
