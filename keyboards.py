from aiogram.types import ReplyKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(*["Start credit line"])
main_keyboard.add(*["View my credit lines"])

select_date_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
select_date_keyboard.add(*["30.05.2021", "31.05.2021", "1.06.2021"])
select_date_keyboard.add(*["2.06.2021", "3.06.2021", "4.06.2021"])
select_date_keyboard.add(*["Cancel"])
