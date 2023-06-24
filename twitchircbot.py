import os
import requests
import json
import threading
import configparser
import irc.bot

config = configparser.ConfigParser()
config.read('config.ini')

server = config.get('irc', 'server')
port = config.getint('irc', 'port')
channel = config.get('irc', 'channel')
nickname = config.get('irc', 'nickname')

twitch_user = config.get('twitch', 'twitch_user')
twitch_client_id = config.get('twitch', 'twitch_client_id')
twitch_secret = config.get('twitch', 'twitch_secret')

class TwitchIRCBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port, twitch_user):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.twitch_user = twitch_user
        self.filename = 'StreamTwitch_01Bot.txt'
        self.is_online = False

    def on_welcome(self, connection, event):
        connection.join(self.channel)

    def on_join(self, connection, event):
        self.check_twitch_status()

    def on_pubmsg(self, connection, event):
        pass

    def on_ping(self, connection, event):
        connection.pong(event.target)

    def check_twitch_status(self):
        try:

            token_url = 'https://id.twitch.tv/oauth2/token?client_id=' + twitch_client_id + \
                        '&client_secret=' + twitch_secret + '&grant_type=client_credentials'

            response = requests.post(token_url)
            response.raise_for_status()
            oauth_token = response.json()["access_token"]

            response = requests.get('https://api.twitch.tv/helix/streams?user_login=' +
                                    self.twitch_user, headers={'Authorization': 'Bearer ' +
                                                               oauth_token, 'Client-Id': twitch_client_id})
            var = json.loads(response.content)

            if var['data'] and not self.is_online:
                message = 'Stream of [' + self.twitch_user + '] (https://www.twitch.tv/' + self.twitch_user + ') is online'
                self.connection.privmsg(self.channel, message)
                self.is_online = True
                self.update_status_file()

            if not var['data'] and self.is_online:
                self.connection.privmsg(self.channel, self.twitch_user + ' is offline')
                self.is_online = False
                self.update_status_file()

        except Exception as e:
            print(e)

        threading.Timer(15, self.check_twitch_status).start()

    def update_status_file(self):
        with open(self.filename, 'w') as f:
            f.write(str(self.is_online))

    def run(self):
        self.check_twitch_status()
        self.start()

def main():
    bot = TwitchIRCBot(channel, nickname, server, port, twitch_user)
    bot.run()

if __name__ == "__main__":
    main()
