import os
from telebot import TeleBot
import datetime
from telebot.types import LabeledPrice
import re
import time
from excel import read_excel_file, create_excel_template_file
import geopy
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import generate_contact, sending_resume, deliver_contact, back_name, generate_catalogs_basket, generate_basket, generate_contact_phone, \
    get_geolocation, bron_contact, generate_main_menu, to_basket, generate_net, generate_link_tg, generate_link_inst, \
    generate_bron_person, generate_grade,\
    generate_setting, change_lang, generate_bron, \
    generate_bron_times, generate_bron_times_today, user_info, generate_subcatalogs, generate_catalogs, back, deliver_phone, \
    time_deliver_person, select_payment, commit_location, generate_inline_button_product_sign, bastket_keyboard, coords_to_geo_data
import repository.repository as repo
import config.config as c
from localization.bot_lang import basket_report,work_time_off, deliver_go, success_delivery,change_meal, added_text, you_are_not_admin, \
    error_text, send_resume, manual_bot, error_excel_catalog_row_text, error_excel_subcatalog_row_text, \
    error_excel_product_row_text, error_excel_warning_text, welcome_text, send_me_contact_bot, \
    incorrect_format, send_contact_mandatory, location_contact_text, rate_server, work_time, our_network, \
    enter_settings, \
    select_book_table_time, select_book_table_date, how_many_people_do_you_book, who_is_booking_enter_name, \
    send_your_phone, \
    booking_table_data, done_booking, delivery_warning_text, \
    clear_basket_text, enter_delivery_time, delivery_report, accepted_text, select_payment_type, order_report_text, \
    check_user_location, error_geolocation_format, send_your_location, product_caption_text, error_payment, \
    success_payment, \
    select_item_from_menu, empty_your_locations, select_your_location, \
    empty_basket_text, rate_meal_quality, comments_your_oponion, thanks_your_comment, \
    accepted_your_idea, \
    booking_table_data_for_canal, welcome_to_admin, success_update_excel_file, basket_report_group, select_options
from localization.keyboard_lang import rate_me, social_media,back_button_name, back_to_main_menu, yes_word, no_word, \
    cash_payment, back_button, manual, resume, go_delivery, phone_delivery,\
    my_locations, save_to_basket, basket_button, change_language_text, idea_report_text, settings_text, menu_text, \
    book_table, \
    location_contact
import log.logrus as logrus


log = logrus.init_logrus()
cfg = c.BotConfig(".env")
repo = repo.Repository(cfg, log, migration_state=True)
mig_result = repo.migration.migration()
if mig_result:
    log.info("MIGRATION SUCCESSFUL")
else:
    log.error("MIGRATION FAILED")

bot = TeleBot(cfg.token)

click_token = cfg.click_token
payme_token = cfg.payme_token
default_photo = cfg.default_photo
deliver_price = 10000
numbers = {}
user_baskets = {}
user_locations = {}
order_num = {}
user_langs = {}
total_price = {}
user_selected_product = {}
order_delivery_time = {}
user_bookings = {}
user_feedbacks = {}
idea_channel_id = cfg.idea_canal_id
bron_channel_id = cfg.bron_canal_id
order_channel_id = cfg.order_canal_id
user_transaction = {}
user_restart_status = {}
main_video = cfg.default_video


@bot.message_handler(commands=["admin"])
def admin_panel(message):
    user_id = message.chat.id
    lang = message.from_user.language_code
    lang = user_langs.get(user_id, lang)
    user_langs[user_id] = lang
    user = repo.user.get_one(user_id)
    if not user['success']:
        start(message)
    elif user['success']:
        lang = user['body']['set_language']
        user_langs[user_id] = lang
    if str(user_id) in cfg.admin_tg_id:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_change_menu = types.KeyboardButton(text=change_meal[lang])
        keyboard.row(btn_change_menu)
        bot.send_message(user_id, text=welcome_to_admin[lang], reply_markup=keyboard)
        bot.register_next_step_handler(message, admin_panel_menu, keyboard)
    elif str(user_id) not in cfg.admin_tg_id:
        bot.send_message(user_id, you_are_not_admin[lang])
        bot.send_message(user_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)


def admin_panel_menu(message, keyboard):
    chat_id = message.chat.id
    lang = "uz"
    lang = user_langs.get(chat_id, lang)
    if message.text == change_meal[lang]:
        back_to_admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_change_menu = types.KeyboardButton(text=back_button[lang])
        back_to_admin.row(btn_change_menu)
        bot.send_message(chat_id, change_meal[lang], reply_markup=back_to_admin)
        create_excel_template_file(repo)
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H-%M-%S")
        os.rename('get_db.xlsx', f'{formatted_time}.xlsx')
        bot.send_document(chat_id, open(f"{formatted_time}.xlsx", "rb"))
        os.remove(f"{formatted_time}.xlsx")
        bot.register_next_step_handler(message, change_exel, keyboard)
        print(114)

    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)




def change_exel(message, keyboard):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    print(131)
    if message.document:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open('file.xlsx', 'wb') as f:
            f.write(downloaded_file)
        error_data = read_excel_file(repo, log, open("file.xlsx", "rb"))
        if bool(error_data):
            print(138)
            bot.send_message(chat_id, error_text[lang])
            if isinstance(error_data['catalog_error_data_list'], list):
                if len(error_data['catalog_error_data_list']) != 0:
                    error_list = ','.join(str(x) for x in error_data['catalog_error_data_list'])
                    bot.send_message(chat_id,
                                     error_excel_catalog_row_text(error_list, lang))
            if isinstance(error_data['subcatalog_error_data_list'], list):
                if len(error_data['subcatalog_error_data_list']) != 0:
                    error_list = ','.join(str(x) for x in error_data['subcatalog_error_data_list'])
                    bot.send_message(chat_id, error_excel_subcatalog_row_text(error_list, lang))
            if isinstance(error_data['product_error_data_list'], list):
                if len(error_data['product_error_data_list']) != 0:
                    error_list = ','.join(str(x) for x in error_data['product_error_data_list'])
                    bot.send_message(chat_id,
                                     error_excel_product_row_text(error_list, lang))
            if isinstance(error_data['catalog_error_data_list'], dict) or isinstance(
                    error_data['product_error_data_list'], dict) or isinstance(
                error_data['subcatalog_error_data_list'], dict):
                if 'error' in error_data['subcatalog_error_data_list'] or 'error' in error_data[
                    'product_error_data_list'] or 'error' in error_data['catalog_error_data_list']:
                    bot.send_message(chat_id, error_excel_warning_text[lang])

        else:
            bot.send_message(chat_id, success_update_excel_file[lang])
            bot.send_message(chat_id, text=welcome_to_admin[lang], reply_markup=keyboard)
            bot.register_next_step_handler(message, admin_panel, keyboard)

    if message.text == back_button[lang]:
        bot.send_message(chat_id, text=welcome_to_admin[lang], reply_markup=keyboard)
        bot.register_next_step_handler(message, admin_panel_menu, keyboard)

    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)




@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.chat.id
    user_restart_status[user_id] = True
    lang = user_langs.get(user_id, "uz")
    lang = user_langs.get(user_id, lang)
    user_langs[user_id] = lang
    user = repo.user.get_one(user_id)
    photo=open( "files/main photo.jpg",'rb' )
    bot.send_photo( message.chat.id,photo,caption = welcome_text[lang],reply_markup = generate_main_menu( lang ) )
    if user['success']:
        lang = user['body']['set_language']
        user_langs[user_id] = lang
        if len(user['body']['phone']) == 0:
            bot.send_message(user_id, send_me_contact_bot[lang],
                             reply_markup=generate_contact(lang))
            bot.register_next_step_handler(message, menu)
        if len(user['body']['phone']) > 0:
            bot.send_message(user_id, select_options[lang], reply_markup=generate_main_menu(lang))
            bot.register_next_step_handler(message, to_menu)
    elif not user['success']:
        bot.send_message(user_id, send_me_contact_bot[lang],
                         reply_markup=generate_contact(lang))
        bot.register_next_step_handler(message, menu)


def contact(message):
    chat_id = message.chat.id
    user_restart_status[chat_id] = True
    lang = user_langs.get(chat_id, "uz")
    bot.send_message(chat_id, send_me_contact_bot[lang],
                     reply_markup=generate_contact(lang))
    bot.register_next_step_handler(message, menu)


def menu(message):
    chat_id = message.chat.id
    user_contact = message.contact
    user_restart_status[chat_id] = True
    user = repo.user.get_one(chat_id)
    lang = user_langs.get(chat_id, "uz")
    if not user['success']:
        if user_contact:
            if user_contact.first_name == None:
                user_contact.first_name = ""
            if user_contact.last_name == None:
                user_contact.last_name = ""
            user_data = dict(full_name=f'{user_contact.first_name} {user_contact.last_name}',
                             phone=user_contact.phone_number, chat_id=chat_id, lang=lang)
            repo.user.create(user_data)
            bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
            bot.register_next_step_handler(message, to_menu)
        else:
            bot.send_message(chat_id, incorrect_format[lang])
            bot.send_message(chat_id, send_contact_mandatory[lang],
                             reply_markup=generate_contact(lang))
            bot.register_next_step_handler(message, menu)
    else:
        bot.send_message(chat_id, send_contact_mandatory[lang],
                         reply_markup=generate_contact(lang))
        bot.register_next_step_handler(message, menu)

    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/admin":
        return admin_panel(message)


def to_menu(message):
    lang = user_langs.get(message.chat.id, "uz")
    chat_id = message.chat.id
    user_restart_status[chat_id] = True
    if message.text == social_media[lang]:
        social = bot.send_message(chat_id, our_network[lang], reply_markup=generate_net(lang))
        bot.register_next_step_handler(social, to_social)
    elif message.text == location_contact[lang]:
        keyboard = types.InlineKeyboardMarkup()
        btn_google = types.InlineKeyboardButton(text="Google Kart",
                                                url="https://www.google.com/maps/place/Dilkash/@40.8604685,69.5879287,15z/data=!4m2!3m1!1s0x0:0x154125d6439a644e?sa=X&ved=2ahUKEwiui8nnvI3_AhU_rIQIHX21ADIQ_BJ6BAg7EAg")
        btn_yandex = types.InlineKeyboardButton(text="Yandex Kart",
                                                url="https://yandex.uz/maps/10328/almalik/house/YkAYcw9mTk0GQFpqfXR3cXljZQ==/?ll=69.586642%2C40.860434&rtext=40.844396%2C69.606388~40.845884%2C69.607101&rtt=auto&ruri=~ymapsbm1%3A%2F%2Forg%3Foid%3D140801717212&utm_source=main_stripe_big&z=17.8")
        keyboard.row(btn_google, btn_yandex)
        bot.send_photo(chat_id, open("files/img.png", "rb"),
                       caption=location_contact_text[lang])
        bot.send_location(chat_id, latitude=40.86091, longitude=69.58965, reply_markup=keyboard)
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    elif message.text == rate_me[lang]:
        grades = bot.send_message(chat_id, rate_server[lang],
                                  reply_markup=generate_grade())
        bot.register_next_step_handler(grades, grade)

    elif message.text == settings_text[lang]:
        setting = bot.send_message(chat_id, enter_settings[lang], reply_markup=generate_setting(lang))
        bot.register_next_step_handler(setting, settings)

    elif message.text == book_table[lang]:
        current_time = datetime.datetime.now().time()
        if current_time > datetime.time(8, 0) and current_time < datetime.time(22, 0):
            bot.send_message(chat_id, work_time[lang], reply_markup=back(lang))
            bot.send_message(chat_id, select_book_table_date[lang], reply_markup=generate_bron())
            bot.register_next_step_handler(message, back_page)

        else:
            bot.send_message(chat_id, work_time_off[lang], reply_markup=generate_main_menu(lang))
            bot.register_next_step_handler(message, to_menu)

    elif message.text == menu_text[lang]:
        user_geo = bot.send_message(chat_id, select_options[lang], reply_markup=get_geolocation(lang))
        bot.register_next_step_handler(user_geo, select_geo)

    elif message.text == resume[lang]:
        bot.send_message(chat_id, send_resume[lang], reply_markup=sending_resume(lang, url="https://t.me/dilkash_olmaliq_bot"))
        menus = bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(menus, to_menu)

    elif message.text == manual[lang]:
        video = open(main_video, 'rb')
        bot.send_video(chat_id, video, caption=manual_bot[lang], reply_markup=generate_main_menu(lang))
        video.close()
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)


    if message.text == "/admin":
        return admin_panel(message)

# Stol bron-------------------------------------------------------
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


@bot.callback_query_handler(func=lambda call: call.data == formatted_today)
@bot.callback_query_handler(func=lambda call: call.data == tomorrow_formatted)
@bot.callback_query_handler(func=lambda call: call.data == after_tomorrow_formatted)
@bot.callback_query_handler(func=lambda call: call.data == after_tomorrow_formatted_2)
@bot.callback_query_handler(func=lambda call: call.data == after_tomorrow_formatted_3)
@bot.callback_query_handler(func=lambda call: call.data == after_tomorrow_formatted_4)
@bot.callback_query_handler(func=lambda call: call.data == after_tomorrow_formatted_5)
def get_callback_data(call):
    lang = user_langs.get(call.message.chat.id, "uz")
    chat_id = call.message.chat.id
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(call.message, to_menu)
        return

    if call.data == formatted_today:
        bot.send_message(chat_id, select_book_table_time[lang], reply_markup=generate_bron_times_today())
        user_bookings[chat_id] = dict(date=call.data)
        bot.register_next_step_handler(call.message, to_menu)

    elif call.data == tomorrow_formatted or call.data == after_tomorrow_formatted or call.data == after_tomorrow_formatted_2 or call.data == after_tomorrow_formatted_3 or call.data == after_tomorrow_formatted_4 or call.data == after_tomorrow_formatted_5:
        bot.send_message(chat_id, select_book_table_time[lang], reply_markup=generate_bron_times())
        user_bookings[chat_id] = dict(date=call.data)
        bot.register_next_step_handler(call.message, to_menu)

    get_callback_names(call)


@bot.callback_query_handler(func=lambda call: call.data == "09:00-10:30")
@bot.callback_query_handler(func=lambda call: call.data == "11:00-12:30")
@bot.callback_query_handler(func=lambda call: call.data == "13:00-14:30")
@bot.callback_query_handler(func=lambda call: call.data == "15:00-16:30")
@bot.callback_query_handler(func=lambda call: call.data == "17:00-18:30")
@bot.callback_query_handler(func=lambda call: call.data == "19:00-20:30")
@bot.callback_query_handler(func=lambda call: call.data == "21:00-22:00")
def get_callback_names(call):
    lang = user_langs.get(call.message.chat.id, "uz")
    chat_id = call.message.chat.id
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(call.message, to_menu)
        return
    bot.delete_message(chat_id, call.message.id)
    if call.data == "09:00-10:30" or call.data == "11:00-12:30" or call.data == "13:00-14:30" or call.data == "15:00-16:30" or call.data == "17:00-18:30" or call.data == "19:00-20:30" or call.data == "21:00-22:00":
        bot.send_message(chat_id, how_many_people_do_you_book[lang], reply_markup=generate_bron_person())
        user_booking = user_bookings.get(chat_id, dict())
        if bool(user_booking):
            user_bookings[chat_id] = dict(time=call.data, date=user_booking['date'])
    get_callback_person(call)


@bot.callback_query_handler(func=lambda call: call.data == "2")
@bot.callback_query_handler(func=lambda call: call.data == "3")
@bot.callback_query_handler(func=lambda call: call.data == "4")
@bot.callback_query_handler(func=lambda call: call.data == "5")
@bot.callback_query_handler(func=lambda call: call.data == "6")
@bot.callback_query_handler(func=lambda call: call.data == "7")
@bot.callback_query_handler(func=lambda call: call.data == "8")
@bot.callback_query_handler(func=lambda call: call.data == "9")
@bot.callback_query_handler(func=lambda call: call.data == "10")
@bot.callback_query_handler(func=lambda call: call.data == "11")
@bot.callback_query_handler(func=lambda call: call.data == "12")
@bot.callback_query_handler(func=lambda call: call.data == "13")
@bot.callback_query_handler(func=lambda call: call.data == "14")
@bot.callback_query_handler(func=lambda call: call.data == "15")
@bot.callback_query_handler(func=lambda call: call.data == "16")
def get_callback_person(call):
    lang = user_langs.get(call.message.chat.id, "uz")
    chat_id = call.message.chat.id
    user_status = user_restart_status.get(chat_id, False)

    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(call.message, to_menu)
    elif call.data in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"]:
        bot.send_message(chat_id, who_is_booking_enter_name[lang], reply_markup=back_name(lang))
        user_booking = user_bookings.get(chat_id, dict())
        if bool(user_booking):
            user_bookings[chat_id] = dict(time=user_booking['time'], date=user_booking['date'],
                                          person_number=call.data)
        bot.register_next_step_handler(call.message, phone_num)


@bot.message_handler(func=lambda call: True)
def phone_num(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    name = message.text
    user_status = user_restart_status.get(chat_id, False)

    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
    else:
        if name:
            bot.send_message(chat_id, send_your_phone[lang], reply_markup=bron_contact(lang))
            bot.register_next_step_handler(message, bron_user_contact, name)
        elif message.text == back_button_name[lang]:
            bot.send_message(chat_id, "", reply_markup=generate_main_menu(lang))
            bot.register_next_step_handler(message, to_menu)

    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/admin":
        return admin_panel(message)


def bron_user_contact(message, name):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
        return
    if message.contact:
        user_contact = message.contact.phone_number
        user_booking = user_bookings.get(chat_id, dict())
        if bool(user_booking):
            user_bookings[chat_id] = dict(time=user_booking['time'], date=user_booking['date'],
                                          person_number=user_booking['person_number'], contact=user_contact,
                                          name=name)
            if bool(user_contact) and bool(name) and bool(user_booking['date']) and bool(
                    user_booking['time']) and bool(
                user_booking['person_number']):
                bot.send_message(chat_id, booking_table_data(
                    dict(date=user_booking['date'], time=user_booking['time'],
                         people_number=user_booking['person_number'], name=name,
                         phone=user_contact), lang)
                                 , reply_markup=user_info(lang))
                bot.register_next_step_handler(message, selection, name, user_contact)

    else:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/admin":
        return admin_panel(message)


@bot.message_handler(func=lambda call: True)
def selection(message, name, user_contact):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    user_name = message.from_user.username
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
        return
    if message.text == yes_word[lang]:
        bot.send_message(chat_id, done_booking[lang])
        user_booking = user_bookings.get(chat_id, dict())
        if bool(user_booking):
            user_bookings[chat_id] = dict(time=user_booking['time'], date=user_booking['date'],
                                          person_number=user_booking['person_number'],
                                          contact=user_booking['contact'],
                                          name=user_booking['name'], username=user_name)
            bot.send_message(bron_channel_id, booking_table_data_for_canal(
                dict(date=user_booking['date'], time=user_booking['time'],
                     people_number=user_booking['person_number'],
                     name=name,
                     username=user_name, phone=user_contact), lang))
            menus = bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
            user_data = repo.user.get_one(chat_id)
            if user_data['success']:
                repo.booking.create(
                    dict(user_id=user_data['body']['id'], booking_date=user_booking['date'],
                         booking_time=user_booking['time'],
                         person_count=user_booking['person_number'], user_name=name, nick_name=user_name,
                         phone=user_contact))
            bot.register_next_step_handler(menus, to_menu)
            del user_bookings[chat_id]

    elif message.text == no_word[lang]:
        menus = bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(menus, to_menu)

    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/admin":
        return admin_panel(message)


@bot.callback_query_handler(func=lambda call: call.data == "back_btn")
@bot.callback_query_handler(func=lambda call: call.data == "deliver_btn")
@bot.callback_query_handler(func=lambda call: call.data == "clear_btn")
@bot.callback_query_handler(func=lambda call: call.data == "time_btn")
def call_back_deliver(call):
    chat_id = call.message.chat.id
    lang = user_langs.get(chat_id, "uz")
    catalog_list = repo.category.get_list(0, 1000, lang)
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(call.message, to_menu)
        return
    prices = 0
    response = "Savatda : "
    user_basket = user_baskets.get(chat_id, dict())
    if bool(user_basket):
        for product in user_basket['products']:
            name = product["product_name"]
            price = product["product_amount"]
            quantity_num = product["product_count"]
            prices += price * quantity_num
            response += f"\n{quantity_num} ✖️ {name}"
    if call.data == "back_btn":
        bot.send_message(chat_id, select_options[lang],
                         reply_markup=generate_catalogs(catalog_list, lang))
    elif call.data == "deliver_btn":
        bot.send_message(chat_id, delivery_warning_text[lang]
                         ,
                         reply_markup=deliver_phone(lang))
        bot.register_next_step_handler(call.message, deliver_pay)
    elif call.data == "clear_btn":
        del user_baskets[chat_id]
        bot.delete_message(chat_id, call.message.id + 1)
        bot.delete_message(chat_id, call.message.id)
        bot.send_message(chat_id, clear_basket_text[lang], reply_markup=generate_catalogs(catalog_list, lang))
        bot.register_next_step_handler(call.message, speacial_catalog_menu)
    elif call.data == "time_btn":
        bot.delete_message(chat_id, call.message.id + 1)
        bot.delete_message(chat_id, call.message.id)
        bot.send_message(chat_id, enter_delivery_time[lang])
        bot.send_message(chat_id,
                         delivery_report(
                             dict(response=response, price=prices, deliver=deliver_price,
                                  total_price=prices + deliver_price),
                             lang),
                         reply_markup=time_deliver_person())
        time_deliver(call)


@bot.callback_query_handler(func=lambda call: call.data == "09:00")
@bot.callback_query_handler(func=lambda call: call.data == "09:30")
@bot.callback_query_handler(func=lambda call: call.data == "10:00")
@bot.callback_query_handler(func=lambda call: call.data == "10:30")
@bot.callback_query_handler(func=lambda call: call.data == "11:00")
@bot.callback_query_handler(func=lambda call: call.data == "11:30")
@bot.callback_query_handler(func=lambda call: call.data == "12:00")
@bot.callback_query_handler(func=lambda call: call.data == "12:30")
@bot.callback_query_handler(func=lambda call: call.data == "13:00")
@bot.callback_query_handler(func=lambda call: call.data == "13:30")
@bot.callback_query_handler(func=lambda call: call.data == "14:00")
@bot.callback_query_handler(func=lambda call: call.data == "14:30")
@bot.callback_query_handler(func=lambda call: call.data == "15:00")
@bot.callback_query_handler(func=lambda call: call.data == "15:30")
@bot.callback_query_handler(func=lambda call: call.data == "16:00")
@bot.callback_query_handler(func=lambda call: call.data == "16:30")
@bot.callback_query_handler(func=lambda call: call.data == "17:00")
@bot.callback_query_handler(func=lambda call: call.data == "17:30")
@bot.callback_query_handler(func=lambda call: call.data == "18:00")
@bot.callback_query_handler(func=lambda call: call.data == "18:30")
@bot.callback_query_handler(func=lambda call: call.data == "19:00")
@bot.callback_query_handler(func=lambda call: call.data == "19:30")
@bot.callback_query_handler(func=lambda call: call.data == "20:00")
@bot.callback_query_handler(func=lambda call: call.data == "20:30")
@bot.callback_query_handler(func=lambda call: call.data == "21:00")
@bot.callback_query_handler(func=lambda call: call.data == "21:30")
@bot.callback_query_handler(func=lambda call: call.data == "22:00")
def time_deliver(call):
    chat_id = call.message.chat.id
    lang = user_langs.get(chat_id, "uz")
    prices = 0
    response = "Savatda : "
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(call.message, to_menu)
        return

    user_basket = user_baskets.get(chat_id, dict())
    if bool(user_basket):
        for product in user_basket['products']:
            name = product["product_name"]
            price = product["product_amount"]
            quantity_num = product["product_count"]
            prices += price * quantity_num
            response += f"\n{quantity_num} ✖️ {name}"
    if call.data == "09:00" or call.data == "09:30" or call.data == "10:00" or \
            call.data == "10:30" or call.data == "11:00" or call.data == "11:30" or call.data == "12:00" or call.data == "12:30" or call.data == "13:00" or call.data == "13:30" or call.data == "14:00" or call.data == "14:30" or \
            call.data == "15:00" or call.data == "15:30" or call.data == "16:00" or call.data == "16:30" or call.data == "17:00" or call.data == "17:30" or call.data == "18:00" or call.data == "18:30" or call.data == "19:00" or call.data == "19:30" or call.data == "20:00" or call.data == "20:30" or call.data == "21:00" or call.data == "21:30" or call.data == "22:00":
        deleviry_time = order_delivery_time.get(chat_id, "00:00")

        if not bool(deleviry_time):
            order_delivery_time[chat_id] = call.data

        if bool(deleviry_time):
            order_delivery_time[chat_id] = call.data
        bot.delete_message(chat_id, call.message.id)
        bot.delete_message(chat_id, call.message.id - 1)
        bot.send_message(chat_id, accepted_text[lang])
        bot.send_message(chat_id,
                          delivery_report(
                              dict(response=response, price=prices, deliver=deliver_price,
                                    total_price=prices + deliver_price),
                              lang),
                          reply_markup=generate_basket(lang))


def deliver_pay(message):
    chat_id = message.chat.id
    product_name = ""
    product_price = 0
    user_basket = user_baskets.get(chat_id, dict())
    if bool(user_basket):
        for product in user_basket['products']:
            product_name += str(product["product_name"]) + ","
            product_price += product["product_amount"] * product["product_count"]
    user_location = user_locations.get(chat_id, dict())['data_text']
    lang = user_langs.get(chat_id, "uz")
    user_status = user_restart_status.get(chat_id, False)

    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
        return

    if message.contact:
        bot.send_message(chat_id, order_report_text(
            dict(location=user_location, price=product_price,
                 total_price=product_price + deliver_price,
                 deleviry_price=deliver_price, response=product_name), lang)
                         , reply_markup=select_payment(lang))
        bot.send_message(chat_id, select_payment_type[lang])
        bot.register_next_step_handler(message, list_payment)

    elif message.text == back_to_main_menu[lang]:
        return speacial_catalog_menu(message)

    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/admin":
        return admin_panel(message)


def list_payment(message):
    chat_id = message.chat.id
    payment_user = message.text
    product_name = ""
    product_price = 0
    lang = user_langs.get(chat_id, "uz")
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
        return
    user = repo.user.get_one(chat_id)
    user_basket = user_baskets.get(chat_id, dict())
    if bool(user_basket):
        for product in user_basket['products']:
            product_name += str(product["product_name"]) + ","
            product_price += product["product_amount"] * product["product_count"]
    if message.text == cash_payment[lang]:
        username = message.from_user.username
        user_id = message.from_user.id
        user_location = user_locations.get(chat_id, dict())
        print(user_location)
        prices = 0
        products = []
        response = ""
        if bool(user_basket):
            for item in user_basket['products']:
                products.append(item)
                product_name = item["product_name"]
                price = item["product_amount"]
                quantity_num = item["product_count"]
                prices += price * quantity_num
                response += f"\n{quantity_num} ✖️ {product_name}"
            if user_id in order_num:
                current_order_number = order_num[user_id]
            else:
                current_order_number = 1
            order_num[user_id] = current_order_number + 1
            bot.send_location(order_channel_id, latitude=user_location["lat"], longitude=user_location["long"])
            bot.send_message(order_channel_id, basket_report_group(
                dict(order_id=order_num[user_id], name=user['body']['full_name'], user_name=username,
                     phone=user['body']['phone'],
                     response=response, prices=prices, deliver=deliver_price,
                     total_price=prices + deliver_price,
                     payment=payment_user,
                     location=user_location['data_text'],
                     delivery_time=order_delivery_time.get(chat_id, "")),
                lang))
        del user_baskets[chat_id]
        order_time = order_delivery_time.get(chat_id, dict())
        if bool(order_time):
            del order_delivery_time[chat_id]
        bot.send_message(chat_id, success_delivery[lang])
        return speacial_catalog_menu(message)
    elif message.text == "Payme":
        bot.send_message(chat_id, "Payme", reply_markup=back(lang))
        INVOICE = {
            "title": product_name,
            "description": product_name,
            "invoice_payload": "bot-defined invoice payload",
            "provider_token": payme_token,
            "start_parameter": "pay",
            "currency": "UZS",
            "prices": [LabeledPrice(label=product_name, amount=(product_price + deliver_price) * 100)]
        }
        bot.send_invoice(chat_id, **INVOICE)
        bot.register_next_step_handler(message, handle_successful_payment, payment_user)

    elif message.text == "Click":
        bot.send_message(chat_id, "Click", reply_markup=back(lang))
        INVOICE = {
            "title": product_name,
            "description": product_name,
            "invoice_payload": "bot-defined invoice payload",
            "provider_token": click_token,
            "start_parameter": "pay",
            "currency": "UZS",
            "prices": [LabeledPrice(label=product_name, amount=(product_price + deliver_price) * 100)]
        }
        bot.send_invoice(chat_id, **INVOICE)
        bot.register_next_step_handler(message, handle_successful_payment, payment_user)

    elif message.text == back_button[lang]:
        return speacial_catalog_menu(message)

    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/admin":
        return admin_panel(message)


@bot.pre_checkout_query_handler(func=lambda query: True)
def invoice_checkout(query):
    bot.answer_pre_checkout_query(query.id, ok=True)


@bot.message_handler(content_types=["successful_payment"])
def handle_successful_payment(message, payment_user):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    if message.text == back_button[lang]:
        bot.send_message(chat_id, select_payment_type[lang], reply_markup=select_payment(lang))
        bot.register_next_step_handler(message, list_payment)

    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
        return

    if message.successful_payment:
        user_id = message.from_user.id
        bot.send_message(chat_id, success_delivery[lang])
        bot.send_message(message.chat.id, success_payment[lang])
        username = message.from_user.username
        user_location = user_locations.get(chat_id, dict())
        user = repo.user.get_one(chat_id)
        prices = 0
        products = []
        order_id = 1
        response = ""
        user_basket = user_baskets.get(chat_id, dict())
        if bool(user_basket):
            for item in user_basket['products']:
                products.append(item)
                product_name = item["product_name"]
                price = item["product_amount"]
                quantity_num = item["product_count"]
                prices += price * quantity_num
                response += f"\n{quantity_num} ✖️ {product_name}"
            if user_id in order_num:
                current_order_number = order_num[user_id]
            else:
                current_order_number = 1
            order_num[user_id] = current_order_number + 1
            bot.send_location(order_channel_id, latitude=user_location["lat"], longitude=user_location["long"])
            bot.send_message(order_channel_id, basket_report_group(
                dict(order_id=order_id, name=user['body']['full_name'], user_name=username,
                     phone=user['body']['phone'],
                     response=response, prices=prices, deliver=deliver_price,
                     total_price=prices + deliver_price,
                     payment=payment_user,
                     location=user_location['data_text'],
                     delivery_time=order_delivery_time.get(chat_id, "")),
                lang))
        del user_baskets[chat_id]
        order_time = order_delivery_time.get(chat_id, dict())
        if bool(order_time):
            del order_delivery_time[chat_id]
        return speacial_catalog_menu(message)

    elif not message.successful_payment and not message.text == back_button[lang]:
        bot.send_message(chat_id, error_payment[lang], reply_markup=select_payment(lang))
        bot.register_next_step_handler(message, list_payment)

    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/admin":
        return admin_panel(message)

# Geolokatsiya
def select_geo(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
        return
    user_location = message.location
    if user_location:
        if message.location.latitude and message.location.longitude:
            geolocator = geopy.Nominatim(user_agent="GetLoc")
            latitude = message.location.latitude
            longitude = message.location.longitude
            coordinates = geolocator.reverse(f"{latitude}, {longitude}")
            address = coordinates.raw["address"]
            loc_address = [*address.values()]
            house_number = loc_address[0]
            road = loc_address[1]
            neighbourhood = loc_address[2]
            county = loc_address[3]
            city = loc_address[4]
            bot.send_message(chat_id, check_user_location(
                dict(house_number=house_number, road=road, neighbourhood=neighbourhood, county=county,
                     city=city), lang)
                             ,
                             reply_markup=commit_location(lang))
            user_loc = user_locations.get(chat_id, dict())
            if not bool(user_loc):
                user_locations[chat_id] = dict(chat_id=chat_id, long=longitude, lat=latitude,
                                               data_text=f"{house_number},{road},{neighbourhood},{county},{city}")

            else:
                user_locations[chat_id] = dict(chat_id=chat_id, long=longitude, lat=latitude,
                                               data_text=f"{house_number},{road},{neighbourhood},{county},{city}")

            user_loc = user_locations.get(chat_id, dict())
            if bool(user_loc):
                bot.register_next_step_handler(message, catalog_menu)


            else:
                bot.send_message(chat_id, error_geolocation_format[lang])
                user_geo = bot.send_message(chat_id, send_your_location[lang], reply_markup=get_geolocation(lang))
                bot.register_next_step_handler(user_geo, select_geo)

    elif message.text == my_locations[lang]:
        user_data = repo.user.get_one(chat_id)
        if user_data['success']:

            if len(user_data['body']['locations']) == 0:
                bot.send_message(chat_id, empty_your_locations[lang])
                user_geo = bot.send_message(chat_id, send_your_location[lang], reply_markup=get_geolocation(lang))
                bot.register_next_step_handler(user_geo, select_geo)

            else:
                db_locations = re.sub('[{}()"]', "", user_data['body']['locations']).split(",")
                locations = [eval(i) for i in db_locations]
                bot.send_message(chat_id, select_your_location[lang],
                                 reply_markup=coords_to_geo_data(locations, lang))
                bot.register_next_step_handler(message, commit_loc)

    elif message.text == back_to_main_menu[lang]:
        menus = bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(menus, to_menu)

    else:
        bot.send_message( chat_id,error_text[lang] )
        bot.send_message( chat_id,select_options[lang],reply_markup = generate_main_menu( lang ) )
        bot.register_next_step_handler( message,to_menu )

    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/admin":
        return admin_panel(message)


def commit_loc(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
        return

    if len(message.text) >= 4:
        user_data = repo.user.get_one(chat_id)
        db_locations = re.sub('[{}()"]', "", user_data['body']['locations']).split(",")
        locations = [eval(i) for i in db_locations]
        user_locations_text = []
        if len(locations) % 2 == 0:
            for i in range(0, len(locations), 2):
                geolocator = geopy.Nominatim(user_agent="GetLoc")
                latitude = locations[i + 1]
                longitude = locations[i]
                coordinates = geolocator.reverse(f"{latitude}, {longitude}")
                address = coordinates.raw["address"]
                loc_address = [*address.values()]
                house_number = loc_address[0]
                road = loc_address[1]
                neighbourhood = loc_address[2]
                county = loc_address[3]
                city = loc_address[4]
                user_locations_text.append(dict(chat_id=chat_id, long=longitude, lat=latitude,
                                                  data_text=f"{house_number}, {road}, {neighbourhood}, {county}, {city}"))
            for i in user_locations_text:
                if message.text == i['data_text']:
                    user_locations[chat_id] = dict(long=i['long'], lat=i['lat'], data_text=message.text)
                    catalog_list = repo.category.get_list(0, 1000, lang)
                    bot.send_message(chat_id, select_item_from_menu[lang],
                                      reply_markup=generate_catalogs(catalog_list, lang))
                    bot.register_next_step_handler(message, subcatalog_menu)
                    break

        else:
            bot.send_message(chat_id, send_your_location[lang], reply_markup=get_geolocation(lang))
            bot.register_next_step_handler(message, select_geo)


    elif len(message.text) < 4:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)


def catalog_menu(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
        return

    if message.text == yes_word[lang]:
        user_data = repo.user.get_one(chat_id)
        if user_data['success']:
            if user_data['body']['locations'] is None:
                user_loc = user_locations.get(chat_id, dict())
                if bool(user_loc):
                    bot.register_next_step_handler(message, catalog_menu)
                    repo.user.update_location(dict(chat_id=chat_id, long=user_loc['long'], lat=user_loc['lat']))
            else:
                db_locations = re.sub('[{}()"]', "", user_data['body']['locations']).split(",")
                locations = [eval(i) for i in db_locations]
                location_datas = []
                if len(locations) % 2 == 0:
                    for i in range(0, len(locations), 2):
                        geolocator = geopy.Nominatim(user_agent="GetLoc")
                        latitude = locations[i + 1]
                        longitude = locations[i]
                        coordinates = geolocator.reverse(f"{latitude}, {longitude}")
                        address = coordinates.raw["address"]
                        loc_address = [*address.values()]
                        house_number = loc_address[0]
                        road = loc_address[1]
                        neighbourhood = loc_address[2]
                        county = loc_address[3]
                        city = loc_address[4]
                        location_datas.append(f"{house_number}, {road}, {neighbourhood}, {county}, {city}")
                user_loc = user_locations.get(chat_id, dict())
                if bool(user_loc):
                    coordinates = geolocator.reverse(f"{user_loc['lat']}, {user_loc['long']}")
                    address = coordinates.raw["address"]
                    loc_address = [*address.values()]
                    house_number = loc_address[0]
                    road = loc_address[1]
                    neighbourhood = loc_address[2]
                    county = loc_address[3]
                    city = loc_address[4]
                    text = f"{house_number}, {road}, {neighbourhood}, {county}, {city}"
                    if text not in location_datas:
                        repo.user.update_location(
                            dict(chat_id=chat_id, long=user_loc['long'], lat=user_loc['lat']))
            catalog_list = repo.category.get_list(0, 1000, lang)
            bot.send_message(chat_id, select_item_from_menu[lang],
                             reply_markup=generate_catalogs(catalog_list, lang))
            bot.register_next_step_handler(message, subcatalog_menu)

    elif message.text == no_word[lang]:
        del user_locations[chat_id]
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
        return

    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/admin":
        return admin_panel(message)


def speacial_catalog_menu(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    catalog_list = repo.category.get_list(0, 1000, lang)
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
        return
    bot.send_message(chat_id, select_options[lang],
                     reply_markup=generate_catalogs(catalog_list, lang))
    bot.register_next_step_handler(message, subcatalog_menu)

    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/admin":
        return admin_panel(message)

def subcatalog_menu(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
        return
    catalog_list = repo.category.get_list(0, 1000, lang)
    if catalog_list["success"]:
        for i in catalog_list["body"]:
            if message.text == i["category_name"][lang]:
                subcatalog_list = repo.subcategory.get_list_by_category(0, 1000, i["id"])
                photo = default_photo
                if len(i["photo"]) != 0:
                    photo = i["photo"]
                photo_paths = photo.split(',')
                print(photo_paths)
                media = [types.InputMediaPhoto(media=link) for link in photo_paths]
                bot.send_message(chat_id, select_options[lang], reply_markup=generate_subcatalogs(subcatalog_list, lang))
                bot.send_media_group(chat_id, media)
                bot.register_next_step_handler(message, product_menu)

    if message.text == go_delivery[lang]:
        foto = "https://cdn.itechacademy.uz/catalog/Tog'ora%20umumiy.png"
        bot.send_photo(chat_id, foto, caption=deliver_go[lang], reply_markup=deliver_contact(lang))
        bot.register_next_step_handler(message, product_menu)

    if message.text == back_to_main_menu[lang]:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/admin":
        return admin_panel(message)


def product_menu(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
        return
    catalog_list = repo.category.get_list(0, 1000, lang)
    subcatalog_list = repo.subcategory.get_list(0, 1000)
    if subcatalog_list["success"]:
        for i in subcatalog_list["body"]:
            if message.text == i['subcategory_name'][lang]:
                product_list = repo.product.get_list_by_subcategory(0, 1000, i["id"])
                if product_list['success']:
                    if len(product_list["body"]) == 0:
                        speacial_catalog_menu(message)
                        break
                    elif len(product_list["body"]) == 1:
                        user_selected_product[chat_id] = dict(product_id=product_list["body"][0]['id'],
                                                              product_name=product_list['body'][0]['product_name'][
                                                                  lang],
                                                              product_price=product_list['body'][0]['price'])
                        user_product = user_selected_product.get(chat_id, dict())
                        if bool(user_product):
                            photo = default_photo
                            if len(i["photo"]) != 0:
                                photo = i["photo"]
                            print(user_product)
                            bot.send_message(chat_id, select_options[lang],
                                             reply_markup=bastket_keyboard(lang))
                            bot.send_photo(chat_id, photo,
                                           caption=product_caption_text(dict(
                                               product_name=product_list['body'][0]['product_name'][lang],
                                               price=product_list['body'][0]['price'],
                                               product_igredents=product_list['body'][0]['ingredients'][lang]), lang),
                                           reply_markup=to_basket(lang))
                            bot.register_next_step_handler(message, basket_page)
                            break
                    elif len(product_list["body"]) > 1:
                        photo = default_photo
                        if len(i["photo"]) != 0:
                            photo = i["photo"]
                        bot.send_message(chat_id, select_options[lang],
                                         reply_markup=generate_catalogs(catalog_list, lang))
                        bot.send_photo(chat_id, photo,
                                       reply_markup=generate_inline_button_product_sign(product_list, lang))
                        bot.register_next_step_handler(message, catalog_menu)


    if message.text == phone_delivery[lang]:
        bot.send_photo(chat_id, open("files/img.png", "rb"),
                       caption=location_contact_text[lang])
        return speacial_catalog_menu(message)

    if message.text == back_button[lang]:
        return speacial_catalog_menu(message)

    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/admin":
        return admin_panel(message)


@bot.callback_query_handler(func=lambda call: True)
def products_counter(call):
    chat_id = call.message.chat.id
    lang = user_langs.get(chat_id, "uz")
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(call.message, to_menu)
        return

    product_list = repo.product.get_list(0, 1000)

    if product_list['success']:
        print(product_list["body"])
        for i in product_list["body"]:
            if call.data == i["product_name"][lang] + ' ' + i["special_sign"][lang]:
                user_selected_product[chat_id] = dict(product_id=i['id'],
                                                      product_name=i['product_name'][lang],
                                                      product_price=i['price'])
                user_product = user_selected_product.get(chat_id, dict())
                if bool(user_product):
                    print(user_product)
                    user_selected_product[chat_id] = dict(product_id=i['id'],
                                                          product_name=i['product_name'][lang],
                                                          product_price=i['price'])
                    bot.send_message(chat_id, select_options[lang], reply_markup=bastket_keyboard(lang))
                    photo = default_photo
                    if len(i["photo"]) != 0:
                        photo = i["photo"]
                    print(photo)
                    bot.send_photo(chat_id, photo,
                                   caption=product_caption_text(dict(
                                       product_name=i['product_name'][lang],
                                       price=i['price'],
                                       product_igredents=i['ingredients'][lang]), lang),
                                   reply_markup=to_basket(lang))
                    bot.register_next_step_handler(call.message, basket_page)
    basket_callback_data(call)


@bot.callback_query_handler(func=lambda call: call.data == 'basket_call')
@bot.callback_query_handler(func=lambda call: call.data == '+')
@bot.callback_query_handler(func=lambda call: call.data == '-')
@bot.callback_query_handler(func=lambda call: call.data == 'number')
def basket_callback_data(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    numbers[chat_id] = numbers.get(chat_id, 1)
    lang = user_langs.get(chat_id, "uz")
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(call.message, to_menu)
        return
    product_id = 0
    product_name = ""
    product_price = 0
    user_product = user_selected_product.get(chat_id, dict())
    if bool(user_product):
        product_id = user_product['product_id']
        product_name = user_product['product_name']
        product_price = user_product['product_price']
    if call.data == '+':
        numbers[chat_id] = numbers.get(chat_id, 1) + 1
        bot.answer_callback_query(call.id, text=f"+ 1 ta")
        keyboard_now = InlineKeyboardMarkup()
        btn__1 = InlineKeyboardButton(text='➖', callback_data="-")
        btn__2 = InlineKeyboardButton(f"{numbers.get(chat_id, 1)}", callback_data="number")
        btn__3 = InlineKeyboardButton(text='➕', callback_data="+")
        btn__4 = InlineKeyboardButton(text=save_to_basket[lang], callback_data="basket_call")
        keyboard_now.row(btn__1, btn__2, btn__3)
        keyboard_now.row(btn__4)
        bot.edit_message_reply_markup(chat_id, message_id, reply_markup=keyboard_now)
        return

    elif call.data == '-':
        numbers[chat_id] = max(numbers.get(chat_id, 1) - 1, 0)
        bot.answer_callback_query(call.id, text=f"- 1 ta")
        keyboard_now = InlineKeyboardMarkup()
        btn__1 = InlineKeyboardButton(text='➖', callback_data="-")
        btn__2 = InlineKeyboardButton(f"{numbers.get(chat_id, 1)}", callback_data="number")
        btn__3 = InlineKeyboardButton(text='➕', callback_data="+")
        btn__4 = InlineKeyboardButton(text=save_to_basket[lang], callback_data="basket_call")
        keyboard_now.row(btn__1, btn__2, btn__3)
        keyboard_now.row(btn__4)
        bot.edit_message_reply_markup(chat_id, message_id, reply_markup=keyboard_now)
        return

    elif call.data == "number":
        bot.answer_callback_query(call.id, text=f"{numbers.get(chat_id, 1)} ta")

    elif call.data == "basket_call":
        catalog_list = repo.category.get_list(0, 1000, lang)
        bot.send_message(chat_id, select_options[lang],
                         reply_markup=generate_catalogs_basket(catalog_list, lang))
        bot.register_next_step_handler(call.message, subcatalog_menu)
        bot.answer_callback_query(call.id, text=added_text[lang])
        quantity = numbers.get(chat_id, 1)
        product = dict(product_id=product_id, product_name=product_name, product_amount=product_price,
                       product_count=quantity)
        user_basket = user_baskets.get(chat_id, dict())
        if not bool(user_basket):
            user_baskets[chat_id] = dict(products=[product])
        elif bool(user_basket):
            exist = False
            for i in user_baskets[chat_id]['products']:
                if i['product_id'] == product['product_id']:
                    exist = True
            if exist:
                for i in user_baskets[chat_id]['products']:
                    if i['product_id'] == product['product_id']:
                        i.update(dict(product_id=product_id, product_name=product_name,
                                      product_amount=product_price,
                                      product_count=i['product_count'] + product['product_count']))
            else:
                user_baskets[chat_id]['products'].append(product)
        del numbers[chat_id]


def basket_page(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
        return
    if message.text == basket_button[lang]:
        user_basket = user_baskets.get(chat_id, dict())
        if not bool(user_basket):
            bot.reply_to(message, empty_basket_text[lang])
            bot.register_next_step_handler(message, basket_page)
            return
        response = ""
        prices = 0
        user_basket = user_baskets.get(chat_id, dict())
        for product in user_basket["products"]:
            name = product["product_name"]
            price = product["product_amount"]
            quantity_num = product["product_count"]
            prices += price * quantity_num
            response += f"\n{quantity_num} ✖️ {name}"
        bot.send_message(chat_id, basket_report(
            dict(response=response, prices=prices, deliver=deliver_price, total_price=prices + deliver_price),
            lang), reply_markup=generate_basket(lang))
        catalog_list = repo.category.get_list(0, 1000, lang)
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_catalogs(catalog_list, lang))
        bot.register_next_step_handler(message, subcatalog_menu)


    elif message.text == back_button[lang]:
        return speacial_catalog_menu(message)


    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/admin":
        return admin_panel(message)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def back_to_main_page(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    if message.text == back_button[lang]:
        menus = bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(menus, to_menu)


    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/admin":
        return admin_panel(message)


# Tarmoqlar
def to_social(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
        return
    if message.text == "Telegram":
        bot.send_photo(chat_id, open("files/img.png", "rb"),
                       reply_markup=generate_link_tg("https://t.me/+sR4CcuhA7KE3Yjgy"))
        bot.register_next_step_handler(message, to_social)
    elif message.text == "Instagram":
        bot.send_photo(chat_id, open("files/img.png", "rb"),
                       reply_markup=generate_link_inst(
                           "https://instagram.com/dilkash.restaurant?igshid=MzRlODBiNWFlZA=="))
        bot.register_next_step_handler(message, to_social)
    elif message.text == back_button[lang]:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/admin":
        return admin_panel(message)


# Baholash
def grade(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
        return
    if message.text == "⭐⭐⭐⭐⭐" or message.text == "⭐⭐⭐⭐" or message.text == "⭐⭐⭐" or message.text == "⭐⭐" or message.text == "⭐":
        servis_grade = bot.send_message(chat_id, rate_meal_quality[lang],
                                        reply_markup=generate_grade())
        user_feedbacks.get(chat_id, dict())
        user_feedbacks[chat_id] = dict(service_rate=message.text)
        bot.register_next_step_handler(servis_grade, gread_food)


    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
    if message.text == "/admin":
        return admin_panel(message)

def gread_food(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
        return
    if message.text == "⭐⭐⭐⭐⭐" or message.text == "⭐⭐⭐⭐" or message.text == "⭐⭐⭐" or message.text == "⭐⭐" or message.text == "⭐":
        bot.send_message(chat_id, comments_your_oponion[lang])
        user_feedback = user_feedbacks.get(chat_id, dict())
        user_feedbacks[chat_id] = dict(service_rate=user_feedback['service_rate'], food_rate=message.text)
        bot.register_next_step_handler(message, idea_user)

    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/admin":
        return admin_panel(message)


def idea_user(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
        return

    bot.send_message(chat_id, thanks_your_comment[lang]
                     ,
                     reply_markup=generate_contact_phone(lang))
    user_feedback = user_feedbacks.get(chat_id, dict())
    user_feedbacks[chat_id] = dict(service_rate=user_feedback['service_rate'], food_rate=user_feedback['food_rate'],
                                   user_idea=message.text)
    bot.register_next_step_handler(message, get_idea)


    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/admin":
        return admin_panel(message)

def get_idea(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
        return
    if message.contact:
        user_name = message.from_user.username
        phone_num = message.contact.phone_number
        user_feedback = user_feedbacks.get(chat_id, dict())
        if bool(user_feedback):
            bot.send_message(chat_id, accepted_your_idea[lang])
            bot.send_message(idea_channel_id, idea_report_text(
                dict(servis=user_feedback['service_rate'], food_rate=user_feedback['food_rate'],
                     user_idea=user_feedback['user_idea'],
                     user_name=user_name, phone_number=phone_num), lang))
            bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
            bot.register_next_step_handler(message, to_menu)
    elif message.text == back_to_main_menu[lang]:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/admin":
        return admin_panel(message)


# Sozlamalar
def settings(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
        return
    if message.text == change_language_text[lang]:
        settin = bot.send_message(chat_id, change_language_text[lang], reply_markup=change_lang(lang))
        bot.register_next_step_handler(settin, change_language)
    elif message.text == back_button[lang]:
        menus = bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(menus, to_menu)

    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/admin":
        return admin_panel(message)


def change_language(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
        return
    if message.text == "🇺🇿O'zbekcha":
        lang = "uz"
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
    elif message.text == "🇷🇺Русский":
        lang = "ru"
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    elif message.text == "🇬🇧English":
        lang = "en"
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
    user_langs[chat_id] = lang
    repo.user.update_languge(dict(chat_id=chat_id, lang=lang))
    if message.text == back_button[lang]:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)


    if message.text == "/admin":
        return admin_panel(message)


def back_page(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
        return

    if message.text == back_button_name[lang] and not message.text == "/start" and not message.text == "/admin":
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/admin":
        return admin_panel(message)


def back_pay(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    user_status = user_restart_status.get(chat_id, False)
    if not user_status:
        bot.send_message(chat_id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)
        return
    if message.text == back_button[lang]:
        bot.send_message(chat_id, select_payment_type[lang], reply_markup=select_payment(lang))
        bot.register_next_step_handler(message, list_payment)

    if message.text == "/start":
        photo = open("files/main photo.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, caption=welcome_text[lang])
        bot.send_message(message.chat.id, select_options[lang], reply_markup=generate_main_menu(lang))
        bot.register_next_step_handler(message, to_menu)

    if message.text == "/admin":
        return admin_panel(message)


try:
    log.info("BOT RUN!")
    bot.polling()
except Exception as exp:
    log.info(f'BOT ERROR {exp.__class__.__name__}: {exp}')
    bot.stop_polling()
    time.sleep(5)



