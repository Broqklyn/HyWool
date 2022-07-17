# NOTICE! 
#
# The source code is 100% for educational purposes and it isn't meant 
# to be copied + pasted, we are under the "Eclipse Public License - v 2.0" 
# Please read the License file before hand or read the license here:
# https://www.eclipse.org/legal/epl-2.0/ 
#
# Only use this for educational purposes! :)

import json
import discord
import requests
import asyncio
from discord import Embed

from discord.ext import commands

bot = commands.Bot(command_prefix='!')

partners = [659665397389328405, 639958702748860423, 930945255166075000, 791942627268362290] #Servers

partnerNames = ["DaBqmb#0001", "Expiry#0005", "Dru#1000", "Lennos#3244", "RgB2#0001"] #Users

botDev = ["DaBqmb#0001"]

# Achievement progression emojis
level_emojis = {
    0: ":zero:",
	1: ":one:",
	2: ":two:",
	3: ":three:",
	4: ":four:",
	5: ":five: :white_check_mark:"
}

@bot.event
async def on_ready():
    print('Connected to woolwars.net!')
    game = discord.Game("Wool Wars | mc.hypixel.net | 1.8 - 1.18.2")
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.command()
async def hywool(ctx):
    embed=discord.Embed(title="HyWool Mod Installation Steps", color=0x7289da)
    embed.add_field(name="Step #1", value="Install ChatTriggers from https://chattriggers.com/ for 1.8.9!", inline=False)
    embed.add_field(name="Step #2", value="Install Forge for 1.8.9 or use Feather client", inline=False)
    embed.add_field(name="Step #3", value="Install the client one not the server one of forge in the launcher", inline=False)
    embed.add_field(name="Step #4", value="Go to your mods folder and drag and drop ChatTriggers into it then load up minecraft", inline=False)
    embed.add_field(name="Step #5", value="Type **/ct import HyWool** to install the HyWool stats bot into your game and use it whenever!", inline=False)
    embed.add_field(name="Step #6", value="Type **/ww** for the main help menu so you can learn the commands with ease", inline=False)
    embed.add_field(name="Step #7", value="Have fun playing with HyWool just note though you don't need to use the bot anymore as everything is now in-game that you would really need. You may need to type the command more then once to get the physical stats itself ( Due to API being sorta buggy on some days ).", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="ww", aliases=["wwhelp","wwh"])
async def ww(ctx):
    embed=discord.Embed(title="HyWool Help Menu", description="Learn the commands of the official wool wars bot!", color=0x7289da)

    embed.add_field(name="ChatTriggers Module", value="`!hywool` - Get the official hywool mod in-game!", inline=False)
    embed.add_field(name="Profile Stats", value="`!wwp <player>` - Check a users stats", inline=False)
    embed.add_field(name="Profile Leaderboards", value="`!wwlb <player>` - Check a users leaderboard positions", inline=False) 
    embed.add_field(name="Profile Achievements", value="`!wwa <player>` - Check a users achievements", inline=False)
    embed.add_field(name="Profile Class Stats", value="`!wwcs <player>` - Check a users class stats (Sends more then 1 embed!)", inline=False)
    embed.add_field(name="Invite HyWool", value="`!wwinv` - Invite HyWool to your server!", inline=False)
    embed.add_field(name="HyWool Partners", value="`!wwpar` - View all partners of HyWool!", inline=False)
    embed.add_field(name="Wool Wars Leaderboards", value="`!wwlbs` - View the global leaderboards!", inline=False)
    embed.add_field(name="HyWool Level XP Calculator", value="`!wwcalc <number>` - Calculate the amount of EXP to get to a level!", inline=False)
    embed.add_field(name="Profile Stats (UUID Edition)", value="`!wwpid <uuid of player>` - Check a users stats via uuid obtain the uuid through the id command!", inline=False)
    embed.add_field(name="Looking For Party", value="`!wwlfp <party size>` - Sends out a looking for party message under your ign!", inline=False)
    embed.add_field(name="Player To UUID", value="`!id <player>` - Convert IGNs to UUIDs fast!", inline=False)
    await ctx.send(embed=embed)

    if ctx.guild.id in partners:
        embed=discord.Embed(title="HyWool Help Menu (Partners)", description="All these commands unlock while being partnered!", color=0x9b59b6)
        embed.add_field(name="User Profiles", value="`!profile <user>` - View the profile of a user!", inline=False)
        embed.add_field(name="HyWool Shop", value="`!shop` - View the hywool shop!", inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def wwlfp(ctx, arg=None):
    if arg == None:
        embed=discord.Embed(title="Looking For Party Error", description="`!wwlfp <party size>` - Send a looking for party status!", color=0x7289da)
        await ctx.send(embed=embed)
        return
    else:
        await ctx.message.delete()
        embed=discord.Embed(title=ctx.author.name + "'s Party", description=ctx.author.name + " Is currently looking for players! " + arg + "!", color=0x7289da)
        await ctx.send(embed=embed)
        return

def star_to_xp(star):
    stars = [0, 1000, 2000, 3000, 4000] + ([5000] * 95)
    xp_per_prestige = sum(stars)
    prestige = star // 100
    return prestige*xp_per_prestige + sum(stars[:star % 100])

def xp_to_star(xp):
    stars = [0, 1000, 2000, 3000, 4000] + ([5000] * 95)
    xp_per_prestige, summed_star_xp = sum(stars), 0
    for star, star_xp in enumerate(stars):
        summed_star_xp += star_xp
        if xp % xp_per_prestige < summed_star_xp:
            return round(float(f"{int(xp // xp_per_prestige)}{str(star).zfill(2)}"))

@bot.command()
async def wwcalc(ctx, arg=None):
    if arg == None:
        embed=discord.Embed(title="HyWool Level EXP Calculator", description="Please specify a number to see the total EXP for that level!", color=0x7289da)
        await ctx.send(embed=embed)
        return
    else:
        embed=discord.Embed(title="HyWool Level EXP Calculator", description="*This is starting from 1 stars!*", color=0x7289da)
        embed.add_field(name="Result:", value="EXP: " + str(star_to_xp(int(arg))) + " Required EXP to hit level " + arg, inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def wwlbs(ctx):
    r = requests.get('http://woolwars.net/leaderboard/detailed')
    data = r.json()

    loop_count = 0
    embed=discord.Embed(title="Wool Wars Level Leaderboard", color=0x7289da)

    for user in data["general"]["experience"]: # Loop through the top 10 users on the leaderboard
        if loop_count < 10:
            embed.add_field(name=f"**{len(leaderboard)}.** " + user["ign"], value="Level: [" + str(xp_to_star(user["value"])) + "✫]", inline=False) # Create leaderboard embed
            loop_count += 1
        else:
            await ctx.send(embed=embed) # Send the embed once the embed leaderboard has been created
            break


@bot.command()
async def shop(ctx):
    if ctx.guild.id in partners:
        embed=discord.Embed(title="HyWool Shop", description="This feature is coming soon!", color=0x7289da)
        await ctx.send(embed=embed)
        return
    else:
        embed=discord.Embed(title="HyWool Error", description="This is a partnered server only command!", color=0x7289da)
        await ctx.send(embed=embed)
        return

@bot.command()
async def profile(ctx, arg=None):
    if ctx.guild.id in partners:
        if arg == None:
            embed=discord.Embed(title="HyWool Profile Error", description="Please specify a discord username! *Don't ping the user just put there name and the #*", color=0x7289da)
            await ctx.send(embed=embed)
            return
        else:
            embed=discord.Embed(title=arg + "'s HyWool Profile", color=0x7289da)
            if arg in partnerNames:
                embed.add_field(name="Partnered:", value=":white_check_mark:", inline=True)
                embed.add_field(name="Dev Status:", value=":x:", inline=True)
            else:

                embed.add_field(name="Partnered:", value=":x:", inline=True)
                embed.add_field(name="Dev Status:", value=":x:", inline=True)
            if arg in botDev:
                embed.add_field(name="Dev Status:", value=":ballot_box_with_check:", inline=True)

            embed.add_field(name="Blurple Wool Collected:", value="Coming Soon", inline=True)
            embed.add_field(name="HyWool EXP:", value="Coming Soon", inline=True)
            embed.add_field(name="HyWool Level:", value="Coming Soon", inline=True)
            embed.add_field(name="HyWool Shards:", value="Coming Soon", inline=True)
            await ctx.send(embed=embed)
            return
    else:
        embed=discord.Embed(title="HyWool Error", description="This is a partnered server only command!", color=0x7289da)
        await ctx.send(embed=embed)
        return

@bot.command()
async def wwpar(ctx):
    embed=discord.Embed(title="HyWool Official Partners", description=f"*This is the top 10 verified partners!*", color=0x7289da)
    embed.add_field(name="**1.** Donut Shack", value="[Click Here](https://discord.gg/tsgnHG3urr) To join the community!", inline=False)
    embed.add_field(name="**2.** Expiry's Attor", value="[Click Here](https://discord.gg/rKZmxnjavF) To join the community!", inline=False)
    embed.add_field(name="**3.** Drucord", value="[Click Here](https://discord.gg/JsNNk2mh5A) To join the community!", inline=False)
    embed.add_field(name="**4.** Hypixel Classic Duels", value="[Click Here](https://discord.gg/WS7BkEcQuR) To join the community!", inline=False)
    embed.add_field(name="**5.** Papara ✭ stickers • pings", value="[Click Here](https://discord.gg/ping) To join the community!", inline=False)
    
    await ctx.send(embed=embed)

@bot.command()
async def wwinv(ctx):
    embed=discord.Embed(title="HyWool Invite Link", description=f"Watching Over {len(bot.guilds)} Servers!", color=0x7289da)
    embed.add_field(name="`Invite HyWool`", value="[Click Here](https://discord.com/api/oauth2/authorize?client_id=976605342555324476&permissions=8&scope=bot) To Invite HyWool To Your Server!", inline=False)
    embed.add_field(name="`Invite HyWool 2`", value="[Click Here](https://discord.com/api/oauth2/authorize?client_id=980319615672537128&permissions=8&scope=bot) To Invite HyWool 2 To Your Server!", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def wwpid(ctx, arg=None):
    if arg == None:
        embed=discord.Embed(title="HyWool Error", description="Please specify a minecraft uuid from https://namemc.com/!", color=0x7289da)
        await ctx.send(embed=embed)
        return
    else:
        msg = await ctx.reply('Pulling live data from in-game please give me a couple of seconds! *If nothing shows this means that they have never played!*')

        r1 = requests.get('http://woolwars.net/player/update?uuid=' + arg + '&ranks=true')

        json1 = r1.json()
        coin = json1["general"]["coins"]
        star = json1["general"]["star"]
        powerups = json1["stats"]["overall"]["powerups_gotten"]
        layers = json1["general"]["available_layers"]
        clas = json1["general"]["selected_class"]
        ws = json1["general"]["winstreak"]
        hws = json1["general"]["highest_winstreak"]
        win = json1["stats"]["overall"]["wins"]
        los = json1["stats"]["overall"]["losses"]
        deaths = json1["stats"]["overall"]["deaths"]
        wlr = json1["stats"]["overall"]["wlr"]
        kdr = json1["stats"]["overall"]["kdr"]
        kills = json1["stats"]["overall"]["kills"]
        assists = json1["stats"]["overall"]["assists"]
        placed = json1["stats"]["overall"]["wool_placed"]
        broken = json1["stats"]["overall"]["blocks_broken"]

        await msg.delete()

        embed=discord.Embed(title=arg + "'s Wool Wars Profile", description="", color=0x7289da)
        embed.set_thumbnail(url="https://crafatar.com/avatars/" + arg)
        embed.add_field(name="`Lobby Stats`", value="*Currently pulled stats*", inline=False)
        embed.add_field(name="Level:", value="[" + str(star) + "✫]", inline=True)
        embed.add_field(name="Coins:", value="" + str(coin), inline=True)
        embed.add_field(name="Layers:", value="" + str(layers), inline=True)
        
        embed.add_field(name="`Pre-Lobby Stats`", value="*Currently pulled stats*", inline=False)
        embed.add_field(name="Class Selected:", value="" + str(clas), inline=True)

        embed.add_field(name="`Profile Stats`", value="*Currently pulled stats*", inline=False)
        embed.add_field(name="Win Streak:", value="" + str(ws), inline=True)
        embed.add_field(name="Wins:", value="" + str(win), inline=True)
        embed.add_field(name="Losses:", value="" + str(los), inline=True)
        embed.add_field(name="Best Win Streak:", value="" + str(hws), inline=True)
        embed.add_field(name="Kills:", value="" + str(kills), inline=True)
        embed.add_field(name="Assists:", value="" + str(assists), inline=True)
        embed.add_field(name="Deaths:", value="" + str(deaths), inline=True)
        embed.add_field(name="Broken:", value="" + str(broken), inline=True)
        embed.add_field(name="Placed:", value="" + str(placed), inline=True)
        embed.add_field(name="WLR:", value="" + str(wlr), inline=True)
        embed.add_field(name="KDR:", value="" + str(kdr), inline=True)
        embed.add_field(name="Gained Powerups:", value="" + str(powerups), inline=True)

        await ctx.send(embed=embed)

@bot.command()
async def id(ctx, arg=None):
    if arg == None:
        embed=discord.Embed(title="Player To UUID", description="Please specify a minecraft username to get the uuid of that user!", color=0x7289da)
        await ctx.send(embed=embed)
        return
    else:
        r = requests.get('http://woolwars.net/player?name=' + arg + '&ranks=true')
        json_data = r.json()
        uuid = json_data["uuid"]
        embed=discord.Embed(title="Player To UUID", color=0x7289da)
        embed.add_field(name=arg + "'s UUID Is:", value="" + str(uuid), inline=True)
        await ctx.send(embed=embed)
        return

@bot.command()
async def wwcs(ctx, arg=None):
    if arg == None:
        embed=discord.Embed(title="HyWool Error", description="Please specify a minecraft username!", color=0x7289da)
        await ctx.send(embed=embed)
        return
    else:
        msg1 = await ctx.reply('Pulling live data from in-game please give me a couple of seconds! *If nothing shows this means that they have never played!*')
        r = requests.get('http://woolwars.net/player?name=' + arg + '&ranks=true')
        json_data = r.json()
        uuid = json_data["uuid"]

        r1 = requests.get('http://woolwars.net/player/update?uuid=' + uuid + '&ranks=true')

        json1 = r1.json()
        tankplayed = json1["stats"]["tank"]["games_played"]
        tankwins = json1["stats"]["tank"]["wins"]
        tanklosses = json1["stats"]["tank"]["losses"]
        tankkills = json1["stats"]["tank"]["kills"]
        tankdeaths = json1["stats"]["tank"]["deaths"]
        tankpowerups = json1["stats"]["tank"]["powerups_gotten"]
        tankplaced = json1["stats"]["tank"]["wool_placed"]
        tankbroken = json1["stats"]["tank"]["blocks_broken"]
        tankassists = json1["stats"]["tank"]["assists"]
        tankwlr = json1["stats"]["tank"]["wlr"]
        tankkdr = json1["stats"]["tank"]["kdr"]

        assaultplayed = json1["stats"]["assault"]["games_played"]
        assaultwins = json1["stats"]["assault"]["wins"]
        assaultlosses = json1["stats"]["assault"]["losses"]
        assaultkills = json1["stats"]["assault"]["kills"]
        assaultdeaths = json1["stats"]["assault"]["deaths"]
        assaultpowerups = json1["stats"]["assault"]["powerups_gotten"]
        assaultplaced = json1["stats"]["assault"]["wool_placed"]
        assaultbroken = json1["stats"]["assault"]["blocks_broken"]
        assaultassists = json1["stats"]["assault"]["assists"]
        assaultwlr = json1["stats"]["assault"]["wlr"]
        assaultkdr = json1["stats"]["assault"]["kdr"]

        archerplayed = json1["stats"]["archer"]["games_played"]
        archerwins = json1["stats"]["archer"]["wins"]
        archerlosses = json1["stats"]["archer"]["losses"]
        archerkills = json1["stats"]["archer"]["kills"]
        archerdeaths = json1["stats"]["archer"]["deaths"]
        archerpowerups = json1["stats"]["archer"]["powerups_gotten"]
        archerplaced = json1["stats"]["archer"]["wool_placed"]
        archerbroken = json1["stats"]["archer"]["blocks_broken"]
        archerassists = json1["stats"]["archer"]["assists"]
        archerwlr = json1["stats"]["archer"]["wlr"]
        archerkdr = json1["stats"]["archer"]["kdr"]

        swordsmanplayed = json1["stats"]["swordsman"]["games_played"]
        swordsmanwins = json1["stats"]["swordsman"]["wins"]
        swordsmanlosses = json1["stats"]["swordsman"]["losses"]
        swordsmankills = json1["stats"]["swordsman"]["kills"]
        swordsmandeaths = json1["stats"]["swordsman"]["deaths"]
        swordsmanpowerups = json1["stats"]["swordsman"]["powerups_gotten"]
        swordsmanplaced = json1["stats"]["swordsman"]["wool_placed"]
        swordsmanbroken = json1["stats"]["swordsman"]["blocks_broken"]
        swordsmanassists = json1["stats"]["swordsman"]["assists"]
        swordsmanwlr = json1["stats"]["swordsman"]["wlr"]
        swordsmankdr = json1["stats"]["swordsman"]["kdr"]

        await msg1.delete()
        await ctx.reply('This will scroll through class stats every 20 seconds!')

        tank = embed=discord.Embed(title=arg + "'s Tank Class Stats", color=0x7289da)
        tank = embed.add_field(name="Games Played:", value="" + str(tankplayed), inline=True)
        tank = embed.add_field(name="Wins:", value="" + str(tankwins), inline=True)
        tank = embed.add_field(name="Losses:", value="" + str(tanklosses), inline=True)
        tank = embed.add_field(name="Kills:", value="" + str(tankkills), inline=True)
        tank = embed.add_field(name="Deaths:", value="" + str(tankdeaths), inline=True)
        tank = embed.add_field(name="Power Ups:", value="" + str(tankpowerups), inline=True)
        tank = embed.add_field(name="Blocks Placed:", value="" + str(tankplaced), inline=True)
        tank = embed.add_field(name="Blocks Broken:", value="" + str(tankbroken), inline=True)
        tank = embed.add_field(name="Assists:", value="" + str(tankassists), inline=True)
        tank = embed.add_field(name="WLR:", value="" + str(tankwlr), inline=True)
        tank = embed.add_field(name="KDR:", value="" + str(tankkdr), inline=True)

        assault = embed=discord.Embed(title=arg + "'s Assault Class Stats", color=0x1abc9c)
        assault = embed.add_field(name="Games Played:", value="" + str(assaultplayed), inline=True)
        assault = embed.add_field(name="Wins:", value="" + str(assaultwins), inline=True)
        assault = embed.add_field(name="Losses:", value="" + str(assaultlosses), inline=True)
        assault = embed.add_field(name="Kills:", value="" + str(assaultkills), inline=True)
        assault = embed.add_field(name="Deaths:", value="" + str(assaultdeaths), inline=True)
        assault = embed.add_field(name="Power Ups:", value="" + str(assaultpowerups), inline=True)
        assault = embed.add_field(name="Blocks Placed:", value="" + str(assaultplaced), inline=True)
        assault = embed.add_field(name="Blocks Broken:", value="" + str(assaultbroken), inline=True)
        assault = embed.add_field(name="Assists:", value="" + str(assaultassists), inline=True)
        assault = embed.add_field(name="WLR:", value="" + str(assaultwlr), inline=True)
        assault = embed.add_field(name="KDR:", value="" + str(assaultkdr), inline=True)

        archer = embed=discord.Embed(title=arg + "'s Archer Class Stats", color=0x9b59b6)
        archer = embed.add_field(name="Games Played:", value="" + str(archerplayed), inline=True)
        archer = embed.add_field(name="Wins:", value="" + str(archerwins), inline=True)
        archer = embed.add_field(name="Losses:", value="" + str(archerlosses), inline=True)
        archer = embed.add_field(name="Kills:", value="" + str(archerkills), inline=True)
        archer = embed.add_field(name="Deaths:", value="" + str(archerdeaths), inline=True)
        archer = embed.add_field(name="Power Ups:", value="" + str(archerpowerups), inline=True)
        archer = embed.add_field(name="Blocks Placed:", value="" + str(archerplaced), inline=True)
        archer = embed.add_field(name="Blocks Broken:", value="" + str(archerbroken), inline=True)
        archer = embed.add_field(name="Assists:", value="" + str(archerassists), inline=True)
        archer = embed.add_field(name="WLR:", value="" + str(archerwlr), inline=True)
        archer = embed.add_field(name="KDR:", value="" + str(archerkdr), inline=True)

        swordsman = embed=discord.Embed(title=arg + "'s Swordsman Class Stats", color=0xe74c3c)
        swordsman = embed.add_field(name="Games Played:", value="" + str(swordsmanplayed), inline=True)
        swordsman = embed.add_field(name="Wins:", value="" + str(swordsmanwins), inline=True)
        swordsman = embed.add_field(name="Losses:", value="" + str(swordsmanlosses), inline=True)
        swordsman = embed.add_field(name="Kills:", value="" + str(swordsmankills), inline=True)
        swordsman = embed.add_field(name="Deaths:", value="" + str(swordsmandeaths), inline=True)
        swordsman = embed.add_field(name="Power Ups:", value="" + str(swordsmanpowerups), inline=True)
        swordsman = embed.add_field(name="Blocks Placed:", value="" + str(swordsmanplaced), inline=True)
        swordsman = embed.add_field(name="Blocks Broken:", value="" + str(swordsmanbroken), inline=True)
        swordsman = embed.add_field(name="Assists:", value="" + str(swordsmanassists), inline=True)
        swordsman = embed.add_field(name="WLR:", value="" + str(swordsmanwlr), inline=True)
        swordsman = embed.add_field(name="KDR:", value="" + str(swordsmankdr), inline=True)


        msg = await ctx.send(embed=tank)
        await asyncio.sleep(20)
        await msg.edit(embed=assault)
        await asyncio.sleep(20)
        await msg.edit(embed=archer)
        await asyncio.sleep(20)
        await msg.edit(embed=swordsman)

@bot.command()
async def wwp(ctx, arg=None):
    if arg == None:
        embed=discord.Embed(title="HyWool Error", description="Please specify a minecraft username!", color=0x7289da)
        await ctx.send(embed=embed)
        return
    else:
        msg = await ctx.reply('Pulling live data from in-game please give me a couple of seconds! *If nothing shows this means that they have never played!*')
        r = requests.get('http://woolwars.net/player?name=' + arg + '&ranks=true')
        json_data = r.json()
        uuid = json_data["uuid"]

        r1 = requests.get('http://woolwars.net/player/update?uuid=' + uuid + '&ranks=true')

        json1 = r1.json()
        coin = json["general"]["coins"]
        star = json["general"]["star"]
        powerups = json["stats"]["overall"]["powerups_gotten"]
        layers = json["general"]["available_layers"]
        clas = json["general"]["selected_class"]
        ws = json["general"]["winstreak"]
        hws = json["general"]["highest_winstreak"]
        win = json["stats"]["overall"]["wins"]
        los = json["stats"]["overall"]["losses"]
        deaths = json["stats"]["overall"]["deaths"]
        wlr = json["stats"]["overall"]["wlr"]
        kdr = json["stats"]["overall"]["kdr"]
        kills = json["stats"]["overall"]["kills"]
        assists = json["stats"]["overall"]["assists"]
        placed = json["stats"]["overall"]["wool_placed"]
        broken = json["stats"]["overall"]["blocks_broken"]

        await msg.delete()

        embed=discord.Embed(title=arg + "'s Wool Wars Profile", description="", color=0x7289da)
        embed.set_thumbnail(url="https://crafatar.com/avatars/" + uuid)
        embed.add_field(name="`Lobby Stats`", value="*Currently pulled stats*", inline=False)
        embed.add_field(name="Level:", value="[" + str(star) + "✫]", inline=True)
        embed.add_field(name="Coins:", value="" + str(coin), inline=True)
        embed.add_field(name="Layers:", value="" + str(layers), inline=True)
        
        embed.add_field(name="`Pre-Lobby Stats`", value="*Currently pulled stats*", inline=False)
        embed.add_field(name="Class Selected:", value="" + str(clas), inline=True)

        embed.add_field(name="`Profile Stats`", value="*Currently pulled stats*", inline=False)
        embed.add_field(name="Win Streak:", value="" + str(ws), inline=True)
        embed.add_field(name="Wins:", value="" + str(win), inline=True)
        embed.add_field(name="Losses:", value="" + str(los), inline=True)
        embed.add_field(name="Best Win Streak:", value="" + str(hws), inline=True)
        embed.add_field(name="Kills:", value="" + str(kills), inline=True)
        embed.add_field(name="Assists:", value="" + str(assists), inline=True)
        embed.add_field(name="Deaths:", value="" + str(deaths), inline=True)
        embed.add_field(name="Broken:", value="" + str(broken), inline=True)
        embed.add_field(name="Placed:", value="" + str(placed), inline=True)
        embed.add_field(name="WLR:", value="" + str(wlr), inline=True)
        embed.add_field(name="KDR:", value="" + str(kdr), inline=True)
        embed.add_field(name="Gained Powerups:", value="" + str(powerups), inline=True)

        await ctx.send(embed=embed)

@bot.command()
async def wwlb(ctx, arg=None):
    if arg == None:
        embed=discord.Embed(title="HyWool Error", description="Please specify a minecraft username!", color=0x7289da)
        await ctx.send(embed=embed)
        return
    else:
        msg = await ctx.reply('Pulling live data from in-game please give me a couple of seconds! *If nothing shows this means that they have never played!*')
        r = requests.get('http://woolwars.net/player?name=' + arg + '&ranks=true')
        json_data = r.json()
        uuid = json_data["uuid"]

        r1 = requests.get('http://woolwars.net/player/update?uuid=' + uuid + '&ranks=true')

        json = r1.json()

        killz = json["stats"]["overall"]["kills_rank"] 
        winz = json["stats"]["overall"]["wins_rank"]
        deathz = json["stats"]["overall"]["deaths_rank"]
        bbroken = json["stats"]["overall"]["blocks_broken_rank"]
        wplaced = json["stats"]["overall"]["wool_placed_rank"]
        apos = json["stats"]["overall"]["assists_rank"]
        pupos = json["stats"]["overall"]["powerups_gotten_rank"]

        await msg.delete()

        embed=discord.Embed(title=arg + "'s Leaderboard Positions", description="", color=0x7289da)
        embed.set_thumbnail(url="https://crafatar.com/avatars/" + uuid)
        embed.add_field(name="`General Positions`", value="*Currently pulled data*", inline=False)
        embed.add_field(name="Kills Position:", value="#" + str(killz), inline=True)
        embed.add_field(name="Wins Position:", value="#" + str(winz), inline=True)
        embed.add_field(name="Deaths Position:", value="#" + str(deathz), inline=True)
        embed.add_field(name="Blocks Broken Position:", value="#" + str(bbroken), inline=True)
        embed.add_field(name="Wool Placed Position:", value="#" + str(wplaced), inline=True)
        embed.add_field(name="Assists Position:", value="#" + str(apos), inline=True)
        embed.add_field(name="Powerups Position:", value="#" + str(pupos), inline=True)
        
        
        await ctx.send(embed=embed)

@bot.command()
async def wwa(ctx, arg=None):
    if arg == None:
        embed=discord.Embed(title="HyWool Error", description="Please specify a minecraft username!", color=0x7289da)
        await ctx.send(embed=embed)
        return
    else:
        msg = await ctx.reply('Pulling live data from in-game please give me a couple of seconds! *If nothing shows this means that they have never played!*')
        r = requests.get('http://woolwars.net/player?name=' + arg + '&ranks=true')
        json_data = r.json()
        uuid = json_data["uuid"]

        r1 = requests.get('http://woolwars.net/player/update?uuid=' + uuid + '&ranks=true')

        json1 = r1.json()

        keystone = json1["achievements_one_time"]["keystone"] 
        merciless = json1["achievements_one_time"]["merciless"] 
        top_killer = json1["achievements_one_time"]["top_killer"] 
        survivor = json1["achievements_one_time"]["survivor"] 
        stock_pile = json1["achievements_one_time"]["stock_pile"] 
        first_blood = json1["achievements_one_time"]["first_blood"] 
        its_dark_down_there = json1["achievements_one_time"]["its_dark_down_there"] 
        ace = json1["achievements_one_time"]["ace"] 
        true_leader = json1["achievements_one_time"]["true_leader"] 
        enderman = json1["achievements_one_time"]["enderman"] 

        wool_warrior = json1["achievements_tiered"]["wool_warrior"] 
        wool_killer = json1["achievements_tiered"]["wool_killer"] 
        wool_contest = json1["achievements_tiered"]["wool_contest"] 
        wool_moutain = json1["achievements_tiered"]["wool_mountain_of_wool"] 


        await msg.delete()

        embed=discord.Embed(title=arg + "'s Challenge Achievements", description="", color=0x7289da)
        embed.set_thumbnail(url="https://crafatar.com/avatars/" + uuid)
        if keystone == True:
            embed.add_field(name="Keystone:", value="Unlocked: :white_check_mark:", inline=True)
        else:
            embed.add_field(name="Keystone:", value="Unlocked: :x:", inline=True)
        if merciless == True:
            embed.add_field(name="Merciless:", value="Unlocked: :white_check_mark:", inline=True)
        else:
            embed.add_field(name="Merciless:", value="Unlocked: :x:", inline=True)
        if top_killer == True:
            embed.add_field(name="Top Killer:", value="Unlocked: :white_check_mark:", inline=True)
        else:
            embed.add_field(name="Top Killer:", value="Unlocked: :x:", inline=True)
        if survivor == True:
            embed.add_field(name="Survivor:", value="Unlocked: :white_check_mark:", inline=True)
        else:
            embed.add_field(name="Survivor:", value="Unlocked: :x:", inline=True)
        if stock_pile == True:
            embed.add_field(name="Stock Pile:", value="Unlocked: :white_check_mark:", inline=True)
        else:
            embed.add_field(name="Stock Pile:", value="Unlocked: :x:", inline=True)
        if first_blood == True:
            embed.add_field(name="First Blood:", value="Unlocked: :white_check_mark:", inline=True)
        else:
            embed.add_field(name="First Blood:", value="Unlocked: :x:", inline=True)
        if its_dark_down_there == True:
            embed.add_field(name="Its Dark Down There:", value="Unlocked: :white_check_mark:", inline=True)
        else:
            embed.add_field(name="Its Dark Down There:", value="Unlocked: :x:", inline=True)
        if ace == True:
            embed.add_field(name="Ace:", value="Unlocked: :white_check_mark:", inline=True)
        else:
            embed.add_field(name="Ace:", value="Unlocked: :x:", inline=True)
        if true_leader == True:
            embed.add_field(name="True Leader:", value="Unlocked: :white_check_mark:", inline=True)
        else:
            embed.add_field(name="True Leader:", value="Unlocked: :x:", inline=True)
        if enderman == True:
            embed.add_field(name="Enderman:", value="Unlocked: :white_check_mark:", inline=True)
        else:
            embed.add_field(name="Enderman:", value="Unlocked: :x:", inline=True)
        
        await ctx.send(embed=embed)

        embed=discord.Embed(title=arg + "'s Tiered Achievements Progression", description="", color=0x9b59b6)

        # Less hard coded, so it's simpler to change the numeric emojis later as you please
        embed.add_field(name="Wool Warrior:", value="Level: "+level_emojis[wool_warrior], inline=True)
        embed.add_field(name="Wool Killer:", value="Level: "+level_emojis[wool_killer], inline=True)
        embed.add_field(name="Wool Contest:", value="Level: "+level_emojis[wool_contest], inline=True)
        embed.add_field(name="Mountain of Wool:", value="Level: "+level_emojis[wool_mountain, inline=True)
        
        await ctx.send(embed=embed)

bot.run('your bot token here.')
