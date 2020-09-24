import redis
rmacan = redis.Redis(host='localhost')
print(rmaca.hget('pms1','voltage'))
