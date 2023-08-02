import telebot
from telebot import types

bot = telebot.TeleBot("6433719050:AAE6tnR7jOSBza4uelfvAW5JTYmQW-GiAk8")

print('_____ START BOT _____')
counters = {
    "menu": 0
}
users = {}

### REPLY KEYBOARD

def main_reply_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('💡Ask me'), types.KeyboardButton('💧Btn 2'), types.KeyboardButton('🔥Btn 3'))
    markup.row(types.KeyboardButton('InlineMenu'))
    markup.row(types.KeyboardButton('/start'), types.KeyboardButton('/update'))
    return markup

def second_reply_menu():
    markup_2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup_2.row(types.KeyboardButton('Btn1'), types.KeyboardButton('Btn2'), types.KeyboardButton('Btn3'))
    markup_2.row(types.KeyboardButton('Btn4'), types.KeyboardButton('Btn5'))
    markup_2.row(types.KeyboardButton('back'), types.KeyboardButton('next'))
    return markup_2

def third_reply_menu():
    markup_3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup_3.row(types.KeyboardButton('Btn6'), types.KeyboardButton('Btn7'), types.KeyboardButton('Btn8'))
    markup_3.row(types.KeyboardButton('back'), types.KeyboardButton('main'), types.KeyboardButton('next'))
    return markup_3

def fourth_reply_menu():
    markup_4 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup_4.row(types.KeyboardButton('Btn9'), types.KeyboardButton('Btn10'))
    markup_4.row(types.KeyboardButton('back'), types.KeyboardButton('main'))
    return markup_4

### INLINE MENU

def i_test_menu():
    kb = types.InlineKeyboardMarkup()
    btn_one = types.InlineKeyboardButton('Btn one', callback_data='Btn1')
    btn_two = types.InlineKeyboardButton('Show Photo', callback_data='photo')
    kb.row(btn_one, btn_one)
    kb.row(btn_two)
    return kb

def get_user_name(msg):
    cid = msg.chat.id
    txt = msg.text
    users[f'{cid}'] = {}
    users[f'{cid}']['name'] = txt
    mess = bot.send_message(cid, 'Input your age: ')
    bot.register_next_step_handler(mess, get_user_age)

def get_user_age(msg):
    cid = msg.chat.id
    txt = msg.text
    users[f"{cid}"]["age"] = txt
    msg_text = f'Name: {users[f"{cid}"]["name"]} \n' \
               f'Age: {users[f"{cid}"]["age"]}'
    bot.send_message(cid, msg_text, reply_markup=main_reply_menu())

@bot.message_handler(commands=['start'])
def send_welcome(msg):
    cid = msg.chat.id
    temp_text = '<u>Test</u>'
    bot.send_message(cid, temp_text, reply_markup=main_reply_menu(), parse_mode='html')

@bot.message_handler(commands=['update'])
def some_msg(msg):
    bot.reply_to(msg, "Update✅", reply_markup=main_reply_menu(), parse_mode='html')

@bot.callback_query_handler(func=lambda call: True)
def inline_menu(call):
    cid = call.message.chat.id
    data = call.data
    if data == 'Btn1':
        bot.send_message(cid, 'Success inline key!')
    elif data == 'photo':
        photo = open('img/oppenheimer.png', 'rb')
        bot.send_photo(cid, photo, caption='Photo')

@bot.message_handler(func=lambda message: True)
def echo_all(msg):
    cid = msg.chat.id
    if msg.text == 'InlineMenu':
        bot.send_message(cid, 'InlineMenu', reply_markup=i_test_menu())

    elif msg.text == '💧Btn 2' and counters['menu'] == 0:
        bot.send_message(cid, 'Done✅', reply_markup=second_reply_menu())
        counters['menu'] += 1
    elif msg.text == 'next' and counters['menu'] == 1:
        bot.send_message(cid, 'Done✅', reply_markup=third_reply_menu())
        counters['menu'] += 1
    elif msg.text == 'next' and counters['menu'] == 2:
        bot.send_message(cid, "Done✅", reply_markup=fourth_reply_menu())
        counters['menu'] += 1

    elif msg.text == 'main':
        bot.send_message(cid, "Returned to main✅", reply_markup=main_reply_menu())
        counters['menu'] -= counters['menu']
    elif msg.text == 'back' and counters['menu'] == 1:
        bot.send_message(cid, "Returned back✅", reply_markup=main_reply_menu())
        counters['menu'] -= counters['menu']
    elif msg.text == 'back' and counters['menu'] == 2:
        bot.send_message(cid, "Returned back✅", reply_markup=second_reply_menu())
        counters['menu'] -= 1
    elif msg.text == 'back' and counters['menu'] == 3:
        bot.send_message(cid, "Returned back✅", reply_markup=third_reply_menu())
        counters['menu'] -= 1
    elif msg.text == '💡Ask me':
        mess = bot.send_message(cid, 'Input your name: ')
        bot.register_next_step_handler(mess, get_user_name)

bot.infinity_polling()