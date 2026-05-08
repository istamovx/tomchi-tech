"""
TomchiTech Farm Monitoring Telegram Bot
Render.com uchun webhook rejimi | Barcha navigatsiya inline tugmalar orqali
"""

import os
import random
import logging
import httpx
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────
BOT_TOKEN   = os.environ.get("BOT_TOKEN", "8655345849:AAGzYvepKRkyZPo7hw5_a0LFU8NMeSV3kH4")
PORT        = int(os.environ.get("PORT", 8443))
# Render.com RENDER_EXTERNAL_URL ni avtomatik belgilaydi
WEBHOOK_URL = os.environ.get("WEBHOOK_URL") or os.environ.get("RENDER_EXTERNAL_URL", "")

ALERT_TEMP_MAX  = 35.0
ALERT_HUMID_MIN = 20.0
ALERT_SOIL_MIN  = 15.0
ALERT_LIGHT_MAX = 95000

# ── Demo ma'lumotlar ──────────────────────────────────────────────────────────
FARMS = {
    "f1": {"nomi": "Yangi Hayot fermasi",   "joy": "Toshkent viloyati, Zangiota"},
    "f2": {"nomi": "Barakali Dala fermasi",  "joy": "Samarqand viloyati, Urgut"},
    "f3": {"nomi": "Yashil Bog' fermasi",    "joy": "Farg'ona viloyati, Quva"},
}

EKINLAR = {
    "f1": ["Bug'doy", "Makkajo'xori"],
    "f2": ["Paxta", "Sholi"],
    "f3": ["Sabzavot", "Poliz ekinlari"],
}

MUTAXASSISLAR = [
    {"ism": "Alisher Karimov",   "lavozim": "Agrotexnolog",               "tel": "+998 90 123-45-67", "email": "a.karimov@tomchitech.uz",   "soha": "Bug'doy, don ekinlari"},
    {"ism": "Dilnoza Yusupova",  "lavozim": "Fitosanitariya mutaxassisi", "tel": "+998 91 234-56-78", "email": "d.yusupova@tomchitech.uz",  "soha": "O'simlik kasalliklari"},
    {"ism": "Bobur Toshmatov",   "lavozim": "Suv resurslari muhandisi",   "tel": "+998 93 345-67-89", "email": "b.toshmatov@tomchitech.uz", "soha": "Sug'orish tizimlari"},
    {"ism": "Sarvar Mirzayev",   "lavozim": "Agronomist",                 "tel": "+998 94 456-78-90", "email": "s.mirzayev@tomchitech.uz",  "soha": "Tuproq holati, o'g'it"},
    {"ism": "Gulnora Rashidova", "lavozim": "Meteorolog-agrar",           "tel": "+998 97 567-89-01", "email": "g.rashidova@tomchitech.uz", "soha": "Ob-havo, qurg'oqchilik"},
]

# ── Sensor simulyatsiyasi ─────────────────────────────────────────────────────
def sensor(farm_id: str) -> dict:
    kritik = random.random() < 0.08
    if kritik:
        temp    = round(random.uniform(36.0, 42.0), 1)
        humid   = round(random.uniform(8.0,  18.0), 1)
        soil    = round(random.uniform(5.0,  14.0), 1)
        light   = random.randint(96000, 105000)
        battery = random.randint(5, 15)
    else:
        temp    = round(random.uniform(18.0, 34.0), 1)
        humid   = round(random.uniform(22.0, 75.0), 1)
        soil    = round(random.uniform(20.0, 65.0), 1)
        light   = random.randint(10000, 90000)
        battery = random.randint(30, 100)
    return {
        "farm_id": farm_id, "temp": temp, "humid": humid,
        "soil": soil, "light": light, "battery": battery,
        "vaqt": datetime.now().strftime("%d.%m.%Y %H:%M"),
    }

def holat(d: dict) -> str:
    if (d["temp"] > ALERT_TEMP_MAX or d["humid"] < ALERT_HUMID_MIN or
            d["soil"] < ALERT_SOIL_MIN or d["light"] > ALERT_LIGHT_MAX or
            d["battery"] < 20):
        return "🔴 KRITIK"
    if d["temp"] > 30 or d["humid"] < 35 or d["soil"] < 30 or d["battery"] < 40:
        return "🟡 EHTIYOT"
    return "🟢 NORMAL"

def tavsiyalar(d: dict) -> list[str]:
    t = []
    if d["temp"] > ALERT_TEMP_MAX:
        t.append("🌡️ Harorat kritik! Darhol soyabonlash/sovutish kerak.")
    elif d["temp"] > 30:
        t.append("🌡️ Harorat yuqori. Sug'orish rejimini kuchaytiring.")
    if d["humid"] < ALERT_HUMID_MIN:
        t.append("💧 Nam juda past! Zudlik bilan sug'orish kerak.")
    elif d["humid"] < 35:
        t.append("💧 Nam pasaymoqda. Sug'orish jadvalini tezlashtiring.")
    if d["soil"] < ALERT_SOIL_MIN:
        t.append("🌱 Tuproq namligi kritik! Tomchilatib sug'orish tizimini to'liq oching.")
    elif d["soil"] < 30:
        t.append("🌱 Tuproq qurib qolmoqda. Sug'orish miqdorini oshiring.")
    if d["light"] > ALERT_LIGHT_MAX:
        t.append("☀️ Yorug'lik haddan tashqari kuchli. To'r yoki soya tavsiya etiladi.")
    if d["battery"] < 20:
        t.append("🔋 Sensor batareyasi kritik past! Zaryad ulang.")
    elif d["battery"] < 40:
        t.append("🔋 Sensor zaryadlanishi kerak.")
    return t or ["✅ Barcha ko'rsatkichlar me'yorida. Hozirgi rejimni davom ettiring."]

# ── Formatlash ────────────────────────────────────────────────────────────────
def ferma_blok(fid: str, d: dict) -> str:
    f    = FARMS[fid]
    ekin = ", ".join(EKINLAR[fid])
    h    = holat(d)
    tips = "\n".join(f"  • {x}" for x in tavsiyalar(d))
    return (
        f"<b>🌾 {f['nomi']}</b>\n"
        f"📍 {f['joy']} | 🌱 {ekin}\n"
        f"─────────────────\n"
        f"🌡️ Harorat:         <b>{d['temp']}°C</b>\n"
        f"💧 Namlik:          <b>{d['humid']}%</b>\n"
        f"🌱 Tuproq namligi:  <b>{d['soil']}%</b>\n"
        f"☀️ Yorug'lik:       <b>{d['light']:,} lux</b>\n"
        f"🔋 Sensor zaryadi:  <b>{d['battery']}%</b>\n"
        f"⏱ {d['vaqt']}\n"
        f"─────────────────\n"
        f"Holat: {h}\n"
        f"📋 <b>Tavsiya:</b>\n{tips}"
    )

# ── Klaviaturalar ─────────────────────────────────────────────────────────────
def main_menu_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Hisobot",           callback_data="hisobot"),
         InlineKeyboardButton("🌾 Fermalar",           callback_data="fermalar")],
        [InlineKeyboardButton("🚨 Ogohlantirishlar",  callback_data="ogohlar"),
         InlineKeyboardButton("👨‍🔬 Mutaxassislar",    callback_data="mutax")],
        [InlineKeyboardButton("ℹ️ Yordam",             callback_data="yordam")],
    ])

def back_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Asosiy menyu", callback_data="menu")]
    ])

def farm_list_kb():
    rows = []
    for fid, f in FARMS.items():
        rows.append([InlineKeyboardButton(f"🌾 {f['nomi']}", callback_data=f"farm_{fid}")])
    rows.append([InlineKeyboardButton("⬅️ Asosiy menyu", callback_data="menu")])
    return InlineKeyboardMarkup(rows)

# ── Xabar yuborish ────────────────────────────────────────────────────────────
async def send(context, chat_id, text, kb=None, **kw):
    try:
        await context.bot.send_message(
            chat_id=chat_id, text=text, parse_mode="HTML",
            reply_markup=kb, **kw
        )
    except Exception as e:
        logger.error("send error %s: %s", chat_id, e)

# ── /start ────────────────────────────────────────────────────────────────────
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.bot_data.setdefault("subscribers", set()).add(update.effective_chat.id)
    user = update.effective_user
    matn = (
        f"👋 Salom, <b>{user.first_name}</b>!\n\n"
        "🌿 <b>TomchiTech</b> ferma monitoring botiga xush kelibsiz!\n\n"
        "Sensor ma'lumotlarini real vaqtda kuzatamiz, kritik holatlarda "
        "<b>darhol</b> xabardor qilamiz.\n\n"
        "⏰ Har soatda avtomatik hisobot\n"
        "🔴 Kritik holat — zudlik bilan ogohlantirish\n\n"
        "Quyidagi tugmalardan birini tanlang:"
    )
    await update.message.reply_text(matn, parse_mode="HTML", reply_markup=main_menu_kb())

# ── Callback handler ──────────────────────────────────────────────────────────
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q    = update.callback_query
    data = q.data
    cid  = q.message.chat_id
    await q.answer()

    # ── Asosiy menyu ──
    if data == "menu":
        await q.message.edit_text(
            "🏠 <b>Asosiy menyu</b>\n\nQuyidagi tugmalardan birini tanlang:",
            parse_mode="HTML", reply_markup=main_menu_kb()
        )
        return

    # ── Hisobot ──
    if data == "hisobot":
        await q.message.edit_text("⏳ Ma'lumotlar yuklanmoqda...", parse_mode="HTML")
        bloklar = []
        kritik_son = 0
        for fid in FARMS:
            d = sensor(fid)
            bloklar.append(ferma_blok(fid, d))
            if holat(d).startswith("🔴"):
                kritik_son += 1
        umumiy = "🔴 DIQQAT: Kritik holatlar mavjud!" if kritik_son else "🟢 Umumiy holat: Yaxshi"
        header = (
            f"📊 <b>FERMA HISOBOTI</b>\n"
            f"🕐 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
            f"{umumiy}\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
        )
        full = header + "\n\n━━━━━━━━━━━━━━━━━━\n\n".join(bloklar)
        # Birinchi qism mavjud xabarga edit qilinadi
        await q.message.edit_text(full[:4096], parse_mode="HTML", reply_markup=back_kb())
        # Qolgan qismlar yangi xabar sifatida yuboriladi
        for chunk_start in range(4096, len(full), 4096):
            await send(context, cid, full[chunk_start:chunk_start+4096], kb=back_kb())
        return

    # ── Fermalar ro'yxati ──
    if data == "fermalar":
        matn = "🌾 <b>FERMALAR RO'YXATI</b>\n\nQaysi ferma ma'lumotlarini ko'rmoqchisiz?\n\n"
        for fid, f in FARMS.items():
            ekin = ", ".join(EKINLAR[fid])
            matn += f"<b>{f['nomi']}</b>\n📍 {f['joy']}\n🌱 {ekin}\n\n"
        await q.message.edit_text(matn, parse_mode="HTML", reply_markup=farm_list_kb())
        return

    # ── Bitta ferma sensori ──
    if data.startswith("farm_"):
        fid = data.split("_", 1)[1]
        d   = sensor(fid)
        blok = ferma_blok(fid, d)
        matn = f"📡 <b>SENSOR MA'LUMOTLARI</b>\n\n{blok}"
        await q.message.edit_text(matn, parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Yangilash",       callback_data=f"farm_{fid}"),
                 InlineKeyboardButton("⬅️ Fermalar",        callback_data="fermalar")],
                [InlineKeyboardButton("⬅️ Asosiy menyu",   callback_data="menu")],
            ])
        )
        return

    # ── Ogohlantirishlar ──
    if data == "ogohlar":
        kritiklar = []
        ehtiyotlar = []
        for fid in FARMS:
            d = sensor(fid)
            h = holat(d)
            if h.startswith("🔴"):
                kritiklar.append(ferma_blok(fid, d))
            elif h.startswith("🟡"):
                ehtiyotlar.append(ferma_blok(fid, d))

        if kritiklar:
            header = (
                f"🚨 <b>KRITIK OGOHLANTIRISHLAR</b>\n"
                f"⏱ {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                f"━━━━━━━━━━━━━━━━━━\n\n"
            )
            full = header + "\n\n━━━━━━━━━━━━━━━━━━\n\n".join(kritiklar)
            await q.message.edit_text(full[:4096], parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("👨‍🔬 Mutaxassislar", callback_data="mutax")],
                    [InlineKeyboardButton("⬅️ Asosiy menyu",  callback_data="menu")],
                ])
            )
        elif ehtiyotlar:
            header = (
                f"🟡 <b>EHTIYOT HOLATLAR</b>\n"
                f"⏱ {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                f"━━━━━━━━━━━━━━━━━━\n\n"
            )
            full = header + "\n\n━━━━━━━━━━━━━━━━━━\n\n".join(ehtiyotlar)
            await q.message.edit_text(full[:4096], parse_mode="HTML", reply_markup=back_kb())
        else:
            await q.message.edit_text(
                "✅ <b>Hozirda hech qanday ogohlantirish yo'q.</b>\n\n"
                "Barcha fermalar normal ishlayapti. 🌿",
                parse_mode="HTML", reply_markup=back_kb()
            )
        return

    # ── Mutaxassislar ──
    if data == "mutax":
        matn = (
            "👨‍🔬 <b>MUTAXASSISLAR</b>\n"
            "Kritik holatlarda quyidagilar bilan bog'laning:\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
        )
        for m in MUTAXASSISLAR:
            matn += (
                f"<b>{m['ism']}</b>\n"
                f"💼 {m['lavozim']}\n"
                f"🔬 {m['soha']}\n"
                f"📞 {m['tel']}\n"
                f"📧 {m['email']}\n\n"
            )
        matn += "⏰ Ish vaqti: Du–Jum 08:00–18:00\n🆘 Favqulodda: 24/7 telefon orqali"
        await q.message.edit_text(matn[:4096], parse_mode="HTML", reply_markup=back_kb())
        return

    # ── Yordam ──
    if data == "yordam":
        matn = (
            "ℹ️ <b>YORDAM</b>\n\n"
            "📋 <b>Tugmalar:</b>\n"
            "📊 Hisobot — barcha fermalar holati\n"
            "🌾 Fermalar — alohida ferma sensori\n"
            "🚨 Ogohlantirishlar — kritik/ehtiyot holatlar\n"
            "👨‍🔬 Mutaxassislar — kontakt ma'lumotlari\n\n"
            "🔔 <b>Avtomatik bildirishnomalar:</b>\n"
            "• ⏰ Har soatda umumiy hisobot\n"
            "• 🔴 Kritik holat — darhol xabar\n\n"
            f"⚠️ <b>Kritik chegara:</b>\n"
            f"• Harorat > {ALERT_TEMP_MAX}°C\n"
            f"• Namlik < {ALERT_HUMID_MIN}%\n"
            f"• Tuproq namligi < {ALERT_SOIL_MIN}%\n"
            f"• Yorug'lik > {ALERT_LIGHT_MAX:,} lux\n\n"
            "📞 Texnik yordam: support@tomchitech.uz"
        )
        await q.message.edit_text(matn, parse_mode="HTML", reply_markup=back_kb())
        return

# ── Soatlik avtomatik hisobot ─────────────────────────────────────────────────
async def soatlik_hisobot(context: ContextTypes.DEFAULT_TYPE):
    subscribers = context.bot_data.get("subscribers", set())
    if not subscribers:
        return
    bloklar    = []
    kritik_son = 0
    for fid in FARMS:
        d = sensor(fid)
        bloklar.append(ferma_blok(fid, d))
        if holat(d).startswith("🔴"):
            kritik_son += 1
    umumiy = "🔴 DIQQAT: Kritik holatlar mavjud!" if kritik_son else "🟢 Umumiy holat: Yaxshi"
    matn   = (
        f"⏰ <b>SOATLIK HISOBOT</b>\n"
        f"🕐 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
        f"{umumiy}\n━━━━━━━━━━━━━━━━━━\n\n"
        + "\n\n━━━━━━━━━━━━━━━━━━\n\n".join(bloklar)
    )
    for cid in list(subscribers):
        for i in range(0, len(matn), 4096):
            await send(context, cid, matn[i:i+4096])
    logger.info("Soatlik hisobot %d obunachiga yuborildi.", len(subscribers))

# ── Kritik holat monitoring (5 daqiqada) ──────────────────────────────────────
async def kritik_tekshiruv(context: ContextTypes.DEFAULT_TYPE):
    subscribers = context.bot_data.get("subscribers", set())
    if not subscribers:
        return
    for fid in FARMS:
        d = sensor(fid)
        if not holat(d).startswith("🔴"):
            continue
        tips = "\n".join(f"• {x}" for x in tavsiyalar(d))
        # Mutaxassis tavsiyasi
        mutax = []
        if d["temp"] > ALERT_TEMP_MAX:
            mutax.append("Gulnora Rashidova — +998 97 567-89-01")
        if d["humid"] < ALERT_HUMID_MIN or d["soil"] < ALERT_SOIL_MIN:
            mutax.append("Bobur Toshmatov — +998 93 345-67-89")
        m_text = ("\n\n👨‍🔬 <b>Darhol bog'laning:</b>\n" + "\n".join(f"• {m}" for m in mutax)) if mutax else ""
        matn = (
            f"🚨 <b>KRITIK OGOHLANTIRISH!</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🌾 <b>{FARMS[fid]['nomi']}</b>\n"
            f"⏱ {d['vaqt']}\n\n"
            f"🌡️ Harorat: <b>{d['temp']}°C</b>\n"
            f"💧 Namlik: <b>{d['humid']}%</b>\n"
            f"🌱 Tuproq: <b>{d['soil']}%</b>\n"
            f"🔋 Zaryad: <b>{d['battery']}%</b>\n\n"
            f"📋 <b>Zudlik bilan:</b>\n{tips}{m_text}"
        )
        for cid in list(subscribers):
            await send(context, cid, matn)

# ── Render.com free tier uchun keep-alive ─────────────────────────────────────
async def keep_alive(context: ContextTypes.DEFAULT_TYPE):
    if WEBHOOK_URL:
        try:
            async with httpx.AsyncClient() as client:
                await client.get(f"{WEBHOOK_URL}/healthz", timeout=10)
            logger.info("Keep-alive ping yuborildi.")
        except Exception as e:
            logger.debug("Keep-alive xato (normal): %s", e)

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CallbackQueryHandler(callback_handler))

    jq = app.job_queue
    jq.run_repeating(soatlik_hisobot,  interval=3600, first=60)
    jq.run_repeating(kritik_tekshiruv, interval=300,  first=30)
    jq.run_repeating(keep_alive,       interval=840,  first=120)  # 14 daqiqada bir

    if WEBHOOK_URL:
        logger.info("Webhook rejimida ishga tushmoqda: %s", WEBHOOK_URL)
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}",
            secret_token="tomchitech-2025",
            url_path=BOT_TOKEN,
        )
    else:
        logger.info("Polling rejimida ishga tushmoqda (lokal test)...")
        app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
