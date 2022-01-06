# This example requires the 'members' privileged intents

import discord
import random
import uuid
import time

# get command line args
import sys
CONFIGFILE = sys.argv[1]
DATABASE_PATH = sys.argv[2]

# get configuration file
import json
CONFIG = json.load(open(CONFIGFILE,'r'))
AUTHORIZATION_TOKEN = CONFIG['token']

# create database connection
import sqlite3
conn = sqlite3.connect(DATABASE_PATH)

########################################################################
#
# FUNCTION: runQuery(sql,ctx)
# function to extract the data from the raw message class to a dict
#
########################################################################
def runQuery(sql,ctx):
    c = ctx.cursor()
    c.execute(sql)
    return c.fetchall()


########################################################################
#
# FUNCTION: commitQuery(sql,ctx)
# function to extract the data from the raw message class to a dict
#
########################################################################
def commitQuery(sql,ctx):
    c = ctx.cursor()
    c.execute(sql)
    ctx.commit()
    return c.fetchall()

########################################################################
#
# FUNCTION: getActiveChannelIDs
# function to extract the data from the raw message class to a dict
#
########################################################################
def getActiveChannelIDs(ctx):
    sql = f'''select distinct channel_id
        from channels
        where active = True
    '''
    return runQuery(sql,ctx)[0]

########################################################################
#
# FUNCTION: getActiveServerIDs
# function to extract the data from the raw message class to a dict
#
########################################################################
def getActiveServerIDs(cursor):
    sql = f'''select distinct guild_id
        from servers
        where active = True
    '''
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    print(fetchall)

########################################################################
#
# FUNCTION: discordMessageToDict
# function to extract the data from the raw message class to a dict
#
########################################################################
def discordMessageToDict(message):
    # init variables
    message_id = None
    channel_name = None
    channel_id = None
    category_id = None
    author_name = None
    author_id = None
    author_bot = None
    guild_name = None
    guild_id = None
    guild_size = None
    message_body = None

    # exception handling for each variable
    try:
        message_id  = message.id
    except:
        pass
    try:
        channel  = message.channel.name
    except:
        pass
    try:
        channel_id = message.channel.id
    except:
        pass
    try:
        category_id = message.channel.category_id
    except:
        pass
    try:
        author_name = message.author.name
    except:
        pass
    try:
        author_id = message.author.id
    except:
        pass
    try:
        author_bot = message.author.bot
    except:
        pass
    try:
        guild_name = message.guild.name
    except:
        pass
    try:
        guild_id  = message.guild.id
    except:
        pass
    try:
        guild_size = message.guild.member_count
    except:
        pass
    try:
        message_body = message.content
    except:
        pass
    try:
        # data with no errors
        return {
            'status':200,
            'status_message':'success',
            'message_id' : message_id,
            'channel' : channel,
            'channel_id': channel_id,
            'category_id': category_id,
            'author_name': author_name,
            'author_id': author_id,
            'author_bot': author_bot,
            'guild_name': guild_name,
            'guild_id' : guild_id,
            'guild_size': guild_size,
            'message_body': message_body
        }
    except Exception as e:
        # data if there is an error
        return {
            'status':400,
            'status_message':str(e),
            'message_id' : message_id,
            'channel' : channel,
            'channel_id': channel_id,
            'category_id': category_id,
            'author_name': author_name,
            'author_id': author_id,
            'author_bot': author_bot,
            'guild_name': guild_name,
            'guild_id' : guild_id,
            'guild_size': guild_size,
            'message_body': message_body
        }

########################################################################
#
# OPERATION: Create SQL tables
#
########################################################################

try:
    createTableQuery_channels = '''CREATE TABLE or REPLACE channels
                (date_added int, active bool, channel_name varchar, channel_id int, guild_name varchar, guild_id int)'''
    commitQuery(sql=createTableQuery_channels,ctx=conn)
except:
    print('[SQL] table CHANNELS already created.')
    pass
try:
    createTableQuery_messages = '''CREATE TABLE messages
                (timestamp int, uid varchar, message_body varchar, raw variant)'''
    commitQuery(sql=createTableQuery_messages,ctx=conn)
except:
    print('[SQL] table MESSAGES already created.')
    pass

# initialize discord client
client = discord.Client()

# handler for when connected to server
@client.event
async def on_ready():
    print('[DSC] logged into Discord as {0.user}'.format(client))

# handler for ANY MESSAGE sent to the server on ANY CHANNEL.
# ToDo: have users direct the bot to only grab data from specific channels.
@client.event
async def on_message(message):
    # only run iff in approved channel list
    if message.channel.id in getActiveChannelIDs(conn):
        # create a unique identifier for the event
        uid = str(uuid.uuid4()).replace('-','')
        
        # generate a timestamp
        timestamp = time.time()

        # generate data
        data = discordMessageToDict(message)
        dataJSON = json.dumps(data)

        # message body
        message_body = data['message_body']

        # store data to database
        sql = f'''insert into messages (
            timestamp,
            uid,
            message_body,
            raw
        ) values (
            '{timestamp}',
            '{uid}',
            '{message_body}',
            '{dataJSON}'
        )
        '''
        commitQuery(sql, conn)

        # print message to stdout
        print(f'[DSC] New message: {message_body}')


# main runtime
client.run(AUTHORIZATION_TOKEN)