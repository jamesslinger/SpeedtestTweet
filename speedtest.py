#! /usr/bin/python3
## RASPBIAN Pi4 VERSION ##

import os
import re
import subprocess
import time
import tweepy


PROMISED_UP = 100.0
PROMISED_DOWN = 700.0


CONS_API_KEY = "ZH8bxiYyJ6TujX79V0q7vcZAb"
CONS_API_SECRET = "4j7imhjhs06dOMRVF3qAvrMfdBGkDtWeV5DEWhz8WmAmK8hOT4"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAAMafgEAAAAAEntAG7k42kT7Fue9IEWuOB5My1U%3DFfgwf5HCavTNT34QD4ec5u31otIQrGPvKNr5Iv1rNqm9AQijjt"
ACCESS_TOKEN = "1541797946152427523-FpaeMjiXZXdC5DQ1HTjlJ2KjefJGom"
AT_SECRET = "wb3rCVyRvj3pzstY1frFytT4wELbbsp13gzPqMjZaMOmH"
CLIENT_ID = "bk1BRWYtdEdoTVhFdHVtb21QOWg6MTpjaQ"
CLIENT_SECRET = "KrXVjUdSOjWXAWE_h4ABWUdkOsT1gdrX4tGvAH44HpFZX0xaHB"


class InternetSpeedTwitterBot:
    def __init__(self):
        self.promised_up = PROMISED_UP
        self.promised_down = PROMISED_DOWN
        self.current_down = 0.0
        self.current_up = 0.0
        self.ping = 0.0
        self.jitter = 0.0

    def get_internet_speed(self):
        response = subprocess.Popen('/usr/bin/speedtest --accept-license --accept-gdpr', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        ping = re.search('Latency:\s+(.*?)\s', response, re.MULTILINE)
        download = re.search('Download:\s+(.*?)\s', response, re.MULTILINE)
        upload = re.search('Upload:\s+(.*?)\s', response, re.MULTILINE)
        jitter = re.search('Latency:.*?jitter:\s+(.*?)ms', response, re.MULTILINE)

        ping = ping.group(1)
        download = download.group(1)
        upload = upload.group(1)
        jitter = jitter.group(1)

        try:
            f = open('/home/pi4/speedtest/speedtest.csv', 'a+')
            if os.stat('/home/pi4/speedtest/speedtest.csv').st_size == 0:
                    f.write('Date,Time,Ping (ms),Jitter (ms),Download (Mbps),Upload (Mbps)\r\n')
        except:
            pass

        f.write('{},{},{},{},{},{}\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), ping, jitter, download, upload))
        self.current_down = float(download)
        self.current_up = float(upload)
        self.ping = float(ping)
        self.jitter = float(jitter)


    def tweet_my_provider(self):
        client = tweepy.Client(bearer_token=BEARER_TOKEN)
        client = tweepy.Client(consumer_key=CONS_API_KEY,
                               consumer_secret=CONS_API_SECRET,
                               access_token=ACCESS_TOKEN,
                               access_token_secret=AT_SECRET)

        response = client.create_tweet(text=f"Hey Internet Service Provider, my internet speed isn't as promised."
                             f"\nIt's currently;"
                             f"\n- Down: {self.current_down}Mbps, Up: {self.current_up}Mbps"
                             f"\nwhen it should be at least;"
                             f"\n- Down: {self.promised_down}Mbps, Up: {self.promised_up}Mbps"
                             f"\n(Ping: {self.ping}ms, Jitter: {self.jitter}ms)"
                             f"\nWhat gives?")
        print("Tweet sent. All done. Goodbye.")


auto_checker = InternetSpeedTwitterBot()
auto_checker.get_internet_speed()

if auto_checker.current_down < auto_checker.promised_down or auto_checker.current_up < auto_checker.promised_up:
    print("Slow speeds, tweeting ISP!")
    auto_checker.tweet_my_provider()
else:
    print("Speed's good today! Ending application. Goodbye.")