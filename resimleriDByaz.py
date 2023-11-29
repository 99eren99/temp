import base64
from PIL import Image
from io import BytesIO
import pymongo
import os

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["antalyangundemgazetesiDB"]#dbname

resimler=db["resimler"]

        
for yearFolder in reversed(range(2023,2024)):
    for monthFolder in reversed(range(1,13)):
        try:
            images=os.listdir(f"./{yearFolder}/{monthFolder}/")
        except:
            continue

        #filter images

        for imageName in images:
            try:
                print(f"./{yearFolder}/{monthFolder}/{imageName}")
                ref=f"https://antalyaningundemi.com/wp-content/uploads/{yearFolder}/{monthFolder}/{imageName}"
                img=Image.open(f"./{yearFolder}/{monthFolder}/{imageName}").convert("RGB")
                buff = BytesIO()
                img.save(buff, format="JPEG")
                base64img = base64.b64encode(buff.getvalue()).decode("utf-8")
                resimDocument={"href":ref,"base64img":base64img}
                resimler.insert_one(resimDocument)
            except:
                pass
