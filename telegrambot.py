import os
import time
import telepot
import RPi.GPIO as GPIO
import requests
import netifaces as ni
import subprocess
import re
import vlc
from gtts import gTTS

it = re.compile('/tts_it *')
en = re.compile('/tts_en *')

def tts_ita(string):
    tts = gTTS(string[8:],lang='it')
    tts.save('tts.mp3')
    vlc.MediaPlayer("tts.mp3").play()
    
def tts_eng(string):
    tts = gTTS(string[8:],lang='en')
    tts.save('tts.mp3')
    vlc.MediaPlayer("tts.mp3").play()
    
    
def open_kodi():
    subprocess.call(['sh', 'launch_kodi.sh'])
    return 'Opening Kodi'

def get_ip_address(ifname):
    try:
        ni.ifaddresses(ifname)
        ip = ni.ifaddresses(ifname)[ni.AF_INET][0]['addr']
        return ip
    except:
        return f'No address found for {ifname}'

def ip():
    url = "http://checkip.dyndns.org"
    request = requests.get(url)
    clean = request.text.split(': ', 1)[1]
    return clean.split('</body></html>', 1)[0]

#LED
def on(pin):
        GPIO.output(pin,GPIO.HIGH)
        return 'The led is on'
def off(pin):
        GPIO.output(pin,GPIO.LOW)
        return 'The led is off'
# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
# set up GPIO output channel
GPIO.setup(11, GPIO.OUT)

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text'].lower()

    print('Got command: %s' % command)

    if command == '/on':
       bot.sendMessage(chat_id, on(11))
    elif command =='/off':
       bot.sendMessage(chat_id, off(11))
    elif command =='/ip':
       bot.sendMessage(chat_id, ip())
    elif (command =='/wlan0'):
       bot.sendMessage(chat_id, get_ip_address('wlan0'))
    elif (command =='/eth0'):
       bot.sendMessage(chat_id, get_ip_address('eth0'))
    elif (it.match(command)):
       tts_ita(command)
       bot.sendMessage(chat_id, 'Frase letta')
    elif (en.match(command)):
       tts_eng(command)
       bot.sendMessage(chat_id, 'Sentence read')
    elif command == '/kodi' :
        bot.sendMessage(chat_id,open_kodi())
    elif command=='/help':
        bot.sendMessage(chat_id,'''
here are the commands and what they do:
/on Turn on the LED on my Raspberry Pi
/off Turn off the LED on my Raspberry Pi
/ip Get the IP address of my raspberry Pi
/wlan0 and /eth0 get you the local IP address
/kodi open kodi on my raspberry Pi. I'd appreciate if you didn't''')

bot = telepot.Bot('1317490638:AAERowzbM91ne1EZE06_n4GWxzWwA0OQFsc')
bot.message_loop(handle)
print('I am listening...')

while 1:
    try:
        time.sleep(10)
    
    except KeyboardInterrupt:
        print('\n Program interrupted')
        GPIO.cleanup()
        exit()
    
    except:
        print('Other error or exception occured!')
        GPIO.cleanup()
