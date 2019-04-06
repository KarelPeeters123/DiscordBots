import json

from chart import Chart
class Election:
    def __init__(self, id=None, position=None, candidates=None, json=None):
        if json is not None:
            self.id = json['id']
            self.position = json['position']
            self.candidates = json['candidates']
        else:
            self.id = id
            self.position = position
            self.candidates = candidates
        self.emojis = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫',
                  '🇬', '🇭', 'ℹ', '🇯', '🇰', '🇱',
                  '🇲', '🇳', '🇴', '🇵', '🇶', '🇷',
                  '🇸', '🇹']
        self.maxVotes = {"vote": 1,
                    "consul": 2,
                    "senator": 4,
                    "centurion": 5}

    def register(self, user):
        self.candidates[user] = 0
    def unregister(self, user):
        del self.candidates[user]

    async def setup_vote(self, bot, ctx):
        embed = await Chart(self.candidates, 'Election: ' + str(self.id)).get_embed(bot, election=self)
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
        counter = 0
        for key in self.candidates.keys():
            await msg.add_reaction(self.emojis[counter])
            counter += 1

    def can_vote(self, payload, vote_id, selected):
        user_ids = {}
        with open('userids.json', 'r') as f:
            user_ids = json.load(f)
        if str(payload.user_id) not in user_ids[vote_id]['votes'].keys():
            user_ids[vote_id]['votes'][str(payload.user_id)] = []
        if selected in user_ids[vote_id]['votes'][str(payload.user_id)]:
            return False
        return len(user_ids[vote_id]['votes'][str(payload.user_id)]) < self.maxVotes[self.position]

    async def vote(self, bot, payload, vote_id, selected):
        self.candidates[selected] += 1
        user_ids = {}
        with open('userids.json', 'r') as f:
            user_ids = json.load(f)
        if str(payload.user_id) not in user_ids[vote_id]['votes'].keys():
            user_ids[vote_id]['votes'][str(payload.user_id)] = []
        print(user_ids[vote_id]['votes'])
        user_ids[vote_id]['votes'][str(payload.user_id)].append(selected)
        with open('userids.json', 'w') as f:
            json.dump(user_ids, f, indent=4)
        await (await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)).remove_reaction(payload.emoji, bot.get_user(payload.user_id))
        embed = await Chart(self.candidates, 'Election: ' + str(self.id)).get_embed(bot, election=self)
        await (await bot.get_channel(payload.channel_id).fetch_message(vote_id)).edit(embed=embed)
