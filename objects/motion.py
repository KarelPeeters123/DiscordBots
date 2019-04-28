import json
import discord
from discord.ext import commands
from discord.utils import get

from chart import Chart

class Motion:
    def __init__(self, id=None, content=None, author=None, created_at=None, json=None):
        if json is not None:
            self.id = json['id']
            self.content = json['content']
            self.author = json['author']
            self.created_at = json['created_at']
            self.result = json['result']
        else:
            self.id = id
            self.content = content
            self.author = author
            self.created_at = created_at
            self.result = {'aye':0, 'nay':0}


    def to_string(self):
        return self.author + '\n' + self.created_at + '\n' + self.content + '\naye: ' + str(self.result['aye']) + '\nnay: ' + str(self.result['nay'])

    async def setup_vote(self, bot, ctx):
        embed = await Chart(self.result, 'Vote: motion #' + str(self.id)).get_embed(bot, motion=self)
        msg = await ctx.channel.send(embed=embed)
        vote_id = str(msg.id)

        user_ids_json = {}
        try:
            with open('userids.json', 'r') as f:
                user_ids_json = json.load(f)
        except:
            print('file created')
        user_ids_json[vote_id] = {'id':self.id, 'votes':{}}
        with open('userids.json', 'w') as f:
            json.dump(user_ids_json, f, indent=4)

        await msg.add_reaction('✅')
        await msg.add_reaction('❌')

    def can_vote(self, payload, vote_id):
        print("votecheck")
        user_ids = {}
        with open('userids.json', 'r') as f:
            user_ids = json.load(f)
        print(user_ids[vote_id]['votes'].keys())
        return str(payload.user_id) not in user_ids[vote_id]['votes'].keys()

    async def vote(self, bot, payload, vote_id, selected):
        self.result[selected] += 1
        user_ids = {}
        with open('userids.json', 'r') as f:
            user_ids = json.load(f)
        user_ids[vote_id]['votes'][payload.user_id] = selected
        with open('userids.json', 'w') as f:
            json.dump(user_ids, f, indent=4)
        await (await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)).remove_reaction(payload.emoji, bot.get_user(payload.user_id))
        embed = await Chart(self.result, 'Vote: motion #' + str(self.id)).get_embed(bot, motion=self)
        # chartmsg = await bot.get_channel(549991724026691584).send(file=discord.File("foo.png"))
        # embed = discord.Embed(title='Votes for motion #' + str(self.id), description="", color=0x00ff00)
        # embed.set_image(url=chartmsg.attachments[0].url)
        # embed.add_field(name='aye ✅', value=self.result['aye'], inline=False)
        # embed.add_field(name='nay ❎', value=self.result['nay'], inline=False)
        await (await bot.get_channel(payload.channel_id).fetch_message(vote_id)).edit(embed=embed)
