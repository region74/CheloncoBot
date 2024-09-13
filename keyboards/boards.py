from aiogram import types


def device_kb():
    buttons = [[
        types.InlineKeyboardButton(text="Принять с ремонта", callback_data="get_device"),
        types.InlineKeyboardButton(text="Отправить в ремонт", callback_data="send_device"),
    ]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def device_place_change():
    buttons = [[
        types.InlineKeyboardButton(text="Изменить", callback_data="change_place"),
        types.InlineKeyboardButton(text="Оставить", callback_data="skip_place"),
    ]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
