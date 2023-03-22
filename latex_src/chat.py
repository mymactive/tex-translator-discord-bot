# This example requires the 'message_content' intent.

from pydoc import cli
import discord
import sys
import os
import subprocess
import numpy as np
import openai

# このプログラムを実行するには、discordボットのトークンが必要。これはgithubにアップできないので、どうするか考え中。このトークンを記述したテキストファイル（例えば token.txt）をローカルのどこかに配置する。
# プログラムを実行するときは /latex_src ディレクトリから python tut.py token.txt のように実行する。


# コマンドライン引数を受け取る。
args = sys.argv
openai.api_key_path = ".key"

def my_chatgpt(prompt):
# Set up the OpenAI GPT-3 model
    # model_engine = "text-davinci-002"
    # model_engine = "gpt-4"
    # prompt = "Are you a humankind?"
    temperature = 0.7
    max_tokens = 60

# Generate text using the OpenAI GPT-3 model
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages=[{"role": "user", "content":prompt}]
        )
    return response

class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        # もし'$'から始まるメッセージを受けとったら
        if message.content.startswith('?'):
            prompt = message.content[1:]
            response = my_chatgpt(prompt)
            await message.channel.send(response.choices[0]["message"]["content"])


# この部分はdiscord.pyのチュートリアルのまま。仕組みは謎。
intents = discord.Intents.default()
intents.message_content = True

# おそらくここで、インスタンスを生成している。
client = MyClient(intents=intents)

# コマンドラインで受け取ったファイルを読み、tokenに格納する。
token = 'mytoken'
with open(args[1]) as f:
    token = f.readline()

# ボットを起動
client.run(token)
