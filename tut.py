# This example requires the 'message_content' intent.

from pydoc import cli
import discord
import sys
import numpy as np

# コマンドライン引数を受け取る
args = sys.argv


class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if message.content.startswith('!'):
            await message.channel.send('hello')


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

token = 'mytoken'
with open(args[1]) as f:
    token = f.readline()
client.run(token)
