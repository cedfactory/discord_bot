import discord
from discord.ext import commands
import urllib
import json
import os
from dotenv import load_dotenv
import pandas as pd


load_dotenv()
token = os.getenv('BOT_TOKEN')


def function_list(market):
    fdp_url = os.getenv('FPD_URL')
    url = fdp_url+"/list?markets="+market

    request = urllib.request.Request(url)
    request.add_header('User-Agent',"cheese")
    data = urllib.request.urlopen(request).read()
    data_json = json.loads(data)
    if data_json['status'] != "ok" or data_json['result'][market]['status'] != "ok":
        return "no data received"

    dataframe_market = data_json["result"][market]['dataframe']
    df = pd.read_json(dataframe_market)
    print(df["name"].tolist())
    return df["name"].tolist()



class CedFactoryBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/")
        
        @self.command(name='hello')
        async def custom_command(ctx):
            await ctx.channel.send("Hello {}".format(ctx.author.name))
        
        @self.command(name='list')
        async def custom_command(ctx, *args):
            if len(args) >= 1:
                msg = function_list(args[0])
            else:
                msg = "I need a market as argument"
            await ctx.channel.send(msg)

    async def on_ready(self):
        print("cedfactory_bot is ready")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bot = CedFactoryBot()
    bot.run(token)
