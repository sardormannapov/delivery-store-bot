import geopy
from telebot import types
import datetime

from localization.keyboard_lang import send_contact, reseume_sending, back_to_main_menu, send_location, my_locations, back_button_name, menu_text, \
    book_table, go_delivery, manual, resume, phone_delivery,\
    rate_me, location_contact, social_media, back_button, change_language_text, yes_word, no_word, save_to_basket, \
    basket_button, \
    booking_meal, clear_basket, time_delivery, cash_payment, cancel, conformation, settings_text


def generate_contact(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reg_button = types.KeyboardButton(text=send_contact[lang], request_contact=True)
    keyboard.row(reg_button)
    return keyboard


def generate_contact_phone(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reg_button = types.KeyboardButton(text="📞", request_contact=True)
    btn_back = types.KeyboardButton(text=back_to_main_menu[lang])
    keyboard.row(reg_button)
    keyboard.row(btn_back)
    return keyboard


def bron_contact(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reg_button = types.KeyboardButton(text="📞", request_contact=True)
    btn_back = types.KeyboardButton(text=back_to_main_menu[lang])
    keyboard.row(reg_button)
    keyboard.row(btn_back)
    return keyboard

def deliver_contact(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reg_button = types.KeyboardButton(text=phone_delivery[lang])
    btn_back = types.KeyboardButton(text=back_button[lang])
    keyboard.row(reg_button)
    keyboard.row(btn_back)
    return keyboard

def sending_resume(lang, url):
    keyboard = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text=reseume_sending[lang], url=url)
    keyboard.row(btn)
    return keyboard


def get_geolocation(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    geo_button = types.KeyboardButton(text=send_location[lang], request_location=True)
    my_geo = types.KeyboardButton(text=my_locations[lang])
    btn_back = types.KeyboardButton(text=back_to_main_menu[lang])
    keyboard.row(geo_button)
    keyboard.row(my_geo)
    keyboard.row(btn_back)
    return keyboard


def generate_main_menu(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_menu = types.KeyboardButton(text=menu_text[lang])
    btn_bron = types.KeyboardButton(text=book_table[lang])
    btn_change = types.KeyboardButton(text=settings_text[lang])
    btn_grade = types.KeyboardButton(text=rate_me[lang])
    btn_loc = types.KeyboardButton(text=location_contact[lang])
    btn_inst = types.KeyboardButton(text=social_media[lang])
    btn_manual = types.KeyboardButton(text=manual[lang])
    btn_resume = types.KeyboardButton(text=resume[lang])
    keyboard.row(btn_menu, btn_bron)
    keyboard.row(btn_grade, btn_change)
    keyboard.row(btn_loc, btn_inst)
    keyboard.row(btn_manual, btn_resume)
    return keyboard


def generate_net(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_menu = types.KeyboardButton(text="Telegram")
    btn_bron = types.KeyboardButton(text="Instagram")
    btn_back = types.KeyboardButton(text=back_button[lang])
    keyboard.row(btn_menu, btn_bron)
    keyboard.row(btn_back)
    return keyboard


def generate_link_tg(url):
    keyboard = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text="Telegram", url=url)
    keyboard.row(btn)
    return keyboard


def generate_link_inst(url):
    keyboard = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text="Instagram", url=url)
    keyboard.row(btn)
    return keyboard


def generate_grade():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_star_5 = types.KeyboardButton(text="⭐⭐⭐⭐⭐")
    btn_star_4 = types.KeyboardButton(text="⭐⭐⭐⭐")
    btn_star_3 = types.KeyboardButton(text="⭐⭐⭐")
    btn_star_2 = types.KeyboardButton(text="⭐⭐")
    btn_star_1 = types.KeyboardButton(text="⭐")
    keyboard.row(btn_star_5)
    keyboard.row(btn_star_4)
    keyboard.row(btn_star_3)
    keyboard.row(btn_star_2)
    keyboard.row(btn_star_1)
    return keyboard


def generate_setting(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_lan = types.KeyboardButton(text=change_language_text[lang])
    btn_back = types.KeyboardButton(text=back_button[lang])
    keyboard.row(btn_lan)
    keyboard.row(btn_back)
    return keyboard


# boshladik menyu uchun
def change_lang(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_uzb = types.KeyboardButton(text="🇺🇿O'zbekcha")
    btn_rus = types.KeyboardButton(text="🇷🇺Русский")
    btn_eng = types.KeyboardButton(text="🇬🇧English")
    btn_back = types.KeyboardButton(text=back_button[lang])
    keyboard.row(btn_uzb, btn_rus, btn_eng)
    keyboard.row(btn_back)
    return keyboard


def generate_bron():
    today = datetime.date.today()
    formatted_today = today.strftime('%d-%m')
    tomorrow = today + datetime.timedelta(days=1)
    tomorrow_formatted = tomorrow.strftime('%d-%m')
    after_tomorrow = today + datetime.timedelta(days=2)
    after_tomorrow_formatted = after_tomorrow.strftime('%d-%m')
    after_tomorrow_2 = today + datetime.timedelta(days=3)
    after_tomorrow_formatted_2 = after_tomorrow_2.strftime('%d-%m')
    after_tomorrow_3 = today + datetime.timedelta(days=4)
    after_tomorrow_formatted_3 = after_tomorrow_3.strftime('%d-%m')
    after_tomorrow_4 = today + datetime.timedelta(days=5)
    after_tomorrow_formatted_4 = after_tomorrow_4.strftime('%d-%m')
    after_tomorrow_5 = today + datetime.timedelta(days=6)
    after_tomorrow_formatted_5 = after_tomorrow_5.strftime('%d-%m')
    keyboard = types.InlineKeyboardMarkup()
    btn_today = types.InlineKeyboardButton(text=formatted_today, callback_data=formatted_today)
    btn_tomorrow = types.InlineKeyboardButton(text=tomorrow_formatted, callback_data=tomorrow_formatted)
    btn_after_tomorrow = types.InlineKeyboardButton(text=after_tomorrow_formatted,
                                                    callback_data=after_tomorrow_formatted)

    btn_after_tomorrow_2 = types.InlineKeyboardButton(text=after_tomorrow_formatted_2,
                                                    callback_data=after_tomorrow_formatted_2)

    btn_after_tomorrow_3 = types.InlineKeyboardButton(text=after_tomorrow_formatted_3,
                                                    callback_data=after_tomorrow_formatted_3)

    btn_after_tomorrow_4 = types.InlineKeyboardButton(text=after_tomorrow_formatted_4,
                                                    callback_data=after_tomorrow_formatted_4)

    btn_after_tomorrow_5 = types.InlineKeyboardButton(text=after_tomorrow_formatted_5,
                                                    callback_data=after_tomorrow_formatted_5)


    keyboard.row(btn_today, btn_tomorrow, btn_after_tomorrow)
    keyboard.row(btn_after_tomorrow_2, btn_after_tomorrow_3, btn_after_tomorrow_4)
    keyboard.row(btn_after_tomorrow_5)
    return keyboard


def generate_bron_times_today():
    current_time = datetime.datetime.now().time()
    keyboard = types.InlineKeyboardMarkup()
    btn_now1 = types.InlineKeyboardButton(text='09:00-10:30', callback_data="09:00-10:30")
    btn_now2 = types.InlineKeyboardButton(text='11:00-12:30', callback_data="11:00-12:30")
    btn_now3 = types.InlineKeyboardButton(text='13:00-14:30', callback_data="13:00-14:30")
    btn_now4 = types.InlineKeyboardButton(text='15:00-16:30', callback_data="15:00-16:30")
    btn_now5 = types.InlineKeyboardButton(text='17:00-18:30', callback_data="17:00-18:30")
    btn_now6 = types.InlineKeyboardButton(text='19:00-20:30', callback_data="19:00-20:30")
    btn_now7 = types.InlineKeyboardButton(text='21:00-22:00', callback_data="21:00-22:00")
    if current_time > datetime.time(8, 0) and current_time < datetime.time(9, 0):
        keyboard.row(btn_now1, btn_now2)
        keyboard.row(btn_now3, btn_now4)
        keyboard.row(btn_now5, btn_now6)
        keyboard.row(btn_now7)

    elif current_time > datetime.time(9, 0) and current_time < datetime.time(11, 0):
        keyboard.row(btn_now2, btn_now3)
        keyboard.row(btn_now4, btn_now5)
        keyboard.row(btn_now6, btn_now7)


    elif current_time > datetime.time(11, 0) and current_time < datetime.time(13, 0):
        keyboard.row(btn_now3, btn_now4)
        keyboard.row(btn_now5, btn_now6)
        keyboard.row(btn_now7)

    elif current_time > datetime.time(13, 0) and current_time < datetime.time(15, 0):
        keyboard.row(btn_now4, btn_now5)
        keyboard.row(btn_now6, btn_now7)


    elif current_time > datetime.time(15, 0) and current_time < datetime.time(17, 0):
        keyboard.row(btn_now5, btn_now6)
        keyboard.row(btn_now7)


    elif current_time > datetime.time(17, 0) and current_time < datetime.time(19, 0):
        keyboard.row(btn_now6, btn_now7)


    elif current_time > datetime.time(19, 0) and current_time < datetime.time(21, 0):
        keyboard.row(btn_now7)

    return keyboard


def generate_bron_times():
    keyboard = types.InlineKeyboardMarkup()
    btn_now1 = types.InlineKeyboardButton(text='09:00-10:30', callback_data="09:00-10:30")
    btn_now2 = types.InlineKeyboardButton(text='11:00-12:30', callback_data="11:00-12:30")
    btn_now3 = types.InlineKeyboardButton(text='13:00-14:30', callback_data="13:00-14:30")
    btn_now4 = types.InlineKeyboardButton(text='15:00-16:30', callback_data="15:00-16:30")
    btn_now5 = types.InlineKeyboardButton(text='17:00-18:30', callback_data="17:00-18:30")
    btn_now6 = types.InlineKeyboardButton(text='19:00-20:30', callback_data="19:00-20:30")
    btn_now7 = types.InlineKeyboardButton(text='21:00-22:00', callback_data="21:00-22:00")
    keyboard.row(btn_now1, btn_now2)
    keyboard.row(btn_now3, btn_now4)
    keyboard.row(btn_now5, btn_now6)
    keyboard.row(btn_now7)

    return keyboard


def generate_bron_person():
    keyboard = types.InlineKeyboardMarkup()
    btn_per_2 = types.InlineKeyboardButton(text='2', callback_data="2")
    btn_per_3 = types.InlineKeyboardButton(text='3', callback_data="3")
    btn_per_4 = types.InlineKeyboardButton(text='4', callback_data="4")
    btn_per_5 = types.InlineKeyboardButton(text='5', callback_data="5")
    btn_per_6 = types.InlineKeyboardButton(text='6', callback_data="6")
    btn_per_7 = types.InlineKeyboardButton(text='7', callback_data="7")
    btn_per_8 = types.InlineKeyboardButton(text='8', callback_data="8")
    btn_per_9 = types.InlineKeyboardButton(text='9', callback_data="9")
    btn_per_10 = types.InlineKeyboardButton(text='10', callback_data="10")
    btn_per_11 = types.InlineKeyboardButton(text='11', callback_data="11")
    btn_per_12 = types.InlineKeyboardButton(text='12', callback_data="12")
    btn_per_13 = types.InlineKeyboardButton(text='13', callback_data="13")
    btn_per_14 = types.InlineKeyboardButton(text='14', callback_data="14")
    btn_per_15 = types.InlineKeyboardButton(text='15', callback_data="15")
    btn_per_16 = types.InlineKeyboardButton(text='16', callback_data="16")
    keyboard.row(btn_per_2, btn_per_3, btn_per_4)
    keyboard.row(btn_per_5, btn_per_6, btn_per_7)
    keyboard.row(btn_per_8, btn_per_9, btn_per_10)
    keyboard.row(btn_per_11, btn_per_12, btn_per_13)
    keyboard.row(btn_per_14, btn_per_15, btn_per_16)
    return keyboard


def user_info(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_ok = types.KeyboardButton(text=yes_word[lang])
    btn_no = types.KeyboardButton(text=no_word[lang])
    keyboard.row(btn_ok, btn_no)
    return keyboard


def commit_location(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_ok = types.KeyboardButton(text=yes_word[lang])
    btn_no = types.KeyboardButton(text=no_word[lang])
    keyboard.row(btn_ok, btn_no)
    return keyboard


def generate_catalogs(catalog_list, lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in range(0, len(catalog_list["body"]), 2):
        if len(catalog_list["body"]) % 2 == 1 and i == len(catalog_list["body"]) - 1:
            keyboard.add(types.KeyboardButton(text=catalog_list["body"][i]["category_name"][lang]))
        else:
            keyboard.add(types.KeyboardButton(text=catalog_list["body"][i]["category_name"][lang]),
                         types.KeyboardButton(text=catalog_list["body"][i + 1]["category_name"][lang]))
    btn_deliver = types.KeyboardButton(text=go_delivery[lang])
    btn_back = types.KeyboardButton(text=back_to_main_menu[lang])
    keyboard.row(btn_deliver)
    keyboard.row(btn_back)
    return keyboard


def generate_subcatalogs(subcatalog_list, lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in range(0, len(subcatalog_list["body"]), 2):
        if len(subcatalog_list["body"]) % 2 == 1 and i == len(subcatalog_list["body"]) - 1:
            keyboard.add(types.KeyboardButton(text=subcatalog_list["body"][i]["subcategory_name"][lang]))
        else:
            keyboard.add(types.KeyboardButton(text=subcatalog_list["body"][i]["subcategory_name"][lang]),
                         types.KeyboardButton(text=subcatalog_list["body"][i + 1]["subcategory_name"][lang]))
    btn_back = types.KeyboardButton(text=back_button[lang])
    keyboard.row(btn_back)
    return keyboard


def generate_products(product_list, lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in range(0, len(product_list["body"]), 2):
        if len(product_list["body"]) % 2 == 1 and i == len(product_list["body"]) - 1:
            keyboard.add(types.KeyboardButton(text=product_list["body"][i]["product_name"][lang]))
        else:
            keyboard.add(types.KeyboardButton(text=product_list["body"][i]["product_name"][lang]),
                         types.KeyboardButton(text=product_list["body"][i + 1]["product_name"][lang]))
    btn_back = types.KeyboardButton(text=back_button[lang])
    keyboard.row(btn_back)
    return keyboard


def to_basket(lang):
    keyboard = types.InlineKeyboardMarkup()
    btn_order_1 = types.InlineKeyboardButton(text='➖', callback_data="-")
    btn_order_2 = types.InlineKeyboardButton("1", callback_data="number")
    btn_order_3 = types.InlineKeyboardButton(text='➕', callback_data="+")
    btn_order_4 = types.InlineKeyboardButton(text=save_to_basket[lang], callback_data="basket_call")
    keyboard.row(btn_order_1, btn_order_2, btn_order_3)
    keyboard.row(btn_order_4)
    return keyboard


def bastket_keyboard(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_savatcha = types.KeyboardButton(text=basket_button[lang])
    btn_back_basket = types.KeyboardButton(text=back_button[lang])
    keyboard.row(btn_savatcha)
    keyboard.row(btn_back_basket)
    return keyboard


def generate_basket(lang):
    keyboard = types.InlineKeyboardMarkup()
    btn_per2 = types.InlineKeyboardButton(text=back_button[lang], callback_data="back_btn")
    btn_per3 = types.InlineKeyboardButton(text=booking_meal[lang], callback_data="deliver_btn")
    btn_per4 = types.InlineKeyboardButton(text=clear_basket[lang], callback_data="clear_btn")
    btn_per5 = types.InlineKeyboardButton(text=time_delivery[lang], callback_data="time_btn")
    keyboard.row(btn_per2, btn_per3)
    keyboard.row(btn_per4, btn_per5)
    return keyboard


def back(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_back_basket = types.KeyboardButton(text=back_button[lang])
    keyboard.row(btn_back_basket)
    return keyboard


def deliver_phone(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reg_button = types.KeyboardButton(text="📞", request_contact=True)
    btn_back = types.KeyboardButton(text=back_to_main_menu[lang])
    keyboard.row(reg_button)
    keyboard.row(btn_back)
    return keyboard


def time_deliver_person():
    keyboard_time = types.InlineKeyboardMarkup()
    btn_btn1 = types.InlineKeyboardButton(text='09:00', callback_data="09:00")
    btn_btn2 = types.InlineKeyboardButton(text='09:30', callback_data="09:30")
    btn_btn3 = types.InlineKeyboardButton(text='10:00', callback_data="10:00")
    btn_btn4 = types.InlineKeyboardButton(text='10:30', callback_data="10:30")
    btn_btn5 = types.InlineKeyboardButton(text='11:00', callback_data="11:00")
    btn_btn6 = types.InlineKeyboardButton(text='11:30', callback_data="11:30")
    btn_btn7 = types.InlineKeyboardButton(text='12:00', callback_data="12:00")
    btn_btn8 = types.InlineKeyboardButton(text='12:30', callback_data="12:30")
    btn_btn9 = types.InlineKeyboardButton(text='13:00', callback_data="13:00")
    btn_btn10 = types.InlineKeyboardButton(text='13:30', callback_data="13:30")
    btn_btn11 = types.InlineKeyboardButton(text='14:00', callback_data="14:00")
    btn_btn12 = types.InlineKeyboardButton(text='14:30', callback_data="14:30")
    btn_btn13 = types.InlineKeyboardButton(text='15:00', callback_data="15:00")
    btn_btn14 = types.InlineKeyboardButton(text='15:30', callback_data="15:00")
    btn_btn15 = types.InlineKeyboardButton(text='16:00', callback_data="16:00")
    btn_btn16 = types.InlineKeyboardButton(text='16:30', callback_data="16:30")
    btn_btn17 = types.InlineKeyboardButton(text='17:00', callback_data="17:00")
    btn_btn18 = types.InlineKeyboardButton(text='17:30', callback_data="17:30")
    btn_btn19 = types.InlineKeyboardButton(text='18:00', callback_data="18:00")
    btn_btn20 = types.InlineKeyboardButton(text='18:30', callback_data="18:30")
    btn_btn21 = types.InlineKeyboardButton(text='19:00', callback_data="19:00")
    btn_btn22 = types.InlineKeyboardButton(text='19:30', callback_data="19:30")
    btn_btn23 = types.InlineKeyboardButton(text='20:00', callback_data="20:00")
    btn_btn24 = types.InlineKeyboardButton(text='20:30', callback_data="20:30")
    btn_btn25 = types.InlineKeyboardButton(text='21:00', callback_data="21:00")
    btn_btn26 = types.InlineKeyboardButton(text='21:30', callback_data="21:30")
    btn_btn27 = types.InlineKeyboardButton(text='22:00', callback_data="22:00")
    keyboard_time.row(btn_btn1, btn_btn2, btn_btn3)
    keyboard_time.row(btn_btn4, btn_btn5, btn_btn6)
    keyboard_time.row(btn_btn7, btn_btn8, btn_btn9)
    keyboard_time.row(btn_btn10, btn_btn11, btn_btn12)
    keyboard_time.row(btn_btn13, btn_btn14, btn_btn15)
    keyboard_time.row(btn_btn16, btn_btn17, btn_btn18)
    keyboard_time.row(btn_btn19, btn_btn20, btn_btn21)
    keyboard_time.row(btn_btn22, btn_btn23, btn_btn24)
    keyboard_time.row(btn_btn25, btn_btn26, btn_btn27)
    return keyboard_time


def select_payment(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    money = types.KeyboardButton(text=cash_payment[lang])
    click = types.KeyboardButton(text="Click")
    payme = types.KeyboardButton(text="Payme")
    btn_back = types.KeyboardButton(text=back_button[lang])
    keyboard.row(money)
    keyboard.row(click)
    keyboard.row(payme)
    keyboard.row(btn_back)
    return keyboard


def commit_pay(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes_pay = types.KeyboardButton(text=conformation[lang])
    no_pay = types.KeyboardButton(text=cancel[lang])
    keyboard.row(yes_pay)
    keyboard.row(no_pay)
    return keyboard

def back_name(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_n = types.KeyboardButton(text=back_button_name[lang])
    keyboard.row(back_n)
    return keyboard

def generate_inline_button_product_sign(product_list, lang):
    keyboards = types.InlineKeyboardMarkup(row_width=2)
    for i in range(0, len(product_list["body"]), 1):
        keyboards.add(types.InlineKeyboardButton(
            text=f"{product_list['body'][i]['special_sign'][lang]} - {product_list['body'][i]['price']}",
            callback_data=product_list["body"][i]["product_name"][lang] + ' ' + product_list["body"][i]["special_sign"][lang]))
    return keyboards


def coords_to_geo_data(list, lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if len(list) % 2 == 0:
        for i in range(0, len(list), 2):
            geolocator = geopy.Nominatim(user_agent="GetLoc")
            latitude = list[i + 1]
            longitude = list[i]
            coordinates = geolocator.reverse(f"{latitude}, {longitude}")
            address = coordinates.raw["address"]
            loc_address = [*address.values()]
            house_number = loc_address[0]
            road = loc_address[1]
            neighbourhood = loc_address[2]
            county = loc_address[3]
            city = loc_address[4]
            keyboard.add(types.KeyboardButton(text=f"{house_number}, {road}, {neighbourhood}, {county}, {city}"))
    return keyboard


def generate_catalogs_basket(catalog_list, lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_basket = types.KeyboardButton(text=basket_button[lang])
    keyboard.row(btn_basket)
    for i in range(0, len(catalog_list["body"]), 2):
        if len(catalog_list["body"]) % 2 == 1 and i == len(catalog_list["body"]) - 1:
            keyboard.add(types.KeyboardButton(text=catalog_list["body"][i]["category_name"][lang]))
        else:
            keyboard.add(types.KeyboardButton(text=catalog_list["body"][i]["category_name"][lang]),
                         types.KeyboardButton(text=catalog_list["body"][i + 1]["category_name"][lang]))
    btn_back = types.KeyboardButton(text=back_button[lang])
    keyboard.row(btn_back)
    return keyboard
