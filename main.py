import datetime
import json
from typing import List, Dict
import parser2
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

TOKEN = '6312104744:AAGUU7QrN2q_g7fXsgyQxTmZOTu2Tt-etNQ'
bot = telebot.TeleBot(TOKEN)

news = {}


def parse_call(call: CallbackQuery) -> Dict:
    return json.loads(call.data)


def serialize_call_data(data: Dict) -> str:
    return json.dumps(data)


ui_markup = [
    InlineKeyboardButton('Select Another', callback_data=serialize_call_data({
        'action': 'ui', 'command': 'select'
    })),
    InlineKeyboardButton('Quit', callback_data=serialize_call_data({
        'action': 'ui', 'command': 'quit'
    })),
    InlineKeyboardButton('List News', callback_data=serialize_call_data({
        'action': 'ui', 'command': 'list'
    }))
]


def get_news() -> dict:
    global news
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    url = f'https://kaktus.media/?lable=8&date={today}&order=time'
    if not news or news['validated'] < datetime.datetime.now():
        news = {
            'validated': datetime.datetime.now() + datetime.timedelta(seconds=60),
            'news': parser2.get_news(parser2.get_html(url))
        }
        return news
    return news


@bot.message_handler(commands=['start'])
def start_handler(message: Message):
    bot.send_message(message.chat.id, 'This actions are available', reply_markup=InlineKeyboardMarkup().row(
        *ui_markup
    ))


def list_news(message: Message):
    news_list = get_news()
    bot.send_message(message.chat.id, '\n'.join([
        f'{news_list["news"].index(n)+1}. {n["title"]}'
        for n in news_list['news']
    ]))
    bot.send_message(message.chat.id, 'Type number of news')
    bot.register_next_step_handler(message, show_details)


def show_details_handler(message: Message):
    bot.send_message(message.chat.id, 'Enter number of news between 1 and 20')
    bot.register_next_step_handler(message, show_details)


def show_details(message: Message):
    if message.text.isdigit() and 1 <= int(message.text) <= 20:
        news_item = get_news()['news'][int(message.text) - 1]
        keyboard = InlineKeyboardMarkup()
        keyboard_buttons = ui_markup.copy()
        keyboard_buttons.append(InlineKeyboardButton('Description', callback_data=serialize_call_data({
            'action': 'show_description',
            'news_id': int(message.text) - 1
        })))
        keyboard.add(
            *keyboard_buttons
        )
        bot.send_photo(message.chat.id, news_item['image'], news_item['title'], reply_markup=keyboard)
    else:
        show_details_handler(message)


@bot.callback_query_handler(func=lambda call: parse_call(call)['action'] == 'show_description')
def show_description(call: CallbackQuery):
    call_data = parse_call(call)
    news_item = get_news()['news'][call_data['news_id']]
    bot.send_message(
        call.message.chat.id, parser2.get_description(parser2.get_html(news_item['link'])),
        reply_markup=InlineKeyboardMarkup().row(*ui_markup)
    )


@bot.message_handler(commands=['quit'])
def quit_command(message: Message):
    bot.send_message(message.chat.id, 'Good Bye')


@bot.callback_query_handler(func=lambda call: parse_call(call)['action'] == 'ui')
def handle_ui_call(call: CallbackQuery):
    call_data = parse_call(call)

    action_list = {
        'list': list_news,
        'select': show_details_handler,
        'quit': quit_command
    }

    action_list[call_data['command']](call.message)


bot.polling()
