import socket, ssl, subprocess, time, os, json, random, httplib, urllib, ConfigParser
from subprocess import *

Config = ConfigParser.ConfigParser()
Config.read("config.ini")

server = Config.get("irc", "server")
port = Config.getint("irc", "port")
channel = Config.get("irc", "channel")
botnick = Config.get("irc", "botnick")
password = Config.get("irc", "password")

def ping(): 
  ircsock.send("PONG :pingis\n")  

def sendmsg(msg): 
  ircsock.send("PRIVMSG "+ channel +" :"+ msg +"\n") 

def api_call(method, endpoint, params):
    content_type = Config.get("api", "content_type")
    authorization = Config.get("api", "authorization")
    headers = {'Content-type': content_type,'Authorization': authorization}
    conn = httplib.HTTPConnection(Config.get("api", "host"))
    conn.request(method, endpoint, params, headers)
    return conn.getresponse()

def soundlist():
    response = api_call("GET", "/api/v1/sfx", "")
    print response.read()

def sadsax():
    params = json.dumps({'file': 'sounds/sadsax.mp3','file_type': 'sfx'})
    response = api_call("POST", "/api/v1/play", params)

def mcmanus():
    params = json.dumps({'file': 'sounds/mcmanus.wav','file_type': 'sfx'})
    response = api_call("POST", "/api/v1/play", params)

def headphones():
    params = json.dumps({'file': 'sounds/headphones-on.wav','file_type': 'sfx'})
    response = api_call("POST", "/api/v1/play", params)

def notouching():
    params = json.dumps({'file': 'sounds/notouching.mp3','file_type': 'sfx'})
    response = api_call("POST", "/api/v1/play", params)

def bear():
    params = json.dumps({'file': 'sounds/bear3.wav','file_type': 'sfx'})
    response = api_call("POST", "/api/v1/play", params)

def sir():
    params = json.dumps({'file': 'sounds/sir.wav','file_type': 'sfx'})
    response = api_call("POST", "/api/v1/play", params)

def wtf():
    params = json.dumps({'file': 'sfx/Roby.wav','file_type': 'sfx'})
    response = api_call("POST", "/api/v1/play", params)

def js():
    params = json.dumps({'file': 'sounds/javascript.mp3','file_type': 'sfx'})
    response = api_call("POST", "/api/v1/play", params)

def claps():
    params = json.dumps({'file': 'sounds/claps.wav','file_type': 'sfx'})
    response = api_call("POST", "/api/v1/play", params)

def stop():
    params = json.dumps({'song': 'skip'})
    response = api_call("POST", "/api/v1/control", params)

def getvol():
    params = json.dumps({'song': 'skip'})
    response = api_call("GET", "/api/v1/control", params)
    response = json.loads(response.read())
    current_vol = response['volume']['current']
    sendmsg("Current Volume: " + current_vol)

def setvol(vol):
    (_, _, vol) = vol.partition("!setvol ")
    params = json.dumps({'volume': vol})
    api_call("PATCH", "/api/v1/control", params)

def say(ircstr):
    (_, _, content) = ircstr.partition("!say")
    params = {'content': content }
    params = json.dumps(params)
    api_call("PATCH", "/api/v1/say", params)

def commands():
    sendmsg("!mcmanus")
    sendmsg("!bear")
    sendmsg("!headphones")
    sendmsg("!sadsax")
    sendmsg("!notouching")
    sendmsg("!sir")
    sendmsg("!wtf")
    sendmsg("!js")
    sendmsg("!claps")
    sendmsg("!stop")

def puppet(ircstr):
  (_, _, puppetstr) = ircstr.partition("!puppet")
  sendmsg(puppetstr)
  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port)) 
ircsock = ssl.wrap_socket(s)
ircsock.send("PASS "+ password +"\n") 
ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +"QA PUSHER BOT!!!! \n") 
ircsock.send("NICK "+ botnick +"\n") 
ircsock.send("JOIN "+ channel +"\n")

while 1: 
  ircmsg = ircsock.recv(2048) 
  ircmsg = ircmsg.strip('\n\r') 
  print(ircmsg)

  if ircmsg.find(":!commands") != -1:
    commands()

  if ircmsg.find(":!sadsax") != -1:
    sadsax()

  if ircmsg.find(":!mcmanus") != -1:
    mcmanus()

  if ircmsg.find(":!bear") != -1:
    bear()

  if ircmsg.find(":!js") != -1:
    js()

  if ircmsg.find(":!claps") != -1:
    claps()

  if ircmsg.find(":!wtf") != -1:
    wtf()

  if ircmsg.find(":!notouching") != -1:
    notouching()

  if ircmsg.find(":!headphones") != -1:
    headphones()

  if ircmsg.find(":!sir") != -1:
    sir()

  if ircmsg.find(":!getvol") != -1:
    getvol()

  if ircmsg.find(":!setvol") != -1:
    setvol(ircmsg)

  if ircmsg.find(":!stop") != -1:
    stop()

  if ircmsg.find(":!maxlist") != -1:
    soundlist()

  if ircmsg.find(":!say") != -1:
    say(ircmsg)

  if ircmsg.find(":!puppet") != -1:
    puppet(ircmsg)

  if ircmsg.find("lotion") != -1:
    sendmsg("IT PUTS THE LOTION ON ITS SKIN!")

  if ircmsg.find("PING :") != -1: 
    ping()