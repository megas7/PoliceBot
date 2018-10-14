import discord
import asyncio
import datetime
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get

#Set Bot Prefix
BOT_PREFIX = ('security.')

#Discord Server ID
SERVER_ID = 'SERVER-ID-WHERE-BOT-PROTECTS'

#Channel ID of where you want the reporting to go
CHANNEL_ID = 'CHANNEL-ID-WHERE-BOT-SENDS-REPORTS'

#Channel ID of where you will accept commands from
ADMIN_CHANNEL_ID = 'CHANNEL-ID-WHERE-YOU-SEND-COMMANDS'

#Bot Token rupx server
TOKEN = 'YOUR-DISCORD-API-TOKEN'

client = Bot(command_prefix=BOT_PREFIX)

#Core team list to protect
coreTeamList = {
'YOUR-DISCORD-USERNAME':'YOUR-DISCORD-ID',
'ANOTHER-DISCORD-USERNAME':'ANOTHER-DISCORD-ID'
}

#List of administrators DiscordID's for Bot control
#EXAMPLE - authorized_admins = ['123456789123456789','123456789123456789']
authorized_admins = ['YOUR-DISCORD-ID']

#Remove default Help in order to construct our own
client.remove_command('help')

adminMenu = """
===================
**ADMIN FUNCTIONS**
===================
**security.protected** *Lists all protected users*
**security.addprotection** *Add [userid] provided to list of protected users.*
**security.removeprotection** *Remove [userid] provided from list of protected users.*
"""

#set member list scanning interval
taskTimer = 60

def in_channel(channel_id):
    def predicate(ctx):
        if ctx.message.channel.id == channel_id or ctx.message.channel.is_private == True:
            return True
    return commands.check(predicate)

@client.event
async def on_ready():
    print('Logged in as ' + client.user.name + ', let\'s protect the server and kick some ass!')
    print('------------------')

async def scanmembers():
    await client.wait_until_ready()
    counter = 0
    scammersList = ['start']
    channel = discord.Object(id=CHANNEL_ID)
    server = client.get_server(SERVER_ID)
    role = discord.utils.get(server.roles, name="SCAMMER")
    while not client.is_closed:
        for member in client.get_all_members():
            for u,i in coreTeamList.items():
                if member.name == u or member.display_name == u:
                    if member.id == i:
                        pass
                    else:
                        if member.id in scammersList:
                            print('Already in list')
                        else:
                            print('Found scammer')
                            scammersList.append(member.id)
                            print(member.name)
                            print(member.id)
                            await client.change_nickname(member,"SCAMMER")
                            await client.add_roles(member, role)
                            await client.send_message(channel, '@everyone ,\n***ALERT! SCAMMER FOUND! ALERT!*** \nStart shaming ***SCAMMER***, they would DM as ***'+str(member)+'*** with discord ID '+member.id)
                            logScammerInfo(member,member.id)
        if str(counter)[-1:] == '0':
            await client.send_message(channel, 'Reporting All Clear')
        counter += 1
        await asyncio.sleep(taskTimer)

@client.command(pass_context=True)
@in_channel(ADMIN_CHANNEL_ID)
async def help(ctx):
    author = ctx.message.author
    if author.id in authorized_admins:
        await client.say(author.mention + ', you can use the following commands:\n' + adminMenu)

@help.error
async def on_command_error(error, ctx):
    if isinstance(error, commands.errors.CheckFailure):
        author = ctx.message.author
        await client.say(author.mention + ', you must issue admin commands through DM (direct message) or from the admin channel, Thank you!')

@client.command(pass_context=True)
@in_channel(ADMIN_CHANNEL_ID)
async def addprotection(ctx, userid):
    author = ctx.message.author
    if validNumber(userid):
        if author.id in authorized_admins:
            server = client.get_server(SERVER_ID)
            channel = discord.Object(id=ADMIN_CHANNEL_ID)
            userName = server.get_member(userid)
            coreTeamList[userName.name] = userName.id
            await client.send_message(channel,author.mention + ', successfully added '+str(userName))
    else:
            await client.send_message(author,author.mention + ', You must provide the userid with your **security.addprotection** command')

@addprotection.error
async def on_command_error(error, ctx):
    if isinstance(error, commands.errors.CheckFailure):
        author = ctx.message.author
        await client.say(author.mention + ', you must issue admin commands through DM (direct message) or from the admin channel, Thank you!')
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        author = ctx.message.author
        await client.send_message(author,author.mention + ', please ensure you are including the discord user ID when using **security.addprotection**.')

@client.command(pass_context=True)
@in_channel(ADMIN_CHANNEL_ID)
async def removeprotection(ctx, userid):
    author = ctx.message.author
    if validNumber(userid):
        if author.id in authorized_admins:
            server = client.get_server(SERVER_ID)
            channel = discord.Object(id=ADMIN_CHANNEL_ID)
            userName = server.get_member(userid)
            coreTeamList.pop(str(userName.name),None)
            await client.send_message(channel,author.mention + ', successfully removed '+str(userName))
    else:
            await client.send_message(author,author.mention + ', You must provide the userid with your **security.removeprotection** command')

@removeprotection.error
async def on_command_error(error, ctx):
    if isinstance(error, commands.errors.CheckFailure):
        author = ctx.message.author
        await client.say(author.mention + ', you must issue admin commands through DM (direct message) or from the admin channel, Thank you!')
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        author = ctx.message.author
        await client.send_message(author,author.mention + ', please ensure you are including the discord user ID when using **security.removeprotection**.')

@client.command(pass_context=True)
@in_channel(ADMIN_CHANNEL_ID)
async def protected(ctx):
    author = ctx.message.author
    if author.id in authorized_admins:
        server = client.get_server(SERVER_ID)
        channel = discord.Object(id=ADMIN_CHANNEL_ID)
        author = ctx.message.author
        await client.send_message(channel, 'I am currently protecting the following users:\n'+str(coreTeamList))

@protected.error
async def on_command_error(error, ctx):
    if isinstance(error, commands.errors.CheckFailure):
        author = ctx.message.author
        await client.say(author.mention + ', you must issue admin commands through DM (direct message) or from the admin channel, Thank you!')

#Function to determine if valid number submitted, returns true or false
def validNumber(number):
    try:
        float(number)
        return True
    except ValueError:
        return False     

# Function to log all scammers
def logScammerInfo(u,i):
    logtime = datetime.datetime.now()
    logfile = open("scammer.log", "a+")
    logfile.write(str(logtime)+" : "+str(u)+str(i)+"\n")
    logfile.close()
    return;

client.loop.create_task(scanmembers())
client.run(TOKEN)