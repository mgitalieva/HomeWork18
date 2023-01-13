import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message):
    text = f'Привет, {message.from_user.first_name}! Это бот для конвертации валют.\nУзнать как конвертировать: /help \
\nСписок доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=["help"])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу введите комманду в следующем формате:\n<имя валюты>  \
<в какую валюту перевести>  \
<количество переводимой валюты>\n\nУвидеть список всех доступных валют для конвертации: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Указано неверное количество параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'''Цена {amount} "{quote}" в "{base}" : {total_base}'''
        bot.send_message(message.chat.id, text)


bot.polling()
