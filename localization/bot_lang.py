import datetime
change_meal=dict( uz = "Taomlarni o'zgartirish!",ru = "Изменить блюда!",en = "Change meals!" )
comments_users=dict( uz = "Obunachilarning fikr-mulohazalari!",ru = "Комментарии подписчиков!",
                     en = "Comments of subscribers!" )
booking_list=dict( uz = "Buyurtmalar ro'yxati!",ru = "Список заказов!",en = "List of orders!" )
booking_order=dict( uz = "Buyurtma qilingan Stollar ro'yhati!",ru = "Список заказов!",en = "List of orders!" )
select_options=dict( uz = "Quyidagilardan birini tanlang!",ru = "Выберите один из следующих!",
                     en = "Select one of the following!" )
you_are_not_admin=dict( uz = "Siz admin emassiz!",ru = "Вы не админ!",en = "You are not admin!" )

welcome_to_admin=dict( uz = "Admin Panelga xush kelibsiz!",ru = "Добро пожаловать в панель администратора!",
                       en = "Welcome to the admin panel!" )
error_text=dict( uz = "Xatolik yuz berdi!",ru = "Произошла ошибка!",en = "An error occurred!" )
success_delivery=dict( uz = "Buyurtmangiz qabul qilindi!",ru = "Ваш заказ принят!",en = "Your order has been accepted!" )

def error_excel_catalog_row_text (error_data,lang):
    lang_dict=dict(
        uz = f"sizni kiritgan excel filegi Katalog Sheet nomidagi shu  {error_data} qatorlarda  xatoliklar bor",
        ru = f"в вашем введенном файле excel есть ошибки в строках {error_data} в листе SubKatalog",
        en = f"your entered excel file has errors in rows {error_data} in the SubKatalog sheet" )
    return lang_dict[lang]

def error_excel_subcatalog_row_text (error_data,lang):
    lang_dict=dict(
        uz = f"sizni kiritgan excel filegi SubKatalog Sheet nomidagi shu  {error_data} qatorlarda  xatoliklar bor",
        ru = f"в вашем введенном файле excel есть ошибки в строках {error_data} в листе SubKatalog",
        en = f"your entered excel file has errors in rows {error_data} in the SubKatalog sheet" )
    return lang_dict[lang]


def error_excel_product_row_text (error_data,lang):
    lang_dict=dict(
        uz = f"sizni kiritgan excel filegi Product Sheet nomidagi shu  {error_data} qatorlarda  xatoliklar bor",
        ru = f"в вашем введенном файле excel есть ошибки в строках {error_data} в листе SubKatalog",
        en = f"your entered excel file has errors in rows {error_data} in the SubKatalog sheet" )
    return lang_dict[lang]


error_excel_warning_text=dict(
    uz = "Sizga tashlab bergan excel failgagi sheet nomilari va ustun nomlari o'zgartirilgan . Iltimos sheet nomlari va ustun nomlari o'zgartirmang. Sizga tashlab berilgan excel failga faqat malumot qo'shing.!",
    en = "Your excel file has a warning sheet name and sheet name. Please enter the sheet name and the sheet name. Please enter the sheet name and the sheet name." ,
ru="Ваш файл Excel имеет предупреждающее имя листа и имя листа. Пожалуйста, введите имя листа и имя листа. Пожалуйста, введите имя листа и имя листа." )

welcome_text=dict(
    uz = "Hurmatli va qadrli mehmonlarimiz!\nSizni milliy va turk taomlari tayyorlanadigan «Dilkash Shirin taom» oilaviy restoranimizda garshi olishdan mamnunmiz!\n«Dilkash Shirin taom» oilaviy restorani bu - turk va yevropa oshxonasi uyg'unlashuvidir.\n🌙 Aziz yurtdoshlar va yurtimiz mehmonlarini afsonaviy Dilkash oilaviy restoraniga taklif qilamiz, sizga manzur keladigan iliqlik va mazali taomlarni taqdim etishga tayyormiz\n🍽 Restoranimiz menyusida 120 dan ziyod turli millatlarga mansub taomlar, 25 dan ziyod suyuq taomlar va 30 dan ortiq salatlar qad rostlaga\n✅ Служба доставки национальной сети ресторан  Dilkash 🥘 \n📲 Заказывайте с 9:00 до 22:00😋\n☎️ 97 616 08 88 \n————————————————————————————\n✅'Dilkash Milliy Taomlar' restoraning yetkazib berish xizmati 🥘\n📲 10:00 dan 23:00 gacha buyurtma bering😋\n☎️ 97 616 08 88 ",
    ru = "Уважаемые и уважаемые гости!\nМы рады приветствовать Вас в нашем семейном ресторане 'Дилкаш Ширин Таом', где готовят национальные и турецкие блюда!\nСемейный ресторан 'Дилкаш Ширин Таом' - это сплав турецкой и европейской кухни.\n 🌙 Дорогие соотечественники и гости нашей страны.Приглашаем вас в легендарный семейный ресторан Дилкаш, готовы угостить вас теплыми и вкусными блюдами\n🍽 В меню нашего ресторана более 120 блюд разных национальностей, более 25 жидких блюд и более 30 салатов. ———————————————————————————\n ✅ Служба доставки ресторана «Дилкаш Миллий Таомлар» 🥘\n📲 Заказ с 9:00 до 22:00 😋\n☎️ 97 616 08 88 ",
    en = "Dear and respected guests!\nWe are pleased to welcome you to our family restaurant «Dilkash Shirin taom» where national and Turkish dishes are prepared!\n«Dilkash Shirin taom» family restaurant is a combination of Turkish and European cuisine.\n🌙 We invite our dear compatriots and guests of our country to the fabulous Dilkash family restaurant, we are ready to offer you delicious and delicious dishes that you will like\n🍽 The menu of our restaurant includes more than 120 dishes of various nationalities, more than 25 cold dishes and more than 30 salads\n✅ National restaurant delivery service Dilkash 🥘 \n📲 Order from 9:00 to 22:00😋\n☎️ 97 616 08 88 \n————————————————————————————\n✅'Dilkash Milliy Taomlar' restaurant delivery service 🥘\n📲 Order from 10:00 to 23:00😋\n☎️ 97 616 08 88 " )
send_me_contact_bot=dict( uz = "Botdan foydalanish uchun kontaktingizni yuboring!",
                          ru = "Отправьте свой контакт, чтобы воспользоваться ботом!",
                          en = "Send your contact to use the bot!" )
incorrect_format=dict( uz = "Noto'g'ri format!",ru = "Неправильный формат!",en = "Incorrect format!" )
send_contact_mandatory=dict( uz = "Botdan foydalanish uchun kontaktingizni yuboring!",
                             ru = "Отправьте свой контакт, чтобы воспользоваться ботом!",
                             en = "Send your contact to use the bot!" )
location_contact_text=dict(
    uz = f"Dilkash Restaurant:\n\n📱 Buyurtma uchun telefon: +998976160888\n📥 Onlayn buyurtma: @dilkash_olmaliq\n🚦 Ish vaqtimiz: 09:00-22:00\n📍 Manzilimiz:Olmaliq shahar, Prospekt Primkulova (Mo'ljal: Olmaliq Mudofa Ishlari Binosi)",
    ru = f"Ресторан Дилкаш:\n\n📱 Телефон для заказа: +998976160888\n📥 Онлайн заказ: @dilkash_olmaliq\n🚦 Время работы: 09:00-22:00\n📍 Наш адрес: город Алмалык, проспект Примкулова (Направление : Здание Алмалыкского Военкомата)",
    en = f"Dilkash Restaurant:\n\n📱 Phone for order: +998976160888\n📥 Online order: @dilkash_olmaliq\n🚦 Our working hours: 09:00-22:00\n📍 Our address: Almaliq city, Prospekt Primkulova (Destination : Almalyk Defense Works Building)")
rate_server=dict( uz = "Iltimos, Servis Sifatini 1 dan 5 gacha baholang: ",ru = "Пожалуйста, оцените сервер от 1 до 5",
                  en = "Please rate the server from 1 to 5" )
deliver_go=dict( uz = {"🍚Choyxona palov - 210 000 so'm\n🥨To'y qovurdoq + padnos - 450 000 so'm\n🧇Norin 1kg - 85 000 so'm\n🥟Manti 1dona - 6500 so'm\n🍚Toy oshi 1kg - 190 000 so'm\n🥓Xasip 1kg - 80 000 so'm\n🍗KFC 1kg - 92 000 so'm\n🍖Tabaka jo'ja 1kg - 85 000 so'm\n\nTog'ara uchun buyurtmalar 1 kun oldin qabul qilinadi."},
                 ru = {"🍚Чайхана плов – 210 000 сум\n🥨Свадебное жаркое + паднос - 450 000 сум\n🧇Нasddорин 1кг - 85 000 сум\n🥟Манты 1 шт. - 6 500 сум\n🍚Свадебный плов 1 кг - 190 000 сум\n🥓K хасип 1кг - 80 000 сум\n🍗KFC 1кг - 92 000 сум\n🍖Табака курица 1кг - 85 000 сум\n\nЗаказы на тогары принимаются за 1 день."},
                  en = {"🍚Teahouse pilaf - 210,000 soums\n🥨Wedding roast + padnos - 450,000 soums\n🧇Noridan 1kg - 85,000 soums\n🥟Manti 1 piece - 6,500 soums\n🍚Wedding dinner 1kg/ - 190,000 soums\n🥓Khasip 1kg - 80,000 soums\n🍗KFC 1kg - 92,000 soums\n🍖Tabaka chicken 1kg - 85,000 soums\n\nOrders for togara are accepted in 1 day."})
work_time=dict( uz = "Ish vaqtimiz: 09:00-22:00",ru = "Наше время работы: 09:00-22:00",
                en = "Our working time: 09:00-22:00" )
work_time_off=dict( uz = "Ish vaqtimiz: 09:00-22:00\nRestaurant ochilishini kuting!",ru = "Наше время работы: 09:00-22:00\nДождитесь открытия ресторана!",
                en = "Our working time: 09:00-22:00\nWait for the restaurant to open!" )
select_book_table_date=dict( uz = "Bron qilish sanasini tanlang",ru = "Выберите дату бронирования",
                             en = "Select the booking date" )
select_book_table_time=dict( uz = "Bron qilish vaqtni tanlang",ru = "Выберите время бронирования",
                             en = "Select the booking time" )
our_network=dict( uz = "Bizning tarmoqlarimiz:",ru = "Наши сети:",en = "Our networks:" )
enter_settings=dict( uz = "Sozlamalarga kiriting",ru = "Войти в настройки",en = "Enter settings" )
how_many_people_do_you_book=dict( uz = "Neche kishi uchun bron qilmoqchisiz?",
                                  ru = "На сколько человек вы хотите забронировать?",
                                  en = "How many people do you want to book?" )

send_your_phone=dict( uz = "Siz bilan bog'lanish uchun telefon raqamingizni yuboring:",
                      ru = "Отправьте свой номер телефона для связи с вами:",
                      en = "Send your phone number to contact you:" )
please_enter_correct_name=dict( uz = "Iltimos, ismingizni to'g'ri kiriting",
                                ru = "Пожалуйста, введите свое имя правильно",en = "Please enter your name correctly" )
who_is_booking_enter_name=dict( uz = "Kimning nomiga bron qilmoqchisiz?\nIsmni yuboring:",
                                ru = "Кому вы хотите забронировать?\nОтправьте имя:",
                                en = "Who do you want to book?\nSend the name:" )


def booking_table_data (data,lang):
    data_lang=dict(
        uz = f"Dilkash Stol Bron:\n\nSana: {data['date']}\nVaqt: {data['time']}\nMehmonlar soni: {data['people_number']}\nIsm: {data['name']}\nTelefon raqam: {data['phone']} ",
        ru = f"Дилкаш Забронировать стол:\n\nДата: {data['date']}\nВремя: {data['time']}\nКоличество: {data['people_number']}\nИмя: {data['name']}\nТелефон: {data['phone']}",
        en = f"Dilkash Table Booking:\n\nDate: {data['date']}\nTime: {data['time']}\nNumber of guests: {data['people_number']}\nName: {data['name']}\nPhone: {data['phone']}" )
    return data_lang[lang]


def booking_table_data_for_canal (data,lang):
    data_lang=dict(
        uz = f"Dilkash Stol Bron:\n\nSana: {data['date']}\nVaqt: {data['time']}\nMehmonlar soni: {data['people_number']}\nIsm: {data['name']}\nUsername: @{data['username']}\nTelefon raqam: {data['phone']} ",
        ru = f"Дилкаш Забронировать стол:\n\nДата: {data['date']}\nВремя: {data['time']}\nКоличество: {data['people_number']}\nИмя: {data['name']}\nТелефон: {data['phone']}",
        en = f"Dilkash Table Booking:\n\nDate: {data['date']}\nTime: {data['time']}\nNumber of guests: {data['people_number']}\nName: {data['name']}\nUsername: @{data['username']}\nPhone: {data['phone']}" )
    return data_lang[lang]


done_booking=dict( uz = "Bron qilindi!",ru = "Забронировано!",en = "Booked!" )
delivery_warning_text=dict(
    uz = "Telefon raqamingizni quyidagi formatda yuboring yoki kiriting: +998 ** *** ** ** \nEslatma: Agar siz onlayn buyurtma uchun Click yoki Payme orqali toʻlashni rejalashtirmoqchi boʻlsangiz, tegishli xizmatda hisob qaydnomasi roʻyxatdan oʻtgan telefon raqamini koʻrsating.",
    ru = "Отправьте свой номер телефона в следующем формате или введите: +998 ** *** ** ** \nПредупреждение: Если вы хотите оплатить онлайн заказ через Click или Payme, укажите номер телефона, зарегистрированный в соответствующем сервисе.",
    en = "Send your phone number in the following format or enter: +998 ** *** ** ** \nWarning: If you want to pay for an online order through Click or Payme, specify the phone number registered in the relevant service." )
clear_basket_text=dict( uz = "Savat tozalandi",ru = "Корзина очищена",en = "Basket clean" )
enter_delivery_time=dict( uz = "Yetkazib berish vaqtni kiriting",ru = "Введите время доставки",
                          en = "Enter delivery time" )

def delivery_report (data,lang):
    data_lang=dict(
        uz = f"{data['response']} \nMahsulotlar: {data['price']}\nYetkazib berish: {data['deliver']} so'm \nJami:{data['total_price']}",
        ru = f"{data['response']} \nПродукты: {data['price']}\nДоставка: {data['deliver']} сум \nИтого:{data['total_price']}",
        en = f"{data['response']} \nProducts: {data['price']}\nDelivery: {data['deliver']} сум \nTotal:{data['total_price']}" )
    return data_lang[lang]


accepted_text=dict( uz = "Buyurtma qabul qilindi!",ru = "Заказ принят!",en = "Order accepted!" )
select_payment_type=dict( uz = "To'lov turini tanlang",ru = "Выберите тип оплаты",en = "Select payment type" )


def order_report_text (data,lang):
    data_lang=dict(
        uz = f"Sizning buyurtmangiz:{data['response']}\nManzil:{data['location']}\n\nMahsulotlar: {data['price']}\nYetkazib berish: {data['deleviry_price']} so'm \nJami:{data['total_price']} so'm",
        ru = f"Ваш заказ:{data['response']}\nАдрес:{data['location']}\nПродукты: {data['price']}\nДоставка: {data['deleviry_price']} сум \nИтого:{data['total_price']} сум",
        en = f"Your order:{data['response']}\nAddress:{data['location']}\nProducts: {data['price']}\nDelivery: {data['deleviry_price']} sum \nTotal:{data['total_price']} sum" )
    return data_lang[lang]


def check_user_location (data,lang):
    data_lang=dict(
        uz = f"Geolokatsiyangizni tasdiqlang! Sizning manzilingiz: {data['house_number']}, {data['road']}, {data['neighbourhood']}, {data['county']}, {data['city']}  mi?",
        ru = f"Подтвердите свое местоположение! Ваш адрес: {data['house_number']}, {data['road']}, {data['neighbourhood']}, {data['county']}, {data['city']}  ?",
        en = f"Confirm your location! Your address: {data['house_number']}, {data['road']}, {data['neighbourhood']}, {data['county']}, {data['city']}  ?" )
    return data_lang[lang]


added_text=dict( uz = "Savatga qo'shildi",en = "Added to basket",ru = "Добавлено в корзину" )
error_geolocation_format=dict( uz = "Geolokatsiya formatida xatolik!",ru = "Ошибка в формате геолокации!",
                               en = "Geolocation format error!" )
send_your_location=dict( uz = "Geolokatsiyangizni yuboring",ru = "Отправьте свое местоположение",
                         en = "Send your location" )
error_payment=dict( uz = "To'lovda xatolik",en = "Payment error",ru = "Ошибка оплаты" )
success_payment=dict( uz = "To'lov muvaffaqiyatli amalga oshirildi",en = "Payment successful",
                      ru = "Оплата прошла успешно" )
select_item_from_menu=dict( uz = "Quyidagi menulardan birini tanlang.",en = "Select one of the following menus.",
                            ru = "Выберите одно из следующих меню." )
conformed=dict( uz = "Tasdiqlandi!",en = "Conformed",ru = " принят" )
empty_your_locations=dict( uz = "Sizning geolokatsiyalariz mavjud emas",en = "You have no locations",
                           ru = "У вас нет локаций" )
select_your_location=dict( uz = "Geolokatsiyangizni tanlang",en = "Select your location",ru = "Выберите свою локацию" )
error_not_exist_our_location=dict( uz = "Sizning manzilingizda bizning xizmatimiz mavjud emas!",
                                   en = "Our service is not available at your address!",
                                   ru = "Наша служба не доступна по вашему адресу!" )
error_phone_format=dict( uz = "Telefon raqam formati noto'g'ri",en = "Phone number format is incorrect",
                         ru = "Неверный формат номера телефона" )

def product_caption_text (data,lang):
    data_lang=dict( uz = f"Taomlar nomini: {data['product_name']} \nTarkibi:{data['product_igredents']}  \nNarxi: {data['price']} so'm \n ",
                    ru = f"Название продукта: {data['product_name']} \n Состав:{data['product_igredents']}  \nЦена: {data['price']} сум\n ",
                    en = f"Product name: {data['product_name']} \n Ingredients:{data['product_igredents']}  \nPrice: {data['price']} sum\n " )
    return data_lang[lang]


empty_basket_text=dict( uz = "Savat bo'sh",en = "Basket is empty",ru = "Корзина пуста" )
manual_bot=dict( uz = "Siz quyidagi video orqali botni qanday ishlashini bilib olasiz.",en = "You will learn how the bot works in the video below.",ru = "О том, как работает бот, вы узнаете из видео ниже." )
send_resume=dict( uz = "Resumeyingizni ushbu link orqali yuboring.",en = "Submit your resume via this link.",ru = "Отправьте свое резюме по этой ссылке." )


def basket_report(data, lang):
    data_lang = dict(
        uz=f"Savatda:\n {data['response']}  \nMahsulotlar: {data['prices']}\nYetkazib berish: {data['deliver']} so'm \nJami:{data['total_price']}",
        ru=f"В корзине:\n {data['response']}  \nПродукты: {data['prices']}\nДоставка: {data['deliver']} сум \nИтого:{data['total_price']}",
        en=f"In the basket:\n {data['response']}  \nProducts: {data['prices']}\nDelivery: {data['deliver']} sum \nTotal:{data['total_price']}")

    return data_lang[lang]


def basket_report_text (data,lang):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%d%m%y")
    data_lang=dict(
        uz = f"Buyurtma Raqami: {data['order_id']}{formatted_time}\nManzil: {data['location']}\n\n To'lov turi: {data['payment']}\n\n {data['response']}  \nMahsulotlar: {data['prices']}\nYetkazib berish: {data['deliver']} so'm \nJami:{data['total_price']}\n\nBuyurtmangiz qabul qilindi.\n Yetkazib berish vaqti - {data['delivery_time']}",
        ru=f"Номер заказа: {data['order_id']}{formatted_time}\nАдрес: {data['location']}\n Тип оплаты: {data['payment']}\n {data['response']}  \nПродукты: {data['prices']}\nДоставка: {data['deliver']} сум \nИтого:{data['total_price']}\nВаш заказ принят.\n Время доставки - {data['delivery_time']}",
        en=f"Order number: {data['order_id']}{formatted_time}\nAddress: {data['location']}\n Payment type: {data['payment']}\n {data['response']}  \nProducts: {data['prices']}\nDelivery: {data['deliver']} sum \nTotal:{data['total_price']}\nYour order has been accepted.\n Delivery time - {data['delivery_time']}"
        )
    return data_lang[lang]

def basket_report_group (data,lang):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%d%m%y")
    data_lang=dict(
        uz = f"Buyurtma Raqami: {data['order_id']}{formatted_time}\n\n User Ism Familiyasi:{data['name']},\n User Kontakt :  {data['phone']}\n User Name : @{data['user_name']} \n\n Manzil: {data['location']}\n\n To'lov turi: {data['payment']}\n\n {data['response']}  \nMahsulotlar: {data['prices']}\nYetkazib berish: {data['deliver']} so'm \nJami:{data['total_price']}\n\nBuyurtmangiz qabul qilindi.\n Yetkazib berish vaqti - {data['delivery_time']}",
        ru=f"Номер заказа: {data['order_id']}{formatted_time}\n User Имя Фамилия:{data['name']},\n User Контакт :  {data['phone']} User Name : @{data['user_name']} \n Адрес: {data['location']}\n Тип оплаты: {data['payment']}\n {data['response']}  \nПродукты: {data['prices']}\nДоставка: {data['deliver']} сум \nИтого:{data['total_price']}\nВаш заказ принят.\n Время доставки - {data['delivery_time']}",
        en=f"Order number: {data['order_id']}{formatted_time}\n User Name Surname:{data['name']},\n User Contact :  {data['phone']} User Name : @{data['user_name']} \n Address: {data['location']}\n Payment type: {data['payment']}\n {data['response']}  \nProducts: {data['prices']}\nDelivery: {data['deliver']} sum \nTotal:{data['total_price']}\nYour order has been accepted.\n Delivery time - {data['delivery_time']}"
        )
    return data_lang[lang]


rate_meal_quality=dict( uz = "Iltimos, Taom Sifatini 1 dan 5 gacha baholang:",
                        en = "Please rate the quality of the dish from 1 to 5:",
                        ru = "Пожалуйста, оцените качество блюда от 1 до 5:" )
comments_your_oponion=dict( uz = "Fikr-mulohazangizni xabar sifatida qoldiring:",
                            en = "Please write your opinion about the dish:",
                            ru = "Пожалуйста, напишите ваш отзыв о блюде:" )
thanks_your_comment=dict(
    uz = "Fikr-mulohazangiz uchun rahmat! Vaziyatni hal qilish uchun barcha sa'y-harakatlarimizni qilamiz! Siz bilan bog'lanishimiz uchun iltimos telefon raqamingizni yuboring:",
    ru = "Спасибо за отзыв! Ваш отзыв будет отправлен на обработку! Пожалуйста, укажите свой телефон для связи:",
    en = "Thank you for your feedback! Your feedback will be sent for processing! Please specify your phone number for communication:" )

accepted_your_idea=dict( uz = "Qabul qilindi, rahmat!",en = "Accepted, thank you!",ru = "Принято, спасибо!" )
success_update_excel_file=dict( uz = "Excel fayl muvaffaqiyatli yangilandi",en = "Excel file updated successfully",
                                ru = "Excel файл успешно обновлен" )
order_accepted_text=dict( uz = "Buyurtma qabul qilindi",en = "Order accepted",ru = "Заказ принят." )