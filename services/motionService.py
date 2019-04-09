import json
import discord

from objects.motion import Motion

class MotionService:
    def __init__(self):
        self.read()

    def read(self):
        try:
            with open('motions.json', 'r') as f:
                self.motion_dict = json.load(f)
        except:
            self.motion_dict = {}
            self.write()
        try:
            with open('resolved.json', 'r') as f:
                self.resolved_dict = json.load(f)
        except:
            self.resolved_dict = {}
            self.write()
    def write(self):
        with open('motions.json', 'w') as f:
            json.dump(self.motion_dict, f, indent=4)
        with open('resolved.json', 'w') as f:
            json.dump(self.resolved_dict, f, indent=4)

    def add(self, motion):
        self.read()
        self.motion_dict[motion.id] = motion.__dict__
        self.write()

    def resolve(self, motion_id):
        self.read()
        self.resolved_dict[str(motion_id)] = self.motion_dict[str(motion_id)]
        del self.motion_dict[str(motion_id)]
        self.write()

    def resolve_all(self):
        for key in self.motion_dict.keys():
            self.resolve(key)

    def generate_id(self):
        return str(len(self.motion_dict) + len(self.resolved_dict) + 1)

    def get_motion(self, motion_id):
        return Motion(json=self.motion_dict[str(motion_id)])

    def get_motions_embed(self):
        embed=discord.Embed(title="Motions:", color=0x932092)
        for key in [str(mykey) for mykey in self.motion_dict.keys()].sort():
            motion = Motion(json=self.motion_dict[key])
            embed.add_field(name=motion.id, value=motion.to_string(), inline=False)
        return embed

    async def vote(self, bot, payload, vote_id, motion_id, selected):
        self.read()
        print(self.get_motion(motion_id).can_vote(payload, vote_id))
        if self.get_motion(motion_id).can_vote(payload, vote_id):
            await self.get_motion(motion_id).vote(bot, payload, vote_id, selected)
        self.write()
