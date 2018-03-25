import requests
import codecs
from IPython.display import HTML

face_key =  'f0c8fa92e85040138b4bad7e01767aa0'

headers = {
    #'Content-Type': 'application/json',
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': face_key
}

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}

binary_path="/mnt/files/unsorted/Pictures/2018-03-24-192927.jpg"


image_url = "https://tvdownloaddw-a.akamaihd.net/stills/images/vdt/2016/beng160405_099_janbruckhand_01c_1.jpg"
# face_api_url="https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect?"

#response = requests.post(face_api_url, params=params, headers=headers, json={"url": image_url})
with open(binary_path, "rb") as fjpg:
    response = requests.post(face_api_url, params=params, headers=headers, data=fjpg)

faces = response.json()
print(faces)
print("DONE")
quit()

