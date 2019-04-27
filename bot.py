import matplotlib
matplotlib.use('Agg')
import discord
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

from objects.motion import Motion
from objects.election import Election
from services.motionService import MotionService
from services.electionService import ElectionService

commandPrefix = '*'
bot_id = 559469690812891138
bot = commands.Bot(command_prefix=commandPrefix)
motion_service = MotionService()
election_service = ElectionService()

eligible_for = {"consul": ['Cabbage Farmer', 'Imperator', 'Consul', 'Senator', 'Centurion', 'Heir to the Emperorship'],
                "senator": ['Cabbage Farmer', 'Imperator', 'Consul', 'Senator', 'Centurion', 'Heir to the Emperorship', 'Marinus', 'Legionnaire', 'Explorator'],
                "centurion": ['Cabbage Farmer', 'Imperator', 'Consul', 'Senator', 'Centurion', 'Heir to the Emperorship', 'Marinus', 'Legionnaire', 'Explorator', 'Roman Citizen']}


maxVotes = {"vote": 1,
            "consul": 2,
            "senator": 4,
            "centurion": 5}
emojis = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫',
          '🇬', '🇭', 'ℹ', '🇯', '🇰', '🇱',
          '🇲', '🇳', '🇴', '🇵', '🇶', '🇷',
          '🇸', '🇹']
letters = ['A', 'B', 'C', 'D', 'E', 'F',
           'G', 'H', 'I', 'J', 'K', 'L',
           'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T']

@bot.event
async def on_ready():
    print('bot is ready')
    motion_service = MotionService()
    election_service = ElectionService()
    await my_background_task()

@bot.command()
async def logout():
    await bot.logout()


async def my_background_task():
    await bot.wait_until_ready()
    channel = bot.get_channel(559359387009941524)
    while not bot.is_closed():
        if datetime.date.today().strftime("%A") == "Saturday" and datetime.datetime.now().strftime("%H:%M:%S") == "21:00:00":
            await channel.send("@everyone our weekly senate meeting commences now")
            await asyncio.sleep(1)
        else:
            await asyncio.sleep(1)

@bot.event
async def on_message(msg):
    content = msg.content
    response = ''
    words = content.split(' ')
    if not msg.author.id == bot_id and re.search(r'[0-9]+ .*', content):
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
        await msg.channel.send(response)
    elif not msg.author.id == bot_id and re.search(r'[0-9]+(a|A|p|P)[mM] [a-zA-Z]', content):
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
        await msg.channel.send(response)
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

def has_role(user, role):
    return role in [str(user_role) for user_role in user.roles]
def has_one_of_roles(user, roles):
    for role in roles:
        if has_role(user, role):
            return True
    return False

@bot.command(pass_context = True)
async def votechart(ctx):
    with open('results.json') as f:
        results = json.load(f)
    makeChart(results, "Vote")
    await ctx.message.channel.send(file="foo.png")

@bot.command(pass_context = True)
async def power(ctx):
    power = {}
    message = ctx.message.content
    members = ctx.message.guild.members
    if message == '*power':
        for member in members:
            for role in member.roles:
                if role.name.startswith('Imperator'):
                    for gens in member.roles:
                        if gens.name.startswith('Gens'):
                            if gens.name not in power.keys():
                                power[gens.name] = 0
                            power[gens.name] = power[gens.name] + 7
                if role.name.startswith('Consul'):
                    for gens in member.roles:
                        if gens.name.startswith('Gens'):
                            if gens.name not in power.keys():
                                power[gens.name] = 0
                            power[gens.name] = power[gens.name] + 5
                if role.name.startswith('Senator'):
                    for gens in member.roles:
                        if gens.name.startswith('Gens'):
                            if gens.name not in power.keys():
                                power[gens.name] = 0
                            power[gens.name] = power[gens.name] + 3
                if role.name.startswith('Centurion'):
                    for gens in member.roles:
                        if gens.name.startswith('Gens'):
                            if gens.name not in power.keys():
                                power[gens.name] = 0
                            power[gens.name] = power[gens.name] + 1
        makeChart(power, "Distribution of higher ups")
        await ctx.message.channel.send(file=discord.File("foo.png"))

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
    return  role == 'Cabbage Farmer' or role == 'Imperator' or role == 'Consul' or role == 'Senator' or role == 'Centurion' or role == 'Heir to the Emperorship' or role == 'Dictator' or role == 'Praefectus' or role == 'Legatus'
# def is_higher_up(user):
#     return has_role('Cabbage')
@bot.event
async def on_member_join(member):
    for role in member.server.roles:
        if role.name == "Roman Subject":
            await member.add_roles(role)

@bot.event
async def on_raw_reaction_add(payload):
    print(payload.user_id)
    print(bot_id)
    if not payload.user_id == bot_id:
        user_ids = {}
        with open('userids.json', 'r') as f:
            user_ids = json.load(f)
        if str(payload.emoji) == '✅':
            for identifier in user_ids.keys():
                print(user_ids[identifier]['id'])
                await motion_service.vote(bot, payload, identifier, user_ids[identifier]['id'], 'aye')
        elif str(payload.emoji) == '❌':
            for identifier in user_ids.keys():
                print(user_ids[identifier]['id'])
                await motion_service.vote(bot, payload, identifier, user_ids[identifier]['id'], 'nay')
        elif str(payload.emoji) in emojis:
            for identifier in user_ids.keys():
                id = user_ids[identifier]['id']
                election = election_service.get_election(user_ids[identifier]['id'])
                for i in range(0, len(emojis)):
                    if emojis[i] == str(payload.emoji):
                        await election_service.vote(bot, payload, identifier, user_ids[identifier]['id'], list(election.candidates.keys())[i])

@bot.command()
async def getjson(ctx):
    await ctx.send(file=discord.File("motions.json"))
    await ctx.send(file=discord.File("resolved.json"))
    await ctx.send(file=discord.File("elections.json"))
    await ctx.send(file=discord.File("userids.json"))
@bot.command(pass_context = True)
async def commands(ctx):
    await ctx.channel.send('```\n' +
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
            await ctx.message.channel.send( '**secret commands**\n' +
                    commandPrefix + 'docs - gives the link to the docs\n' +
                    commandPrefix + 'suggestions - returns all suggestions meant for you')
@bot.command()
async def procedures(ctx):
    await ctx.send(commandPrefix  + 'conquer - procedure to conquer a discord\n' +
        commandPrefix + 'absence - procedure for what to do in case of higher-up absence\n' +
            commandPrefix + 'spy - procedure for what to do when a spy is found\n')

@bot.command(pass_context = True)
async def gens(ctx):
    members = ctx.message.guild.members
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
    await ctx.channel.send(resultMsg)

@bot.command(pass_context = True)
async def setup(ctx):
    msg = ctx.message.content
    arr = msg.split(' ')
    id = arr[1] + '-' + arr[2]
    position = arr[1]
    time = arr[2]

    election = Election(id=id,
                        position=position,
                        candidates={})
    election_service.add_election(election)

    await ctx.channel.send(position + ' elections will take place at the end of ' + arr[2])
@bot.command(pass_context = True)
async def elections(ctx):
    allowed_roles = ['Cabbage Farmer', 'Imperator', 'Consul', 'Senator', 'Centurion', 'Heir to the Emperorship']
    if has_one_of_roles(ctx.message.author, allowed_roles):
        msg = ctx.message.content
        id = msg.split(' ')[1]
        election = election_service.get_election(id)
        await election.setup_vote(bot, ctx)
    else:
        await ctx.channel.send('You are not authorised to organise a vote. Speak to a higher-up to organise a vote')

@bot.command(pass_context = True)
async def register(ctx):
    user = ctx.message.author.name
    msg = ctx.message.content
    if len(msg.split(' ')) == 1:
        await ctx.channel.send('please specify for which election you\'d like to register f.ex. `*register consul-nov18`')
    elif msg.split(' ')[1] not in election_service.election_dict.keys():
        await ctx.channel.send('That\'s not a valid election id')
    else:
        election = election_service.get_election(msg.split(' ')[1])
        if has_one_of_roles(ctx.message.author, eligible_for[election.position]):
            election_service.register(election.id, user)
            await ctx.channel.send(ctx.message.author.mention + ' has been registered as a candidate for the ' + election.position + ' elections of ' + election.id.split('-')[1])
        else:
            await ctx.channel.send('You are not eligible for the position of ' + election.position)

@bot.command(pass_context = True)
async def unregister(ctx):
    user = ctx.message.author.name
    msg = ctx.message.content
    if len(msg.split(' ')) == 1:
        await ctx.channel.send('please specify for which election you\'d like to unregister f.ex.`*unregister consul-nov18`')
    elif msg.split(' ')[1] not in election_service.election_dict.keys():
        await ctx.channel.send('That\'s not a valid election id')
    election = election_service.get_election(msg.split(' ')[1])
    election_service.unregister(election.id, user)
    await ctx.channel.send(ctx.message.author.mention + ' has been unregistered as a candidate for the ' + election.position + ' elections of ' + election.id.split('-')[1])

@bot.command(pass_context = True)
async def candidates(ctx):
    print(ctx.message.content.split(' '))
    id = ctx.message.content.split(' ')[1]
    if '-' not in id:
        embed = discord.Embed(title='Elections for ' + id, description="", color=0x00ff00)
        embed = add_election_field_to_embed(embed, id, 'consul')
        embed = add_election_field_to_embed(embed, id, 'senator')
        embed = add_election_field_to_embed(embed, id, 'centurion')
    else:
        embed = discord.Embed(title='Elections for ' + id, description="", color=0x00ff00)
        for key in election_service.election_dict.keys():
            if id in key:
                role = key.split('-')[0]
                candidates = ''
                keylist = sorted(election_service.get_election(key).candidates.keys())
                for candidate in keylist:
                    candidates += candidate + '\n'
                embed.add_field(name=role, value=candidates, inline=False)
    embed.set_footer(text='Consuls are only elected every other electoral cycle')
    await ctx.channel.send(embed=embed)

def add_election_field_to_embed(embed, id, position):
    candidates = ''
    keylist = sorted(election_service.get_election(position + '-' + id).candidates.keys())
    for candidate in keylist:
        candidates += candidate + '\n'
    embed.add_field(name=position, value=candidates, inline=False)
    return embed

@bot.command(pass_context = True)
async def vote(ctx):
    if isHigherUp(ctx.message.author.top_role.name):
        id = str(ctx.message.content)[6:].lstrip()
        await motion_service.get_motion(id).setup_vote(bot, ctx)
    else:
        await ctx.channel.send('You are not authorised to organise a vote. Speak to a higher-up to organise a vote')

@bot.command(pass_context = True)
async def motion(ctx):
    currentmotion = Motion(id=motion_service.generate_id(),
                            content=str(ctx.message.content)[8:],
                            author=str(ctx.message.author),
                            created_at=str(ctx.message.created_at.strftime('%d/%m/%Y %H:%M:%S')))
    motion_service.add(currentmotion)
    await ctx.channel.send("Motion is noted. View all motions with the [*motions] command")

@bot.command(pass_context = True)
async def resolve(ctx):
    index = str(ctx.message.content).split(' ')[1]
    if index == 'all':
        motion_service.resolve_all()
        await ctx.channel.send('All motions are resolved.')
    else:
        user = str(ctx.message.author)
        owner = Motion(motion_service.get_motion(str(index))).author
        top_role = ctx.message.author.top_role.name
        if isHigherUp(top_role) or owner == user:
            motion_service.resolve(index)
            await ctx.channel.send("Motion is resolved.")
        else:
            await ctx.channel.send("You do not have the authority to resolve this motion")
@bot.command()
async def motions(ctx):
    response = motion_service.get_motions_embed()
    if len(response.fields) == 0:
        await ctx.send('There are no standing motions right now')
    else:
        await ctx.send(embed=response)

@bot.command(pass_context = True)
async def docs(ctx):
    if str(ctx.message.channel) == "temple-of-jupiter-optimus-maximus":
        await ctx.message.channel.send("https://drive.google.com/drive/folders/1W7A4sExEJCjSOEt4UFz-flP7JSH99ORS?usp=sharing")
    else:
        await ctx.message.channel.send("This information is top secret")

@bot.command()
async def conquer(ctx):
    await ctx.send('**Rough romans will attempt to conquer a discord server and establish a province if said server is yielded over after a war or coup d’etat. The following steps will be taken to turn the server from a chaotic, leaderless server to a flourishing province of roma:**\n' +
                  '**1.** The emperor, 1 of the consuls, or the dictator will receive ownership from the conquered barbarians and will be the de facto ruler of the discord for the time being\n' +
                  '**2.** Meanwhile, in roma, 2 polls will take place: firstly, the vote for who will be the governor of the conquered province, and what the province will be named as. Both polls will be considered closed after 1 hours\n' +
                  '**3.** The server name will be changed and the server icon will receive a “romanized” version\n' +
                  '**4.** The current ruler of the province will hand over the server to the elected governor\n' +
                  '**5.** Trouble-makers will be banned\n' +
                  '**6.** Free passage between the newly subjugated province will be made available once the trouble-makers are gone to facilitate assimilation\n' +
                  '**7.** For the next few days, romans will be posting cross-over memes regularly to integrate their culture with that of roma and to romanize their server without appearing to be unreasonable\n' +
                  '__***The intent of establishing a province is NOT to appear oppressive and take their home away from them. They should be heavily encouraged to continue to post their own memes. Establishing a province should look more like a happy union of 2 servers rather than a total and cruel subjugation to roma***__')

@bot.command()
async def absence(ctx):
    await ctx.send('```'
                  '**To avoid chaos in case one of the higher ups leaves, unexpectedly or not, the following guidelines will be followed. I’ll split them up in whether there is a plan for return or whether they will step down forever. If someone is inactive for 2 full weeks, they will be considered as resigned**\n' +
                  '**In case there are plans for return:**\n' +
                  '\tImperator    ->     appoints a dictator to act in his absence (citizens and subjects are not eligible for dictatorship)\n' +
                  '\tConsul       ->     the residing co-consul will be de facto ruler alongside the imperator\n' +
                  '\tSenator      ->     no need for replacements\n'
                  '```')

    await ctx.send('```'
                  '**In case there are no plans for return:**\n'
                  '\tImperator    ->    the imperator will always have an heir. Current order of succession:\n' +
                  '\tConsul       ->     consular elections are planned instantly (preferably within 24 hours). The residing co-consul will oversee the elections. 1 new consul will be elected to serve alongside the remaining co-consul until the end of his consular term (even if this is only a week).' +
                  'If the consular term ends in less than 48 hours, there will be no election until the end of the term. In this case the residing co-consul will be the de facto leader alongside the imperator.\n' +
                  '\tSenator      ->   No action will be taken unless only half of the senatorial seats are filled. If this is the case, the spots will be filled with the current centurions (which centurions take the positions will be decided amongst the higher-ups)'
                  '```')
@bot.command()
async def spy(ctx):
    await ctx.send('**Spies can pose a serious threat to our discord. They should be dealt with as fast as possible while simultaneously avoiding banning innocent romans. This procedure will focus on maximising damage control and giving the accused the ability to defend themselves.**\n' +
                  '**1.** A rough roman notices suspicious behavior and suspects a member to be a spy\n' +
                  '**2.** The loyal roman will report this (via DM to avoid mass panic) to the praetorian guard (ideally the head of the guard) or, if none are online/don’t respond in time, the highest available higher-up will be informed\n' +
                  '**3.** Upon receiving the report, the higher-up will use his best judgement to assess the situation. If the case has no supporting evidence or is fueled by personal hatred, the case is ignored. If there is even a small chance of it being a real spy, his ranks will be taken away as soon as possible(to avoid further intel being gathered from the exclusive channels) and he will notify the other #higher-ups\n' +
                  '**4.** His case will be held in #courts as soon as a consul hears about the issue where he may defend himself.\n' +
                  '**5.** In case he is proven innocent, he will be awarded his old ranks back and will receive a formal apology from the suspecting roman, the higher-up who demoted him and the consul who oversaw the case. If he is proven guilty, he will be banned from the discord\n' +
                  '**6.** If it is revealed who the culprit is spying for, they will be added to potential future war targets if they aren’t already. No rash decisions will be taken on the matter. Only the senate may declare war. It is a very real possibility that the spy was acting as a rogue agent')
bot.run(os.environ.get('TOKEN'))
