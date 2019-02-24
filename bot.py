import matplotlib
matplotlib.use('Agg')
from discord.ext import commands
from discord.utils import get
from pylab import *
import random
import asyncio
import datetime
import json
import logging
import re
import os
commandPrefix = '*'
bot = commands.Bot(command_prefix=commandPrefix)

logging.basicConfig(filename="catoBot.log", level=logging.INFO)

maxVotes = {"vote": 1,
            "consul": 2,
            "senator": 3,
            "centurion": 5}
emojis = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫',
          '🇬', '🇭', 'ℹ', '🇯', '🇰', '🇱',
          '🇲', '🇳', '🇴', '🇵', '🇶', '🇷',
          '🇸', '🇹']
letters = ['A', 'B', 'C', 'D', 'E', 'F',
           'G', 'H', 'I', 'J', 'K', 'L',
           'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T']

ruleList = ['Rule 1: Enacted 13/8/18\n' +
            'Usage of, “The N-Word”, as well as usage of its variants, is not permitted, with the exception of the variation, “nibba” for humorous purposes.\n',
            'Rule 2: Enacted 13/8/18\n' +
            'The video game, “Fortnite”, and all media and other objects related to it must be destroyed.\n',
            'Rule 3: Enacted 13/8/18\n' +
            'All barbarian peoples are forbidden from entering the Roman Province.\n',
            'Rule 4: Enacted 13/8/18\n' +
            'The city of Carthage, its holdings, and its allies must be destroyed.\n',
            'Rule 5: Enacted 15/8/18\n' +
            'Any media deemed, “Not Safe For Work”, may only be posted on the, “NSFW”, channel.\n',
            'Rule 6: Enacted 24/8/18\n' +
            'Roman citizens must behave and act in accordance to their status as members of the providence: civilized.\n',
            'Rule 7: Enacted 30/8/18\n' +
            'Any Roman citizen apprehended engaging in Fortnite-related activities is to be sentenced to exile from the Roman providence.\n',
            'Rule 8: Enacted 31/8/18\n' +
            'In accordance with the ideals of the Pax Romana, all racism within the Empire is forbidden, excluding that which pertains to barbarian peoples.\n',
            'Rule 9: Enacted 2/9/2018\n' +
            'All political subjects are confined to #politics due to the controversy that this posses.\n',
            'Rule 10: Enacted  3/9/2018\n' +
            'Continued harassment to other members of our community will not be tolerated.\n',
            'Rule 11: Enacted 14/9/2018\n' +
            'The act of civil revolts and and instigations of civil war is punishable by death  to protect the safety of the empire.\n',
            'Rule 12: Enacted 21/9/2018\n' +
            'Any member of a foreign community in the premises of rome can use the #alliance channel for discussion of international policies\n',
            'Rule 13: Enacted 29/9/2018\n' +
            'All political extremism is banned from our glorious empire\n',
            'Rule 14: Enacted 2/10/2018\n' +
            'Political parties are not allowed in the empire due to the  damage and anarchy they can cause.\n',
            'Rule 15: Enacted 29/10/2018\n'
            'The time zone that is to be used for official  matters will be GMT and Senate meetings will be held every Saturday at 8pm GMT.\n',
            'Rule 16: Enacted 17/11/2018\n'
            'Unsolicited advertising of gens will not be allowed through private channels, such as DMs.\n',
            'Rule 17: Enacted 8/12/2018\n'
            'Any citizen proposing insincere motions will be demoted by one rank.\n',
            'Rule 18: Enacted 3/1/2019\n'
            'Any attempt of electoral fraud is strictly forbidden.']

@bot.event
async def on_ready():
    print('bot is ready')
    await my_background_task()

async def my_background_task():
    await bot.wait_until_ready()
    channel = bot.get_channel('476871636277264385')
    while not bot.is_closed:
        if datetime.date.today().strftime("%A") == "Saturday" and datetime.datetime.now().strftime("%H:%M:%S") == "20:00:00":
            await bot.send_message(channel, "@everyone our weekly senate meeting commences now")
            await asyncio.sleep(1)
        else:
            await asyncio.sleep(1)

@bot.event
async def on_message(msg):
    content = msg.content
    response = ''
    words = content.split(' ')
    if not msg.author.id == '502181308483633152' and re.search(r'[0-9]+ .*', content):
        for i in range(1, len(words)):
            if re.search(r'inch', words[i]) and re.match(r'-?([0-9]\.)*[0-9]+', words[i-1]):
                value = convert(words[i], float(words[i-1]))
                response += words[i-1] + " " + words[i] + ' -> ' + str(value)[:5] + ' cm.\n'
            if re.match(r'f(ee)?t', words[i]) and re.match(r'-?([0-9]\.)*[0-9]+', words[i-1]):
                value = convert(words[i], float(words[i - 1]))
                response += words[i - 1] + " " + words[i] + ' -> ' + str(value)[:5] + ' m.\n'
            if re.match(r'(((f|F)$)|((f|F) ))', words[i]) and re.match(r'-?([0-9]\.)*[0-9]+', words[i - 1]):
                value = convert(words[i], float(words[i - 1]))
                response += words[i - 1] + " " + words[i] + ' -> ' + str(value)[:5] + ' C.\n'
            if re.match(r'(lb|pounds)', words[i]) and re.match(r'-?([0-9]\.)*[0-9]+', words[i - 1]):
                value = convert(words[i], float(words[i - 1]))
                response += words[i - 1] + " " + words[i] + ' -> ' + str(value)[:5] + ' kg.\n'
            if re.match(r'mile', words[i]) and re.match(r'-?([0-9]\.)*[0-9]+', words[i - 1]):
                value = convert(words[i], float(words[i - 1]))
                response += words[i - 1] + " " + words[i] + ' -> ' + str(value)[:5] + ' km.\n'
            if re.match(r'freedom', words[i]) and re.match(r'-?([0-9]\.)*[0-9]+', words[i - 1]):
                value = random.randint(1, 100000)
                units = ['m', 'kg', 'V', 'C', 'mol', 's']
                index = random.randint(0, 5)
                response += words[i - 1] + " " + words[i] + ' -> ' + str(value)[:5] + ' ' + units[index] + '.\n'
        await bot.send_message(msg.channel, response)
    elif not msg.author.id == '502181308483633152' and re.search(r'[0-9]+(a|A|p|P)[mM] [a-zA-Z]', content):
        for i in range(1, len(words)):
            if re.match(r'(CET|cet)', words[i]) and re.match(r'[0-9]+(a|A|p|P)[mM]', words[i - 1]):
                value = convertTimezone(words[i], words[i - 1])
                response += words[i - 1] + " " + words[i] + ' -> ' + value + ' UTC.\n'
            if re.match(r'(CST|cst)', words[i]) and re.match(r'[0-9]+(a|A|p|P)[mM]', words[i - 1]):
                value = convertTimezone(words[i], words[i - 1])
                response += words[i - 1] + " " + words[i] + ' -> ' + value + ' UTC.\n'
            if re.match(r'(EST|est)', words[i]) and re.match(r'[0-9]+(a|A|p|P)[mM]', words[i - 1]):
                value = convertTimezone(words[i], words[i - 1])
                response += words[i - 1] + " " + words[i] + ' -> ' + value + ' UTC.\n'
        await bot.send_message(msg.channel, response)
    else:
        await bot.process_commands(msg)

def makeChart(input, h1):
    figure(1, figsize=(6, 6))
    clf()
    ax = axes([0.1, 0.1, 0.8, 0.8])

    # The slices will be ordered and plotted counter-clockwise.
    labels = input.keys()
    fracs = input.values()

    pie([float(f) for f in fracs], labels=labels,
        autopct='%1.1f%%', shadow=False, startangle=90)
    # The default startangle is 0, which would start
    # the Frogs slice on the x-axis.  With startangle=90,
    # everything is rotated counter-clockwise by 90 degrees,
    # so the plotting starts on the positive y-axis.

    title(h1, bbox={'facecolor': '0.8', 'pad': 5})

    savefig("foo.png")

@bot.command(pass_context = True)
async def votechart(ctx):
    with open('results.json') as f:
        results = json.load(f)
    makeChart(results, "Vote")
    await bot.send_file(ctx.message.channel, "foo.png")

def convert(freedomUnit, value):
    if re.match(r'inch', freedomUnit):
        return value/0.39370
    if re.match(r'f(ee)?t', freedomUnit):
        return value*0.3048
    if re.match(r'(((f|F)$)|((f|F) ))', freedomUnit):
        return (value - 32.0) / 1.8
    if re.match(r'(lb|pounds)', freedomUnit):
        return value/ 2.2046
    if re.match(r'mile', freedomUnit):
        return value / 0.62137

def convertTimezone(zone, value):
    time24h = 0
    if re.match(r'(p|P)[mM]', value[len(value)-2:]):
        time24h = int(value[:1]) + 12
    else:
        time24h = int(value[:1])
    if re.match(r'(CET|cet)', zone):
        time24h -= 1
    if re.match(r'(CST|cst)', zone):
        time24h += 6
    if re.match(r'(EST|est)', zone):
        time24h += 5

    return str(time24h) + ':00'

def isHigherUp(role):
    return  role == 'Imperator' or role == 'Consul' or role == 'Senator' or role == 'Centurion' or role == 'Heir to the Emperorship' or role == 'Dictator' or role == 'Praefectus' or role == 'Legatus'

@bot.event
async def on_member_join(member):
    role = get(member.server.roles, name="Roman Subject")
    await bot.add_roles(member, role)

@bot.event
async def on_reaction_add(reaction, user):
    if not user.id == '502181308483633152':
        with open('userids.json') as f:
            userids = json.load(f)
        channel = reaction.message.channel
        with open('voteID.txt', 'r') as f:
            text = f.read()
            voteId = text.split('|')[0]
            voteType = text.split('|')[1]
        candidates = []
        with open('elections.txt', 'r') as file:
            for line in file.readlines():
                if line.startswith(voteType):
                    candidates.append(line[(len(voteType)+3):].strip('\n'))
        if voteId == reaction.message.id:
            print(userids.keys())
            if user.id not in userids.keys():
                print(user.id)
                with open('userids.json', 'w') as f:
                    userids[user.id] = []
                    json.dump(userids, f)
            for i in range(len(emojis)):
                if reaction.emoji == emojis[i]:

                    if candidates[i] not in userids[user.id] and len(userids[user.id]) < maxVotes[voteType]:
                        print('reached this point')
                        with open('results.json') as f:
                            results = json.load(f)
                        results[candidates[i]] = results[candidates[i]] + 1
                        await bot.remove_reaction(reaction.message, reaction.emoji, user)
                        with open('userids.json', 'w') as f:
                            print(candidates[i])
                            userids[user.id].append(candidates[i])
                            json.dump(userids, f)
                        scoreboard = '```python\n'
                        for i in range(len(candidates)):
                            scoreboard = scoreboard + candidates[i] + ' has ' + str(results[candidates[i]]) + ' votes. (' + letters[i] + ')\n'
                        scoreboard = scoreboard + '```'
                        await bot.edit_message(await bot.get_message(channel, voteId), scoreboard)
                        with open('results.json', 'w') as f:
                            json.dump(results, f)
            if voteType == 'vote' and len(userids[user.id]) < 1:
                if reaction.emoji == '✅':
                    with open('results.json') as f:
                        results = json.load(f)
                    results['aye'] = results['aye'] + 1
                    await bot.remove_reaction(reaction.message, reaction.emoji, user)
                    await bot.edit_message(await bot.get_message(channel, voteId), '```python\n' +
                            str(results['aye']) + ' romans have voted AYE. (✅)\n' +
                            str(results['nay']) + ' romans have voted NAY. (❎)\n'
                            '```')
                    with open('userids.json', 'w') as f:
                        userids[user.id].append('aye')
                        json.dump(userids, f)
                elif reaction.emoji == '❎':
                    with open('results.json') as f:
                        results = json.load(f)
                    results['nay'] = results['nay'] + 1
                    await bot.remove_reaction(reaction.message, reaction.emoji, user)
                    await bot.edit_message(await bot.get_message(channel, voteId), '```python\n' +
                            str(results['aye']) + ' romans have voted AYE. (✅)\n' +
                            str(results['nay']) + ' romans have voted NAY. (❎)\n'
                            '```')
                    with open('userids.json', 'w') as f:
                        userids[user.id].append('nay')
                        json.dump(userids, f)
                with open('results.json', 'w') as f:
                    json.dump(results, f)

@bot.command(pass_context = True)
async def commands(ctx):
    await bot.say('```\n' +
            commandPrefix + 'commands - overview of all commands\n' +
            commandPrefix + 'procedures - overview of all procedures\n' +
            commandPrefix + 'conquer - procedure to conquer a discord\n' +
            commandPrefix + 'absence - procedure for what to do in case of hihger-up absence\n' +
            commandPrefix + 'spy - procedure for what to do when a spy is found\n' +
            commandPrefix + 'rule [X] - shows rule number [X]\n' +
            commandPrefix + 'rules - gives an overview of all rules\n' +
            commandPrefix + 'motion - propose a motion to the senate\n' +
            commandPrefix + 'motions - gives an overview of the currently unresolved motions\n' +
            commandPrefix + 'resolve [X] - resolves the motion with the ID = [X], it will no longer be visible with "' + commandPrefix + 'motions" but the motion will still be logged. Only Centurions or higher can execute this command\n' +
            commandPrefix + 'resolve all - resolves all standing motions. Only to be used at the end of senate meeting by higher ups\n' +
            commandPrefix + 'register [X] -  register yourself for the election of position [X] use actual positions with lower case letters (centurion, senator, consul)\n' +
            commandPrefix + 'register [X] [Y] - as a higher-up, register another member [Y] for the elections of position [X]\n' +
            commandPrefix + 'unregister [X] - unregister yourself for the election of postion [X] *only unregister yourself for postions you were previously registered with*\n' +
            commandPrefix + 'unregister [X] "[Y]" - as a higher-up, unregister another member [Y] who registered for position [X]. make sure to put " around the name and don\'t @ them\n' +
            commandPrefix + 'unregister all - as a higher-up, unregister all current candidates *to be used sparingly. preferably only after elections\n' +
            commandPrefix + 'candidates - view all candidates registered for each position\n' +
            commandPrefix + 'elections [X] - creates a vote for the elections of role [X]\n' +
            commandPrefix + 'vote [X] - vote Aye or Nay on the motion with id [X]\n' +
            commandPrefix + 'gens - gives a list of all members in each gens\n'
                            '```')

    if str(ctx.message.channel) == "temple-of-jupiter-optimus-maximus":
            await bot.say( '**secret commands**\n' +
                    commandPrefix + 'docs - gives the link to the docs\n' +
                    commandPrefix + 'suggestions - returns all suggestions meant for you')
@bot.command()
async def procedures():
    await bot.say(commandPrefix  + 'conquer - procedure to conquer a discord\n' +
        commandPrefix + 'absence - procedure for what to do in case of higher-up absence\n' +
            commandPrefix + 'spy - procedure for what to do when a spy is found\n')

@bot.command(pass_context = True)
async def gens(ctx):
    members = ctx.message.server.members
    resultMsg = ''
    gens = {}
    for member in members:
        for role in member.roles:
            if role.name.startswith('Gens'):
                if role.name not in gens.keys():
                    gens[role.name] = []
                newMembers = gens[role.name]
                newMembers.append(member.name)
                gens[role.name] = newMembers
    for key in gens.keys():
        resultMsg += '__***' + key + '***__\n'
        for familyMember in gens[key]:
            resultMsg += familyMember + '\n'
    await bot.say(resultMsg)

@bot.command(pass_context = True)
async def elections(ctx):
    if isHigherUp(ctx.message.author.top_role.name):
        msg = ctx.message.content
        voteType = ''
        if re.search(r'consul', msg):
            voteType = 'consul'
        if re.search(r'senator', msg):
            voteType = 'senator'
        if re.search(r'centurion', msg):
            voteType = 'centurion'
        candidates = []
        with open('elections.txt', 'r') as file:
            for line in file.readlines():
                if line.startswith(voteType):
                    candidates.append(line[(len(voteType) + 3):].strip('\n'))
        emptyDict = {}
        emptyResultsDict = {}
        for candidate in candidates:
            emptyResultsDict[candidate] = 0
        with open('userids.json', 'w') as f:
            json.dump(emptyDict, f)
        with open('results.json', 'w') as f:
            json.dump(emptyResultsDict, f)
        scoreboard = '```python\n'
        for i in range(len(candidates)):
            scoreboard = scoreboard + candidates[i] + ' has 0 votes. (' + letters[i] + ')\n'
        scoreboard = scoreboard + '```'
        msg = await bot.say(scoreboard)
        voteId = msg.id + '|' + voteType
        with open('voteID.txt', 'w') as f:
            f.write(voteId)
        for i in range(len(candidates)):
            await bot.add_reaction(msg, emojis[i])
    else:
        await bot.say('You are not authorised to organise a vote. Speak to a higher-up to organise a vote')

@bot.command(pass_context = True)
async def register(ctx):
    top_role = ctx.message.author.top_role.name
    print(top_role)
    if isHigherUp(top_role) or top_role == 'Explorator' or top_role == 'Marinus' or top_role == 'Legionnaire' \
            or top_role == 'Roman Citizen' or top_role == 'Cabbage Farmer' or top_role == 'Frumentarius':
        msg = str(ctx.message.content)
        if re.search(r'@', msg) and (isHigherUp(top_role)):
            member = (await bot.get_user_info(msg.split('@')[1].split('>')[0])).name
            role = msg[10:].split(' ')[0]

            text = role + ' : ' + member
            if role == 'consul' or role == 'senator' or role == 'centurion':
                with open('elections.txt', 'a') as file:
                    file.write(text + '\n')
                await bot.say('The following candidate has been registered:\n' + text)
            else:
                await bot.say('That\'s not a viable role!\n'
                              'Type `*register consul`, `*register senator` or `*register centurion`')
        elif not re.search(r'@', msg):
            member = (await bot.get_user_info(str(ctx.message.author.id))).name
            role = msg[10:]
            text = role + ' : ' + member
            canregister = False
            if role == 'consul':
                if isHigherUp(top_role):
                    canregister = True
                else:
                    canregister = False
            elif role == 'senator':
                if isHigherUp(top_role) or top_role == 'Explorator' or top_role == 'Marinus' or top_role == 'Legionnaire' or top_role == 'Cabbage Farmer' or top_role == 'Frumentarius':
                    canregister = True
                else:
                    canregister = False
            elif role == 'centurion':
                print("centurion")
                canregister = True
            if canregister:
                if role == 'consul' or role == 'senator' or role == 'centurion':
                    with open('elections.txt', 'a') as file:
                        file.write(text + '\n')
                    await bot.say('The following candidate has been registered:\n' + text)
                else:
                    await bot.say('That\'s not a viable role!\n'
                                  'Type `*register consul`, `*register senator` or `*register centurion`')
            else:
                await bot.say('You are not eligible for this position!')
        elif not isHigherUp(top_role):
            print('this shouldn\'t happen')
            await bot.say('You are not authorised to register other users for elections')
    else:
        await bot.say('You are not eligible for this position!')

@bot.command(pass_context = True)
async def unregister(ctx):
    top_role = ctx.message.author.top_role.name
    if re.search(r'all', str(ctx.message.content)):
        if isHigherUp(top_role):
            open('elections.txt', 'w').close()
            await bot.say('removed all candidates')
        else:
            await bot.say('you do not have the authority to unregister other candidates')
    else:
        msg = str(ctx.message.content)
        member = (await bot.get_user_info(str(ctx.message.author.id))).name
        role = msg[12:].split(' ')[0]
        error = False
        if re.search(r'"', msg):
            if isHigherUp(top_role):
                member = msg[12:].split('"')[1].split('"')[0]
            else:
                error = True
        if not error:
            text = role + ' : ' + member + '\n'
            newlines = []
            with open('elections.txt', 'r') as file:
                lines = file.readlines()
            with open('elections.txt', 'w') as file:
                for line in lines:
                    if not line.startswith(text):
                        print(text)
                        print(line)
                        newlines.append(line)
                file.writelines(newlines)
            await bot.say(member + ' is no longer running for ' + role)
        else:
            await bot.say('you are not authorised to unregister other users')
@bot.command()
async def candidates():
    consuls = '__***consular elections***__\n'
    senators = '__***senatorial elections***__\n'
    centurions = '__***centurion elections***__\n'
    with open('elections.txt', 'r') as file:
        for line in file.readlines():
            if line.startswith('consul'):
                consuls += line[9:]
            elif line.startswith('senator'):
                senators += line[10:]
            elif line.startswith('centurion'):
                centurions += line[12:]
    await bot.say(consuls + '\n' +
            senators + '\n' +
            centurions + '\n' +
            '__***Consuls are only elected every other electoral cycle***__')

@bot.command(pass_context = True)
async def vote(ctx):
    top_role = ctx.message.author.top_role.name
    if isHigherUp(top_role):
        id = int(str(ctx.message.content)[6:].lstrip())
        motion = ''
        with open("motions.txt", 'r') as file:
            for line in file:
                if '#' + str(id) + ' ' in line:
                    motion = line.split(' : ')[1]
                    print(motion)
        emptyDict = {}
        emptyResultsDict = {"aye": 0, "nay": 0}
        with open('userids.json', 'w') as f:
            json.dump(emptyDict, f)
        with open('results.json', 'w') as f:
            json.dump(emptyResultsDict, f)
        await bot.say('__***' + motion + '***__')
        msg = await bot.say('```python\n' +
                            '0 romans have voted AYE. (✅)\n' +
                            '0 romans have voted NAY. (❎)\n'
                            '```')
        voteId = msg.id + '|vote'
        with open('voteID.txt', 'w') as f:
            f.write(voteId)
        await bot.add_reaction(msg, '✅')
        await bot.add_reaction(msg, '❎')
    else:
        await bot.say('You are not authorised to organise a vote. Speak to a higher-up to organise a vote')

@bot.command(pass_context = True)
async def motion(ctx):
    msg = str(ctx.message.content)[8:]
    num_lines = sum(1 for line in open('motions.txt'))
    num_lines += sum(1 for line in open('resolved.txt'))
    id = num_lines + 1
    motion = '#' + str(id) + ' | ' + str(ctx.message.author) + ' @ ' + \
             ctx.message.timestamp.strftime('%d/%m/%Y %H:%M:%S') + ' : ' + msg + '\n'
    with open('motions.txt', 'a') as file:
        file.write(motion)
    print(motion)
    # logging.info(motion)
    await bot.say("Motion is noted. view all motions with the [*motions] command")
@bot.command(pass_context = True)
async def resolve(ctx):
    top_role = ctx.message.author.top_role.name
    index = str(ctx.message.content)
    index = index.split(' ')[1]
    if index == 'all':
        lines = []
        with open('motions.txt', 'r') as file:
            for line in file:
                if '#' not in line:
                    lines.append(line)
                if '#' in line:
                    with open('resolved.txt', 'a') as file:
                        file.write(line)
        with open('motions.txt', 'w') as file:
            file.writelines(lines)
        await bot.say('All motions are resolved.')
    else:
        resolvedMotion = ''
        index = int(index)
        lines = []
        with open('motions.txt', 'r') as file:
            for line in file:
                if '#' + str(index) not in line:
                    lines.append(line)
                if '#' + str(index) in line:
                    resolvedMotion = line
        owner = resolvedMotion.split(' ')[2]
        user = str(ctx.message.author)
        if isHigherUp(top_role) or owner == user:
            with open('resolved.txt', 'a') as file:
                file.write(resolvedMotion)
            with open('motions.txt', 'w') as file:
                file.writelines(lines)
            await bot.say("Motion is resolved.")
        else:
            await bot.say("You do not have the authority to resolve this motion")
@bot.command()
async def motions():
    motions = {}
    with open("motions.txt", 'r') as file:
        for line in file:
            motions[str(line[1:].split(' | ')[0])] = line
    if len(motions) == 0:
        await bot.say('There are no standing motions right now')
    allMotions = ""
    keyList = motions.keys()
    keyList = sorted(keyList)
    for i in keyList:
        allMotions += motions[i]
    await bot.say(allMotions)
# @bot.command(pass_context = True)
# async def resolved():
#     motions = {}
#     with open("catoBot.log", 'r') as file:
#         for line in file:
#             if "resolve" in line:
#                 motions[str(line.split('#')[1].split(' | ')[0])] = line[10:]
#     for i in motions:
#         await bot.say(motions[i])

@bot.command(pass_context = True)
async def rule(ctx):
    index = str(ctx.message.content)
    index = int(index[5:].lstrip()) - 1
    await bot.say("```python\n" + ruleList[index] + "```")
@bot.command()
async def rules():
    output = ''
    for rule in ruleList:
        output += rule
    await bot.say("```python\n" + output + "```")
@bot.command(pass_context = True)
async def docs(ctx):
    if str(ctx.message.channel) == "temple-of-jupiter-optimus-maximus":
        await bot.say("https://drive.google.com/drive/folders/1W7A4sExEJCjSOEt4UFz-flP7JSH99ORS?usp=sharing")
    else:
        await bot.say("This information is top secret")

@bot.command(pass_context = True)
async def suggestion(ctx):
    msg = str(ctx.message.content)
    content = ''
    for i in msg[12:].split(' ')[1:]:
        content += i + ' '
    suggestion = 'suggestion for ' + msg[12:].split(' ')[0] + ' : ' + content
    print(suggestion)
    with open('suggestions.txt', 'a') as file:
        file.write(suggestion + '\n')
    await bot.say('suggestion is noted')

@bot.command(pass_context = True)
async def suggestions(ctx):
    mySuggestions = ''
    author = ctx.message.author.name
    with open('suggestions.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if re.search('\[everyone]', line):
                mySuggestions += line
            if re.search(author.split(' ')[0], line):
                mySuggestions += line
    await bot.say(mySuggestions)

@bot.command()
async def conquer():
    await bot.say('**Rough romans will attempt to conquer a discord server and establish a province if said server is yielded over after a war or coup d’etat. The following steps will be taken to turn the server from a chaotic, leaderless server to a flourishing province of roma:**\n' +
                  '**1.** The emperor, 1 of the consuls, or the dictator will receive ownership from the conquered barbarians and will be the de facto ruler of the discord for the time being\n' +
                  '**2.** Meanwhile, in roma, 2 polls will take place: firstly, the vote for who will be the governor of the conquered province, and what the province will be named as. Both polls will be considered closed after 1 hours\n' +
                  '**3.** The server name will be changed and the server icon will receive a “romanized” version\n' +
                  '**4.** The current ruler of the province will hand over the server to the elected governor\n' +
                  '**5.** Trouble-makers will be banned\n' +
                  '**6.** Free passage between the newly subjugated province will be made available once the trouble-makers are gone to facilitate assimilation\n' +
                  '**7.** For the next few days, romans will be posting cross-over memes regularly to integrate their culture with that of roma and to romanize their server without appearing to be unreasonable\n' +
                  '__***The intent of establishing a province is NOT to appear oppressive and take their home away from them. They should be heavily encouraged to continue to post their own memes. Establishing a province should look more like a happy union of 2 servers rather than a total and cruel subjugation to roma***__')

@bot.command()
async def absence():
    await bot.say('**To avoid chaos in case one of the higher ups leaves, unexpectedly or not, the following guidelines will be followed. I’ll split them up in whether there is a plan for return or whether they will step down forever. If someone is inactive for 2 full weeks, they will be considered as resigned**\n' +
                  '**In case there are plans for return:**\n' +
                  '\tImperator    ->     appoints a dictator to act in his absence (citizens and subjects are not eligible for dictatorship)\n' +
                  '\tConsul       ->     the residing co-consul will be de facto ruler alongside the imperator\n' +
                  '\tSenator      ->     no need for replacements\n')

    await bot.say('**In case there are no plans for return:**\n'
                  '\tImperator    ->    the imperator will always have an heir. Current order of succession:\n' +
                  '\t\tUncreative Human\n' +
                  '\t\tPesa\n' +
                  '\tConsul       ->     consular elections are planned instantly (preferably within 24 hours). The residing co-consul will oversee the elections. 1 new consul will be elected to serve alongside the remaining co-consul until the end of his consular term (even if this is only a week).' +
                  'If the consular term ends in less than 48 hours, there will be no election until the end of the term. In this case the residing co-consul will be the de facto leader alongside the imperator.\n' +
                  '\tSenator      ->   No action will be taken unless only half of the senatorial seats are filled. If this is the case, the spots will be filled with the current centurions (which centurions take the positions will be decided amongst the higher-ups)')
@bot.command()
async def spy():
    await bot.say('**Spies can pose a serious threat to our discord. They should be dealt with as fast as possible while simultaneously avoiding banning innocent romans. This procedure will focus on maximising damage control and giving the accused the ability to defend themselves.**\n' +
                  '**1.** A rough roman notices suspicious behavior and suspects a member to be a spy\n' +
                  '**2.** The loyal roman will report this (via DM to avoid mass panic) to the praetorian guard (ideally the head of the guard) or, if none are online/don’t respond in time, the highest available higher-up will be informed\n' +
                  '**3.** Upon receiving the report, the higher-up will use his best judgement to assess the situation. If the case has no supporting evidence or is fueled by personal hatred, the case is ignored. If there is even a small chance of it being a real spy, his ranks will be taken away as soon as possible(to avoid further intel being gathered from the exclusive channels) and he will notify the other #higher-ups\n' +
                  '**4.** His case will be held in #courts as soon as a consul hears about the issue where he may defend himself.\n' +
                  '**5.** In case he is proven innocent, he will be awarded his old ranks back and will receive a formal apology from the suspecting roman, the higher-up who demoted him and the consul who oversaw the case. If he is proven guilty, he will be banned from the discord\n' +
                  '**6.** If it is revealed who the culprit is spying for, they will be added to potential future war targets if they aren’t already. No rash decisions will be taken on the matter. Only the senate may declare war. It is a very real possibility that the spy was acting as a rogue agent')
bot.run(os.environ.get('TOKEN'))

# values = dict(question = motion, a0 = 'Aye', a1 = 'Nay')
#         url = 'https://strawpoll.com/new'
#         data = parse.urlencode(values)
#         data = data.encode('utf-8')
#         req = request.Request(url, data)
#         req.add_header("Content-type", "application/x-www-form-urlencoded")
#         with request.urlopen(req) as response:
#             the_page = response.read().decode('utf-8')
#         list = re.findall(r'https://strawpoll.com/.*\"', the_page)
#         await bot.say(list[0][:-1])
#     else:
#         await bot.say('You are not authorised to organise a vote. Speak to a higher-up to organise a vote')
