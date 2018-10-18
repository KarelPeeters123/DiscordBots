from discord.ext import commands
import logging
TOKEN = 'NTAyMTgxMzA4NDgzNjMzMTUy.DqkN_Q.y1o0bR4kaMYh2J2-FWtkWBhRokw'

bot = commands.Bot(command_prefix='^')

logging.basicConfig(filename="catoBot.log", level=logging.INFO)

ruleList = ['Rule #1: Enacted 8/13/18\n' +
         'Usage of, “The N-Word”, as well as usage of its variants, is not permitted, with the exception of the variation, “nibba” for humorous purposes.\n',
         'Rule #2: Enacted 8/13/18\n' +
         'The video game, “Fortnite”, and all media and other objects related to it must be destroyed.\n',
         'Rule #3: Enacted 8/13/18\n' +
         'All barbarian peoples are forbidden from entering the Roman Province.\n',
         'Rule #4: Enacted 8/13/18\n' +
         'The city of Carthage, its holdings, and its allies must be destroyed.\n',
         'Rule #5: Enacted 8/15/18\n' +
         'Any media deemed, “Not Safe For Work”, may only be posted on the, “NSFW”, channel.\n',
         'Rule #6: Enacted 8/24/18\n' +
         'Roman citizens must behave and act in accordance to their status as members of the providence: civilized.\n',
         'Rule #7: Enacted 8/30/18\n' +
         'Any Roman citizen apprehended engaging in Fortnite-related activities is to be sentenced to exile from the Roman providence.\n',
         'Rule #8: Enacted 8/31/18\n' +
         'In accordance with the ideals of the Pax Romana, all racism within the Empire is forbidden, excluding that which pertains to barbarian peoples.\n',
         'Rule #9: Enacted 2/9/2018\n' +
         'All political subjects are confined to #politics due to the controversy that this posses.\n',
         'Rule #10:Enacted  3/9/2018\n' +
         'Continued harassment to other members of our community will not be tolerated.\n',
         'Rule #11: Enacted 14/9/2018\n' +
         'The act of civil revolts and and instigations of civil war is punishable by death  to protect the safety of the empire.\n',
         'Rule #12: Enacted 21/9/2018\n' +
         'Any member of a foreign community in the premises of rome can use the #alliance channel for discussion of international policies\n',
         'Rule #13: Enacted 29/9/2018\n' +
         'All political extremism is banned from our glorious empire\n',
         'Rule #14: Enacted 30/9/10\n' +
         'The  group known as "reclaimers" (users from r/reclaimtheholyland) are banned to enter the premises of Rome and execute public offices\n',
         'Rule #15: Enacted 2/10/2018\n' +
         'Political parties are not allowed in the empire due to the  damage and anarchy they can cause.\n']


@bot.event
async def on_ready():
    print('bot is ready')
    logging.info('bot is ready')
@bot.command(pass_context = True)
async def rule(ctx):
    index = str(ctx.message.content)
    index = int(index[5:].lstrip()) - 1
    await bot.say(ruleList[index])
@bot.command()
async def rules():
    output = ''
    for rule in ruleList:
        output += rule
    await bot.say(output)
@bot.command(pass_context = True)
async def docs(ctx):
        if str(ctx.message.channel) == "temple-of-jupiter-optimus-maximus":
            await bot.say("https://drive.google.com/drive/folders/1W7A4sExEJCjSOEt4UFz-flP7JSH99ORS?usp=sharing")
        else:
            await bot.say("This information is top secret")
@bot.command(pass_context = True)
async def commands(ctx):
    await bot.say('^ commands - overview of all commands\n' +
            '^ procedures - overview of all procedures\n' +
            '^ suggestion - gives a suggestion to the bot-owner (f.ex.: \'^ suggestion improve the layout on command x\')\n' +
            '^ conquer - procedure to conquer a discord\n' + 
            '^ absence - procedure for what to do in case of hihger-up absence\n' + 
            '^ spy - procedure for what to do when a spy is found\n\n')
    if str(ctx.message.channel) == "temple-of-jupiter-optimus-maximus":
            await bot.say( '**secret commands**\n' +
                    '^ docs - gives the link to the docs')            
@bot.command()
async def procedures():
    await bot.say('^ conquer - procedure to conquer a discord\n' +
        '^ absence - procedure for what to do in case of higher-up absence\n'
            '^ spy - procedure for what to do when a spy is found\n')
@bot.command(pass_context = True)
async def suggestion(ctx):
        suggestion = str(ctx.message.author) + ' : ' + str(ctx.message.content)
        print(suggestion)
        logging.info(suggestion)
        await bot.say('suggestion is noted')

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
                  '\t\tCreative Human\n' +
                  '\t\tPesa\n' +
                  '\t\tJustinian\n' +
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
bot.run(TOKEN)
