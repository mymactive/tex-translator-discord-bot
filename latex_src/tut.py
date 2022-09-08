# This example requires the 'message_content' intent.

from pydoc import cli
import discord
import sys
import os
import subprocess
import numpy as np

# このプログラムを実行するには、discordボットのトークンが必要。これはgithubにアップできないので、どうするか考え中。このトークンを記述したテキストファイル（例えば token.txt）をローカルのどこかに配置する。
# プログラムを実行するときは /latex_src ディレクトリから python tut.py token.txt のように実行する。


# コマンドライン引数を受け取る。
args = sys.argv


class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        # もし'$'から始まるメッセージを受けとったら
        if message.content.startswith('$'):
            # ./latex_src/main.texファイルを書込みモードで開く。
            with open('main.tex', 'w') as f:
                # メッセージの内容を./latex_src/main.texに書き込む。
                f.write(message.content)
            subprocess.Popen('tex2img structure.tex fig.png',
                             shell=True).communicate()
            # 生成したものが'fig.png'として出力されるので、これを読み込み、sendする。
            with open('fig.png', 'rb') as g:
                pic = discord.File(g)
                await message.channel.send(file=pic)


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
