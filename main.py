# -*- coding: utf-8 -*-

###########
# Imports #
###########

import json
import discord
from discord.ext import commands
import game
import random
import asyncio


################
# Setup part 1 #
################


def get_prefix(my_client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    my_client.number = 2
    return prefixes[str(message.guild.id)]


token = open("token.txt", "r").readlines()[0]
client = commands.Bot(command_prefix=get_prefix, help_command=None)


################
# Setup part 2 #
################


@client.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "-"
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Connect 4"))
    print("Online")


@client.event
async def on_message(msg):
    if not msg.guild and msg.author != client.user:
        pass

    elif msg.mentions and msg.mentions[0] == client.user:
        await help(msg)

    await client.process_commands(msg)


#############
# Functions #
#############


def emotify(n: int) -> str:
    if n == 0:
        return ":black_circle:"
    if n == 1:
        return ":red_circle:"
    if n == 2:
        return ":yellow_circle:"


############
# Commands #
############


@client.command()
@commands.has_permissions(administrator=True)
async def prefix(ctx, new_prefix):
    """To change the prefix of the bot in a server"""
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = new_prefix
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f)

    await ctx.send(f"My new prefix here is `{new_prefix}` :slight_smile:")


@client.command()
async def punch(ctx, *, new_punch):
    """To add a punchline to your wins"""
    with open("punch.json", "r") as f:
        punchs = json.load(f)
    punchs[str(ctx.message.author.id)] = new_punch
    with open("punch.json", "w") as f:
        json.dump(punchs, f)
    await ctx.message.add_reaction("\u2705")


@client.command()
async def ping(ctx):
    """Gives the ping of the bot"""
    await ctx.send(f"My current ping is : {client.latency * 1000} ms")


@client.command()
async def board(ctx):
    """Shows an empty board for now"""
    empty_board = game.Game(None, None)
    description = "​"
    for row in empty_board.board:
        line = "　"
        for element in row:
            line += emotify(element) + "　"
        description += line + "\n \n"
    description += ":one:　:two:　:three:　:four:　:five:　:six:　:seven:"
    embed = discord.Embed(title="Here's an empty board", color=0x2f3136, description=empty_board.get_embed())
    await ctx.send(embed=embed)


@client.command()
async def play(ctx):
    t = game.Game(ctx.message.author.id, client.user.id)
    message = await ctx.send(embed=discord.Embed(title=f"Random game", color=0x2f3136, description=t.get_embed()))

    while t.ongoing:
        n = random.randint(0, 6)
        t.play(n)
        await message.edit(embed=discord.Embed(title=f"Random game", color=0x2f3136, description=t.get_embed()))
        await asyncio.sleep(1)

    embed = discord.Embed(title=f"Random generated game", color=0x2f3136)
    embed.add_field(name="Congratulations", value=f"{emotify(t.winner.sprite)}  won the game !")
    await message.edit(embed=embed)


@client.command(aliases=["chall"])
async def challenge(ctx, user: discord.Member, *, bullshit=None):
    author = ctx.message.author
    t = game.Game(author.id, user.id)
    message = await ctx.send(embed=discord.Embed(
        title=f"{author.display_name} Versus {user.display_name}", color=0x2f3136, description=t.get_embed()))

    while t.ongoing:
        n = random.randint(0, 6)
        t.play(n)
        await message.edit(embed=discord.Embed(
            title=f"{author.display_name} Versus {user.display_name}", color=0x2f3136, description=t.get_embed()))
        await asyncio.sleep(1)

    embed = discord.Embed(title=f"{author.display_name} Versus {user.display_name}", color=0x2f3136)
    embed.add_field(name=f"Congratulations {emotify(t.winner.sprite)}", value=f"<@{t.winner.id}>  won the game !")

    with open("punch.json", "r") as f:
        punchs = json.load(f)
        try:
            embed.set_footer(text=f'"{punchs[str(t.winner.id)]}"')
        except:
            pass

    await message.edit(embed=embed)


@client.command()
async def help(ctx):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    cur_prefix = prefixes[str(ctx.guild.id)]

    embed = discord.Embed(title="Help page", color=0x2f3136, description=f"My prefix here is {cur_prefix}")
    embed.add_field(name="help", value="Shows this menu")
    embed.add_field(name="prefix", value="To change the prefix of the bot")
    embed.add_field(name="play", value="Watch a game played randomly by bots")
    embed.add_field(name="challenge + @...", value="Place your bet on a game against a friend \
                                                    to prove you're better than them")
    embed.add_field(name="punch + ...", value="Adds your punchline to your wins, write None to reset")
    embed.set_footer(text="This bot was made by ThePotatoPvP#9893. Dm for any questions.")
    await ctx.channel.send(embed=embed)


client.run(token)
