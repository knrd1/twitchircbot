# ChatGPT

Twitch IRC Bot checks if twitch stream is online and sends a notification to IRC channel.

### Prerequisities:

Create an account and get your client ID and secret: https://dev.twitch.tv/docs/authentication/register-app/

Install python3 and additional packages:
```
$ apt install python3 python3-pip (Debian/Ubuntu)
$ yum install python3 python3-pip (RedHat/CentOS)
$ pip3 install irc
$ git clone https://github.com/knrd1/twitchircbot.git
$ cd twitchircbot
$ cp example.config.ini config.ini
```
### Configuration:

Edit config.ini and change variables. Example configuration for IRCNet:
```
[twitch]
twitch_user = TwitchDev
twitch_client_id = xxxxxxxxxxxxxxxxx
twitch_secret = xxxxxxxxxxxxxxx

[irc]
server = open.ircnet.net
port = 6667
channel = #twitch
nickname = TwitchIRCBot

```
### Connecting bot to IRC server:
```
$ python3 twitchircbot.py
```
