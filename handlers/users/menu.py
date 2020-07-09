import hashlib
import json
from datetime import datetime

import requests
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from data.config import AUTH_URL, GET_BALANCE_URL, E_MAIL, REG_URL, BOT_ID, REFILL_URL, CHECK_URL
from keyboards.inline.callback_datas import menu_callback, submenu_callback
from keyboards.inline.menu_buttons import menu, sub_menu
from loader import dp

# TODO Добавить обработку ошибок
# TODO Добавить функцию вывода средств с FSM

secret = ""  # секретный ключ получаемый после авторизации
token = ""  # токен авторизации получаемый после авторизации
request_id = ""  # штамп текущей даты\времени
sign = ""  # сгенерированный ключ авторизации запроса


# Функция создания запроса
# request_id - штамп текущей даты\времени
# sign - генерация ключа авторизации запроса#
def create_request(url):
    global request_id, sign

    request_id = str(datetime.now())
    sign = hashlib.sha256((request_id + secret).encode('utf-8')).hexdigest()

    s = requests.Session()
    s.headers['content-type'] = 'application/json'
    s.headers['X-Auth-Token'] = token
    s.headers['X-Auth-Sign'] = sign

    response = s.post(url, json={"request_id": request_id})
    print(response)

    if response:
        return response
    else:
        print(f'Ошибка - не получен ответ от сервера')


# Функция проверки существования кошелька
# В конфигурационном файле должен быть указан путь к API проверки
def wallet_check(message: Message):
    response = create_request(CHECK_URL)
    if response:
        check_status = json.loads(response.text)
        if check_status['status']:
            await message.answer("Кошелек существует\n", reply_markup=sub_menu)
        else:
            await message.answer("Кошелек не существует\n", reply_markup=sub_menu)
        return check_status['status']
    else:
        print(response)
        await message.answer("Что-то пошло не так. Попробуйте еще раз\n", reply_markup=sub_menu)
        return False


# Вывод главного меню
@dp.message_handler(Command('menu'))
async def show_menu(message: Message):
    await message.answer("Выберите действие: \n", reply_markup=menu)


# Регистрция нового пользователя
# В конфигурационном файле должны быть обязательно указаны e-mail, bot_id
@dp.callback_query_handler(menu_callback.filter(item_name="sign_up"))
async def sign_user(call: CallbackQuery):
    await call.answer(cache_time=20)
    s = requests.Session()
    response = s.post(REG_URL,
                      json={"email": E_MAIL,
                            "chat_id": BOT_ID}
                      )
    sign_status = json.loads(response.text)
    print(sign_status)
    if sign_status["status"]:
        await call.message.answer("Вы успешно зарегестрированы! \n", reply_markup=menu)
    else:
        await call.message.answer(sign_status['error']['message'] + "\n", reply_markup=menu)


# Логин существующего пользователя
# В конфигурационном файле должен быть обязательно указан bot_id
@dp.callback_query_handler(menu_callback.filter(item_name="login"))
async def auth_user(call: CallbackQuery):
    global secret, token
    await call.answer(cache_time=20)
    s = requests.Session()
    response = s.post(AUTH_URL,
                      json={"chat_id": BOT_ID,
                            "request_id": str(datetime.now())}
                      )

    login_status = json.loads(response.text)
    if login_status["status"]:
        # Получение токена и секретного ключа
        secret = login_status["result"]["data"]["secret"]
        token = login_status["result"]["token"]
        await call.message.answer("Вход выполнен успешно!\n", reply_markup=sub_menu)
    elif not login_status['status']:
        await call.message.answer(login_status['error']['message'] + "\n", reply_markup=menu)
    # Если не получен ответ
    else:
        print(response)
        await call.message.answer("Что-то пошло не так. Попробуйте еще раз\n", reply_markup=menu)

    return secret, token


# Проверка текущего баланса
@dp.callback_query_handler(submenu_callback.filter(item_name="balance"))
async def check_balance(call: CallbackQuery):
    await call.answer(cache_time=20)
    if wallet_check(call.message):
        response = create_request(GET_BALANCE_URL)

        if response:
            balance_status = json.loads(response.text)
            if balance_status:
                quantity = balance_status["result"]["balance"]
                currency = balance_status["result"]["currency"]

            await call.message.answer(f"На вашем счете {quantity} {currency}\n", reply_markup=sub_menu)

        else:
            print(response)
            await call.message.answer("Что-то пошло не так. Попробуйте еще раз\n", reply_markup=menu)


#
@dp.callback_query_handler(submenu_callback.filter(item_name="wallet"))
async def wallet_show(call: CallbackQuery):
    await call.answer(cache_time=20)
    if wallet_check(call.message):
        response = create_request(REFILL_URL)
        if response:
            view_status = json.loads(response.text)
            if view_status:
                address = view_status["result"]["address"]
            await call.message.answer(f'Номер Вашего кошелька {address}\n', reply_markup=sub_menu)
        else:
            print(response)
            await call.message.answer("Что-то пошло не так. Попробуйте еще раз\n", reply_markup=menu)


@dp.callback_query_handler(submenu_callback.filter(item_name="back"))
async def step_back(call: CallbackQuery):
    await call.message.answer("Возврат...                          \n", reply_markup=menu)


@dp.callback_query_handler(menu_callback.filter(item_name="exit"))
async def step_back(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=None)
