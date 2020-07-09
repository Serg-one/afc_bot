from aiogram.dispatcher.filters.state import State, StatesGroup


# Класс для транзакций
# Wallet_Address - ожидаем получения номера кошелька
# Amount - ожидаем ввода суммы
class Transaction(StatesGroup):
    Wallet_Address = State()
    Amount = State()
