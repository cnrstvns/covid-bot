import requests
import json
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
from datetime import datetime

client = commands.Bot(command_prefix="$")
client.remove_command("help")

@client.event
async def on_ready():
    for guild in client.guilds:
        print(f"Connected to {guild}")
    await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)} servers"))

@client.event
async def on_guild_join(guild):
    print(f'Joined {guild.name}')
    await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)} servers"))

@client.event
async def on_message_edit(before, after):
    await client.process_commands(after)

@client.command(pass_context=True)
async def help(ctx, menu=None):
    options = ""
    if menu is None:
        options = "```\nValid Queries:\nTop\nSort\nSearch\nPercentages\n\nTo See More Specific Options, do !help <query>```"
    elif menu.lower() == "top":
        options = "```top <number>\n\nex. top 10```"
    elif menu.lower() == "sort":
        options = "```\nsort <query> <number> <direction>\n\nValid Queries:\ncountries\ncases\ndeaths\nrecovered\n\nValid Numbers:\nany so long as it does not give an error.\n\nValid Directions:\nhigh\nlow\n\nex. sort deaths 20 high```"
    elif menu.lower() == "search":
        options = "```\nsearch <country>\n\nValid Countries:\nAny country on the Earth.\n\nex. search United States```"
    elif menu.lower() == "percentages":
        options = "```\npercentages <query> <direction>\n\nValid Queries:\ndeaths\nrecoveries\n\nValid Directions:\nhigh\nlow\n\nex. percentages deaths low"
    embed = discord.Embed(title="COVID-19 Bot Help Menu", description=options, color=discord.Colour.red(), timestamp=datetime.utcnow())
    embed.add_field(name="Support Discord", value="[Join Here](https://discord.gg/s53HrVW)")
    embed.set_footer(text="Covid-19 Bot")
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def info(ctx):
    embed = discord.Embed(title="About the COVID-19 Bot", description="```\nAll data is pulled from Wikipedia currently. All credit/rights go to Wikipedia. This is simply an aggregator of their data. All \"cases\" statistics are current cumulative cases for each query.\n\ncredit for the bot goes to Covid-19 Bot```")
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def top(ctx, num):
    data = pull()
    description = ""
    for i in range(int(num)):

        country = data[i][0]
        cases = data[i][1]
        deaths = data[i][2]
        recovered = data[i][3]
        description += f"{country} has {cases} cases and **{deaths}** deaths\n"
    embed = discord.Embed(title=f"Top {num} CoronaVirus Countries", description=description, color=discord.Colour.red(), timestamp=datetime.utcnow())
    embed.set_footer(text="Covid-19 Bot")
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def sort(ctx, desired, num, direction):
    data = pull()
    description = ""
    if int(num) == 0:
        embed = discord.Embed(title="Invalid Sort Direction", description="```Valid Numbers: any integer > 1```", color=discord.Colour.red(), timestamp=datetime.utcnow())
        embed.set_footer(text="Covid-19 Bot")
        await ctx.send(embed=embed)
        return

    if desired.lower() == "countries":

        if direction.lower() == "low":
            data.sort(key = lambda x: x[0])
            description = ""
            for i in range(int(num)):
                country = data[i][0]
                cases = data[i][1]
                deaths = data[i][2]
                recovered = data[i][3]
                description += f"**{country}** has {cases} cases and {deaths} deaths\n"
            embed = discord.Embed(title=f"Top {num} CoronaVirus Countries", description=description, color=discord.Colour.red(), timestamp=datetime.utcnow())
            embed.set_footer(text="Covid-19 Bot")
            await ctx.send(embed=embed)

        elif direction.lower() == "high":
            data.sort(key = lambda x: x[0], reverse=True)
            description = ""
            for i in range(int(num)):
                country = data[i][0]
                cases = data[i][1]
                deaths = data[i][2]
                recovered = data[i][3]
                description += f"**{country}** has {cases} cases and {deaths} deaths\n"
            embed = discord.Embed(title=f"Top {num} CoronaVirus Countries", description=description, color=discord.Colour.red(), timestamp=datetime.utcnow())
            embed.set_footer(text="Covid-19 Bot")
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="Invalid Sort Direction", description="```Valid Directions:\nlow (sorts from least to most)\nhigh (sorts from most to least)```", color=discord.Colour.red(), timestamp=datetime.utcnow())
            embed.set_footer(text="Covid-19 Bot")
            await ctx.send(embed=embed)

    elif desired.lower() == "cases":

        if direction.lower() == "low":
            data.sort(key = lambda x: x[1])
            for i in range(int(num)):
                country = data[i][0]
                cases = data[i][1]
                deaths = data[i][2]
                recovered = data[i][3]
                description += f"{country} has **{cases}** cases and {deaths} deaths\n"
            embed = discord.Embed(title=f"Top {num} countries with CoronaVirus", description=description, color=discord.Colour.red(), timestamp=datetime.utcnow())
            embed.set_footer(text="Covid-19 Bot")
            await ctx.send(embed=embed)

        elif direction.lower() == "high":
            data.sort(key = lambda x: x[1], reverse=True)
            for i in range(int(num)):
                country = data[i][0]
                cases = data[i][1]
                deaths = data[i][2]
                recovered = data[i][3]
                description += f"{country} has **{cases}** cases and {deaths} deaths\n"
            embed = discord.Embed(title=f"Top {num} CoronaVirus Countries", description=description, color=discord.Colour.red(), timestamp=datetime.utcnow())
            embed.set_footer(text="Covid-19 Bot")
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="Invalid Sort Direction", description="```Valid Directions:\nlow (sorts from least to most)\nhigh (sorts from most to least)```", color=discord.Colour.red(), timestamp=datetime.utcnow())
            embed.set_footer(text="Covid-19 Bot")
            await ctx.send(embed=embed)

    elif desired.lower() == "deaths":
        
        if direction.lower() == "low":
            data.sort(key = lambda x: x[2])
            for i in range(int(num)):
                country = data[i][0]
                cases = data[i][1]
                deaths = data[i][2]
                recovered = data[i][3]
                description += f"{country} has {cases} cases and **{deaths}** deaths\n"
            embed = discord.Embed(title=f"Top {num} CoronaVirus Countries", description=description, color=discord.Colour.red(), timestamp=datetime.utcnow())
            embed.set_footer(text="Covid-19 Bot")
            await ctx.send(embed=embed)

        elif direction.lower() == "high":
            data.sort(key = lambda x: x[2], reverse=True)
            for i in range(int(num)):
                country = data[i][0]
                cases = data[i][1]
                deaths = data[i][2]
                recovered = data[i][3]
                description += f"{country} has {cases} cases and **{deaths}** deaths\n"
            embed = discord.Embed(title=f"Top {num} CoronaVirus Countries", description=description, color=discord.Colour.red(), timestamp=datetime.utcnow())
            embed.set_footer(text="Covid-19 Bot")
            await ctx.send(embed=embed)
        
        else:
            embed = discord.Embed(title="Invalid Sort Direction", description="```Valid Directions:\nlow (sorts from least to most)\nhigh (sorts from most to least)```", color=discord.Colour.red(), timestamp=datetime.utcnow())
            embed.set_footer(text="Covid-19 Bot")
            await ctx.send(embed=embed)

    elif desired.lower() == "recovered":

        if direction.lower() == "low":
            data.sort(key = lambda x: x[3])
            for i in range(int(num)):
                country = data[i][0]
                cases = data[i][1]
                deaths = data[i][2]
                recovered = data[i][3]
                description += f"**{country}** has {cases} cases and **{recovered}** recovered\n"
            embed = discord.Embed(title=f"Top {num} CoronaVirus Countries", description=description, color=discord.Colour.red(), timestamp=datetime.utcnow())
            embed.set_footer(text="Covid-19 Bot")
            await ctx.send(embed=embed)
        
        elif direction.lower() == "high":
            data.sort(key = lambda x: x[3], reverse=True)
            for i in range(int(num)):
                country = data[i][0]
                cases = data[i][1]
                deaths = data[i][2]
                recovered = data[i][3]
                description += f"**{country}** has {cases} cases and **{recovered}** recovered\n"
            embed = discord.Embed(title=f"Top {num} CoronaVirus Countries", description=description, color=discord.Colour.red(), timestamp=datetime.utcnow())
            embed.set_footer(text="Covid-19 Bot")
            await ctx.send(embed=embed)
        
        else:
            embed = discord.Embed(title="Invalid Sort Direction", description="```Valid Directions:\nlow (sorts from least to most)\nhigh (sorts from most to least)", color=discord.Colour.red(), timestamp=datetime.utcnow())
            embed.set_footer(text="Covid-19 Bot")
            await ctx.send(embed=embed)
    
    else:
        embed = discord.Embed(title="Invalid Sort Selection", description="```Valid Selections:\nCountry (sorts by country alphabetically)\nCases (sorts by number of cases)\nDeaths (sorts by number of deaths)\nRecovered (sorts by number of recovered patients)```", color=discord.Colour.red(), timestamp=datetime.utcnow())
        embed.set_footer(text="Covid-19 Bot")
        await ctx.send(embed=embed)

@client.command(pass_context=True)
async def search(ctx, *, query):
    data = pull()
    count = 0
    description = ""
    data.sort(key = lambda x: x[0])
    for i in range(len(data)):
        if str(query.lower()) in str(data[i][0].lower()):
            country = data[i][0]
            cases = data[i][1]
            deaths = data[i][2]
            recovered = data[i][3]
            count += 1
            description += f"**{country}** has {cases} cases, {recovered} recovered, and {deaths} deaths.\n"
    embed = discord.Embed(title=f"", description=description, color=discord.Colour.red(), timestamp=datetime.utcnow())
    embed.set_footer(text="Covid-19 Bot")
    if count == 0:
        embed.title = f"Found 0 Results"
        embed.description = f"```Try a less specific query or ensure your spelling is accurate. Queries are NOT case sensitive.```"
    if count == 1:
        embed.title = f"Found 1 Result"
    else:
        embed.title = f"Found {count} Results"
    embed.set_footer(text="Covid-19 Bot")
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def percentages(ctx, query, direction):

    data = pull()
    description = ""
    if query.lower() == "deaths":
        if direction.lower() == "high":
            data.sort(key = lambda x: x[4], reverse=True)
            for i in range(10):
                country = data[i][0]
                rate = data[i][4]
                description += f"{country} has a death rate of **{str(rate)[:4]}%\n**"
            embed = discord.Embed(title=f"", description=description, color=discord.Colour.red(), timestamp=datetime.utcnow())
            embed.set_footer(text="Covid-19 Bot")
            await ctx.send(embed=embed)

        elif direction.lower() == "low":
            data.sort(key = lambda x: x[4])
            for i in range(10):
                country = data[i][0]
                rate = data[i][4]
                description += f"{country} has a death rate of **{str(rate)[:4]}%\n**"
            embed = discord.Embed(title=f"", description=description, color=discord.Colour.red(), timestamp=datetime.utcnow())
            embed.set_footer(text="Covid-19 Bot")
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="Invalid Sort Direction", description="```Valid Directions:\nlow (sorts from least to most)\nhigh (sorts from most to least)```", color=discord.Colour.red(), timestamp=datetime.utcnow())
            embed.set_footer(text="Covid-19 Bot")
            await ctx.send(embed=embed)

    elif query.lower() == "recoveries":
        if direction.lower() == "high":
            data.sort(key = lambda x: x[5], reverse=True)
            for i in range(10):
                country = data[i][0]
                rate = data[i][5]
                description += f"{country} has a recovery rate of **{str(rate)[:4]}%\n**"
            embed = discord.Embed(title=f"", description=description, color=discord.Colour.red(), timestamp=datetime.utcnow())
            embed.set_footer(text="Covid-19 Bot")
            await ctx.send(embed=embed)

        elif direction.lower() == "low":
            data.sort(key = lambda x: x[5])
            for i in range(10):
                country = data[i][0]
                rate = data[i][5]
                description += f"{country} has a recovery rate of **{str(rate)[:4]}%\n**"
            embed = discord.Embed(title=f"", description=description, color=discord.Colour.red(), timestamp=datetime.utcnow())
            embed.set_footer(text="Covid-19 Bot")
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="Invalid Sort Direction", description="```Valid Directions:\nlow (sorts from least to most)\nhigh (sorts from most to least)```", color=discord.Colour.red(), timestamp=datetime.utcnow())
            embed.set_footer(text="Covid-19 Bot")
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Invalid Query", description="```Valid Queries:\ndeaths: returns death rate for 10 countries\nrecoveries: returns recovery rate for 10 countries", color=discord.Colour.red(), timestamp=datetime.utcnow())
        embed.set_footer(text="Covid-19 Bot")
        await ctx.send(embed=embed)

def pull():
    datas = []
    USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36"
    headers = {"user-agent" : USER_AGENT}
    r = requests.get("https://www.worldometers.info/coronavirus/", headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find('table')
    body = table.find('tbody')
    rows = body.find_all('tr')
    for row in rows:
        try:
            details = row.find_all('td')
            place = details[0].text.strip()
            cases = details[1].text.strip()
            deaths = details[3].text.strip()
            recovered = details[5].text.strip()
            cases = cases.replace(",", "")
            if cases is None:
                cases = 0
            if cases is '':
                cases = 0
            deaths = deaths.replace(",", "")
            if deaths is None:
                deaths = 0
            if deaths is '':
                deaths = 0
            recovered = recovered.replace(",", "")
            if recovered is None:
                recovered = 0
            if recovered is '':
                recovered = 0
            death_rate = (int(deaths) / int(cases)) * 100
            recovery_rate = (int(recovered) / int(cases)) * 100
            data = [place, int(cases), int(deaths), int(recovered), death_rate, recovery_rate]
            datas.append(data)
        except Exception as e:
            print(e)
            continue
    r = requests.get("https://www.worldometers.info/coronavirus/country/us/", headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find('table')
    body = table.find('tbody')
    rows = body.find_all('tr')
    for row in rows:
        try:
            details = row.find_all('td')
            place = details[0].text.strip()
            cases = details[1].text.strip()
            deaths = details[3].text.strip()
            recovered = details[5].text.strip()
            cases = cases.replace(",", "")
            if cases is None:
                cases = 0
            if cases is '':
                cases = 0
            deaths = deaths.replace(",", "")
            if deaths is None:
                deaths = 0
            if deaths is '':
                deaths = 0
            death_rate = (int(deaths) / int(cases)) * 100
            data = [place, int(cases), int(deaths), "unknown", death_rate, "unknown"]
            datas.append(data)
        except Exception as e:
            print(e)
            continue
    return datas

client.run(#BOT_TOKEN_HERE)
