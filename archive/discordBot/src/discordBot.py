# This example requires the 'members' and 'message_content' privileged intents to function.
 
import discord
from discord.ext import commands
import os
from io import StringIO
from contextlib import redirect_stdout
from dotenv import load_dotenv

load_dotenv() 
 
 
description = "A basic bot to run Python code."
 
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
 
bot = commands.Bot(command_prefix="?", description=description, intents=intents)
 
 
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
 
 
@bot.command()
async def run(ctx, *codeList):
    """Run Python code."""
 
    try:
        code = " ".join(codeList)
        code = code.strip("`")
        code = code.strip()
        print(code)                     # for debugging
        f = StringIO()
        with redirect_stdout(f):
 
            # For code to execute, it must contain single-quotes (') only
            # or escaped double-quotes (\")
            # For multiline code, each line must end with a semicolon (;)
            exec(code) 
 
        result = f.getvalue()
        await ctx.send(f"Output: {result}")
    except Exception as e:
        await ctx.send(f"Error: {e}")
 
 
@bot.command()
async def version(ctx):
    """Get the bot's version."""
 
    await ctx.send("Version 1.0")
 
 
bot.run(os.getenv("TOKEN"))
