from datetime import datetime, timedelta
import json
import time

async def is_timestamp_30_days_apart(timestamp):
    dt = datetime.fromtimestamp(float(timestamp))
    now = datetime.now()
    diff = now - dt
    if diff >= timedelta(days=30):
        return True
    else:
        return False
    
async def error_log(ctx, error, code):
    with open("error.log","a") as f:
        f.write(f"{datetime.now()} | {ctx.command} | {ctx.guild_id} | {ctx.author.id} | {ctx.author.name} | {error} | {code}\n")

async def point_log(ID, event, point):
    with open("point.log","a") as f:
        f.write(f"{datetime.now()} | {ID} | {event} | {point}\n")

async def can_check_in(last_check_in_time):
   current_time = datetime.now()
   last_check_in_date = datetime.fromtimestamp(last_check_in_time)
   reset_time = datetime(current_time.year, current_time.month, current_time.day, 0, 0, 0)
   next_reset_time = reset_time + timedelta(days=1)
   if last_check_in_date > reset_time:
      
      return False, int(next_reset_time.timestamp())
   else:
      return True, int(next_reset_time.timestamp())

# 1: 簽到正常, 2: 簽到過了
async def sign(ID,POINT):
    ID = str(ID)
    with open("point.json","r") as f:
        data = json.load(f)
    if ID in data:
        check = await can_check_in(data[ID]['last_sign'])
        if check[0] == False:
            return 2, int(check[1])
        data[ID]['point'] += POINT
        data[ID]['last_sign'] = int(time.time())
    else:
        data[ID] = {}
        data[ID]['point'] = POINT
        data[ID]['last_sign'] = int(time.time())
        
    with open("point.json","w") as f:
        json.dump(data,f)
    current_time = datetime.now()
    return 1, int((datetime(current_time.year, current_time.month, current_time.day, 0, 0, 0)  + timedelta(days=1)).timestamp())

async def check_point(ID):
    ID = str(ID)
    with open("point.json","r") as f:
        data = json.load(f)
    if ID in data:
        return data[ID]['point']
    else:
        return 0

async def check_last_sign_time(ID):
    ID = str(ID)
    with open("point.json","r") as f:
        data = json.load(f)
    if ID in data:
        return data[ID]['last_sign']
    else:
        return 0

async def add_point(ID,point):
    ID = str(ID)
    with open("point.json","r") as f:
        data = json.load(f)
    if ID in data:
        data[ID]['point'] += point
    else:
        data[ID] = {}
        data[ID]['point'] = point
        data[ID]['last_sign'] = 0
    with open("point.json","w") as f:
        json.dump(data,f)
    return

async def sub_point(ID,point):
    ID = str(ID)
    with open("point.json","r") as f:
        data = json.load(f)
    if ID in data:
        data[ID]['point'] -= point
    else:
        data[ID] = {}
        data[ID]['point'] = 0
        data[ID]['last_sign'] = 0
    with open("point.json","w") as f:
        json.dump(data,f)
    return

async def set_point(ID,point):
    ID = str(ID)
    with open("point.json","r") as f:
        data = json.load(f)
    if ID in data:
        data[ID]['point'] = point
    else:
        data[ID] = {}
        data[ID]['point'] = point
        data[ID]['last_sign'] = 0
    with open("point.json","w") as f:
        json.dump(data,f)
    return

async def get_rawpoint_data():
    with open("point.json","r") as f:
        data = json.load(f)
    return data

async def total_point():
    with open("point.json","r") as f:
        data = json.load(f)
    total = 0
    for i in data:
        total += data[i]['point']
    return total

async def total_user():
    with open("point.json","r") as f:
        data = json.load(f)
    return len(data)

async def get_reward():
   data = {}
   with open("reward.json", "r",encoding="UTF-8") as f:
      data = json.load(f)
   return data

async def add_reward_code(id,code):
   data = await get_reward()
   data['reward'][id-1]['code'].append(code)
   data['reward'][id-1]['stock'] += 1
   with open("reward.json", "w",encoding="UTF-8") as f:
      json.dump(data, f, indent=4)

async def pop_reward_code(id):
   data = await get_reward()
   if len(data['reward'][id-1]['code']) == 0:
      return 0
   code = data['reward'][id-1]['code'].pop()
   data['reward'][id-1]['stock'] -= 1
   with open("reward.json", "w",encoding="UTF-8") as f:
      json.dump(data, f, indent=4)
   return code
