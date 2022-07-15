## py client test1 AIS SignUp
import http.client
import json
import ast
import time
from logging import captureWarnings
from re import T
import subprocess
from sqlite3 import Date
from datetime import date, datetime
from tokenize import Hexnumber

l = []
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
    return [neos_id,claim_code]

  y = Patch(user_creds)
  n = y[0]
  c = y[1]
  if i == 1:
    Neos_id2 = n

  # ----------------------------------------------------------------------------------------------------------
  #test 3 Hub Claim

  def Hub_Claim(n,c):
    
    print("neos id "+str(i+1)+":",n,type(n))
    print("claim code "+str(i+1)+": ",c,type(c))

    time.sleep(60)

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
    l.append(stage3_creds["admin_user_id"])
    if i == 1:  
      l.append(stage3_creds["device_id"])
    return l
  z = Hub_Claim(n,c) 
admin_id1 = z[0]
admin_id2 = z[1] 
device_id = z[2]  

# -----------------------------------------------------------------------------------------
# SUB-PROCESS

def Sub_Process(admin_id2, device_id):
  p1 = subprocess.run('go run main.go  --user-id='+admin_id2+' --device-token='+device_id, capture_output= True, text= True, shell=True)
  # print(p1.stdout) // for checking the subprocesse's output
  # print(p1.stderr) // for checking subprocesse's error 
  return p1.stdout
Hub_claim_token = Sub_Process(admin_id2,device_id)
print(Hub_claim_token)


  # ----------------------------------------------------------------------------------------------------------
  #test 4 Post Creation  Post Creation

def PosT_Creation(admin_id1,admin_id2,Neos_id2,Hub_claim_token):
  conn = http.client.HTTPSConnection("neos-"+Neos_id2+".staging.neone.host")
  payload = json.dumps({
      "attachment_count": 2,
      "expandable_link": None,
      "post_text": "Test on 01-07-2022 for staging",
      "recipient_ids": [
        {
          "recipient_user_id": admin_id1
        }
      ]
    })
  headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer '+ Hub_claim_token
    }
  conn.request("POST", "/Neone/neos/v01/users/"+admin_id2+"/posts", payload, headers)
  res = conn.getresponse()
  data = res.read()
  # print(data.decode("utf-8"))

  claim_info = ast.literal_eval(data.decode("utf-8"))    
  print("Post Created: ",claim_info)
PosT_Creation(admin_id1,admin_id2,Neos_id2,Hub_claim_token)
 




