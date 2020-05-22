import pandas as pd
from telethon import TelegramClient, sync, events
import json
import re

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

api_id =  'your api_id'
api_hash = 'yout api hash'
group_username = 'fradpro'#It's temporary off

client = TelegramClient('session_name', api_id, api_hash)
client.start()

@client.on(events.NewMessage(chats=group_username, incoming=True))

async def my_event_handler(event):
    
    chats = await client.get_messages(group_username, 1)
    message =[]
    time = []
    
    if len(chats):
        for chat in chats:
            message.append(chat.message)
            time.append(chat.date)
    data = {'time':time,'message':message}
    df = pd.DataFrame(data)
    
    time = re.search(r'\d{2}:\d{2}:\d{2}', str(df)).group()
    stock = re.search(r'\w{4}\d{2}', str(df))
    if stock:
        stock = stock.group()
    else:
        stock = 'Not found'
    order = re.search(r'(?<=\b)\w{5,6}(?=\\n)', str(df))
    if order:
        order = order.group()
    else:
        order = 'Not found'
    price = re.search(r'(?<=START )\d+,*\d(?=\\n)', str(df))
    if price:
        price = price.group()
    else:
        price = 'Not found'
    partial = re.search(r'^(?<=PARCIAL )\d+,*\d(?=\\n)$', str(df))
    if partial:
        partial = partial.group()
    else:
        partial = 'Not found'
    target = re.search(r'(?<=ALVO )\d+,*\d(?=\\n)', str(df))
    if target:
        target = target.group()
    else:
        target = 'Not found'
    stopLoss = re.search(r'(?<=STOP )\d+,*\d(?=\\n)', str(df))
    if stopLoss:
        stopLoss = stopLoss.group()
    else:
        stopLoss = 'Not found'
        
    call = time+'\n'+stock+'\n'+order+'\n'+price+'\n'+partial+'\n'+target+'\n'+stopLoss
    
    print(call)

client.run_until_disconnected()
