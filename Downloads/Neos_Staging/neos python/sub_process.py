from logging import captureWarnings
from re import T
import subprocess

def Sub_Process(a1, device_id):
# this is for getting details of external files into subprocess
    
  p1 = subprocess.run('go run main.go  --user-id='+a1+' --device-token='+device_id, capture_output= True, text= True, shell=True)
  # print(p1.stdout)
  print(p1.stderr)
  return p1.stdout

sub_token = Sub_Process(a1,device_id)
print(sub_token)













# # this is for getting details of external files into subprocess
# p1 = subprocess.run('go run main.go', capture_output= True, text= True, shell=True)
# print("check", p1.stdout)
# print("err", p1.stderr)

# # p1 = subprocess.Popen(['dir','output.txt'],shell=True,stdout=True, text=True)
# # print(p1.stdout)



# # with open('sub1.py','w') as f:
# #     results = subprocess.run(['dir "hello this is"'], shell=True, stdout=f,text=True)    
# # print(results)


# # print(results.stdout)
# # results = subprocess.run(["ls","-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)