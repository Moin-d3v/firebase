## py client test1 AIS SignUp
from asyncio.windows_events import NULL
import http.client
from typing import final
import requests
import json
import ast
import time
import ssl
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from logging import captureWarnings
from re import T
import subprocess
from sqlite3 import Date
from datetime import date, datetime
from tokenize import Hexnumber
import mimetypes
from codecs import encode
from turtle import pos

sender = []
receiver = []

for i in range(2):

  def SignUp():
    conn = http.client.HTTPSConnection("ais-staging.neone.host")
    date = datetime.now()
    email_today = "NeoneTesting"+date.strftime("%d-%m-%Y-%H-%M-%S")+"@gmail.com"
    payload = json.dumps({
    "user": {
      "email": email_today
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjV6TnlNWUZRdHM2NG5JempLUlVnIiwidHlwIjoiSldUIn0.eyJzY29wZSI6ImNvbm5lY3Rpb25fcmVhZCIsImV4cCI6MTYyNjk4OTkzOSwiaWF0IjoxNjI2Njg5NjM5LCJzdWIiOiJiYzdiMGM1OS0yMjI2LTRlNzYtOWYyNS02NjZjNzdkOGFlZDAifQ.UOiOsi9gd9-7DOYxvcJ1VW3vURu3BQn4sTTF2PwjTnWRjemGIQCAzjyXK5EWoNLJvFAvlJpyz9YbXJyC0-gaoS7U_5Q3nNa-11KfVOXupuo6wKezYACUATP6JhD4AWaZEiJN9RoC_fBwSEKEVx2wDU9WFSjHGt3W2TQ_Pf1etyxQ3N5e_c24yJd9zlBieMQeg2HoAglwEiru0v34fYcAL_Wi4bahK5EVgdFuUV8U_WNV5_tU8urSdviCkWoLBHdYNBPGnUQEHdsvbVJdymlP_MPJ4SmbGkIYNa_9-RMnslIHL-MLleWdqUxcZoZQcfUCjz9UsVxn6t7qmLE2BTMM3A'
    }
    conn.request("POST", "/accounts", payload, headers)
    res = conn.getresponse()
    data = res.read()
    # print(data.decode("utf-8"))
    creds = ast.literal_eval(data.decode("utf-8"))
    user_creds = creds["id"]
    return (user_creds)
  user_creds = SignUp()
    
  # ----------------------------------------------------------------------------------------------------------
  #test2 Patch Method

  def Patch(user_creds):
    user_id = user_creds
    conn = http.client.HTTPSConnection("ais-staging.neone.host")
    payload = json.dumps({
      "plan": {
        "plan_id": "promo"
      }
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': 'APIKEY admin'
    }
    conn.request("PATCH", "/accounts/"+ str(user_id), payload, headers)
    # conn.request("PATCH", "/accounts/test1.x["id"]", payload, headers)
    res = conn.getresponse()
    data = res.read()
    # print(data.decode("utf-8"))
    claim_info = ast.literal_eval(data.decode("utf-8"))
    neos_id = claim_info["neos_id"]
    claim_code = claim_info["claim_code"]
    if i == 0:
      sender.append(neos_id)
      sender.append(claim_code)
    if i == 1:
      receiver.append(neos_id)
      receiver.append(claim_code)
    return [neos_id,claim_code] # returning n1, claim1

  y = Patch(user_creds)
  n = y[0]
  c = y[1]
  if i==0:
    Neos_id1 = n 
  if i == 1:
    Neos_id2 = n

  # ----------------------------------------------------------------------------------------------------------
  #test 3 Hub Claim

  def Hub_Claim(n,c):
    
    print("neos id "+str(i+1)+":",n,type(n))
    print("claim code "+str(i+1)+": ",c,type(c))

    time.sleep(50)

    conn = http.client.HTTPSConnection("neos-"+n+".staging.neone.host")
    payload = json.dumps({
      "claim_code": c,
      "device": {
        "device_key_components": {
          "exponent": "AQAB",
          "modulus": "unlp9dkiMIAm-VM1WwwmsZjmjVDepvilUEJB1P_3HYA1dyxly-9MqaKyW3LIsgsCQDtDyUTLysLMXeP8HzShBo-rFB_LSmLd_yrqy2KyZzldwewCzSDrvwcqZfgNib4mkHH6GhX0VRlNdQb-B9XdvPCly0LT7QaZw32CjPz1BNVCoAFzxHQpw_cMxke1tkENC8tWZWNczlUPjlQwARd0luGN-EhdIfR-ZSzYeCBv3_3Ksc-heNf1gAV-MlQKu0WK4--X6Hce2TXRFZsE6mdn0s0Zf3KMZ7nOtIXRWlRtgUkO2nyUA1a3IUQ7mV_CF_Zoo9wF3xTVzDef9rSXhXjP3w"
        },
        "device_name": "Neone Device ",
        "device_token": "VlSg5DESey3OpfM7jXRA4yiSBsbkZQPllbKRZJlkVWebQpBgsNN50j",
        "device_type": {
          "device_icon_base64_enc": "<AC>",
          "device_platform": "ios",
          "device_type_name": "iPhone"
        }
      },
      "user_configurable_info": {
        "email": "neonetesting@gmail.com",
        "first_name": "Neos",
        "last_name": "Testing",
        "nickname": "testing"
      }
    })
    headers = {
      'Content-Type': 'application/json'
      # 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ilk3RXFFWnVIS2dNZlB4eUdhNXpWIiwidHlwIjoiSldUIn0.eyJzY29wZSI6InBvc3Rfd3JpdGUiLCJleHAiOjE2NTQzOTAwNjUsImlhdCI6MTY1NDA4OTc2NSwic3ViIjoiZjFlN2ZjZTMtMWNhZS00NGIwLWIzZTItZTI3NTljYjI3ODVkIn0.mga7Q14Zwx2S8-QeZ0GjA1KadEfqyF-MisBIS_YNV8wW8o3LN2VVo8CicMipk-DgtEM6E1Zb_8TXZc2ja1nirJNW236ca9S4ND0owmzPj6S0vptw3V6lozW0XPzXUtaN9DcY0UWnPcfdYc5Jj2HJgjEqIXIdP7z_fr5Al-bXOg3KAcQeyoAC4Op5lhcNbklNPehX2vMgSOCjBv_rmvXbqqFnWb3PUdMJS1hlHJ9D6MczdwRGJku1t_vd-HnlYLdsCxpR27jP6sf2X2jkXp91e6IGjeTiYFygKv_HnQU5cEpcZi_zIcq7sAxD-eEoQWo7bAWwcvoIyhj9pzMMYoRK1A'
    }
    conn.request("POST", "/Neone/neos/v01/admin/claim", payload, headers)
    res = conn.getresponse()
    data = res.read()
    # print(data.decode("utf-8"))

    stage3_creds = ast.literal_eval(data.decode("utf-8"))

    print("admin_user_id "+str(i+1)+": ",stage3_creds["admin_user_id"]) 

    print("device_token "+str(i+1)+": ",stage3_creds["device_id"]) 
    if i == 0:
      sender.append(stage3_creds["admin_user_id"])
      sender.append(stage3_creds["device_id"]) 
    if i == 1:
      receiver.append(stage3_creds["admin_user_id"])
      receiver.append(stage3_creds["device_id"])   
  z = Hub_Claim(n,c) 

print("sender's_info", sender)
print("reciever's_info", receiver)


# -----------------------------------------------------------------------------------------
# SUB-PROCESS

def Sub_Process(admin_id, user_id):
  p1 = subprocess.run('go run main.go  --user-id='+admin_id+' --device-token='+user_id, capture_output= True, text= True, shell=True)
  # print(p1.stdout) // for checking the subprocesse's output
  # print(p1.stderr) // for checking subprocesse's error 
  return p1.stdout
Hub_Token2 = Sub_Process(receiver[2],receiver[3])
Hub_Token1 = Sub_Process(sender[2],sender[3])
print("Hub_Claim Token 1:",Hub_Token1)
print("Hub_Claim Token 2:",Hub_Token2)



  # ----------------------------------------------------------------------------------------------------------
  #test 4 Post Creation  Post Creation

def PosT_Creation(admin_id1,admin_id2,Neos_id2,Hub_claim_token):
  print("BackEnd: ",admin_id1,admin_id2,Neos_id2,Hub_claim_token)
  conn = http.client.HTTPSConnection("neos-"+Neos_id2+".staging.neone.host")
  payload = json.dumps({
      "attachment_count": 1,
      "expandable_link": "NULL",
      "post_text": "Check out these star pics.",
      "recipient_ids": [
        admin_id1
      ]
    })
  headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer '+Hub_claim_token
    }
  conn.request("POST", "/Neone/neos/v01/users/"+admin_id2+"/posts", payload, headers)
  res = conn.getresponse()
  data = res.read()
  print(data.decode("utf-8"))
  claim_info = ast.literal_eval(data.decode("utf-8")) 
  print("Claim_info : ",claim_info) 
  Post_id1 = claim_info["post_id"]
  print("Post Created: ",claim_info)
  return [Post_id1]

Post_Created = PosT_Creation(sender[2],receiver[2],Neos_id2,Hub_Token2)
post_id = Post_Created[0]


print("POST_ID",post_id)

#----------------------------------------------------------------------------------------------------------------------
# 5th endpoint
def Req(post_id,a2,N2,tken):

  url = "https://neos-"+N2+".staging.neone.host/Neone/neos/v01/users/"+a2+"/posts/"+post_id+"/attachments"

  test_file = open("961876.jpg", "rb")

  headers = {
    # 'content-type': "multipart/form-data;",
      'authorization': "Bearer "+ tken,
      'cache-control': "no-cache",
      }
  response = requests.request("POST", url, files = {"attachment": test_file}, headers=headers,verify= False)
  # print("Attachment_id: ",response.text)
  att_id = ["Attachment_id: ",response.text]
  print("attt_iddd: ",att_id)
  # b = []
  final_ID = att_id[1]
  # b.append(final_ID)
  print("Final_ID: ",type(final_ID))
  return [att_id,final_ID]

Post_Req = Req(post_id,receiver[2],receiver[0],Hub_Token2)

postt_id = Post_Req[0][1]
attachm_id = Post_Req[1]


print("attachm_id: ",attachm_id)
ATTACH_ID = ""
for i in range(postt_id.index(":")+2,len(postt_id)-3):
  ATTACH_ID = ATTACH_ID + postt_id[i]
# print("check: ",ATTACH_ID)
# print("N1: ",Neos_id2)


# --------------------------------------------------------------------------------------
# 6th Endpoint Post Get From Attachment

def Get_Post():
  conn = http.client.HTTPSConnection("neos-"+receiver[0]+".staging.neone.host")
  payload = ''
  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+ Hub_Token2
  }
  conn.request("GET", "/Neone/neos/v01/users/"+receiver[2]+"/posts/", payload, headers)
  res = conn.getresponse()
  data = res.read()
  print(data.decode("utf-8"))
Get_Post()

# 7th Step 
# ------------------------------------------------------------------------------------------------
def Image():

  conn = http.client.HTTPSConnection("neos-"+receiver[0]+".staging.neone.host")
  payload = ''
  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+ Hub_Token2
  }
  conn.request("GET", "/Neone/neos/v01/users/"+receiver[2]+"/posts/"+post_id+"/attachments/"+ATTACH_ID+"", payload, headers)
  res = conn.getresponse()
  data = res.read()
  # print("GETTING THE IMAGE: ",data)

Image()

# --------------------------------------------------------------------------------------------
# 8th Endpoint Login

def LOGIN():

  conn = http.client.HTTPSConnection("neos-"+receiver[0]+".staging.neone.host")
  payload = ''
  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+ Hub_Token2
  }
  conn.request("GET", "/Neone/neos/v01/users/"+receiver[2]+"/messenger/login", payload, headers)
  res = conn.getresponse()
  data = res.read()
  print(data.decode("utf-8"))

LOGIN()