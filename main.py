import requests
import yaml
from time import sleep

import telebot

from logging_setup import logging

with open('TOKEN.yml') as file:
    token = yaml.safe_load(file)
BOT_TOKEN = token['Bot_token']

bot = telebot.TeleBot(BOT_TOKEN)
start_txt = 'Hi! Cats are in touch! \n Catch a random fact about cats!'


@bot.message_handler(commands=['start'])
def start(message):
    logging.info(f"Bot sent start message")
    logging.info(f"start_txt: {start_txt}")
    bot.send_message(message.from_user.id, start_txt)
    url = 'https://catfact.ninja/fact'
    cat_fact_json = requests.get(url).json()
    # simulation of waiting for a response from the server
    for i in range(3):
        logging.info('wait response from server %d seconds', i, extra={'same_line': True})
        sleep(1)
    cat_fact_str = cat_fact_json['fact']
    logging.info(f"Bot get fact from server")
    logging.info(f"fact about cat: {cat_fact_str}")
    bot.send_message(message.from_user.id, cat_fact_str)


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            logging.error('Something is going wrong!')
