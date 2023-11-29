from bs4 import BeautifulSoup
import requests, base64
from PIL import Image
from io import BytesIO
from datetime import datetime
import json
import pymongo
    
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["xyzswqss"]#dbname

haberler=db["haberler"]

def filterByMetaKey(postMetas,metaKey):
    for postmeta in postMetas:
        try:
            if postmeta.find("wp:meta_key").text==metaKey:
                return postmeta
        except:
            pass

with open('camcı.xml', 'r', encoding="utf8") as f:
    file = f.read() 

soup = BeautifulSoup(file, 'xml')
habers=soup.find_all("item")


counter=0
for haber in habers:
    print(counter)
    counter+=1
    postMetas=haber.find_all("wp:postmeta")

    url=haber.find("link").text
    try:
        thumbnailResimURL=filterByMetaKey(postMetas,"ilan_resmi").find("wp:meta_value").text.split("\"")[3]
    except:
        thumbnailResimURL=None
    #saveImgIntoDatabase(thumbnailResimURL)

    try:
        baslik=filterByMetaKey(postMetas,"ilan_baslik").find("wp:meta_value").text
    except:
        baslik=None

    try:
        ozet=filterByMetaKey(postMetas,"ilan_ozet").find("wp:meta_value").text
    except:
        ozet=None
    haberTuru={"tur":"Resmi İlan","ref":"https://antalyaningundemi.com/resmi-ilan/"}

    try:
        basinNo=filterByMetaKey(postMetas,"ilan_basin_no").find("wp:meta_value").text
    except:
        basinNo=None
    
    #datetime : 2021-02-05T09:39:00.000+00:00
    """ try:
        baslangicTarihi=filterByMetaKey(postMetas,"baslangic_tarihi").find("wp:meta_value").text
        baslangicSaati=filterByMetaKey(postMetas,"baslangic_saati").find("wp:meta_value").text
        baslangicDatetime=baslangicTarihi+"T"+baslangicSaati+".000+00:00"
    except:
        baslangicDatetime=None

    try:
        bitisTarihi=filterByMetaKey(postMetas,"bitis_tarihi").find("wp:meta_value").text
        bitisSaati=filterByMetaKey(postMetas,"bitis_saati").find("wp:meta_value").text
        bitisDatetime=bitisTarihi+"T"+bitisSaati+".000+00:00"
    except:
        bitisDatetime=None """

    kategoriler=[{"Resmi İlan":"https://antalyaningundemi.com/resmi-ilan/"}]

    try:
        metinElementleri=filterByMetaKey(postMetas,"ilan_detayi_editor").find("wp:meta_value").text
    except:
        metinElementleri=None
    
    try:
        girisTarihi=haber.find("wp:post_date").text
        girisTarihi=datetime.strptime(girisTarihi, '%Y-%m-%d %H:%M:%S').isoformat()
    except:
        girisTarihi=None
    try:
        guncellemeTarihi=haber.find("wp:post_modified").text
        guncellemeTarihi=datetime.strptime(guncellemeTarihi, '%Y-%m-%d %H:%M:%S').isoformat()
    except:
        guncellemeTarihi=None

    tags=None
    kaynak=None

    ilanDocument={
            "url":url,
            "basinNo":basinNo,
            "thumbnailResimURL":thumbnailResimURL,
            "baslik":baslik,
            "ozet":ozet,
            "haberTuru":haberTuru,
            "kategoriler":kategoriler,
            "haberTarihi":girisTarihi,
            "guncellenmeTarihi":guncellemeTarihi,
            "metinGovde":metinElementleri,
            "kaynak":kaynak,
            "tags":tags
        }
    
    haberler.insert_one(ilanDocument)

    #print(json.loads(json.dumps(ilanDocument, separators=(" , ", " : "))))
    """ #döküman yolla
    url="https://api.antalyaningundemi.com/haber/create"
    counter=0
    while counter<10:
        resp=requests.post(url,json=ilanDocument)
        if resp.status_code==200:
            break
        counter+=1
    
    
    #resim base64 yolla
    img = Image.open(requests.get(thumbnailResimURL, stream = True).raw)
    buff = BytesIO()
    img.save(buff, format="JPEG")
    base64img = base64.b64encode(buff.getvalue()).decode("utf-8")
    resimDocument={"href":thumbnailResimURL,"base64img":base64img}
    resimPostUrl=""
    counter=0
    while counter<10:
        resp=requests.post(resimPostUrl,json=resimDocument)
        if resp.status_code==200:
            break
        counter+=1 """    
