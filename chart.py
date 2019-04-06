import matplotlib
matplotlib.use('Agg')
import discord
from pylab import *
emojis = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫',
          '🇬', '🇭', 'ℹ', '🇯', '🇰', '🇱',
          '🇲', '🇳', '🇴', '🇵', '🇶', '🇷',
          '🇸', '🇹']
class Chart:
    def __init__(self, input, h1):
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

        savefig('foo.png')
    async def get_embed(self, bot, motion=None, election=None):
        if motion is not None:
            chartmsg = await bot.get_channel(549991724026691584).send(file=discord.File("foo.png"))
            embed = discord.Embed(title=motion.content, description="", color=0x00ff00)
            embed.set_image(url=chartmsg.attachments[0].url)
            embed.add_field(name='aye ✅', value=motion.result['aye'], inline=False)
            embed.add_field(name='nay ❌', value=motion.result['nay'], inline=False)
            return embed
        else:
            emojis = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫',
                      '🇬', '🇭', 'ℹ', '🇯', '🇰', '🇱',
                      '🇲', '🇳', '🇴', '🇵', '🇶', '🇷',
                      '🇸', '🇹']
            chartmsg = await bot.get_channel(549991724026691584).send(file=discord.File("foo.png"))
            embed = discord.Embed(title='election ' + election.id, description="", color=0x00ff00)
            embed.set_image(url=chartmsg.attachments[0].url)
            counter = 0
            for key in election.candidates.keys():
                embed.add_field(name=key + emojis[counter], value=election.candidates[key], inline=False)
                counter += 1
            # embed.add_field(name='aye ✅', value=motion.result['aye'], inline=False)
            # embed.add_field(name='nay ❌', value=motion.result['nay'], inline=False)
            return embed
