from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import token
from parsing import *  
import logging

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)  # Логирование

# Создание кнопок для получения информации о курсе и обмена валют
direction_buttons = [
    types.KeyboardButton(text='Узнать курс'),
    types.KeyboardButton(text='Обмен валюты')
]

direction_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*direction_buttons)

# Обработчик команды start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}! Это бот для обмена валюты.', reply_markup=direction_keyboard)

# Обработчик сообщения (кнопка) "Узнать курс"
@dp.message_handler(text='Узнать курс')
async def info_currency_rate(message: types.Message):
    await message.answer(f'''USD/KGS: {USD_KGS}
EURO/KGS: {EURO_KGS}
RUB/KGS: {RUB_KGS}
KZT/KGS: {KZT_KGS}''')

# Создание кнопок для обмена валют
obmen_buttons = [
    types.KeyboardButton(text='USD'),
    types.KeyboardButton(text='EURO'),
    types.KeyboardButton(text='RUB'),
    types.KeyboardButton(text='KZT'),
    types.KeyboardButton(text='KGS')
]

obmen_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*obmen_buttons)

# Далее - машина состояний
class EnrollState(StatesGroup):
    user_valute = State()
    bank_valute = State()
    user_money = State()

@dp.message_handler(text='Обмен валюты')
async def obmen_valute(message: types.Message):
    await message.answer("Введите валюту, которую хотите обменять", reply_markup=obmen_keyboard)
    await EnrollState.user_valute.set()

@dp.message_handler(state=EnrollState.user_valute)
async def valute_user(message: types.Message, state: FSMContext):
    await state.update_data(user_valute=message.text)
    await message.answer("На какую валюту хотите обменять?")
    await EnrollState.bank_valute.set()

@dp.message_handler(state=EnrollState.bank_valute)
async def valute_bank(message: types.Message, state: FSMContext):
    await state.update_data(bank_valute=message.text)
    await message.answer("Введите сумму, которую хотите обменять")
    await EnrollState.user_money.set()

@dp.message_handler(state=EnrollState.user_money)
async def user_money(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_valute = data['user_valute']
    bank_valute = data['bank_valute']
    # перевел user money на тип данных float чтобы было возможно сделать мотиматическите опертции 
    user_money = float(message.text)

    if user_valute == 'USD' and bank_valute == 'KGS':
        user_update_money = user_money * USD_KGS
        await message.answer(f"Вы даете {user_money} долларов, получаете {user_update_money} сом")

    elif user_valute == 'EURO' and bank_valute == 'KGS':
        user_update_money = user_money * EURO_KGS
        await message.answer(f"Вы даете {user_money} евро, получаете {user_update_money} сом")

    elif user_valute == 'RUB' and bank_valute == 'KGS':
        user_update_money = user_money * RUB_KGS
        await message.answer(f"Вы даете {user_money} рублей, получаете {user_update_money} сом")

    elif user_valute == 'KZT' and bank_valute == 'KGS':
        user_update_money = user_money * KZT_KGS
        await message.answer(f"Вы даете {user_money} тенге, получаете {user_update_money} сом")

    await state.finish()

    
executor.start_polling(dp, skip_updates=True)








