from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import menu_callback, submenu_callback

# Главное меню
# Кнопки:
# 1. Регистрация - регистрация нового пользователя
# 2. Логин - логин существующего пользователя
# 3. Выход - возврат
menu = InlineKeyboardMarkup(row_width=1)

sign_up = InlineKeyboardButton(text="Регистрация", callback_data=menu_callback.new(item_name="signup"))
login = InlineKeyboardButton(text="Логин", callback_data=menu_callback.new(item_name="login"))
back = InlineKeyboardButton(text="Выход", callback_data="exit")

menu.insert(sign_up)
menu.insert(login)
menu.insert(back)

# Подменю с операциями
# Кнопки:
# 1. Посмотреть баланс - вывод баланса на экран
# 2. Отобразить номер кошелька - вывод адреса кошелька
# 3. Пополнение - пополнение кошелька
# 4. Вывод - вывод средств
# 5. Назад - возврат в предыдущее меню
sub_menu = InlineKeyboardMarkup(row_width=1)

get_balance = InlineKeyboardButton(text="Посмотреть баланс", callback_data=submenu_callback.new(item_name='balance'))
wallet_address = InlineKeyboardButton(text="Отобразить номер кошелька", callback_data=submenu_callback.new(
                                      item_name='wallet'))
refill = InlineKeyboardButton(text="Пополнение", callback_data=submenu_callback.new(item_name='refill'))
withdraw = InlineKeyboardButton(text="Вывод", callback_data=submenu_callback.new(item_name='withdraw'))
back_to_menu = InlineKeyboardButton(text="Назад", callback_data=submenu_callback.new(item_name='back'))

sub_menu.insert(get_balance)
sub_menu.insert(wallet_address)
sub_menu.insert(refill)
sub_menu.insert(withdraw)
sub_menu.insert(back_to_menu)
