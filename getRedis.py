
import redis
import requests
import time
redisClient = redis.StrictRedis(host='localhost',port=6379,db=0)

blynkToken = "Z3IpYgan8qOuvPBJ9XGxa1i-nLcbA3th"
url = 'http://119.18.158.237:3579/'+blynkToken


def pushBlynk(virtualPin,data):
    blynkUrl = url+"/update/"+virtualPin+"?value="+str(data)

    # dataBlynk4 = ur4+str(dataMppt1[4])
    blynkPush = requests.get(blynkUrl)
    print(blynkPush)
    print(blynkUrl)

print(redisClient.hget("pms1", "voltage").decode('utf-8'))

numOfPack = 25
Vpack  = []
Ipack = []

pack = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,20,21,22,23,24,25]

for counterPack in range(0,numOfPack-1):
    # if counterPack > 1:
        # pass
    Vpack.append (redisClient.hget("pms"+str(pack[counterPack]), "voltage").decode('utf-8'))
    Ipack.append (redisClient.hget("pms"+str(pack[counterPack]), "current").decode('utf-8'))

#push min max

print(Vpack)
print(Ipack)
pushBlynk("V25",float(max(Vpack))/100)
time.sleep(1)
pushBlynk("V26",float(min(Vpack))/100)
time.sleep(1)

pushBlynk("V39",int(max(Ipack))/10)
time.sleep(1)
pushBlynk("V40",int(min(Ipack))/10)
time.sleep(1)


#push min max

for counterPack in range(0,numOfPack):
    if counterPack > 16:
        counterPack +=1
    print("Vpack :" + str(counterPack+1) + " " + str(Vpack[counterPack]))
    virtual = "V"+str(counterPack+1)
    pushBlynk(virtual,int(Vpack[counterPack])/100)
    time.sleep(0.5)
    virtual = "V"+str(counterPack+1+26)
    print("Ipack :" + str(counterPack+1) + " " + str(Ipack[counterPack]))
    pushBlynk(virtual,int(Ipack[counterPack])/10)
    time.sleep(0.5)




Vpack.clear()
Ipack.clear()

#redis-cli -c hgetall pms1
