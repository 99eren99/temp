import base64
from PIL import Image
from io import BytesIO
import pymongo
import os

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["xyzswqss"]#dbname

resimler=db["resimler"]

        
for yearFolder in range(2017,2024):
    for monthFolder in range(1,13):
        try:
            images=os.listdir(f"./{yearFolder}/{monthFolder}/")
        except:
            continue

        #filter images
        images=list(filter(lambda imgName: not "x" in imgName.split("-")[-1], images))

        for imageName in images:
            print(f"./{yearFolder}/{monthFolder}/{imageName}")
            ref=f"https://antalyaningundemi.com/wp-content/uploads/{yearFolder}/{monthFolder}/{imageName}"
            img=Image.open(f"./{yearFolder}/{monthFolder}/{imageName}")
            buff = BytesIO()
            img.save(buff, format="JPEG")
            base64img = base64.b64encode(buff.getvalue()).decode("utf-8")
            resimDocument={"href":ref,"base64img":base64img}
            resimler.insert_one(resimDocument)