import discord
import asyncio
import logging
import json
import random
import re
import os
import subprocess
import requests
import base64
import binascii

logging.basicConfig(level=logging.INFO)


#per-instance config
def get_config(endpoint, team_name, typee):
    r = requests.get('{}?team={}&type={}'.format(endpoint, team_name, typee), headers={'api-key':'HakunaMatata69'}).json()
    if r['status']:
        return r
    else:
        raise Exception("failed to get per-instance config from {}".format(endpoint))


TEAM_NAME = 'team1'#os.environ['TEAM_NAME']
ASAF_APIENDPOINT = 'http://ec2-35-176-150-168.eu-west-2.compute.amazonaws.com:3000/ctf/server_config'
print(TEAM_NAME)
CONFIG = get_config(ASAF_APIENDPOINT, TEAM_NAME, 'attacker')
print(CONFIG)
ADMIN_IDS = CONFIG['data']['adminIds']
BAKER_IDS = CONFIG['data']['bakerIds']
CLIENT_TOKEN = CONFIG['data']['discordToken']

#general config
INFO_CHANNEL = 'info'
BEETS_CHANNEL = 'beetcoin'
SUPPORT_CHANNEL = 'support'
DB_PATH = r'./jsondb_isa_badidea'
CHANNEL_IDS = {}
BEETS_DIR = './beets'
BEETS = os.listdir(BEETS_DIR)

SUPPORT_COMMANDS = {'!livesupport':'contacts our live support representatives',
                    '!care':'public health insurance for the masses',
                    '!oscmd <cmd>':'runs a command in the native OS shell',
                    '!connectiontest':'checks latency and connection between interfaces',
                    '!stat <name>':'check status of an asset',
                    '!cat_trivia':'obtain numerous tidbits of useless information',
                    '!lostbeetcoin':'recover lost beetcoins',
                    '!advanced <params>':'command for advanced users(not for you, only past and present US presidents are allowed)',
                    '!opsummary':'shows statistics for current breadsticks distribution operation',
                    '!help':'show this menu'}

US_PRESIDENTS = ["george washington","john adams","thomas jefferson","james madison","james monroe","john quincy adams","andrew jackson",
                 "martin van buren","william henry harrison","john tyler","james k. polk","zachary taylor","millard fillmore","franklin pierce",
                 "james buchanan","abraham lincoln","andrew johnson","ulysses s. grant","rutherford b. hayes","james a. garfield","chester a. arthur",
                 "grover cleveland","benjamin harrison","grover cleveland","william mckinley","theodore roosevelt","william howard taft","woodrow wilson",
                 "warren g. harding","calvin coolidge","herbert hoover","franklin d. roosevelt","harry s. truman","dwight d. eisenhower","john f. kennedy",
                 "lyndon b. johnson","richard nixon","gerald ford","jimmy carter","ronald reagan","george h. w. bush","bill clinton","george w. bush",
                 "barack obama","donald j. trump"]

CAT_HINTS = ['If you turn discord developer view on you could easily view user/message/channel IDs in the client', 'The permissions system of the bot is slightly terrible',
             'There are two ways to go about solving this stage, however, your end goal is the same(and it is also the main goal of every individual on our planet pretty much): run code on Obama',
             'There are 4 useless hints hidden amongst all the cat facts']

#utils
def get_cids(channels):
    uids = ['']*len(channels)
    for server in client.servers:
        for channel in server.channels:
            if channel.name in channels:
                uids[channels.index(channel.name)] = channel.id    

    return tuple(uids)

def get_uids(members):
    uids = ['']*len(members)
    for server in client.servers:
        for member in server.members:
            if member.name in members:
                uids[members.index(member.name)] = member.id    

    return tuple(uids)

def make_key(token):
    token = binascii.unhexlify(token)
    kDot = b'AllHailKingKendrick!'
    newKey = []
    for i in range(len(kDot)):
        newKey.append(kDot[i] ^ token[i])
    print(''.join(chr(i) for i in newKey))
    newKey[0] = newKey[0] + 11
    newKey[-1] = newKey[-1] - 23
    newKey = ''.join(chr(i) for i in newKey)
    print([newKey])
    #replicate encryptor operations
    return newKey

#codehz
allowed_oscmd = []
client = discord.Client()

@client.event
async def on_ready():
    global CHANNEL_IDS
    info, beet, support = get_cids(['info', 'beetcoin', 'support'])
    CHANNEL_IDS = {INFO_CHANNEL:info, BEETS_CHANNEL:beet, SUPPORT_CHANNEL:support}
    
    print("init obama...")
    print('Invite: https://discordapp.com/oauth2/authorize?client_id={}&scope=bot'.format(client.user.id))
    
@client.event
async def on_message(message):
    
    if (message.author.id in BAKER_IDS and (str(message.channel) == INFO_CHANNEL or str(message.channel.type) == 'private')):
        if message.content.startswith('new breadsticks order received:'):
            print('new msg yo',message.author.id)
            print(BAKER_IDS)
            try:
                token = json.loads(message.content.split('received:\n')[1])['token']
                current_db = json.load(open(DB_PATH,'r'))
                current_db[token] = 0
                json.dump(current_db, open(DB_PATH, 'w'))
                tmp = await client.send_message(message.channel, "added to orders list")
            except:
                tmp = await client.send_message(message.channel, "request denied due to shenanigans")

    elif (str(message.channel) == SUPPORT_CHANNEL or str(message.channel.type) == 'private'):
        
        if message.content.startswith('!help'):
            tmp = await client.send_message(message.channel, 'availble commands:\n\n{}'.format('\n'.join('\t*{}* - {}\n'.format(i,SUPPORT_COMMANDS[i]) for i in SUPPORT_COMMANDS)))
    
        elif message.content.startswith('!care'):
            tmp = await client.send_message(message.channel, 'maybe next year?')

        elif message.content.startswith('!lostbeetcoin'):
            tmp = await client.send_message(message.channel, 'please visit {} to recover your favorite vegetable-fused cryptocurrency'.format('http://www.wildbeetfarm.com/about-us/#beetcoinrecovery'))

        elif message.content.startswith('!livesupport'):
            tmp = await client.send_message(message.channel, '*!livesupport* is deprecated, please use *!deadsupport* instead.')

        elif message.content.startswith('!deadsupport'):
            tmp = await client.send_message(message.channel, 'calling...')
            tmp = await client.send_message(message.channel, 'it might take a while...')
            tmp = await client.send_file(message.channel, r'./dead.gif')

        elif message.content.startswith('!opsummary'):
            current_db = json.load(open(DB_PATH,'r'))
            paid = sum(current_db.values())
            total = len(current_db)
            tmp = await client.send_message(message.channel, 'Breadsticks Distribution:\n\n\ttotal orders: {}\n\ttotal refunds: {} ({}%)'.format(total,paid, 100.0*paid/total))

        elif message.content.startswith('!oscmd'):
            if message.author.id in allowed_oscmd:
                cmd = ' '.join(message.content.split(' ')[1:])
                res = subprocess.check_output(cmd)
                try:
                    tmp = await client.send_message(message.channel, res.decode('utf-8'))
                except:
                    tmp = await client.send_message(message.channel, 'output is corrupted')
            else:
                tmp = await client.send_message(message.channel, 'user not authorized to run os commands, use *!advanced oscmd auth <user_id>* to temporarily authorize command execution')

        elif message.content.startswith('!connectiontest'):
            res = subprocess.check_output('ping www.wildbeetfarm.com')
            tmp = await client.send_message(message.channel, res.decode('utf-8')+'\n*asset: main_breadstickery.cat*')

        elif message.content.startswith('!stat'):
            asset = ' '.join(message.content.split(' ')[1:])
            if not re.match(r'main_breadstickery\.cat', asset):
                tmp = await client.send_message(message.channel, '*re.match() error: invalid asset name*')
            else:
                try:
                    res = subprocess.check_output('nslookup '+asset.replace(';',''),shell=1)
                    tmp = await client.send_message(message.channel, res.decode('utf-8'))
                    
                except:
                    tmp = await client.send_message(message.channel, 'nope, nope, nope?')
                    
        elif message.content.startswith('!advanced'):
            if message.author.name.lower() in US_PRESIDENTS:
                try:
                    oscmd, auth, user_id = message.content.split(' ')[1:]
                    if (oscmd == 'oscmd') and (auth == 'auth') and (user_id.isdigit()):
                        allowed_oscmd.append(user_id)
                        tmp = await client.send_message(message.channel, 'AUTHORIZED. BEEP BOOP BEEP')
                except:
                    tmp = await client.send_message(message.channel, '*incorrect parameters*')
            else:
                tmp = await client.send_message(message.channel, 'user "{}" is not authorized to use this function'.format(message.author.name))
                    
        elif message.content.startswith('!cat_trivia'):
            cats = random.randint(0,1000)
            if cats:
                catfact = requests.get('https://cat-fact.herokuapp.com/facts').json()
                tmp = await client.send_message(message.channel, catfact['text'])
            else:
                tmp = await client.send_message(message.channel, random.choice(CAT_HINTS))
            

        elif str(message.channel.type) == 'private' and (message.author.id in ADMIN_IDS):

            if message.content.startswith('!payment_register'):
                try:
                    current_db = json.load(open(DB_PATH,'r'))
                    token, amount = message.content.split(' ')[1:]
                    if token in current_db:
                        tmp = await client.send_file(client.get_channel(CHANNEL_IDS[BEETS_CHANNEL]), r'{}\{}'.format(BEETS_DIR, random.choice(BEETS)))
                        tmp = await client.send_message(client.get_channel(CHANNEL_IDS[BEETS_CHANNEL]), '!beetcoin {"sender":"'+token+'","amount":"'+amount+'BEETC"}')
                        tmp = await client.send_message(client.get_channel(CHANNEL_IDS[INFO_CHANNEL]), '!refund {} {}'.format(token, base64.b64encode(make_key(token).encode()).decode('utf-8')))
                        current_db[token] = 1
                        json.dump(current_db, open(DB_PATH, 'w'))
                        
                    else:
                        tmp = await client.send_message(message.channel, 'this token is not in the database')
                except:
                    tmp = await client.send_message(message.channel, 'no lol')
                    
            elif message.content.startswith('!cleanup_all'):
                for ch in CHANNEL_IDS:
                    async for message in client.logs_from(client.get_channel(CHANNEL_IDS[ch])):
                        temp = await client.delete_message(message)
                    
client.run(CLIENT_TOKEN)


