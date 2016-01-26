#!/usr/bin/env python2
import discord
import warnings
import subprocess
import chatterbot as chatbot
import threading
import time

warnings.filterwarnings("ignore")

client = discord.Client()
client.login('spam@shivergaming.com', 'R5mn3gWrTfYd3%HiMok@UA6L')

channels = []

def broadcast(text):
    for channel in channels:
	client.send_message(channel, text)

def test(message):
    client.send_message(message.channel, 'Test was received!\nYou are now subscribed!')
    if message.channel not in channels:
	channels.append(message.channel)

def remove(message):
    channels.remove(message.channel)
    if message.channel in chatbots.keys():
        del chatbots[message.channel]
    client.send_message(message.channel, "You are now unsubscribed!")

def shout(message):
    broadcast('%s shouts %s' % (message.author.name, message.content[7:]))

def fortune(message):
    client.send_message(message.channel,\
	subprocess.check_output("/usr/games/fortune", shell = True) )

game_channels = []
def play(message):
    game_channels.append(message.channel)
    client.send_message(message.channel, "! Game started !")

chatbots = {}
def chat(message):
#    chatbots[message.channel] = chatbot.ChatBot("MassiveDynamic")
#    with open("chat.log") as log:
#	chatbots[message.channel].train(log.read().split("\n"))
#    client.send_message(message.channel, "! Chatbot started !")
    pass

bots = {
    "!test" : test,
    "!shout " : shout,
    "!remove" : remove,
    "!fortune" : fortune,
    "!play" : play,
    "!chat" : chat
    }

last = ""

nope = ('/', '@', '!')

def valid(message):
    if message.content[0] == "~":
        return message.content + "\n"
    else:
        return ""

@client.event
def on_message(message):
    global last

    with open("chat.log", "a") as log:
        if message.content[0] not in nope:
            log.write(valid(message))

    for cmd, func in bots.items():
        if message.content.startswith(cmd):
            func(message)
            return

    if message.channel in chatbots.keys():
	if message.content != last:
	    last = chatbots[message.channel].get_response(message.content)
            client.send_message(message.channel, last)

def mainloop():
    while True:
	broadcast(subprocess.check_output("fortune", shell = True))
        time.sleep(432000)

@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    thread = threading.Thread(target = mainloop)
    thread.daemon = True
    thread.start()

client.run()

