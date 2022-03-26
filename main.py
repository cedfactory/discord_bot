import discord
from discord.ext import commands
import urllib
import json
import os
from dotenv import load_dotenv
import pandas as pd


load_dotenv()
token = os.getenv("BOT_TOKEN")
fdp_url = os.getenv("FDP_URL")

def function_recommendations(exchange):
    url = fdp_url+"/recommendations?screener=crypto&exchange="+exchange
    print(url)

    request = urllib.request.Request(url)
    request.add_header("User-Agent","cheese")
    data = urllib.request.urlopen(request).read()
    data_json = json.loads(data)
    print(data_json)
    if data_json["status"] != "ok":
        return data_json["result"]["reason"]

    response = ""
    symbols = data_json["result"]
    for symbol in symbols:
        response = response + symbol + " : " + symbols[symbol]["RECOMMENDATION"] + "\n"

    return response

def function_list(market):
    url = fdp_url+"/list?markets="+market

    request = urllib.request.Request(url)
    request.add_header("User-Agent","cheese")
    data = urllib.request.urlopen(request).read()
    data_json = json.loads(data)
    if data_json["status"] != "ok" or data_json["result"][market]["status"] != "ok":
        return data_json["result"][market]["reason"]

    symbols = data_json["result"][market]["symbols"]
    return symbols.split(",")

def function_value(value):
    url = fdp_url+"/value?values="+value

    request = urllib.request.Request(url)
    request.add_header("User-Agent","cheese")
    data = urllib.request.urlopen(request).read()
    data_json = json.loads(data)
    if data_json["status"] != "ok" or data_json["result"][value]["status"] != "ok":
        return  data_json["result"][value]["reason"]

    return data_json["result"][value]["info"]

def function_portfolio(ctx):
    url = fdp_url+"/portfolio"

    request = urllib.request.Request(url)
    request.add_header("User-Agent","cheese")
    data = urllib.request.urlopen(request).read()
    data_json = json.loads(data)
    if data_json["status"] != "ok":
        return  data_json["reason"]

    df_portfolio = pd.read_json(data_json["result"]["symbols"])
    embed=discord.Embed(title="portfolio", color=0xFF5733, timestamp= ctx.message.created_at)

    response = ""
    for index, row in df_portfolio.iterrows():
        recommendations = "15min / 30min / 1h : " + row["RECOMMENDATION_15m"] + " / " + row["RECOMMENDATION_30m"] + " / " + row["RECOMMENDATION_1h"]
        response = response + row["symbol"] + " (" + recommendations + ")\n"
    
        embed.add_field(name=row["symbol"], value="""
            > Recos : 15min 30min 1h : """ + row["RECOMMENDATION_15m"] + " " + row["RECOMMENDATION_15m"] + " " + row["RECOMMENDATION_1h"] + """
            > Change : 1h 24h : """ + "{:.2f}".format(row["change1h"]) + " " + "{:.2f}".format(row["change24h"]),inline=False)

    return embed


class CedFactoryBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/")
        
        @self.command(name="hello")
        async def custom_command(ctx):
            await ctx.channel.send("Hello {}".format(ctx.author.name))
        
        @self.command(name="recommendations")
        async def custom_command(ctx, *args):
            exchange = args[0]
            if len(args) >= 1:
                msg = function_recommendations(exchange)
            else:
                msg = "I need a exchange as argument"

            embed=discord.Embed(title=exchange, description=msg, color=0xFF5733)
            await ctx.channel.send(embed=embed)

        @self.command(name="list")
        async def custom_command(ctx, *args):
            market = args[0]
            if len(args) >= 1:
                msg = function_list(market)
            else:
                msg = "I need a market as argument"

            embed=discord.Embed(title=market, description=msg, color=0xFF5733)
            await ctx.channel.send(embed=embed)
        
        @self.command(name="value")
        async def custom_command(ctx, *args):
            symbol = args[0]
            if len(args) >= 1:
                msg = function_value(symbol)
            else:
                msg = "I need a value as argument"

            embed=discord.Embed(title=symbol, description=msg, color=0xFF5733)
            await ctx.channel.send(embed=embed)
        
        @self.command(name="portfolio")
        async def custom_command(ctx, *args):
            embed = function_portfolio(ctx)
            await ctx.channel.send(embed=embed)

    async def on_ready(self):
        print("bot is ready")



# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    bot = CedFactoryBot()
    bot.run(token)
