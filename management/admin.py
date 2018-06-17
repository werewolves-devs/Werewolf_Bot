from discord.ext import commands
from utils import game_masters_only, is_active, chunks

# TODO: GM-Only checks
class Admin:
    """Admin-only commands that make the bot dynamic."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @game_masters_only()
    async def load(self, ctx, *, module: str):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.channel.send('\N{PISTOL}')
            await ctx.channel.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.channel.send('\N{OK HAND SIGN}')

    @commands.command(hidden=True)
    @game_masters_only()
    async def unload(self, ctx, *, module: str):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await ctx.channel.send('\N{PISTOL}')
            await ctx.channel.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.channel.send('\N{OK HAND SIGN}')

    @commands.command(name='reload', hidden=True)
    @game_masters_only()
    async def _reload(self, ctx, *, module: str):
        """Reloads a module."""
        try:
            self.bot.unload_extension(module)
            print('\n\n\n--Extension restart: ' + module + '--\n\n\n')
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.channel.send('\N{PISTOL}')
            await ctx.channel.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.channel.send('\N{OK HAND SIGN}')


def setup(bot):
    bot.add_cog(Admin(bot))
