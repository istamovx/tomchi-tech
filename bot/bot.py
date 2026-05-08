"""TomchiTech Farm Monitoring Bot v2 - Obuna + Sughorish + Ko'p tilli"""
import os, sys, random, logging, sqlite3, threading, httpx, json, asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler

# ── Locale import (bot/ papkasi ichida ishlaydi) ─────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
try:
    import importlib as _il
    _lmod = _il.import_module('locale')
    tr = _lmod.tr
    LANG_LABELS    = _lmod.LANG_LABELS
    LANG_CHANGED_KEY = _lmod.LANG_CHANGED_KEY
except Exception:
    def tr(key, lang='uz', **kw): return key   # fallback — no translation
    LANG_LABELS      = {'uz': "🇺🇿 O'zbek", 'ru': "🇷🇺 Русский", 'en': "🇬🇧 English"}
    LANG_CHANGED_KEY = {'uz': 'lang_changed_uz', 'ru': 'lang_changed_ru', 'en': 'lang_changed_en'}
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN     = os.environ.get("BOT_TOKEN", "8655345849:AAGzYvepKRkyZPo7hw5_a0LFU8NMeSV3kH4")
PORT          = int(os.environ.get("PORT", 8443))
API_PORT      = int(os.environ.get("API_PORT", 8080))
WEBHOOK_URL   = os.environ.get("WEBHOOK_URL") or os.environ.get("RENDER_EXTERNAL_URL", "")
ADMIN_IDS     = set(int(x) for x in os.environ.get("ADMIN_IDS","").split(",") if x.strip().isdigit())
NOTIFY_SECRET = os.environ.get("NOTIFY_SECRET", "tomchitech-irr-2025")
DB_PATH       = "tomchitech.db"
DB_LOCK       = threading.Lock()

ALERT_TEMP_MAX   = 35.0
ALERT_HUMID_MIN  = 20.0
ALERT_SOIL_MIN   = 15.0
ALERT_SOIL_IRRIG = 30.0

PACKAGES = {
    "asosiy": {
        "emoji":"🌱","nomi":"Asosiy","narx":99_000,"muddat":30,
        "max_ferma":1,"sugorish":False,"mutaxassis":False,
        "funksiyalar":["1 ta ferma monitoringi","Sensor malumotlari","Kunlik hisobot","Telegram bot"],
    },
    "standart": {
        "emoji":"🌿","nomi":"Standart","narx":249_000,"muddat":30,
        "max_ferma":3,"sugorish":"manual","mutaxassis":False,
        "funksiyalar":["3 ta ferma monitoringi","Soatlik avtomatik hisobot","Telegram bot","Manual sughorish boshqaruvi","Kritik ogohlantirishlar"],
    },
    "premium": {
        "emoji":"🏆","nomi":"Premium","narx":499_000,"muddat":30,
        "max_ferma":999,"sugorish":"auto","mutaxassis":True,
        "funksiyalar":["Cheksiz ferma monitoringi","Soatlik hisobot + Kritik alertlar","Telegram bot","Avto + Manual sughorish","Mutaxassis chaqirish","Prioritet support"],
    },
}

FARMS = {
    "f1":{"nomi":"Yangi Hayot fermasi","joy":"Toshkent viloyati, Zangiota","ekin":["Bugdoy","Makkajoxori"],"area":5.2},
    "f2":{"nomi":"Barakali Dala fermasi","joy":"Samarqand viloyati, Urgut","ekin":["Paxta","Sholi"],"area":8.7},
    "f3":{"nomi":"Yashil Bog fermasi","joy":"Fargona viloyati, Quva","ekin":["Sabzavot","Poliz"],"area":3.1},
}

MUTAXASSISLAR = [
    {"ism":"Alisher Karimov","lavozim":"Agrotexnolog","tel":"+998 90 123-45-67","soha":"Bugdoy, don ekinlari"},
    {"ism":"Dilnoza Yusupova","lavozim":"Fitosanitariya mutaxassisi","tel":"+998 91 234-56-78","soha":"Osimlik kasalliklari"},
    {"ism":"Bobur Toshmatov","lavozim":"Suv resurslari muhandisi","tel":"+998 93 345-67-89","soha":"Sughorish tizimlari"},
    {"ism":"Sarvar Mirzayev","lavozim":"Agronomist","tel":"+998 94 456-78-90","soha":"Tuproq holati"},
    {"ism":"Gulnora Rashidova","lavozim":"Meteorolog-agrar","tel":"+998 97 567-89-01","soha":"Ob-havo, qurghoqchilik"},
]

# ── Database ──────────────────────────────────────────────────────────────────
def db():
    c = sqlite3.connect(DB_PATH, check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    with DB_LOCK:
        c = db()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY, username TEXT, full_name TEXT,
                joined_at TEXT DEFAULT (datetime('now')),
                user_lang TEXT DEFAULT 'uz');
            CREATE TABLE IF NOT EXISTS subscriptions (
                user_id INTEGER PRIMARY KEY, package TEXT,
                start_date TEXT, end_date TEXT, status TEXT DEFAULT 'active');
            CREATE TABLE IF NOT EXISTS irrigation_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,
                farm_id TEXT, farm_name TEXT, logged_at TEXT DEFAULT (datetime('now')),
                duration_min INTEGER, trigger_type TEXT, soil_before REAL, water_liters REAL);
        """)
        # Migrate: user_lang column qo'shimcha (eski DB uchun)
        try:
            c.execute("ALTER TABLE users ADD COLUMN user_lang TEXT DEFAULT 'uz'")
            c.commit()
        except Exception:
            pass  # already exists
        c.close()

def save_user(uid, username, full_name):
    with DB_LOCK:
        c = db()
        c.execute("INSERT OR IGNORE INTO users (user_id,username,full_name) VALUES (?,?,?)",
                  (uid, username or "", full_name or ""))
        c.commit(); c.close()

def get_sub(uid):
    with DB_LOCK:
        c   = db()
        row = c.execute("SELECT * FROM subscriptions WHERE user_id=? AND status='active'",(uid,)).fetchone()
        c.close()
    if not row: return None
    sub = dict(row)
    if sub["end_date"] < datetime.now().strftime("%Y-%m-%d %H:%M:%S"):
        with DB_LOCK:
            c = db(); c.execute("UPDATE subscriptions SET status='expired' WHERE user_id=?",(uid,)); c.commit(); c.close()
        return None
    return sub

def activate_sub(uid, package):
    start = datetime.now()
    end   = start + timedelta(days=PACKAGES[package]["muddat"])
    with DB_LOCK:
        c = db()
        c.execute("""INSERT INTO subscriptions (user_id,package,start_date,end_date,status)
                     VALUES (?,?,?,?,'active')
                     ON CONFLICT(user_id) DO UPDATE SET
                     package=excluded.package,start_date=excluded.start_date,
                     end_date=excluded.end_date,status='active'""",
                  (uid, package, start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S")))
        c.commit(); c.close()

def log_irr(uid, fid, fname, dur, trigger, soil, water):
    with DB_LOCK:
        c = db()
        c.execute("INSERT INTO irrigation_logs (user_id,farm_id,farm_name,duration_min,trigger_type,soil_before,water_liters) VALUES (?,?,?,?,?,?,?)",
                  (uid,fid,fname,dur,trigger,soil,water))
        c.commit(); c.close()

def all_users():
    with DB_LOCK:
        c    = db()
        rows = c.execute("""SELECT u.user_id,u.full_name,u.username,s.package,s.end_date,s.status
                            FROM users u LEFT JOIN subscriptions s ON u.user_id=s.user_id""").fetchall()
        c.close()
    return [dict(r) for r in rows]

def get_user_lang(uid: int) -> str:
    with DB_LOCK:
        c   = db()
        row = c.execute("SELECT user_lang FROM users WHERE user_id=?", (uid,)).fetchone()
        c.close()
    return (row["user_lang"] if row and row["user_lang"] else None) or 'uz'

def set_user_lang(uid: int, lang: str):
    if lang not in ('uz', 'ru', 'en'):
        lang = 'uz'
    with DB_LOCK:
        c = db()
        c.execute("UPDATE users SET user_lang=? WHERE user_id=?", (lang, uid))
        c.commit(); c.close()

# ── Sensor + Sughorish ────────────────────────────────────────────────────────
def sensor(fid):
    k = random.random() < 0.08
    return {
        "farm_id":fid,
        "temp":   round(random.uniform(36,42) if k else random.uniform(18,34),1),
        "humid":  round(random.uniform(8,18)  if k else random.uniform(22,75),1),
        "soil":   round(random.uniform(5,14)  if k else random.uniform(20,65),1),
        "light":  random.randint(96000,105000) if k else random.randint(10000,90000),
        "battery":random.randint(5,15) if k else random.randint(30,100),
        "vaqt":   datetime.now().strftime("%d.%m.%Y %H:%M"),
    }

def holat(d):
    if d["temp"]>ALERT_TEMP_MAX or d["humid"]<ALERT_HUMID_MIN or d["soil"]<ALERT_SOIL_MIN or d["battery"]<20:
        return "🔴 KRITIK"
    if d["temp"]>30 or d["humid"]<35 or d["soil"]<30 or d["battery"]<40:
        return "🟡 EHTIYOT"
    return "🟢 NORMAL"

def tavsiyalar(d):
    t = []
    if d["temp"]>ALERT_TEMP_MAX: t.append("Harorat kritik! Darhol soyabonlash kerak.")
    elif d["temp"]>30:           t.append("Harorat yuqori. Sughorish rejimini kuchaytiring.")
    if d["humid"]<ALERT_HUMID_MIN: t.append("Nam juda past! Zudlik bilan sughorish kerak.")
    elif d["humid"]<35:            t.append("Nam pasaymoqda. Sughorish jadvalini tezlashtiring.")
    if d["soil"]<ALERT_SOIL_MIN: t.append("Tuproq namligi kritik! Tomchilatib sughorish tizimini to'liq oching.")
    elif d["soil"]<30:           t.append("Tuproq qurib qolmoqda. Sughorish miqdorini oshiring.")
    if d["battery"]<20:          t.append("Sensor batareyasi kritik past! Zaryad ulang.")
    return t or ["Barcha korsatkichlar mevorida. Hozirgi rejimni davom ettiring."]

def calc_irr(soil, temp, area):
    deficit = max(0, 60.0 - soil)
    mins    = deficit * 1.5 * area
    mins   *= (1.35 if temp>35 else 1.18 if temp>30 else 0.80 if temp<15 else 1.0)
    dur     = max(10, min(int(mins), 180))
    return {"davomiylik":dur, "suv_litr":round(dur*2*area,1), "maqsad":60}

def ferma_blok(fid, d, short=False):
    f    = FARMS[fid]
    ekin = ", ".join(f["ekin"])
    h    = holat(d)
    if short:
        return (f"<b>{f['nomi']}</b> — {h}\n"
                f"🌡{d['temp']}C  💧{d['humid']}%  🌱{d['soil']}%  🔋{d['battery']}%")
    tips = "\n".join(f"  • {x}" for x in tavsiyalar(d))
    return (f"<b>🌾 {f['nomi']}</b>\n📍 {f['joy']} | 🌱 {ekin}\n"
            f"────────────────\n"
            f"🌡 Harorat:  <b>{d['temp']}C</b>\n"
            f"💧 Namlik:   <b>{d['humid']}%</b>\n"
            f"🌱 Tuproq:   <b>{d['soil']}%</b>\n"
            f"☀ Yoruglik: <b>{d['light']:,} lux</b>\n"
            f"🔋 Zaryad:   <b>{d['battery']}%</b>\n"
            f"⏱ {d['vaqt']}\n────────────────\n"
            f"Holat: {h}\n📋 <b>Tavsiya:</b>\n{tips}")

# ── Klaviaturalar ─────────────────────────────────────────────────────────────
def main_kb(sub):
    p = PACKAGES[sub["package"]]
    rows = [
        [InlineKeyboardButton("📊 Hisobot",         callback_data="hisobot"),
         InlineKeyboardButton("🌾 Fermalar",         callback_data="fermalar")],
        [InlineKeyboardButton("🚨 Ogohlantirishlar", callback_data="ogohlar"),
         InlineKeyboardButton("ℹ Yordam",            callback_data="yordam")],
        [InlineKeyboardButton("📦 Obuna",            callback_data="obuna_info")],
    ]
    if p["sugorish"]:
        rows.insert(1,[InlineKeyboardButton("💧 Sughorish boshqaruvi", callback_data="sugorish")])
    if p["mutaxassis"]:
        rows.append([InlineKeyboardButton("👨‍🔬 Mutaxassis chaqirish", callback_data="mutax")])
    return InlineKeyboardMarkup(rows)

def pkgs_kb():
    return InlineKeyboardMarkup([[InlineKeyboardButton(
        f"{p['emoji']} {p['nomi']} — {p['narx']:,} som/oy", callback_data=f"pkg_{k}"
    )] for k,p in PACKAGES.items()])

def back_kb():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Asosiy menyu", callback_data="menu")]])

# ── Persistent Reply Keyboard ─────────────────────────────────────────────────
REPLY_TEXTS = {
    "📊 Hisobot":          "hisobot",
    "🌾 Fermalar":         "fermalar",
    "💧 Sug'orish":        "sugorish",
    "🚨 Ogohlantirishlar": "ogohlar",
    "📦 Obuna":            "obuna_info",
    "👨‍🔬 Mutaxassis":    "mutax",
    "ℹ Yordam":            "yordam",
    "🌐 Til":              "til",
}

REPLY_KB = ReplyKeyboardMarkup(
    [
        [KeyboardButton("📊 Hisobot"),    KeyboardButton("🌾 Fermalar")],
        [KeyboardButton("💧 Sug'orish"),  KeyboardButton("🚨 Ogohlantirishlar")],
        [KeyboardButton("📦 Obuna"),      KeyboardButton("👨‍🔬 Mutaxassis")],
        [KeyboardButton("ℹ Yordam"),      KeyboardButton("🌐 Til")],
    ],
    resize_keyboard=True,
    is_persistent=True,
    input_field_placeholder="Bo'lim tanlang...",
)

def pkgs_text():
    lines = []
    for k, p in PACKAGES.items():
        funks = "\n".join(f"   ✅ {f}" for f in p["funksiyalar"])
        lines.append(f"{p['emoji']} <b>{p['nomi']}</b> — <b>{p['narx']:,} som/oy</b>\n{funks}")
    return "\n\n".join(lines)

# ── Helpers ───────────────────────────────────────────────────────────────────
async def send(ctx, cid, text, kb=None):
    try: await ctx.bot.send_message(cid, text[:4096], parse_mode="HTML", reply_markup=kb)
    except Exception as e: logger.error("send %s: %s", cid, e)

async def edit(q, ctx, text, kb=None):
    try: await q.message.edit_text(text[:4096], parse_mode="HTML", reply_markup=kb)
    except Exception: await send(ctx, q.message.chat_id, text, kb)

def is_admin(uid): return uid in ADMIN_IDS

# ── /start ────────────────────────────────────────────────────────────────────
async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u    = update.effective_user
    save_user(u.id, u.username, u.full_name)
    ctx.bot_data.setdefault("subscribers", set()).add(update.effective_chat.id)
    lang = get_user_lang(u.id)
    sub  = get_sub(u.id)
    if not sub:
        await update.message.reply_text(
            tr('welcome_new', lang, name=u.first_name) + "\n\n" + pkgs_text(),
            parse_mode="HTML", reply_markup=pkgs_kb())
    else:
        p = PACKAGES[sub["package"]]
        await update.message.reply_text(
            tr('welcome_back', lang,
               name=u.first_name, emoji=p['emoji'],
               package=p['nomi'], end_date=sub['end_date'][:10]),
            parse_mode="HTML")

# ── /til  (language selector) ─────────────────────────────────────────────────
async def cmd_til(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid  = update.effective_user.id
    lang = get_user_lang(uid)
    def _lbl(code):
        return LANG_LABELS[code] + (" ✓" if lang == code else "")
    await update.message.reply_text(
        tr('lang_choose', lang),
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(_lbl('uz'), callback_data="lang_uz"),
            InlineKeyboardButton(_lbl('ru'), callback_data="lang_ru"),
            InlineKeyboardButton(_lbl('en'), callback_data="lang_en"),
        ]])
    )

# ── Callback ──────────────────────────────────────────────────────────────────
async def cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q    = update.callback_query
    data = q.data
    uid  = q.from_user.id
    await q.answer()

    # ── Til o'zgartirish ─────────────────────────────────────────────────────
    if data.startswith("lang_"):
        new_lang = data[5:]  # uz, ru, en
        if new_lang in ('uz', 'ru', 'en'):
            set_user_lang(uid, new_lang)
            key = LANG_CHANGED_KEY.get(new_lang, 'lang_changed_uz')
            changed_text = tr(key, new_lang)
            try:
                await q.message.edit_text(changed_text, reply_markup=None)
            except Exception:
                await send(ctx, q.message.chat_id, changed_text)
        return

    sub = get_sub(uid)

    # Paket tanlash
    if data.startswith("pkg_"):
        pid = data[4:]; p = PACKAGES[pid]
        funks = "\n".join(f"  ✅ {f}" for f in p["funksiyalar"])
        await edit(q, ctx,
            f"{p['emoji']} <b>{p['nomi']} paketi</b>\n"
            f"💰 <b>{p['narx']:,} som/oy</b> | {p['muddat']} kun\n\n"
            f"<b>Kiruvchi funksiyalar:</b>\n{funks}\n\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"Demo rejimda to'lovni tasdiqlang:",
            kb=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Tolovni tasdiqlash", callback_data=f"pay_{pid}")],
                [InlineKeyboardButton("⬅ Boshqa paket",       callback_data="show_pkgs")],
            ])); return

    if data == "show_pkgs":
        await edit(q, ctx, "📦 <b>Obuna paketlari</b>\n\n" + pkgs_text(), kb=pkgs_kb()); return

    if data.startswith("pay_"):
        pid = data[4:]
        activate_sub(uid, pid)
        sub = get_sub(uid); p = PACKAGES[pid]
        await edit(q, ctx,
            f"🎉 <b>Tabriklaymiz!</b>\n\n{p['emoji']} <b>{p['nomi']}</b> paketi faollashtirildi!\n"
            f"📅 {sub['end_date'][:10]} gacha\n\nEndi TomchiTech xizmatlaridan foydalanishingiz mumkin!")
        # Birinchi marta obuna bo'lganda persistent klaviatura o'rnatiladi
        await send(ctx, q.message.chat_id,
            "⌨️ Tugmalar paneli tayyor! Pastda klaviatura ikonkasini bosib oching.",
            kb=REPLY_KB)
        return

    if not sub:
        await q.message.reply_text("❌ Bu funksiyadan foydalanish uchun obuna kerak.", reply_markup=pkgs_kb()); return

    p = PACKAGES[sub["package"]]
    mf = min(p["max_ferma"], len(FARMS))

    if data == "menu":
        await edit(q, ctx,
            f"🏠 <b>Asosiy menyu</b>\n{p['emoji']} {p['nomi']} | {sub['end_date'][:10]} gacha\n\nTugmalardan birini tanlang:",
            kb=main_kb(sub)); return

    # Hisobot
    if data == "hisobot":
        await q.message.edit_text("⏳ Yuklanmoqda...")
        fids = list(FARMS.keys())[:mf]; bloklar = []; kritik = 0
        for fid in fids:
            d = sensor(fid); bloklar.append(ferma_blok(fid, d))
            if holat(d).startswith("🔴"): kritik += 1
        umumiy = "🔴 DIQQAT: Kritik holatlar!" if kritik else "🟢 Umumiy holat: Yaxshi"
        await edit(q, ctx,
            f"📊 <b>FERMA HISOBOTI</b>\n🕐 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n{umumiy}\n"
            f"━━━━━━━━━━━━━━━━━━\n\n" + "\n\n━━━━━━━━━━━━━━━━━━\n\n".join(bloklar),
            kb=back_kb()); return

    # Fermalar
    if data == "fermalar":
        fids = list(FARMS.keys())[:mf]
        matn = f"🌾 <b>FERMALARINGIZ ({mf} ta)</b>\n\n"
        for fid in fids:
            f = FARMS[fid]; matn += f"<b>{f['nomi']}</b>\n📍 {f['joy']}\n🌱 {', '.join(f['ekin'])}\n\n"
        rows = [[InlineKeyboardButton(f"🌾 {FARMS[fid]['nomi']}", callback_data=f"farm_{fid}")] for fid in fids]
        rows.append([InlineKeyboardButton("⬅ Asosiy menyu", callback_data="menu")])
        await edit(q, ctx, matn, kb=InlineKeyboardMarkup(rows)); return

    if data.startswith("farm_"):
        fid = data[5:]; d = sensor(fid)
        rows = []
        if p["sugorish"]:
            rows.append([InlineKeyboardButton("💧 Sughorish boshlash", callback_data=f"irr_{fid}")])
        rows += [
            [InlineKeyboardButton("🔄 Yangilash", callback_data=f"farm_{fid}"),
             InlineKeyboardButton("⬅ Fermalar",   callback_data="fermalar")],
            [InlineKeyboardButton("⬅ Asosiy menyu", callback_data="menu")],
        ]
        await edit(q, ctx, f"📡 <b>SENSOR MALUMOTLARI</b>\n\n{ferma_blok(fid, d)}", kb=InlineKeyboardMarkup(rows)); return

    # Ogohlantirishlar
    if data == "ogohlar":
        fids = list(FARMS.keys())[:mf]; krit = []; eht = []
        for fid in fids:
            d = sensor(fid); h = holat(d)
            if h.startswith("🔴"): krit.append(ferma_blok(fid, d))
            elif h.startswith("🟡"): eht.append(ferma_blok(fid, d))
        if krit:
            kb_rows = [[InlineKeyboardButton("⬅ Asosiy menyu", callback_data="menu")]]
            if p["mutaxassis"]: kb_rows.insert(0,[InlineKeyboardButton("👨‍🔬 Mutaxassis", callback_data="mutax")])
            await edit(q, ctx,
                f"🚨 <b>KRITIK OGOHLANTIRISHLAR</b>\n⏱ {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                f"━━━━━━━━━━━━━━━━━━\n\n" + "\n\n━━━━━━━━━━━━━━━━━━\n\n".join(krit),
                kb=InlineKeyboardMarkup(kb_rows))
        elif eht:
            await edit(q, ctx,
                f"🟡 <b>EHTIYOT HOLATLAR</b>\n━━━━━━━━━━━━━━━━━━\n\n" + "\n\n━━━━━━━━━━━━━━━━━━\n\n".join(eht),
                kb=back_kb())
        else:
            await edit(q, ctx, "✅ <b>Hozirda hech qanday ogohlantirish yoq.</b>\n\nBarcha fermalar normal. 🌿", kb=back_kb())
        return

    # Sughorish boshqaruvi
    if data == "sugorish":
        if not p["sugorish"]:
            await q.message.reply_text("❌ Bu funksiya faqat Standart va Premium paketlarda mavjud."); return
        fids = list(FARMS.keys())[:mf]
        matn = "💧 <b>SUGHORISH BOSHQARUVI</b>\n\nQaysi fermada sughorish boshlamoqchisiz?\n\n"
        for fid in fids:
            d = sensor(fid)
            matn += f"🌾 <b>{FARMS[fid]['nomi']}</b> — 🌱 Tuproq: <b>{d['soil']}%</b>\n"
        rows = [[InlineKeyboardButton(f"💧 {FARMS[fid]['nomi']}", callback_data=f"irr_{fid}")] for fid in fids]
        rows.append([InlineKeyboardButton("📋 Sughorish tarixi", callback_data="irr_history")])
        rows.append([InlineKeyboardButton("⬅ Asosiy menyu",      callback_data="menu")])
        await edit(q, ctx, matn, kb=InlineKeyboardMarkup(rows)); return

    if data.startswith("irr_") and data != "irr_history":
        fid = data[4:]; d = sensor(fid); f = FARMS[fid]; c = calc_irr(d["soil"], d["temp"], f["area"])
        await edit(q, ctx,
            f"💧 <b>SUGHORISH — {f['nomi']}</b>\n\n"
            f"📊 <b>Hozirgi holat:</b>\n"
            f"🌱 Tuproq namligi: <b>{d['soil']}%</b>\n"
            f"🌡 Harorat: <b>{d['temp']}C</b>\n"
            f"📐 Maydon: <b>{f['area']} ga</b>\n\n"
            f"🤖 <b>Tizim tavsiyasi:</b>\n"
            f"⏱ Davomiylik: <b>{c['davomiylik']} daqiqa</b>\n"
            f"💦 Suv sarfi: <b>{c['suv_litr']} litr</b>\n"
            f"🎯 Maqsad namlik: <b>{c['maqsad']}%</b>\n\n"
            f"Tomchilatib sughorish tizimi tayyor.",
            kb=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"▶ {c['davomiylik']} daqiqa (tavsiya)", callback_data=f"istart_{fid}_{c['davomiylik']}")],
                [InlineKeyboardButton("⏱ 30 daq", callback_data=f"istart_{fid}_30"),
                 InlineKeyboardButton("⏱ 60 daq", callback_data=f"istart_{fid}_60"),
                 InlineKeyboardButton("⏱ 90 daq", callback_data=f"istart_{fid}_90")],
                [InlineKeyboardButton("⬅ Orqaga", callback_data="sugorish")],
            ])); return

    if data.startswith("istart_"):
        parts = data.split("_"); fid = parts[1]; dur = int(parts[2])
        d = sensor(fid); f = FARMS[fid]; water = round(dur*2*f["area"],1)
        soil_after = min(75.0, d["soil"] + dur*0.4)
        log_irr(uid, fid, f["nomi"], dur, "manual", d["soil"], water)
        await edit(q, ctx,
            f"✅ <b>SUGHORISH BOSHLANDI!</b>\n\n"
            f"🌾 Ferma: <b>{f['nomi']}</b>\n"
            f"⏱ Davomiylik: <b>{dur} daqiqa</b>\n"
            f"💦 Suv sarfi: <b>{water} litr</b>\n\n"
            f"📊 <b>Bashorat:</b>\n"
            f"🌱 Tuproq namligi: {d['soil']}% → <b>{soil_after:.1f}%</b>\n\n"
            f"Tomchilatib sughorish tizimi ishga tushdi.\n"
            f"⏰ {dur} daqiqadan keyin avtomatik toxtatiladi.",
            kb=InlineKeyboardMarkup([
                [InlineKeyboardButton("⏹ Toxtatish",    callback_data=f"istop_{fid}")],
                [InlineKeyboardButton("💧 Boshqa ferma", callback_data="sugorish")],
                [InlineKeyboardButton("⬅ Asosiy menyu", callback_data="menu")],
            ])); return

    if data.startswith("istop_"):
        fid = data[6:]
        await edit(q, ctx,
            f"⏹ <b>SUGHORISH TOXTATILDI</b>\n\n🌾 {FARMS[fid]['nomi']}\n✅ Tizim ochirildi.",
            kb=back_kb()); return

    if data == "irr_history":
        with DB_LOCK:
            c = db()
            rows = c.execute("SELECT * FROM irrigation_logs WHERE user_id=? ORDER BY logged_at DESC LIMIT 10",(uid,)).fetchall()
            c.close()
        if not rows:
            matn = "📋 <b>Sughorish tarixi bosh.</b>\n\nHali hech qanday sughorish amalga oshirilmagan."
        else:
            matn = "📋 <b>SONGGI SUGHORISHLAR</b>\n━━━━━━━━━━━━━━━━━━\n\n"
            for r in rows:
                matn += f"🌾 {r['farm_name']}\n⏱ {r['logged_at'][:16]} | {r['duration_min']} daqiqa\n💦 {r['water_liters']} litr | 🌱 {r['soil_before']}%\n\n"
        await edit(q, ctx, matn, kb=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Sughorish", callback_data="sugorish")]])); return

    # Mutaxassislar
    if data == "mutax":
        if not p["mutaxassis"]:
            await edit(q, ctx,
                "👨‍🔬 <b>Mutaxassis chaqirish</b>\n\n❌ Bu funksiya faqat <b>Premium</b> paket uchun.\n\nObunangizni Premium ga yuksaltiring:",
                kb=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🏆 Premium ga otish", callback_data="pkg_premium")],
                    [InlineKeyboardButton("⬅ Asosiy menyu",      callback_data="menu")],
                ])); return
        matn = "👨‍🔬 <b>MUTAXASSISLAR</b>\nKritik holatlarda quyidagilar bilan boglanin:\n━━━━━━━━━━━━━━━━━━\n\n"
        for m in MUTAXASSISLAR:
            matn += f"<b>{m['ism']}</b>\n💼 {m['lavozim']}\n🔬 {m['soha']}\n📞 {m['tel']}\n\n"
        matn += "⏰ Ish vaqti: Du-Jum 08:00-18:00\n🆘 Favqulodda: 24/7"
        await edit(q, ctx, matn, kb=back_kb()); return

    # Obuna info
    if data == "obuna_info":
        remaining = (datetime.strptime(sub["end_date"][:10], "%Y-%m-%d") - datetime.now()).days
        funks     = "\n".join(f"  ✅ {f}" for f in p["funksiyalar"])
        rows      = []
        if sub["package"] != "premium": rows.append([InlineKeyboardButton("⬆ Paketni yuksaltirish", callback_data="show_pkgs")])
        rows.append([InlineKeyboardButton("⬅ Asosiy menyu", callback_data="menu")])
        await edit(q, ctx,
            f"📦 <b>OBUNA MALUMOTLARI</b>\n━━━━━━━━━━━━━━━━━━\n\n"
            f"{p['emoji']} Paket: <b>{p['nomi']}</b>\n"
            f"💰 {p['narx']:,} som/oy\n"
            f"📅 Tugash: {sub['end_date'][:10]}\n"
            f"🕐 Qolgan: <b>{remaining} kun</b>\n\n"
            f"<b>Funksiyalar:</b>\n{funks}",
            kb=InlineKeyboardMarkup(rows)); return

    # Yordam
    if data == "yordam":
        await edit(q, ctx,
            "ℹ <b>YORDAM</b>\n\n"
            "📊 Hisobot — sensor malumotlari hisoboti\n"
            "🌾 Fermalar — alohida ferma sensori\n"
            "💧 Sughorish — tomchilatib sughorish boshqaruvi\n"
            "🚨 Ogohlantirishlar — kritik/ehtiyot holatlar\n"
            "👨‍🔬 Mutaxassis — Premium foydalanuvchilar uchun\n\n"
            f"Kritik chegara:\n"
            f"• Harorat > {ALERT_TEMP_MAX}C\n"
            f"• Namlik < {ALERT_HUMID_MIN}%\n"
            f"• Tuproq namligi < {ALERT_SOIL_MIN}%\n\n"
            "🔔 Har soatda avtomatik hisobot\n\n"
            "📞 support@tomchitech.uz",
            kb=back_kb()); return

    # Admin
    if data == "admin" and is_admin(uid):
        users = all_users(); active = sum(1 for u in users if u.get("status") == "active")
        await edit(q, ctx,
            f"⚙ <b>ADMIN PANEL</b>\n━━━━━━━━━━━━━━━━━━\n\n👥 Jami: <b>{len(users)}</b>\n✅ Faol: <b>{active}</b>\n❌ Obunasiz: <b>{len(users)-active}</b>",
            kb=InlineKeyboardMarkup([[InlineKeyboardButton("👥 Foydalanuvchilar", callback_data="admin_users")]])); return

    if data == "admin_users" and is_admin(uid):
        users = all_users()
        matn  = f"👥 <b>FOYDALANUVCHILAR ({len(users)} ta)</b>\n━━━━━━━━━━━━━━━━━━\n\n"
        for u in users[:20]:
            pk = PACKAGES.get(u.get("package") or "", {}).get("nomi", "Yoq")
            st = "✅" if u.get("status") == "active" else "❌"
            matn += f"{st} {u['full_name']} (@{u['username'] or '-'}) — {pk}\n"
        await edit(q, ctx, matn, kb=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Admin", callback_data="admin")]])); return

# ── Reply keyboard handler ────────────────────────────────────────────────────
async def reply_menu_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Reply keyboard tugmalaridagi matnni callback sifatida qayta ishlaydi."""
    text = update.message.text.strip()
    data = REPLY_TEXTS.get(text)
    if not data:
        return
    uid = update.effective_user.id
    sub = get_sub(uid)

    if not sub:
        await update.message.reply_text(
            "❌ Bu funksiyadan foydalanish uchun obuna kerak.",
            reply_markup=pkgs_kb())
        return

    p  = PACKAGES[sub["package"]]
    mf = min(p["max_ferma"], len(FARMS))

    if data == "hisobot":
        await update.message.reply_text("⏳ Yuklanmoqda...")
        fids = list(FARMS.keys())[:mf]; bloklar = []; kritik = 0
        for fid in fids:
            d = sensor(fid); bloklar.append(ferma_blok(fid, d))
            if holat(d).startswith("🔴"): kritik += 1
        umumiy = "🔴 DIQQAT: Kritik holatlar!" if kritik else "🟢 Umumiy holat: Yaxshi"
        await send(ctx, update.effective_chat.id,
            f"📊 <b>FERMA HISOBOTI</b>\n🕐 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n{umumiy}\n"
            f"━━━━━━━━━━━━━━━━━━\n\n" + "\n\n━━━━━━━━━━━━━━━━━━\n\n".join(bloklar),
            kb=back_kb())

    elif data == "fermalar":
        fids = list(FARMS.keys())[:mf]
        matn = f"🌾 <b>FERMALARINGIZ ({mf} ta)</b>\n\n"
        for fid in fids:
            f = FARMS[fid]; matn += f"<b>{f['nomi']}</b>\n📍 {f['joy']}\n🌱 {', '.join(f['ekin'])}\n\n"
        rows = [[InlineKeyboardButton(f"🌾 {FARMS[fid]['nomi']}", callback_data=f"farm_{fid}")] for fid in fids]
        rows.append([InlineKeyboardButton("⬅ Asosiy menyu", callback_data="menu")])
        await send(ctx, update.effective_chat.id, matn, kb=InlineKeyboardMarkup(rows))

    elif data == "sugorish":
        if not p["sugorish"]:
            await update.message.reply_text("❌ Bu funksiya faqat Standart va Premium paketlarda mavjud.")
            return
        fids = list(FARMS.keys())[:mf]
        matn = "💧 <b>SUGHORISH BOSHQARUVI</b>\n\nQaysi fermada sughorish boshlamoqchisiz?\n\n"
        for fid in fids:
            d = sensor(fid)
            matn += f"🌾 <b>{FARMS[fid]['nomi']}</b> — 🌱 Tuproq: <b>{d['soil']}%</b>\n"
        rows = [[InlineKeyboardButton(f"💧 {FARMS[fid]['nomi']}", callback_data=f"irr_{fid}")] for fid in fids]
        rows.append([InlineKeyboardButton("📋 Sughorish tarixi", callback_data="irr_history")])
        rows.append([InlineKeyboardButton("⬅ Asosiy menyu",      callback_data="menu")])
        await send(ctx, update.effective_chat.id, matn, kb=InlineKeyboardMarkup(rows))

    elif data == "ogohlar":
        fids = list(FARMS.keys())[:mf]; krit = []; eht = []
        for fid in fids:
            d = sensor(fid); h = holat(d)
            if h.startswith("🔴"): krit.append(ferma_blok(fid, d))
            elif h.startswith("🟡"): eht.append(ferma_blok(fid, d))
        cid = update.effective_chat.id
        if krit:
            kb_rows = [[InlineKeyboardButton("⬅ Asosiy menyu", callback_data="menu")]]
            if p["mutaxassis"]: kb_rows.insert(0,[InlineKeyboardButton("👨‍🔬 Mutaxassis", callback_data="mutax")])
            await send(ctx, cid,
                f"🚨 <b>KRITIK OGOHLANTIRISHLAR</b>\n⏱ {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                f"━━━━━━━━━━━━━━━━━━\n\n" + "\n\n━━━━━━━━━━━━━━━━━━\n\n".join(krit),
                kb=InlineKeyboardMarkup(kb_rows))
        elif eht:
            await send(ctx, cid,
                f"🟡 <b>EHTIYOT HOLATLAR</b>\n━━━━━━━━━━━━━━━━━━\n\n" + "\n\n━━━━━━━━━━━━━━━━━━\n\n".join(eht),
                kb=back_kb())
        else:
            await send(ctx, cid, "✅ <b>Hozirda hech qanday ogohlantirish yoq.</b>\n\nBarcha fermalar normal. 🌿", kb=back_kb())

    elif data == "obuna_info":
        remaining = (datetime.strptime(sub["end_date"][:10], "%Y-%m-%d") - datetime.now()).days
        funks     = "\n".join(f"  ✅ {f}" for f in p["funksiyalar"])
        rows      = []
        if sub["package"] != "premium": rows.append([InlineKeyboardButton("⬆ Paketni yuksaltirish", callback_data="show_pkgs")])
        rows.append([InlineKeyboardButton("⬅ Asosiy menyu", callback_data="menu")])
        await send(ctx, update.effective_chat.id,
            f"📦 <b>OBUNA MALUMOTLARI</b>\n━━━━━━━━━━━━━━━━━━\n\n"
            f"{p['emoji']} Paket: <b>{p['nomi']}</b>\n"
            f"💰 {p['narx']:,} som/oy\n"
            f"📅 Tugash: {sub['end_date'][:10]}\n"
            f"🕐 Qolgan: <b>{remaining} kun</b>\n\n"
            f"<b>Funksiyalar:</b>\n{funks}",
            kb=InlineKeyboardMarkup(rows))

    elif data == "mutax":
        if not p["mutaxassis"]:
            await send(ctx, update.effective_chat.id,
                "👨‍🔬 <b>Mutaxassis chaqirish</b>\n\n❌ Bu funksiya faqat <b>Premium</b> paket uchun.\n\nObunangizni Premium ga yuksaltiring:",
                kb=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🏆 Premium ga otish", callback_data="pkg_premium")],
                    [InlineKeyboardButton("⬅ Asosiy menyu",      callback_data="menu")],
                ]))
            return
        matn = "👨‍🔬 <b>MUTAXASSISLAR</b>\nKritik holatlarda quyidagilar bilan boglanin:\n━━━━━━━━━━━━━━━━━━\n\n"
        for m in MUTAXASSISLAR:
            matn += f"<b>{m['ism']}</b>\n💼 {m['lavozim']}\n🔬 {m['soha']}\n📞 {m['tel']}\n\n"
        matn += "⏰ Ish vaqti: Du-Jum 08:00-18:00\n🆘 Favqulodda: 24/7"
        await send(ctx, update.effective_chat.id, matn, kb=back_kb())

    elif data == "yordam":
        lang = get_user_lang(uid)
        await send(ctx, update.effective_chat.id,
            tr('help_text', lang,
               temp_max=ALERT_TEMP_MAX,
               humid_min=ALERT_HUMID_MIN,
               soil_min=ALERT_SOIL_MIN),
            kb=back_kb())

    elif data == "til":
        await cmd_til(update, ctx)

# ── Admin commands ────────────────────────────────────────────────────────────
async def cmd_admin(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_admin(uid): await update.message.reply_text("❌ Ruxsat yoq."); return
    users = all_users(); active = sum(1 for u in users if u.get("status") == "active")
    await update.message.reply_text(
        f"⚙ <b>ADMIN PANEL</b>\n👥 Jami: <b>{len(users)}</b>\n✅ Faol: <b>{active}</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👥 Foydalanuvchilar", callback_data="admin_users")]]))

async def cmd_grant(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_admin(uid): return
    args = ctx.args
    if len(args) < 2: await update.message.reply_text("Ishlatish: /grant <user_id> <asosiy|standart|premium>"); return
    try:
        tid = int(args[0]); pkg = args[1].lower()
        if pkg not in PACKAGES: await update.message.reply_text(f"Notogri paket: {pkg}"); return
        save_user(tid, "", str(tid)); activate_sub(tid, pkg)
        p = PACKAGES[pkg]
        await update.message.reply_text(f"✅ {tid} ga {p['emoji']} {p['nomi']} berildi.")
        try:
            await ctx.bot.send_message(tid,
                f"🎉 <b>Obunangiz faollashtirildi!</b>\n{p['emoji']} <b>{p['nomi']}</b> paketi admin tomonidan berildi.\n/start — botni boshlang",
                parse_mode="HTML")
        except Exception: pass
    except ValueError: await update.message.reply_text("user_id raqam bolishi kerak.")

# ── Scheduled jobs ────────────────────────────────────────────────────────────
async def job_soatlik(ctx: ContextTypes.DEFAULT_TYPE):
    subs = ctx.bot_data.get("subscribers", set())
    if not subs: return
    bloklar = []; kritik = 0
    for fid in FARMS:
        d = sensor(fid); bloklar.append(ferma_blok(fid, d, short=True))
        if holat(d).startswith("🔴"): kritik += 1
    umumiy = "🔴 DIQQAT: Kritik holatlar!" if kritik else "🟢 Umumiy holat: Yaxshi"
    matn = (f"⏰ <b>SOATLIK HISOBOT</b>\n🕐 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
            f"{umumiy}\n━━━━━━━━━━━━━━━━━━\n\n" + "\n\n".join(bloklar))
    for cid in list(subs):
        if get_sub(cid): await send(ctx, cid, matn)

async def job_kritik(ctx: ContextTypes.DEFAULT_TYPE):
    subs = ctx.bot_data.get("subscribers", set())
    if not subs: return
    for fid, f in FARMS.items():
        d = sensor(fid)
        if not holat(d).startswith("🔴"): continue
        tips = "\n".join(f"• {x}" for x in tavsiyalar(d))
        matn = (f"🚨 <b>KRITIK OGOHLANTIRISH!</b>\n━━━━━━━━━━━━━━━━━━\n"
                f"🌾 <b>{f['nomi']}</b>\n⏱ {d['vaqt']}\n\n"
                f"🌡{d['temp']}C  💧{d['humid']}%  🌱{d['soil']}%  🔋{d['battery']}%\n\n"
                f"📋 <b>Zudlik bilan:</b>\n{tips}")
        for cid in list(subs):
            if get_sub(cid): await send(ctx, cid, matn)

async def job_auto_irr(ctx: ContextTypes.DEFAULT_TYPE):
    subs = ctx.bot_data.get("subscribers", set())
    for cid in list(subs):
        sub = get_sub(cid)
        if not sub or sub["package"] != "premium": continue
        for fid, f in FARMS.items():
            d = sensor(fid)
            if d["soil"] >= ALERT_SOIL_IRRIG: continue
            c = calc_irr(d["soil"], d["temp"], f["area"])
            log_irr(cid, fid, f["nomi"], c["davomiylik"], "auto", d["soil"], c["suv_litr"])
            # Boshlash bildirishnomasini yuborish
            await send(ctx, cid,
                f"🤖 <b>AVTOMATIK SUGHORISH BOSHLANDI</b>\n\n"
                f"🌾 {f['nomi']}\n"
                f"🌱 Tuproq namligi: <b>{d['soil']}%</b> (kritik – {ALERT_SOIL_IRRIG}% dan past)\n"
                f"⏱ Davomiylik: <b>{c['davomiylik']} daqiqa</b>\n"
                f"💦 Suv sarfi: <b>{c['suv_litr']} litr</b>\n"
                f"🎯 Maqsad namlik: <b>{c['maqsad']}%</b>\n\n"
                f"⏰ {c['davomiylik']} daqiqadan keyin to'xtaydi.")
            # To'xtatish bildirishnomasini keyinroq rejalashtirish
            ctx.job_queue.run_once(
                _auto_irr_stop,
                when=c["davomiylik"] * 60,
                data={"cid": cid, "farm": f, "dur": c["davomiylik"],
                      "soil_before": d["soil"], "maqsad": c["maqsad"]},
                name=f"irr_stop_{cid}_{fid}",
            )

async def _auto_irr_stop(ctx: ContextTypes.DEFAULT_TYPE):
    d = ctx.job.data
    cid        = d["cid"]
    f          = d["farm"]
    dur        = d["dur"]
    soil_b     = d["soil_before"]
    soil_after = min(75.0, soil_b + dur * 0.4)
    await send(ctx, cid,
        f"✅ <b>AVTOMATIK SUGHORISH YAKUNLANDI</b>\n\n"
        f"🌾 {f['nomi']}\n"
        f"⏱ Davomiylik: <b>{dur} daqiqa</b>\n"
        f"🌱 Tuproq namligi: {soil_b}% → <b>{soil_after:.1f}%</b>\n"
        f"🕐 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
        f"🟢 Tizim normal rejimga qaytdi.")

async def job_keepalive(ctx: ContextTypes.DEFAULT_TYPE):
    if WEBHOOK_URL:
        try:
            async with httpx.AsyncClient() as cl:
                await cl.get(f"{WEBHOOK_URL}/healthz", timeout=10)
        except Exception: pass

# ══════════════════════════════════════════════════════════════════════════════
#  2-DAQIQALIK ALERT BUFFER TIZIMI
# ══════════════════════════════════════════════════════════════════════════════
# {chat_id: [{"time":..., "farm":..., "sensor":..., "holat":..., "qiymat":..., "xabar":...}]}
ALERT_BUFFER: dict = {}
_BUF_LOCK = threading.Lock()


def buf_add(chat_id: int, alert: dict):
    """Bufferga yangi alert qo'shadi."""
    with _BUF_LOCK:
        ALERT_BUFFER.setdefault(chat_id, []).append(alert)


async def flush_alerts(context: ContextTypes.DEFAULT_TYPE):
    """
    Har 2 daqiqada PTB job_queue tomonidan chaqiriladi.
    Bufferdagi alertlarni bitta log xabar sifatida yuboradi.
    """
    with _BUF_LOCK:
        snapshot = {cid: list(alerts) for cid, alerts in ALERT_BUFFER.items() if alerts}
        for cid in snapshot:
            ALERT_BUFFER[cid].clear()

    for cid, alerts in snapshot.items():
        n   = len(alerts)
        now = datetime.now().strftime("%d.%m.%Y %H:%M")

        sep   = '━' * 26
        lines = [
            f"🔔 <b>{n} ta yangi bildirishnoma</b>\n"
            f"⏰ {now}\n" + sep
        ]
        for i, a in enumerate(alerts, 1):
            h    = a.get("holat", "ehtiyot")
            icon = "🔴" if h == "kritik" else "🟡" if h == "ehtiyot" else "🟢"
            farm_name = a.get("farm", "Noma'lum ferma")
            lines.append(
                f"{i}. {icon} <b>{farm_name}</b>\n"
                f"   📡 {a.get('sensor', 'Sensor')} · <code>{a.get('qiymat', '—')}</code>\n"
                f"   💬 {a.get('xabar', '')}\n"
                f"   🕐 {a.get('time', '')}"
            )
        lines.append(sep + "\n📌 <i>Ushbu xabar log sifatida saqlanadi</i>")

        markup = InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ Ko'rib chiqdim", callback_data="ack_log")
        ]])
        try:
            await context.bot.send_message(
                cid,
                "\n\n".join(lines)[:4096],
                parse_mode="HTML",
                reply_markup=markup
            )
        except Exception as e:
            logger.error("flush_alerts → chat %s: %s", cid, e)


async def cb_ack_log(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """
    'Ko'rib chiqdim' tugmasi bosilganda xabarni yangilaydi:
    tugma yo'qoladi, pastga "Ko'rib chiqildi" qo'shiladi.
    """
    q   = update.callback_query
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    await q.answer("✅ Belgilandi!")
    try:
        orig = (q.message.text or "").rstrip()
        new  = orig + f"\n\n{'─' * 26}\n✅ <b>Ko'rib chiqildi</b> — {q.from_user.first_name}\n🕐 {now}"
        await q.message.edit_text(new[:4096], parse_mode="HTML", reply_markup=None)
    except Exception as e:
        logger.warning("cb_ack_log edit: %s", e)


# ══════════════════════════════════════════════════════════════════════════════
#  HTTP API SERVER  (dashboard → bot alertlar)
# ══════════════════════════════════════════════════════════════════════════════
_app_ref = None   # Application instance (main() da o'rnatiladi)


class AlertHandler(BaseHTTPRequestHandler):
    """
    POST /alert   →  dashboard dan sensor alertini qabul qiladi
    GET  /ping    →  health check
    """
    def log_message(self, *a): pass   # access log ni o'chirish

    def _respond(self, code: int, body: bytes = b""):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Secret")
        self.end_headers()

    def do_GET(self):
        if self.path == "/ping":
            buffered = sum(len(v) for v in ALERT_BUFFER.values())
            self._respond(200, json.dumps({"ok": True, "buffered": buffered}).encode())
        else:
            self._respond(404, b'{"error":"Not found"}')

    def do_POST(self):
        if self.path != "/alert":
            self._respond(404, b'{"error":"Not found"}'); return

        secret = self.headers.get("X-Secret", "")
        if secret != NOTIFY_SECRET:
            self._respond(403, b'{"error":"Forbidden"}'); return

        length = int(self.headers.get("Content-Length", 0))
        try:
            data = json.loads(self.rfile.read(length))
        except Exception:
            self._respond(400, b'{"error":"Bad JSON"}'); return

        alert = {
            "time":   datetime.now().strftime("%H:%M:%S"),
            "farm":   data.get("farm", "Noma'lum ferma"),
            "sensor": data.get("sensor", "Sensor"),
            "holat":  data.get("holat", "ehtiyot"),   # kritik | ehtiyot | normal
            "qiymat": data.get("qiymat", "—"),
            "xabar":  data.get("xabar") or data.get("message", ""),
        }

        chat_id = data.get("chat_id")
        if chat_id:
            buf_add(int(chat_id), alert)
        elif _app_ref:
            for cid in _app_ref.bot_data.get("subscribers", set()):
                buf_add(cid, alert)

        total = sum(len(v) for v in ALERT_BUFFER.values())
        self._respond(200, json.dumps({"ok": True, "buffered": total}).encode())


def start_api_server():
    try:
        server = HTTPServer(("0.0.0.0", API_PORT), AlertHandler)
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        logger.info("Alert API server: port %s  (secret: %s***)", API_PORT, NOTIFY_SECRET[:4])
    except Exception as e:
        logger.error("API server start failed: %s", e)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    global _app_ref
    init_db()

    app = Application.builder().token(BOT_TOKEN).build()
    _app_ref = app

    # ── Handlerlar ────────────────────────────────────────────────────────────
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("til",   cmd_til))       # /til — til tanlash
    app.add_handler(CommandHandler("admin", cmd_admin))
    app.add_handler(CommandHandler("grant", cmd_grant))
    # ack_log pattern MUST come before the generic cb handler
    app.add_handler(CallbackQueryHandler(cb_ack_log, pattern=r"^ack_log$"))
    app.add_handler(CallbackQueryHandler(cb))
    app.add_handler(MessageHandler(
        filters.Text(list(REPLY_TEXTS.keys())), reply_menu_handler))

    # ── Job queue ─────────────────────────────────────────────────────────────
    jq = app.job_queue
    jq.run_repeating(flush_alerts,  interval=120,  first=10,  name="alert_flush")
    jq.run_repeating(job_soatlik,   interval=3600, first=60,  name="soatlik")
    jq.run_repeating(job_kritik,    interval=300,  first=30,  name="kritik")
    jq.run_repeating(job_auto_irr,  interval=1800, first=120, name="auto_irr")
    jq.run_repeating(job_keepalive, interval=840,  first=120, name="keepalive")
    logger.info("Jobs: alert_flush(120s), soatlik(1h), kritik(5m), auto_irr(30m), keepalive(14m)")

    # ── HTTP Alert API server ─────────────────────────────────────────────────
    start_api_server()

    # ── Ishga tushirish ───────────────────────────────────────────────────────
    if WEBHOOK_URL:
        hook_url = WEBHOOK_URL.rstrip("/") + "/webhook"
        logger.info("Webhook mode: %s", hook_url)
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path="/webhook",
            webhook_url=hook_url,
        )
    else:
        logger.info("Polling mode ...")
        app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
