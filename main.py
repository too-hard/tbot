import os
import pip
pip.main(['install', 'pytelegrambotapi'])
import telebot
from telebot import types
import time
from datetime import datetime, date, time

bot = telebot.TeleBot('6740900511:AAG-C64U3wU18kkV5oSxfsLe2vLoP9oqoIQ')
button_foo = types.InlineKeyboardButton('Сегодня', callback_data='today')
button_bar = types.InlineKeyboardButton('Завтра', callback_data='tomorrow')
button_baz = types.InlineKeyboardButton('Неделя', callback_data='week')

keyboard = types.InlineKeyboardMarkup()
keyboard.add(button_foo)
keyboard.add(button_bar)
keyboard.add(button_baz)

def get_r(week, day, weekcount):
  if week == 0:
    if day == 1:
      return "11:20 --- БЧиЖ (В-101 л)"
    elif day == 2:
      if weekcount >= 14:
        r = "8:00 --- ИТ (Д-229 лаб)\n9:40 --- ИТ (Д-229 лаб)"
        return r+"\n11:20 --- ВМ (Л-223 л)"
      else:
        return "11:20 --- ВМ (Л-223 л)"
    elif day == 3:
      return "9:40 --- Физра\n13:00 --- Физика (Л-209 л)"
    elif day == 4:
      return "11:20 --- ВМ (Д-504а пр)"
    elif day == 5:
      return "8:00 --- Физра\n11:20 --- БЧиЖ (Л-206 пр)\n13:00 --- БЧиЖ (Л-103 пр)"
    elif day == 6:
      return "8:00 --- Физика (Д-110/112/117 пр)"
  else:
    if day == 1:
      return "11:20 --- МвП (В-101 л)"
    elif day == 2:
      if weekcount <= 13:
        return "8:00 --- ВМТ (В-101 л)\n13:00 --- ВМТ (В-101 пр)"
      else:
        return "13:00 --- ВМТ (В-101 пр)"
    elif day == 3:
      return "9:40 --- Физра"
    elif day == 4:
      return "9:40 --- ИТ (Л-217 л)"
    elif day == 5:
      r = "8:00 --- Физра\n11:20 --- БЧиЖ (Л-206 пр)\n13:00 --- БЧиЖ (Л-103 пр)"
      return r+"\n14:40 --- МвП (В-206 пр)"
    elif day == 6:
      return "8:00 --- Физика (Д-110/112/117 пр)"
    else:
      return "На воскресенье расписания нет"
    
def get_week_r(week):
  r = ""
  a = get_r(week % 2, 1, week)
  if a is not None:
    r = "Понедельник:\n"+a
  a = get_r(week % 2, 2, week)
  if a is not None:
    r += "\n\nВторник:\n" + a
  a = get_r(week % 2, 3, week)
  if a is not None:
    r += "\n\nСреда:\n" + a
  a = get_r(week % 2, 4, week)
  if a is not None:
    r += "\n\nЧетверг:\n" + a
  a = get_r(week % 2, 5, week)
  if a is not None:
    r += "\n\nПятница:\n" + a
  a = get_r(week % 2, 6, week)
  if a is not None:
    r += "\n\nСуббота:\n" + a
  return r

@bot.message_handler(commands=['start'])
def button_message(message):
  bot.send_message(message.chat.id,'Какое расписание скинуть?'),reply_markup=keyboard)
  
@bot.message_handler(commands=['today'])
def today_message(message):
  d = datetime.utcnow().isocalendar()
  repl = get_r(d.week % 2, d.weekday, d.week)
  bot.send_message(message.chat.id,repl),reply_markup=keyboard)

@bot.message_handler(commands=['tomorrow'])
def tomorrow_message(message):
  d = datetime.utcnow().isocalendar()
  repl = ""
  if d.weekday == 7:
    repl = get_r((d.week+1) % 2, 1, d.week+1)
  else:
    repl = get_r(d.week % 2, d.weekday+1, d.week)
  bot.send_message(message.chat.id,repl),reply_markup=keyboard)

@bot.message_handler(commands=['week'])
def week_message(message):
  d = datetime.utcnow().isocalendar()
  repl = get_week_r(d.week)
  bot.send_message(message.chat.id,repl)#,reply_markup=keyboard)

#@bot.message_handler(content_types=['text'])
#def get_text_message(message):
#bot.send_message(message.from_user.id,message.text)
# echo-функция, которая отвечает на любое текстовое сообщение таким же текстом   
#if message.text == "Привет":
#bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")

bot.polling(non_stop=True, interval=0) #запуск бота
