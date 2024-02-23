from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from src.app.utils import predict_with_trained_model
import hashlib
import logging
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

class BotMessageAnswer:

    def start(self):
        executor.start_polling(dp, skip_updates=True)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    """Handler to introduce bot himself."""

    await message.answer("""Привет! Я бот CyberTolya. Я здесь для того, чтобы помочь \
                        тебе освоить анализ данных и машинное обучение. \
                        Задай мне вопрос и я подберу для тебя наиболее \
                        подходящие видеоматериалы.""")
    #print('Пользователь нажал старт')
    log.info('Bot started')
    #me=await bot.get_me().username
    



@dp.message_handler()
async def chat_answer(message: types.Message):
    """Test handler which duplicate every message like echo."""
    me = await bot.get_me()
    trigger_word='@Cyber_Tolya'
    #print(me.username)
    if message.chat.type == 'private':
        link = predict_with_trained_model(message.text)
        await message.answer(link, parse_mode=types.ParseMode.HTML)
        log.info('Bot has message in private')
        me = await bot.get_me()
        print(me.username)
        #if f'{me.username}' in message.text:
        #    print('ok')
    elif message.text.startswith(trigger_word):
        #print('It is group')
        #and f'{me.username}' in message.text 
        link = predict_with_trained_model(message.text)
        await message.answer(link, parse_mode=types.ParseMode.HTML)    
        #log.info('Bot has message in group')
        logdata=message.chat.type
        log.info('Bot has message in '+f"{logdata}")
    elif message.text=='/start_CyberTolya':
        await message.answer("""Привет! Я бот CyberTolya. Я здесь для того, чтобы помочь \
                        тебе освоить анализ данных и машинное обучение. \
                        Задай мне вопрос и я подберу для тебя наиболее \
                        подходящие видеоматериалы.""")
        logdata=message.chat.type
        log.info('Bot has message in '+f"{logdata}")
    else:
        logdata=message.chat.type
        log.info(logdata)



@dp.inline_handler()
async def inline_answer(inline_query: types.InlineQuery):
    """Test handler which duplicate every message like echo."""
    text = inline_query.query or "echo"
    #input_content = types.InputTextMessageContent(text)
    link = predict_with_trained_model(text)
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    item = [types.InlineQueryResultArticle(
        id=result_id,
        title=link,
        input_message_content=types.InputTextMessageContent(message_text=link, 
                                                            parse_mode=types.ParseMode.HTML))]
    await inline_query.answer(item, cache_time=1, is_personal=True)
    log.info('Bot has inline message')