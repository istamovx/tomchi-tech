"""
TomchiTech Bot — Lokalizatsiya moduli
=====================================
Qo'llab-quvvatlanadigan tillar: uz (asosiy), ru, en

Ishlatish:
    from locale import tr          # bot/ papkasida ishga tushirilsa
    text = tr('welcome_new', lang, name="Ali")
"""

# ── Translation strings ────────────────────────────────────────────────────────
STRINGS: dict[str, dict[str, str]] = {

    # ════════════════════════════════════════════════════
    # O'ZBEK (asosiy til)
    # ════════════════════════════════════════════════════
    'uz': {

        # /start
        'welcome_new': (
            "👋 Salom, <b>{name}</b>!\n\n"
            "🌿 <b>TomchiTech</b> — Aqlli ferma monitoring tizimi\n\n"
            "Xizmatdan foydalanish uchun obuna paketini tanlang:"
        ),
        'welcome_back': (
            "👋 Xush kelibsiz, <b>{name}</b>!\n\n"
            "📦 Paketingiz: {emoji} <b>{package}</b>\n"
            "📅 {end_date} gacha\n\n"
            "⌨️ Pastdagi tugmalar panelini ochish uchun input maydonidagi "
            "klaviatura ikonkasini bosing."
        ),

        # Subscription
        'sub_required':     "❌ Bu funksiyadan foydalanish uchun obuna kerak.",
        'sub_activated':    "🎉 <b>Tabriklaymiz!</b>\n\n{emoji} <b>{package}</b> paketi faollashtirildi!\n📅 {end_date} gacha\n\nEndi TomchiTech xizmatlaridan foydalanishingiz mumkin!",
        'keyboard_ready':   "⌨️ Tugmalar paneli tayyor! Pastda klaviatura ikonkasini bosib oching.",
        'main_menu':        "🏠 <b>Asosiy menyu</b>\n{emoji} {package} | {end_date} gacha\n\nTugmalardan birini tanlang:",

        # Report
        'loading':          "⏳ Yuklanmoqda...",
        'report_header':    "📊 <b>FERMA HISOBOTI</b>\n🕐 {time}\n{status}\n━━━━━━━━━━━━━━━━━━\n\n",
        'status_critical':  "🔴 DIQQAT: Kritik holatlar!",
        'status_ok':        "🟢 Umumiy holat: Yaxshi",

        # Farms
        'farms_header':     "🌾 <b>FERMALARINGIZ ({count} ta)</b>\n\n",
        'sensor_header':    "📡 <b>SENSOR MALUMOTLARI</b>\n\n",

        # Irrigation
        'irr_control':      "💧 <b>SUGHORISH BOSHQARUVI</b>\n\nQaysi fermada sughorish boshlamoqchisiz?\n\n",
        'irr_premium_only': "❌ Bu funksiya faqat Standart va Premium paketlarda mavjud.",
        'irr_detail': (
            "💧 <b>SUGHORISH — {farm}</b>\n\n"
            "📊 <b>Hozirgi holat:</b>\n"
            "🌱 Tuproq namligi: <b>{soil}%</b>\n"
            "🌡 Harorat: <b>{temp}C</b>\n"
            "📐 Maydon: <b>{area} ga</b>\n\n"
            "🤖 <b>Tizim tavsiyasi:</b>\n"
            "⏱ Davomiylik: <b>{dur} daqiqa</b>\n"
            "💦 Suv sarfi: <b>{water} litr</b>\n"
            "🎯 Maqsad namlik: <b>{target}%</b>\n\n"
            "Tomchilatib sughorish tizimi tayyor."
        ),
        'irr_started': (
            "✅ <b>SUGHORISH BOSHLANDI!</b>\n\n"
            "🌾 Ferma: <b>{farm}</b>\n"
            "⏱ Davomiylik: <b>{dur} daqiqa</b>\n"
            "💦 Suv sarfi: <b>{water} litr</b>\n\n"
            "📊 <b>Bashorat:</b>\n"
            "🌱 Tuproq namligi: {soil_before}% → <b>{soil_after}%</b>\n\n"
            "Tomchilatib sughorish tizimi ishga tushdi.\n"
            "⏰ {dur} daqiqadan keyin avtomatik toxtatiladi."
        ),
        'irr_stopped':      "⏹ <b>SUGHORISH TOXTATILDI</b>\n\n🌾 {farm}\n✅ Tizim ochirildi.",
        'irr_history_empty':"📋 <b>Sughorish tarixi bosh.</b>\n\nHali hech qanday sughorish amalga oshirilmagan.",
        'irr_history_hdr':  "📋 <b>SONGGI SUGHORISHLAR</b>\n━━━━━━━━━━━━━━━━━━\n\n",

        # Alerts
        'alerts_critical': (
            "🚨 <b>KRITIK OGOHLANTIRISHLAR</b>\n"
            "⏱ {time}\n━━━━━━━━━━━━━━━━━━\n\n"
        ),
        'alerts_warning':   "🟡 <b>EHTIYOT HOLATLAR</b>\n━━━━━━━━━━━━━━━━━━\n\n",
        'alerts_none':      "✅ <b>Hozirda hech qanday ogohlantirish yoq.</b>\n\nBarcha fermalar normal. 🌿",

        # Specialists
        'spec_premium_only': (
            "👨‍🔬 <b>Mutaxassis chaqirish</b>\n\n"
            "❌ Bu funksiya faqat <b>Premium</b> paket uchun.\n\n"
            "Obunangizni Premium ga yuksaltiring:"
        ),
        'spec_header':      "👨‍🔬 <b>MUTAXASSISLAR</b>\nKritik holatlarda quyidagilar bilan boglanin:\n━━━━━━━━━━━━━━━━━━\n\n",
        'spec_hours':       "⏰ Ish vaqti: Du-Jum 08:00-18:00\n🆘 Favqulodda: 24/7",

        # Subscription info
        'sub_info': (
            "📦 <b>OBUNA MALUMOTLARI</b>\n━━━━━━━━━━━━━━━━━━\n\n"
            "{emoji} Paket: <b>{package}</b>\n"
            "💰 {price:,} som/oy\n"
            "📅 Tugash: {end_date}\n"
            "🕐 Qolgan: <b>{days} kun</b>\n\n"
            "<b>Funksiyalar:</b>\n{features}"
        ),

        # Help
        'help_text': (
            "ℹ <b>YORDAM</b>\n\n"
            "📊 Hisobot — sensor malumotlari hisoboti\n"
            "🌾 Fermalar — alohida ferma sensori\n"
            "💧 Sug'orish — tomchilatib sughorish boshqaruvi\n"
            "🚨 Ogohlantirishlar — kritik/ehtiyot holatlar\n"
            "👨‍🔬 Mutaxassis — Premium foydalanuvchilar uchun\n"
            "🌐 Til — interfeys tilini o'zgartirish\n\n"
            "Kritik chegara:\n"
            "• Harorat > {temp_max}C\n"
            "• Namlik < {humid_min}%\n"
            "• Tuproq namligi < {soil_min}%\n\n"
            "🔔 Har soatda avtomatik hisobot\n\n"
            "📞 support@tomchitech.uz"
        ),

        # Language
        'lang_choose':      "🌐 Til tanlang / Выберите язык / Choose language:",
        'lang_changed_uz':  "✅ O'zbek tili tanlandi! 🇺🇿\n\nTizim o'zbek tilida ishlaydi.",
        'lang_changed_ru':  "✅ O'zbek tili tanlandi! 🇺🇿\n\nTizim o'zbek tilida ishlaydi.",
        'lang_changed_en':  "✅ O'zbek tili tanlandi! 🇺🇿\n\nTizim o'zbek tilida ishlaydi.",

        # Inline buttons
        'btn_back_menu':    "⬅ Asosiy menyu",
        'btn_back_farms':   "⬅ Fermalar",
        'btn_back_irr':     "⬅ Sughorish",
        'btn_refresh':      "🔄 Yangilash",
        'btn_irr_start':    "💧 Sughorish boshlash",
        'btn_irr_history':  "📋 Sughorish tarixi",
        'btn_irr_rec':      "▶ {dur} daqiqa (tavsiya)",
        'btn_irr_stop':     "⏹ Toxtatish",
        'btn_irr_other':    "💧 Boshqa ferma",
        'btn_specialist':   "👨‍🔬 Mutaxassis",
        'btn_upgrade':      "⬆ Paketni yuksaltirish",
        'btn_premium':      "🏆 Premium ga otish",
        'btn_pay_confirm':  "✅ Tolovni tasdiqlash",
        'btn_other_pkg':    "⬅ Boshqa paket",
        'btn_ack':          "✅ Ko'rib chiqdim",

        # Package selection
        'pkg_detail': (
            "{emoji} <b>{package} paketi</b>\n"
            "💰 <b>{price:,} som/oy</b> | {days} kun\n\n"
            "<b>Kiruvchi funksiyalar:</b>\n{features}\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "Demo rejimda to'lovni tasdiqlang:"
        ),
        'pkgs_header':      "📦 <b>Obuna paketlari</b>\n\n",

        # Auto irrigation
        'auto_irr_start': (
            "🤖 <b>AVTOMATIK SUGHORISH BOSHLANDI</b>\n\n"
            "🌾 {farm}\n"
            "🌱 Tuproq namligi: <b>{soil}%</b> (kritik – {threshold}% dan past)\n"
            "⏱ Davomiylik: <b>{dur} daqiqa</b>\n"
            "💦 Suv sarfi: <b>{water} litr</b>\n"
            "🎯 Maqsad namlik: <b>{target}%</b>\n\n"
            "⏰ {dur} daqiqadan keyin to'xtaydi."
        ),
        'auto_irr_stop': (
            "✅ <b>AVTOMATIK SUGHORISH YAKUNLANDI</b>\n\n"
            "🌾 {farm}\n"
            "⏱ Davomiylik: <b>{dur} daqiqa</b>\n"
            "🌱 Tuproq namligi: {soil_before}% → <b>{soil_after}%</b>\n"
            "🕐 {time}\n\n"
            "🟢 Tizim normal rejimga qaytdi."
        ),

        # Hourly/critical jobs
        'hourly_report': (
            "⏰ <b>SOATLIK HISOBOT</b>\n"
            "🕐 {time}\n{status}\n━━━━━━━━━━━━━━━━━━\n\n"
        ),
        'critical_alert': (
            "🚨 <b>KRITIK OGOHLANTIRISH!</b>\n━━━━━━━━━━━━━━━━━━\n"
            "🌾 <b>{farm}</b>\n⏱ {time}\n\n"
            "🌡{temp}C  💧{humid}%  🌱{soil}%  🔋{battery}%\n\n"
            "📋 <b>Zudlik bilan:</b>\n{tips}"
        ),

        # Alert buffer (flush)
        'buf_header':       "🔔 <b>{count} ta yangi bildirishnoma</b>\n⏰ {time}\n{'━' * 26}",
        'buf_footer':       "{'━' * 26}\n📌 <i>Ushbu xabar log sifatida saqlanadi</i>",
        'ack_done':         "✅ Belgilandi!",
        'ack_text':         "✅ <b>Ko'rib chiqildi</b> — {name}\n🕐 {time}",

        # Web dashboard API
        'web_irr_start': (
            "💧 <b>WEB DASHBOARD: SUGHORISH BOSHLANDI!</b>\n\n"
            "🌾 Sensor/Ferma: <b>{farm}</b>\n"
            "🌱 Tuproq namligi: <b>{soil}%</b>\n"
            "⏱ Davomiylik: <b>{dur} daqiqa</b>\n"
            "💦 Suv sarfi: ~<b>{water:.0f} litr</b>\n"
            "🖥 Manba: Web dashboard\n"
            "🕐 {time}\n\n"
            "Tomchilatib sughorish tizimi ishga tushdi."
        ),
        'web_irr_stop': (
            "🏁 <b>WEB DASHBOARD: SUGHORISH YAKUNLANDI!</b>\n\n"
            "🌾 Sensor/Ferma: <b>{farm}</b>\n"
            "🌱 Yangi namlik: <b>{soil}%</b>\n"
            "🕐 {time}\n\n"
            "🟢 Tizim normal rejimga qaytdi."
        ),
    },

    # ════════════════════════════════════════════════════
    # РУССКИЙ
    # ════════════════════════════════════════════════════
    'ru': {

        'welcome_new': (
            "👋 Привет, <b>{name}</b>!\n\n"
            "🌿 <b>TomchiTech</b> — Интеллектуальная система мониторинга фермы\n\n"
            "Выберите пакет подписки для использования сервиса:"
        ),
        'welcome_back': (
            "👋 Добро пожаловать, <b>{name}</b>!\n\n"
            "📦 Ваш пакет: {emoji} <b>{package}</b>\n"
            "📅 До {end_date}\n\n"
            "⌨️ Нажмите иконку клавиатуры в поле ввода, чтобы открыть панель кнопок."
        ),

        'sub_required':     "❌ Для использования этой функции необходима подписка.",
        'sub_activated':    "🎉 <b>Поздравляем!</b>\n\n{emoji} <b>{package}</b> пакет активирован!\n📅 До {end_date}\n\nТеперь вы можете пользоваться услугами TomchiTech!",
        'keyboard_ready':   "⌨️ Панель кнопок готова! Нажмите иконку клавиатуры внизу.",
        'main_menu':        "🏠 <b>Главное меню</b>\n{emoji} {package} | До {end_date}\n\nВыберите один из разделов:",

        'loading':          "⏳ Загрузка...",
        'report_header':    "📊 <b>ОТЧЁТ ПО ФЕРМАМ</b>\n🕐 {time}\n{status}\n━━━━━━━━━━━━━━━━━━\n\n",
        'status_critical':  "🔴 ВНИМАНИЕ: Критические ситуации!",
        'status_ok':        "🟢 Общее состояние: Хорошо",

        'farms_header':     "🌾 <b>ВАШИ ФЕРМЫ ({count} шт.)</b>\n\n",
        'sensor_header':    "📡 <b>ДАННЫЕ ДАТЧИКОВ</b>\n\n",

        'irr_control':      "💧 <b>УПРАВЛЕНИЕ ПОЛИВОМ</b>\n\nНа какой ферме начать полив?\n\n",
        'irr_premium_only': "❌ Эта функция доступна только в пакетах Стандарт и Премиум.",
        'irr_detail': (
            "💧 <b>ПОЛИВ — {farm}</b>\n\n"
            "📊 <b>Текущее состояние:</b>\n"
            "🌱 Влажность почвы: <b>{soil}%</b>\n"
            "🌡 Температура: <b>{temp}C</b>\n"
            "📐 Площадь: <b>{area} га</b>\n\n"
            "🤖 <b>Рекомендация системы:</b>\n"
            "⏱ Длительность: <b>{dur} минут</b>\n"
            "💦 Расход воды: <b>{water} л</b>\n"
            "🎯 Целевая влажность: <b>{target}%</b>\n\n"
            "Система капельного орошения готова."
        ),
        'irr_started': (
            "✅ <b>ПОЛИВ НАЧАТ!</b>\n\n"
            "🌾 Ферма: <b>{farm}</b>\n"
            "⏱ Длительность: <b>{dur} минут</b>\n"
            "💦 Расход воды: <b>{water} л</b>\n\n"
            "📊 <b>Прогноз:</b>\n"
            "🌱 Влажность почвы: {soil_before}% → <b>{soil_after}%</b>\n\n"
            "Система капельного орошения запущена.\n"
            "⏰ Автоматически остановится через {dur} минут."
        ),
        'irr_stopped':      "⏹ <b>ПОЛИВ ОСТАНОВЛЕН</b>\n\n🌾 {farm}\n✅ Система отключена.",
        'irr_history_empty':"📋 <b>История полива пуста.</b>\n\nПолив ещё не выполнялся.",
        'irr_history_hdr':  "📋 <b>ПОСЛЕДНИЕ ПОЛИВЫ</b>\n━━━━━━━━━━━━━━━━━━\n\n",

        'alerts_critical':  "🚨 <b>КРИТИЧЕСКИЕ ОПОВЕЩЕНИЯ</b>\n⏱ {time}\n━━━━━━━━━━━━━━━━━━\n\n",
        'alerts_warning':   "🟡 <b>ПРЕДУПРЕЖДЕНИЯ</b>\n━━━━━━━━━━━━━━━━━━\n\n",
        'alerts_none':      "✅ <b>Нет активных оповещений.</b>\n\nВсе фермы в норме. 🌿",

        'spec_premium_only': (
            "👨‍🔬 <b>Вызов специалиста</b>\n\n"
            "❌ Эта функция только для пакета <b>Премиум</b>.\n\n"
            "Повысьте подписку до Премиум:"
        ),
        'spec_header':      "👨‍🔬 <b>СПЕЦИАЛИСТЫ</b>\nСвяжитесь с ними в критических ситуациях:\n━━━━━━━━━━━━━━━━━━\n\n",
        'spec_hours':       "⏰ Рабочее время: Пн-Пт 08:00-18:00\n🆘 Экстренно: 24/7",

        'sub_info': (
            "📦 <b>ИНФОРМАЦИЯ О ПОДПИСКЕ</b>\n━━━━━━━━━━━━━━━━━━\n\n"
            "{emoji} Пакет: <b>{package}</b>\n"
            "💰 {price:,} сум/мес\n"
            "📅 Истекает: {end_date}\n"
            "🕐 Осталось: <b>{days} дн.</b>\n\n"
            "<b>Функции:</b>\n{features}"
        ),

        'help_text': (
            "ℹ <b>СПРАВКА</b>\n\n"
            "📊 Отчёт — данные датчиков\n"
            "🌾 Фермы — датчики отдельной фермы\n"
            "💧 Полив — управление капельным орошением\n"
            "🚨 Оповещения — критические/предупредительные ситуации\n"
            "👨‍🔬 Специалист — для пользователей Премиум\n"
            "🌐 Язык — изменить язык интерфейса\n\n"
            "Критические пороги:\n"
            "• Температура > {temp_max}C\n"
            "• Влажность < {humid_min}%\n"
            "• Влажность почвы < {soil_min}%\n\n"
            "🔔 Автоматический отчёт каждый час\n\n"
            "📞 support@tomchitech.uz"
        ),

        'lang_choose':      "🌐 Til tanlang / Выберите язык / Choose language:",
        'lang_changed_uz':  "✅ Выбран O'zbek 🇺🇿\n\nСистема работает на узбекском языке.",
        'lang_changed_ru':  "✅ Выбран Русский язык! 🇷🇺\n\nСистема работает на русском языке.",
        'lang_changed_en':  "✅ English selected! 🇬🇧\n\nThe system is now in English.",

        'btn_back_menu':    "⬅ Главное меню",
        'btn_back_farms':   "⬅ Фермы",
        'btn_back_irr':     "⬅ Полив",
        'btn_refresh':      "🔄 Обновить",
        'btn_irr_start':    "💧 Начать полив",
        'btn_irr_history':  "📋 История полива",
        'btn_irr_rec':      "▶ {dur} мин. (рекомендация)",
        'btn_irr_stop':     "⏹ Остановить",
        'btn_irr_other':    "💧 Другая ферма",
        'btn_specialist':   "👨‍🔬 Специалист",
        'btn_upgrade':      "⬆ Повысить пакет",
        'btn_premium':      "🏆 Перейти на Премиум",
        'btn_pay_confirm':  "✅ Подтвердить оплату",
        'btn_other_pkg':    "⬅ Другой пакет",
        'btn_ack':          "✅ Проверено",

        'pkg_detail': (
            "{emoji} <b>Пакет {package}</b>\n"
            "💰 <b>{price:,} сум/мес</b> | {days} дн.\n\n"
            "<b>Включённые функции:</b>\n{features}\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "Подтвердите оплату в демо-режиме:"
        ),
        'pkgs_header':      "📦 <b>Пакеты подписки</b>\n\n",

        'auto_irr_start': (
            "🤖 <b>АВТОПОЛИВ НАЧАТ</b>\n\n"
            "🌾 {farm}\n"
            "🌱 Влажность почвы: <b>{soil}%</b> (критично — ниже {threshold}%)\n"
            "⏱ Длительность: <b>{dur} минут</b>\n"
            "💦 Расход воды: <b>{water} л</b>\n"
            "🎯 Целевая влажность: <b>{target}%</b>\n\n"
            "⏰ Остановится через {dur} минут."
        ),
        'auto_irr_stop': (
            "✅ <b>АВТОПОЛИВ ЗАВЕРШЁН</b>\n\n"
            "🌾 {farm}\n"
            "⏱ Длительность: <b>{dur} минут</b>\n"
            "🌱 Влажность почвы: {soil_before}% → <b>{soil_after}%</b>\n"
            "🕐 {time}\n\n"
            "🟢 Система вернулась в нормальный режим."
        ),

        'hourly_report':    "⏰ <b>ЕЖЕЧАСНЫЙ ОТЧЁТ</b>\n🕐 {time}\n{status}\n━━━━━━━━━━━━━━━━━━\n\n",
        'critical_alert': (
            "🚨 <b>КРИТИЧЕСКОЕ ОПОВЕЩЕНИЕ!</b>\n━━━━━━━━━━━━━━━━━━\n"
            "🌾 <b>{farm}</b>\n⏱ {time}\n\n"
            "🌡{temp}C  💧{humid}%  🌱{soil}%  🔋{battery}%\n\n"
            "📋 <b>Срочно:</b>\n{tips}"
        ),

        'buf_header':       "🔔 <b>{count} новых уведомлений</b>\n⏰ {time}",
        'buf_footer':       "📌 <i>Это сообщение сохраняется как журнал</i>",
        'ack_done':         "✅ Отмечено!",
        'ack_text':         "✅ <b>Проверено</b> — {name}\n🕐 {time}",

        'web_irr_start': (
            "💧 <b>ВЕБ-ПАНЕЛЬ: ПОЛИВ НАЧАТ!</b>\n\n"
            "🌾 Датчик/Ферма: <b>{farm}</b>\n"
            "🌱 Влажность почвы: <b>{soil}%</b>\n"
            "⏱ Длительность: <b>{dur} минут</b>\n"
            "💦 Расход воды: ~<b>{water:.0f} л</b>\n"
            "🖥 Источник: Веб-панель\n"
            "🕐 {time}\n\n"
            "Система капельного орошения запущена."
        ),
        'web_irr_stop': (
            "🏁 <b>ВЕБ-ПАНЕЛЬ: ПОЛИВ ЗАВЕРШЁН!</b>\n\n"
            "🌾 Датчик/Ферма: <b>{farm}</b>\n"
            "🌱 Новая влажность: <b>{soil}%</b>\n"
            "🕐 {time}\n\n"
            "🟢 Система вернулась в нормальный режим."
        ),
    },

    # ════════════════════════════════════════════════════
    # ENGLISH
    # ════════════════════════════════════════════════════
    'en': {

        'welcome_new': (
            "👋 Hello, <b>{name}</b>!\n\n"
            "🌿 <b>TomchiTech</b> — Smart Farm Monitoring System\n\n"
            "Select a subscription package to get started:"
        ),
        'welcome_back': (
            "👋 Welcome back, <b>{name}</b>!\n\n"
            "📦 Your plan: {emoji} <b>{package}</b>\n"
            "📅 Valid until {end_date}\n\n"
            "⌨️ Tap the keyboard icon in the input field to open the button panel."
        ),

        'sub_required':     "❌ A subscription is required to use this feature.",
        'sub_activated':    "🎉 <b>Congratulations!</b>\n\n{emoji} <b>{package}</b> plan activated!\n📅 Until {end_date}\n\nYou can now use TomchiTech services!",
        'keyboard_ready':   "⌨️ Button panel ready! Tap the keyboard icon at the bottom.",
        'main_menu':        "🏠 <b>Main Menu</b>\n{emoji} {package} | Until {end_date}\n\nSelect a section:",

        'loading':          "⏳ Loading...",
        'report_header':    "📊 <b>FARM REPORT</b>\n🕐 {time}\n{status}\n━━━━━━━━━━━━━━━━━━\n\n",
        'status_critical':  "🔴 ATTENTION: Critical conditions!",
        'status_ok':        "🟢 Overall status: Good",

        'farms_header':     "🌾 <b>YOUR FARMS ({count})</b>\n\n",
        'sensor_header':    "📡 <b>SENSOR DATA</b>\n\n",

        'irr_control':      "💧 <b>IRRIGATION CONTROL</b>\n\nWhich farm do you want to irrigate?\n\n",
        'irr_premium_only': "❌ This feature is only available in Standard and Premium plans.",
        'irr_detail': (
            "💧 <b>IRRIGATION — {farm}</b>\n\n"
            "📊 <b>Current status:</b>\n"
            "🌱 Soil moisture: <b>{soil}%</b>\n"
            "🌡 Temperature: <b>{temp}C</b>\n"
            "📐 Area: <b>{area} ha</b>\n\n"
            "🤖 <b>System recommendation:</b>\n"
            "⏱ Duration: <b>{dur} minutes</b>\n"
            "💦 Water usage: <b>{water} L</b>\n"
            "🎯 Target moisture: <b>{target}%</b>\n\n"
            "Drip irrigation system is ready."
        ),
        'irr_started': (
            "✅ <b>IRRIGATION STARTED!</b>\n\n"
            "🌾 Farm: <b>{farm}</b>\n"
            "⏱ Duration: <b>{dur} minutes</b>\n"
            "💦 Water usage: <b>{water} L</b>\n\n"
            "📊 <b>Forecast:</b>\n"
            "🌱 Soil moisture: {soil_before}% → <b>{soil_after}%</b>\n\n"
            "Drip irrigation system started.\n"
            "⏰ Will auto-stop in {dur} minutes."
        ),
        'irr_stopped':      "⏹ <b>IRRIGATION STOPPED</b>\n\n🌾 {farm}\n✅ System shut down.",
        'irr_history_empty':"📋 <b>Irrigation history is empty.</b>\n\nNo irrigation has been performed yet.",
        'irr_history_hdr':  "📋 <b>RECENT IRRIGATIONS</b>\n━━━━━━━━━━━━━━━━━━\n\n",

        'alerts_critical':  "🚨 <b>CRITICAL ALERTS</b>\n⏱ {time}\n━━━━━━━━━━━━━━━━━━\n\n",
        'alerts_warning':   "🟡 <b>WARNINGS</b>\n━━━━━━━━━━━━━━━━━━\n\n",
        'alerts_none':      "✅ <b>No active alerts.</b>\n\nAll farms are normal. 🌿",

        'spec_premium_only': (
            "👨‍🔬 <b>Call a Specialist</b>\n\n"
            "❌ This feature is only for <b>Premium</b> plan.\n\n"
            "Upgrade your subscription to Premium:"
        ),
        'spec_header':      "👨‍🔬 <b>SPECIALISTS</b>\nContact them in critical situations:\n━━━━━━━━━━━━━━━━━━\n\n",
        'spec_hours':       "⏰ Working hours: Mon-Fri 08:00-18:00\n🆘 Emergency: 24/7",

        'sub_info': (
            "📦 <b>SUBSCRIPTION INFO</b>\n━━━━━━━━━━━━━━━━━━\n\n"
            "{emoji} Plan: <b>{package}</b>\n"
            "💰 {price:,} UZS/mo\n"
            "📅 Expires: {end_date}\n"
            "🕐 Remaining: <b>{days} days</b>\n\n"
            "<b>Features:</b>\n{features}"
        ),

        'help_text': (
            "ℹ <b>HELP</b>\n\n"
            "📊 Report — sensor data report\n"
            "🌾 Farms — individual farm sensor\n"
            "💧 Irrigation — drip irrigation control\n"
            "🚨 Alerts — critical/warning conditions\n"
            "👨‍🔬 Specialist — for Premium users\n"
            "🌐 Language — change interface language\n\n"
            "Critical thresholds:\n"
            "• Temperature > {temp_max}C\n"
            "• Humidity < {humid_min}%\n"
            "• Soil moisture < {soil_min}%\n\n"
            "🔔 Automatic report every hour\n\n"
            "📞 support@tomchitech.uz"
        ),

        'lang_choose':      "🌐 Til tanlang / Выберите язык / Choose language:",
        'lang_changed_uz':  "✅ O'zbek tili tanlandi! 🇺🇿\n\nThe system is now in Uzbek.",
        'lang_changed_ru':  "✅ Русский язык выбран! 🇷🇺\n\nThe system is now in Russian.",
        'lang_changed_en':  "✅ English selected! 🇬🇧\n\nThe system is now in English.",

        'btn_back_menu':    "⬅ Main Menu",
        'btn_back_farms':   "⬅ Farms",
        'btn_back_irr':     "⬅ Irrigation",
        'btn_refresh':      "🔄 Refresh",
        'btn_irr_start':    "💧 Start Irrigation",
        'btn_irr_history':  "📋 Irrigation History",
        'btn_irr_rec':      "▶ {dur} min (recommended)",
        'btn_irr_stop':     "⏹ Stop",
        'btn_irr_other':    "💧 Other Farm",
        'btn_specialist':   "👨‍🔬 Specialist",
        'btn_upgrade':      "⬆ Upgrade Plan",
        'btn_premium':      "🏆 Switch to Premium",
        'btn_pay_confirm':  "✅ Confirm Payment",
        'btn_other_pkg':    "⬅ Other Package",
        'btn_ack':          "✅ Acknowledged",

        'pkg_detail': (
            "{emoji} <b>{package} Plan</b>\n"
            "💰 <b>{price:,} UZS/mo</b> | {days} days\n\n"
            "<b>Included features:</b>\n{features}\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "Confirm payment in demo mode:"
        ),
        'pkgs_header':      "📦 <b>Subscription Plans</b>\n\n",

        'auto_irr_start': (
            "🤖 <b>AUTO-IRRIGATION STARTED</b>\n\n"
            "🌾 {farm}\n"
            "🌱 Soil moisture: <b>{soil}%</b> (critical — below {threshold}%)\n"
            "⏱ Duration: <b>{dur} minutes</b>\n"
            "💦 Water usage: <b>{water} L</b>\n"
            "🎯 Target moisture: <b>{target}%</b>\n\n"
            "⏰ Will stop in {dur} minutes."
        ),
        'auto_irr_stop': (
            "✅ <b>AUTO-IRRIGATION COMPLETE</b>\n\n"
            "🌾 {farm}\n"
            "⏱ Duration: <b>{dur} minutes</b>\n"
            "🌱 Soil moisture: {soil_before}% → <b>{soil_after}%</b>\n"
            "🕐 {time}\n\n"
            "🟢 System returned to normal mode."
        ),

        'hourly_report':    "⏰ <b>HOURLY REPORT</b>\n🕐 {time}\n{status}\n━━━━━━━━━━━━━━━━━━\n\n",
        'critical_alert': (
            "🚨 <b>CRITICAL ALERT!</b>\n━━━━━━━━━━━━━━━━━━\n"
            "🌾 <b>{farm}</b>\n⏱ {time}\n\n"
            "🌡{temp}C  💧{humid}%  🌱{soil}%  🔋{battery}%\n\n"
            "📋 <b>Urgent:</b>\n{tips}"
        ),

        'buf_header':       "🔔 <b>{count} new notifications</b>\n⏰ {time}",
        'buf_footer':       "📌 <i>This message is saved as a log</i>",
        'ack_done':         "✅ Acknowledged!",
        'ack_text':         "✅ <b>Acknowledged</b> — {name}\n🕐 {time}",

        'web_irr_start': (
            "💧 <b>WEB DASHBOARD: IRRIGATION STARTED!</b>\n\n"
            "🌾 Sensor/Farm: <b>{farm}</b>\n"
            "🌱 Soil moisture: <b>{soil}%</b>\n"
            "⏱ Duration: <b>{dur} minutes</b>\n"
            "💦 Water usage: ~<b>{water:.0f} L</b>\n"
            "🖥 Source: Web dashboard\n"
            "🕐 {time}\n\n"
            "Drip irrigation system started."
        ),
        'web_irr_stop': (
            "🏁 <b>WEB DASHBOARD: IRRIGATION COMPLETE!</b>\n\n"
            "🌾 Sensor/Farm: <b>{farm}</b>\n"
            "🌱 New moisture: <b>{soil}%</b>\n"
            "🕐 {time}\n\n"
            "🟢 System returned to normal mode."
        ),
    },
}


def tr(key: str, lang: str = 'uz', **kwargs) -> str:
    """
    Kalit so'z bo'yicha tarjima qaytaradi.
    Agar berilgan tilda topilmasa — o'zbek tiliga qaytadi.
    Agar o'zbek tilida ham yo'q bo'lsa — kalit so'zning o'zi qaytariladi.

    Misol:
        tr('welcome_new', 'ru', name="Ivan")
        tr('help_text', lang, temp_max=35, humid_min=20, soil_min=15)
    """
    lang = lang if lang in STRINGS else 'uz'
    text = STRINGS[lang].get(key) or STRINGS['uz'].get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, ValueError):
            return text
    return text


# Shortcut: language labels for buttons
LANG_LABELS = {
    'uz': "🇺🇿 O'zbek",
    'ru': "🇷🇺 Русский",
    'en': "🇬🇧 English",
}

LANG_CHANGED_KEY = {
    'uz': 'lang_changed_uz',
    'ru': 'lang_changed_ru',
    'en': 'lang_changed_en',
}
