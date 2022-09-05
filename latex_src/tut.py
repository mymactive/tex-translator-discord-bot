# This example requires the 'message_content' intent.

from pydoc import cli
import discord
import sys
import os
import subprocess
import numpy as np

# コマンドライン引数を受け取る
args = sys.argv


class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        # もし'$'から始まるメッセージを受けとったら
        if message.content.startswith('$'):
            await message.channel.send('hello')
            # ./latex_src/main.texファイルを書込みモードで開く。
            with open('main.tex', 'w') as f:
                # メッセージの内容を./latex_src/main.texに書き込む。
                f.write(message.content)
            # execute.shを実行することでtexをコンパイルする。
            subprocess.Popen('sh execute.sh', shell=True).communicate()
            # 生成したものが'fig.pdf'として出力されるので、これを読み込み、sendする。
            with open('fig.pdf', 'rb') as g:
                pic = discord.File(g)
                await message.channel.send(file=pic)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

token = 'mytoken'
with open(args[1]) as f:
    token = f.readline()
client.run(token)
