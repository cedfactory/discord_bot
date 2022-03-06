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

def function_list(market):
    url = fdp_url+"/list?markets="+market

    request = urllib.request.Request(url)
    request.add_header("User-Agent","cheese")
    data = urllib.request.urlopen(request).read()
    data_json = json.loads(data)
    if data_json["status"] != "ok" or data_json["result"][market]["status"] != "ok":
        return "no data received"

    dataframe_market = data_json["result"][market]["dataframe"]
    df = pd.read_json(dataframe_market)
    return df["symbol"].tolist()

def function_value(value):
    url = fdp_url+"/value?values="+value

    request = urllib.request.Request(url)
    request.add_header("User-Agent","cheese")
    data = urllib.request.urlopen(request).read()
    data_json = json.loads(data)
    if data_json["status"] != "ok" or data_json["result"][value]["status"] != "ok":
        return  data_json["result"][value]["reason"]

    return data_json["result"][value]["info"]



class CedFactoryBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/")
        
        @self.command(name="hello")
        async def custom_command(ctx):
            await ctx.channel.send("Hello {}".format(ctx.author.name))
        
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

    async def on_ready(self):
        print("bot is ready")



# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    bot = CedFactoryBot()
    bot.run(token)
