import requests
import time
import json
import os
import sys
import sqlite3
import uuid
import threading
import random
import re
import html
from collections import Counter 
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from datetime import datetime 
from urllib.parse import urljoin
import pyotp

# লগ
try:
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
except Exception:
    pass

print("🟡 main.py loaded", flush=True)

# ==================== CONFIG ====================
TOKEN = "8925470044:AAG3dTr4SA0Z967zF_w9nqzVViYYOvyj5aY"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
FILE_URL = f"https://api.telegram.org/file/bot{TOKEN}/"
OWNER_ID = 8961596390
CONSOLE_FORWARD_GROUP = "-1004362313105"
SUPPORT_USERNAME = "@Himel8200"
OTP_GROUP = "https://t.me/+rYT72_j66pwxZWY1"
BOT_USERNAME = "@gmailbothelppoorbot"
DB_FILE = "bot_data.json"

# ==================== EMOJIS ====================
PEM = {
    "ok": '<tg-emoji emoji-id="5352694861990501856">✅</tg-emoji>',
    "no": '<tg-emoji emoji-id="5420130255174145507">❌</tg-emoji>',
    "warn": '<tg-emoji emoji-id="5336944168944047463">⚠️</tg-emoji>',
    "admin": '<tg-emoji emoji-id="5353032893096567467">📊</tg-emoji>',
    "user": '<tg-emoji emoji-id="5352861489541714456">👤</tg-emoji>',
    "file": '<tg-emoji emoji-id="5352721946054268944">📁</tg-emoji>',
    "rocket": '<tg-emoji emoji-id="5352597830089347330">🚀</tg-emoji>',
    "graph": '<tg-emoji emoji-id="5352877703043258544">📊</tg-emoji>',
    "money": '<tg-emoji emoji-id="5348469219761626211">💸</tg-emoji>',
    "gift": '<tg-emoji emoji-id="5420396762189831222">🎁</tg-emoji>',
    "msg": '<tg-emoji emoji-id="5337302974806922068">💬</tg-emoji>',
    "gear": '<tg-emoji emoji-id="5420155432272438703">⚙️</tg-emoji>',
    "link": '<tg-emoji emoji-id="5420517437885943844">🔗</tg-emoji>',
    "trash": '<tg-emoji emoji-id="5422557736330106570">🗑</tg-emoji>',
    "upload": '<tg-emoji emoji-id="5353001161878182134">📤</tg-emoji>',
    "world": '<tg-emoji emoji-id="5336972142066047577">🌐</tg-emoji>',
    "lock": '<tg-emoji emoji-id="5353022963132174959">🔐</tg-emoji>',
    "phone": '<tg-emoji emoji-id="5337132498965010628">📱</tg-emoji>',
    "num": '<tg-emoji emoji-id="5352862640592949843">🔢</tg-emoji>',
    "pin": '<tg-emoji emoji-id="5352922460897452503">📍</tg-emoji>',
    "star": '<tg-emoji emoji-id="5352552689983067014">✨</tg-emoji>',
    "hi": '<tg-emoji emoji-id="5353027129250453493">👋</tg-emoji>'
}
GLOBAL_BODY_EMOJIS = {
    "➖": "5870818207383686839", "🚫": "5334807341109908955", "😒": "5334763399299506604",
    "🖥": "5334880948259427772", "🌐": "5334590977837403844", "🌟": "5337102391244263212",
    "🕓": "5336983442125001376", "⌛": "5337172996211648018", "💬": "5337302974806922068",
    "🔐": "5337255927735163754", "🍏": "5337132498965010628", "❔": "5336850036145823599",
    "⚠️": "5336944168944047463", "🔥": "5337267511261960341", "💸": "5348469219761626211",
    "🥚": "5348390922507817684", "👨‍⚖": "5334763399299506604", "🐁": "5348494358205207761",
    "🧻": "5348486915026884464", "⚗": "5346311574221000149", "🛴": "5348075478634766440",
    "📊": "5353032893096567467", "🔢": "5352862640592949843", "👤": "5352861489541714456",
    "📁": "5352721946054268944", "🚀": "5352597830089347330", "💎": "5352838545826420397",
    "📍": "5352922460897452503", "👋": "5353027129250453493", "✅": "5352694861990501856",
    "1️⃣": "5352651766288652742", "2️⃣": "5355186458418257716", "3️⃣": "5352867219028091093",
    "4️⃣": "5352566657216714037", "5️⃣": "5353086880835474989", "6️⃣": "5354859211975071385",
    "7️⃣": "5352859127309707652", "8️⃣": "5352957533600389988", "9️⃣": "5353060913463204207",
    "🔤": "5352727417842606016", "📣": "5352980533150259581", "📤": "5353001161878182134",
    "✨": "5352552689983067014", "🔹": "5352638632278660622", "🎙": "5355102594886833928",
    "💴": "5352985330628730418", "📅": "5352585194295564660", "📴": "5352974971167611327",
    "✏️": "5395444784611480792", "📱": "5337132498965010628", "🔗": "5420517437885943844",
    "❌": "5420130255174145507", "⚙️": "5420155432272438703", "🫂": "5420145051336485498",
    "➕": "5420323438508155202", "🗑": "5422557736330106570", "🎁": "5420396762189831222",
    "➤": "5420618897898381296", "🏢": "5420156334215565595", "💳": "5190899075968441286",
    "📝": "5192739271886282680", "🛡": "5190447043545438788", "🤝": "5192805934073685937",
    "💰": "5190576863226933563", "👀": "5190645917711114179", "🕹": "5193100774988617665",
    "🟢": "5192812028632274956", "🧪": "5190781475468915802", "🎨": "5190751148704833975",
    "📂": "5257969839313526622", "🌍": "5780471598922337683", "📌": "5318986077455795572",
    "📢": "5789428375261023681", "🆔": "5352862640592949843", "📈": "5352877703043258544",
    "🔔": "5352980533150259581", "🏦": "5348469219761626211", "🧾": "5192739271886282680",
    "👨‍⚖️": "5334763399299506604", "🔍": "5463352748751753567",
    "🔑": "5197288647275071607"
}

DEFAULT_CUSTOM_MESSAGES = {
    "start": {"text": "╔═════════════════════════╗\n       📊 MASTER X  OTP EXPERT BOT\n╚═════════════════════════╝\n🚀 Welcome to Number & OTP Service\n━━━━━━━━━━━━\n✅ Choose an option below\nto continue using the bot.\n━━━━━━━━━━━━\n💎 Premium OTP Service", "buttons": []},
    "support": {"text": f"{PEM['msg']} Contact us for any help:", "buttons": []},
    "temp_mail": {"text": f"{PEM['msg']} <b>Temporary Email Service</b>\n\nUse a disposable email address to receive OTPs and messages.\n━━━━━━━━━━━━━━━━━━\n📧 <b>Your Email:</b> {{email}}\n📨 <b>Inbox Messages:</b> {{msg_count}}\n━━━━━━━━━━━━━━━━━━", "buttons": []}
}

# ==================== DATABASE ====================
SQLITE_DB = "bot.db"
_thread_local = threading.local()

def get_db_conn():
    if not hasattr(_thread_local, 'conn') or _thread_local.conn is None:
        conn = sqlite3.connect(SQLITE_DB, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        _init_db_schema(conn)
        _thread_local.conn = conn
    return _thread_local.conn

def _init_db_schema(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            balance REAL DEFAULT 0.0,
            total_refers INTEGER DEFAULT 0,
            total_otps INTEGER DEFAULT 0,
            banned INTEGER DEFAULT 0,
            verified INTEGER DEFAULT 0,
            referred_by TEXT DEFAULT NULL,
            ref_paid INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS withdrawals (
            req_id TEXT PRIMARY KEY,
            user_id TEXT,
            amount REAL,
            method TEXT,
            status TEXT DEFAULT 'pending',
            timestamp TEXT
        );
        CREATE TABLE IF NOT EXISTS bot_config (
            key TEXT PRIMARY KEY,
            value TEXT
        );
        CREATE TABLE IF NOT EXISTS email_accounts (
            user_id TEXT PRIMARY KEY,
            email TEXT,
            token TEXT,
            last_msg_id TEXT,
            created_at TEXT
        );
    """)
    conn.commit()
    try:
        conn.execute("ALTER TABLE email_accounts ADD COLUMN token TEXT")
    except:
        pass
    try:
        conn.execute("ALTER TABLE email_accounts ADD COLUMN last_msg_id TEXT")
    except:
        pass

_init_db_schema(get_db_conn())
print("✅ DB Ready")

bot_settings = {
    "admins": [OWNER_ID],
    "panels": [], 
    "fw_groups": [], 
    "otp_link": "https://t.me/+-Y0k3AG6CgEyYmFl",
    "withdraw_on": True,
    "min_withdraw": 30.0,
    "otp_reward": 0.1,
    "refer_reward": 0.2,
    "cooldown": 10,
    "num_req": 3,
    "num_share": 1, 
    "support_link": "https://t.me/Himel8200",
    "w_methods": ["bKash", "Nagad"],
    "w_group": "", 
    "proof_group": "", 
    "fj_on": False,
    "fj_channels": [], 
    "stex_keys": [], 
    "voltx_keys": [],
    "search_countries": [],
    "stex_services": {},
    "voltx_services": {},
    "premium_flags": {
        "1": {"char": "🇺🇸", "iso": "US", "name": "United States", "id": "5913463998522592692"},
        "880": {"char": "🇧🇩", "iso": "BD", "name": "Bangladesh", "id": "5911365056594973179"},
        "91": {"char": "🇮🇳", "iso": "IN", "name": "India", "id": "5913754823643107921"},
        "92": {"char": "🇵🇰", "iso": "PK", "name": "Pakistan", "id": "5913705895375672082"},
        "44": {"char": "🇬🇧", "iso": "GB", "name": "United Kingdom", "id": "5913443365499703513"}
    },
    "premium_apps": {
        "FACEBOOK": {"char": "🚫", "id": "5334807341109908955", "name": "Facebook"},
        "WHATSAPP": {"char": "🚫", "id": "5334759662677957452", "name": "WhatsApp"}
    },
    "custom_messages": DEFAULT_CUSTOM_MESSAGES.copy()
}
FS_KEYS = [
    "admins", "panels", "fw_groups", "otp_link", "withdraw_on", 
    "min_withdraw", "otp_reward", "refer_reward", "cooldown", 
    "num_req", "num_share", "support_link", "w_methods", "w_group", "proof_group", "stex_keys", "voltx_keys", "search_countries", "stex_services", "voltx_services",
    "fj_on", "fj_channels"
]

number_batches = {}
used_numbers_list = []
stex_assigned_numbers = {} 
voltx_assigned_numbers = {}
STEX_BASE_URL = "https://api.2oo9.cloud/MXS47FLFX0U/tness/@public/api"
VOLTX_BASE_URL = "https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api"
total_uploaded_stats = 0
total_assigned_stats = 0
processed_otps = set() 
recent_traffic = []
user_banned_cache = {}
panel_sessions = {}

# ==================== MAIL.TM EMAIL FEATURE ====================
MAIL_TM_API = "https://api.mail.tm"

def get_mail_domain():
    try:
        resp = requests.get(f"{MAIL_TM_API}/domains", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            members = data.get('hydra:member', [])
            for domain in members:
                if domain.get('isActive', False):
                    return domain.get('domain')
            if members:
                return members[0].get('domain')
    except:
        pass
    return "mail.tm"

def create_mail_tm_account(user_id):
    session = requests.Session()
    for _ in range(3):
        try:
            domain = get_mail_domain()
            username = f"user{user_id}{int(time.time() * 1000)}"
            password = f"Pass{user_id}123!@#"
            address = f"{username}@{domain}"
            payload = {"address": address, "password": password}
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            resp = session.post(f"{MAIL_TM_API}/accounts", json=payload, headers=headers, timeout=10)
            if resp.status_code not in [200, 201]:
                time.sleep(1)
                continue
            token_resp = session.post(f"{MAIL_TM_API}/token", json={"address": address, "password": password}, headers=headers, timeout=10)
            if token_resp.status_code != 200:
                time.sleep(1)
                continue
            token = token_resp.json().get("token")
            if token:
                return address, token
        except:
            time.sleep(1)
            continue
    return None, None

def fetch_messages(token):
    try:
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        resp = requests.get(f"{MAIL_TM_API}/messages", headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get('hydra:member', [])
    except:
        pass
    return []

def fetch_message_detail(token, msg_id):
    try:
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        resp = requests.get(f"{MAIL_TM_API}/messages/{msg_id}", headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return {}

def get_email_data(user_id):
    conn = get_db_conn()
    row = conn.execute("SELECT email, token, last_msg_id FROM email_accounts WHERE user_id = ?", (str(user_id),)).fetchone()
    if row:
        return dict(row)
    return None

def save_email_data(user_id, email, token, last_msg_id=None):
    conn = get_db_conn()
    conn.execute(
        "INSERT OR REPLACE INTO email_accounts (user_id, email, token, last_msg_id, created_at) VALUES (?, ?, ?, ?, ?)",
        (str(user_id), email, token, last_msg_id, datetime.utcnow().isoformat())
    )
    conn.commit()

def delete_email_data(user_id):
    conn = get_db_conn()
    conn.execute("DELETE FROM email_accounts WHERE user_id = ?", (str(user_id),))
    conn.commit()

def update_last_msg_id(user_id, msg_id):
    conn = get_db_conn()
    conn.execute("UPDATE email_accounts SET last_msg_id = ? WHERE user_id = ?", (msg_id, str(user_id)))
    conn.commit()

# ==================== 🔥 শক্তিশালী OTP এক্সট্র্যাক্ট ফাংশন ====================
def extract_otp_code(text):
    if not text:
        return None
    clean_text = re.sub(r'[\u200B-\u200D\uFEFF]', '', str(text))
    
    # ১. মাল্টি-পার্ট OTP (যেমন 123-456 বা 12-34-56)
    multi_part = re.search(r'(\d{3}[-\s]+\d{3})|(\d{2}[-\s]+\d{2}[-\s]+\d{2})', clean_text)
    if multi_part:
        return multi_part.group(0).replace(" ", "")
    
    # ২. কীওয়ার্ড দিয়ে OTP (code, otp, pin ইত্যাদি)
    otp_keywords = ['code', 'is', 'otp', 'pin', 'verification', 'auth', 'কোড', 'رمز', 'your code', 'verification code', 'activation code']
    keywords_pattern = '|'.join(otp_keywords)
    keyword_match = re.search(rf'(?:{keywords_pattern})\s*(?:is|:|-|=|of)?\s*([a-z0-9]{{4,10}})', clean_text, re.I)
    if keyword_match and keyword_match.group(1).isdigit():
        return keyword_match.group(1)
    
    # ৩. রিভার্স কীওয়ার্ড (যেমন "is your code")
    keyword_match_rev = re.search(rf'([a-z0-9]{{4,10}})\s*(?:is your|is the|is|কোড|verification code|activation code)', clean_text, re.I)
    if keyword_match_rev and keyword_match_rev.group(1).isdigit():
        return keyword_match_rev.group(1)
    
    # ৪. জিমেইল OTP (G-123456)
    g_match = re.search(r'[Gg]-(\d{6})', clean_text)
    if g_match:
        return g_match.group(1)
    
    # ৫. সাধারণ ডিজিট সিকোয়েন্স (৪-৮ ডিজিট, কোনো অক্ষর ছাড়া)
    digit_matches = re.findall(r'(?<!\d)\d{4,8}(?!\d)', clean_text)
    if digit_matches:
        # যদি একাধিক থাকে, যেটা বড় সেটা নাও (সাধারণত OTP বড় হয়)
        return max(digit_matches, key=len)
    
    return None

def show_temp_mail_menu(chat_id, edit_msg_id=None):
    data = get_email_data(chat_id)
    if not data:
        txt = f"{PEM['msg']} <b>Temporary Email Service</b>\n\nYou don't have an email address yet.\nTap <b>Generate New</b> to create one."
        kb = {"inline_keyboard": [
            [{"text": "➕ Generate New", "icon_custom_emoji_id": "5352694861990501856", "callback_data": "email_gen", "style": "success"}],
            [{"text": "Close", "icon_custom_emoji_id": "5420130255174145507", "callback_data": "close_msg", "style": "danger"}]
        ]}
        if edit_msg_id:
            edit_message(chat_id, edit_msg_id, render_body_text(txt), reply_markup=kb)
        else:
            send_message(chat_id, render_body_text(txt), reply_markup=kb)
        return

    email = data['email']
    token = data['token']
    messages = fetch_messages(token)
    msg_count = len(messages)
    inbox_text = ""
    if messages:
        latest = messages[0]
        detail = fetch_message_detail(token, latest['id'])
        if detail:
            subject = detail.get('subject', 'No Subject')
            body = detail.get('text', detail.get('intro', ''))
            otp = extract_otp_code(body) or extract_otp_code(subject) or "None"
            inbox_text = f"📩 <b>{subject}</b>\n🔐 OTP: <code>{otp}</code>\n\n📝 {body[:100]}..."
    else:
        inbox_text = "📭 No messages yet."

    c_msg = bot_settings["custom_messages"].get("temp_mail", {})
    raw_txt = c_msg.get("text", "").replace("{email}", email).replace("{msg_count}", str(msg_count))
    if not raw_txt:
        raw_txt = f"{PEM['msg']} <b>Temporary Email Service</b>\n\n📧 <b>Your Email:</b> <code>{email}</code>\n📨 <b>Inbox Messages:</b> {msg_count}\n━━━━━━━━━━━━━━━━━━\n{inbox_text}"
    else:
        raw_txt += f"\n━━━━━━━━━━━━━━━━━━\n{inbox_text}"

    kb = {"inline_keyboard": [
        [{"text": "➕ Generate New", "icon_custom_emoji_id": "5352694861990501856", "callback_data": "email_gen", "style": "success"},
         {"text": "🗑 Delete", "icon_custom_emoji_id": "5422557736330106570", "callback_data": "email_del", "style": "danger"}],
        [{"text": "🔄 Refresh", "icon_custom_emoji_id": "5465368548702446780", "callback_data": "email_refresh", "style": "primary"}],
        [{"text": "Close", "icon_custom_emoji_id": "5420130255174145507", "callback_data": "close_msg", "style": "danger"}]
    ]}
    for b in c_msg.get("buttons", []):
        b_copy = b.copy()
        if "style" not in b_copy: b_copy["style"] = "primary"
        kb["inline_keyboard"].append([b_copy])

    if edit_msg_id:
        edit_message(chat_id, edit_msg_id, render_body_text(raw_txt), reply_markup=kb)
    else:
        send_message(chat_id, render_body_text(raw_txt), reply_markup=kb)

# ==================== AUTO EMAIL CHECKER (অটো নোটিফিকেশন) ====================
def auto_email_checker():
    while True:
        try:
            conn = get_db_conn()
            rows = conn.execute("SELECT user_id, email, token, last_msg_id FROM email_accounts").fetchall()
            for row in rows:
                user_id = row['user_id']
                email = row['email']
                token = row['token']
                last_msg_id = row['last_msg_id']
                messages = fetch_messages(token)
                if messages and messages[0]['id'] != last_msg_id:
                    msg = messages[0]
                    msg_id = msg['id']
                    detail = fetch_message_detail(token, msg_id)
                    if detail:
                        sender = detail.get('from', {}).get('address', 'Unknown')
                        subject = detail.get('subject', 'No Subject')
                        body = detail.get('text', detail.get('intro', ''))
                        otp = extract_otp_code(body) or extract_otp_code(subject) or "None"
                        markup = {"inline_keyboard": [[{"text": "Open in Browser ➡️", "url": "https://mail.tm/"}]]}
                        msg_text = (
                            f"📩 <b>New Email Received!</b>\n\n"
                            f"📧 From: <code>{sender}</code>\n"
                            f"📌 Subject: <b>{subject}</b>\n"
                            f"🔐 OTP: <code>{otp}</code>\n\n"
                            f"📝 Message:\n<code>{body[:500]}</code>"
                        )
                        try:
                            send_message(user_id, render_body_text(msg_text), reply_markup=markup)
                            update_last_msg_id(user_id, msg_id)
                        except:
                            pass
        except:
            pass
        time.sleep(5)

# ==================== LOAD/SAVE DB ====================
def load_db():
    global bot_settings, number_batches, used_numbers_list, total_uploaded_stats, total_assigned_stats, recent_traffic
    try:
        conn = get_db_conn()
        cursor = conn.execute("SELECT key, value FROM bot_config")
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                k, v = row['key'], row['value']
                if k in FS_KEYS:
                    bot_settings[k] = json.loads(v)
            print("✅ Config loaded from SQLite!")
        else:
            for k in FS_KEYS:
                conn.execute(
                    "INSERT OR REPLACE INTO bot_config (key, value) VALUES (?, ?)",
                    (k, json.dumps(bot_settings[k]))
                )
            conn.commit()
            print("✅ SQLite Config Initialized with defaults!")
    except Exception as e:
        print(f"❌ Error loading from SQLite: {e}")

    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding='utf-8') as f:
                data = json.load(f)
                saved_settings = data.get("bot_settings", {})
                for key, val in saved_settings.items():
                    if key not in FS_KEYS:
                        if key == "custom_messages":
                            for m_key, m_val in val.items():
                                bot_settings["custom_messages"][m_key] = m_val
                        else:
                            bot_settings[key] = val
                number_batches = data.get("number_batches", {})
                used_numbers_list = data.get("used_numbers_list", [])
                total_uploaded_stats = data.get("total_uploaded_stats", 0)
                total_assigned_stats = data.get("total_assigned_stats", 0)
                recent_traffic = data.get("recent_traffic", [])
                stex_assigned_numbers = data.get("stex_assigned_numbers", {})
                voltx_assigned_numbers = data.get("voltx_assigned_numbers", {})
            print("✅ Local Stock/UI DB Loaded Successfully!")
        except Exception as e:
            print(f"❌ Error loading local DB: {e}")

def save_local_db():
    local_data = {
        "bot_settings": {k: v for k, v in bot_settings.items() if k not in FS_KEYS},
        "number_batches": number_batches,
        "used_numbers_list": used_numbers_list,
        "total_uploaded_stats": total_uploaded_stats,
        "total_assigned_stats": total_assigned_stats,
        "recent_traffic": recent_traffic,
        "stex_assigned_numbers": stex_assigned_numbers,
        "voltx_assigned_numbers": voltx_assigned_numbers
    }
    try:
        with open(DB_FILE, "w", encoding='utf-8') as f:
            json.dump(local_data, f, indent=4)
    except Exception as e:
        pass

def _sync_fs():
    try:
        conn = get_db_conn()
        for k in FS_KEYS:
            if k in bot_settings:
                conn.execute(
                    "INSERT OR REPLACE INTO bot_config (key, value) VALUES (?, ?)",
                    (k, json.dumps(bot_settings[k]))
                )
        conn.commit()
    except: pass

def save_db():
    save_local_db()
    threading.Thread(target=_sync_fs, daemon=True).start()

load_db()

user_states = {}
temp_data = {}
user_cooldowns = {}
pending_withdrawals = {}

# ==================== TELEGRAM HELPERS ====================
tg_session = requests.Session()

def api_call(method, payload=None):
    url = f"{BASE_URL}/{method}"
    try:
        res = tg_session.post(url, json=payload, timeout=15)
        return res.json()
    except Exception as e:
        return {}

def send_message(chat_id, text, reply_markup=None, parse_mode="HTML"):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode, "disable_web_page_preview": True}
    if reply_markup: payload["reply_markup"] = reply_markup
    result = api_call("sendMessage", payload)
    if not result.get("ok"):
        print(f"❌ sendMessage FAILED to {chat_id}: {result}")
    else:
        print(f"✅ sendMessage OK to {chat_id}: msg_id={result.get('result',{}).get('message_id')}")
    return result

def edit_message(chat_id, message_id, text, reply_markup=None, parse_mode="HTML"):
    payload = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": parse_mode, "disable_web_page_preview": True}
    if reply_markup: payload["reply_markup"] = reply_markup
    result = api_call("editMessageText", payload)
    if not result.get("ok"):
        print(f"❌ editMessageText FAILED for {chat_id}/{message_id}: {result}", flush=True)
    return result

def delete_message(chat_id, message_id):
    return api_call("deleteMessage", {"chat_id": chat_id, "message_id": message_id})

def answer_callback(callback_id, text="", show_alert=False):
    api_call("answerCallbackQuery", {"callback_query_id": callback_id, "text": text, "show_alert": show_alert})

def send_document(chat_id, filename, text_content):
    url = f"{BASE_URL}/sendDocument"
    files = {'document': (filename, text_content)}
    data = {'chat_id': chat_id}
    try: requests.post(url, data=data, files=files)
    except: pass

# ==================== USER MANAGEMENT ====================
user_cache = {}

def get_user(user_id):
    user_id = str(user_id)
    if user_id in user_cache: return user_cache[user_id]
    conn = get_db_conn()
    row = conn.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
    if row:
        data = dict(row)
        data["banned"] = bool(data.get("banned", 0))
        data["verified"] = bool(data.get("verified", 0))
        data["ref_paid"] = bool(data.get("ref_paid", 0))
        user_cache[user_id] = data
        return data
    else:
        new_user = {"user_id": user_id, "balance": 0.0, "total_refers": 0, "total_otps": 0, "banned": False, "verified": False, "referred_by": None, "ref_paid": False}
        conn.execute("INSERT OR IGNORE INTO users (user_id, balance, total_refers, total_otps, banned, verified) VALUES (?, 0.0, 0, 0, 0, 0)", (user_id,))
        conn.commit()
        user_cache[user_id] = new_user
        return new_user

def update_balance(user_id, amount):
    user_id = str(user_id)
    if user_id in user_cache:
        user_cache[user_id]["balance"] = user_cache[user_id].get("balance", 0.0) + float(amount)
    try:
        conn = get_db_conn()
        get_user(user_id)
        conn.execute("UPDATE users SET balance = balance + ? WHERE user_id=?", (float(amount), user_id))
        conn.commit()
    except: pass

def increment_total_refers(user_id):
    user_id = str(user_id)
    if user_id in user_cache:
        user_cache[user_id]["total_refers"] = user_cache[user_id].get("total_refers", 0) + 1
    try:
        conn = get_db_conn()
        get_user(user_id)
        conn.execute("UPDATE users SET total_refers = total_refers + 1 WHERE user_id=?", (user_id,))
        conn.commit()
    except: pass

def increment_total_otps(user_id):
    user_id = str(user_id)
    if user_id in user_cache:
        user_cache[user_id]["total_otps"] = user_cache[user_id].get("total_otps", 0) + 1
    try:
        conn = get_db_conn()
        get_user(user_id)
        conn.execute("UPDATE users SET total_otps = total_otps + 1 WHERE user_id=?", (user_id,))
        conn.commit()
    except: pass

def add_referral(inviter_id, new_user_id):
    conn = get_db_conn()
    row = conn.execute("SELECT 1 FROM users WHERE user_id=?", (str(new_user_id),)).fetchone()
    if not row:
        get_user(new_user_id) 
        reward = bot_settings.get("refer_reward", 0.2)
        update_balance(inviter_id, reward)
        increment_total_refers(inviter_id)
        ref_msg = (
            f"{PEM['gift']} <b>New Referral !</b>\n"
            f"------------------\n"
            f"🔥 <b>You Received {reward} TK</b>\n"
            f"------------------\n"
            f"{PEM['user']} <b>From User ID:</b> <code>{new_user_id}</code>"
        )
        send_message(inviter_id, render_body_text(ref_msg))

# ==================== 🔥 মেনু (শুধু TEMP MAIL + SUPPORT) ====================
def get_cancel_kb():
    return {"inline_keyboard": [[{"text": "Cancel", "icon_custom_emoji_id": "5267490665117275176", "callback_data": "cancel_state", "style": "danger"}]]}

def main_menu(user_id):
    kb = [
        [{"text": "📧 TEMP MAIL", "icon_custom_emoji_id": "5352694861990501856", "style": "primary"}],
        [{"text": "SUPPORT", "icon_custom_emoji_id": "5420145051336485498", "style": "primary"}]
    ]
    if is_admin(user_id): 
        kb.append([{"text": "Admin Panel", "icon_custom_emoji_id": "5420155432272438703", "style": "danger"}])
    return {"keyboard": kb, "resize_keyboard": True}

def get_admin_text():
    users_count = len(all_known_users)
    txt = f"""
{PEM['admin']} <b>ADMIN CONTROL PANEL</b> {PEM['admin']}
━━━━━━━━━━━━━━━━━━
{PEM['graph']} <b>DATABASE OVERVIEW</b>
— — — — — — — — — —
{PEM['user']} Users      » {users_count}
━━━━━━━━━━━━━━━━━━
"""
    return render_body_text(txt)

def admin_panel_keyboard():
    return {"inline_keyboard": [
        [{"text": "LEADER BOARD SYSTEM", "icon_custom_emoji_id": "5353032893096567467", "callback_data": "lb_main", "style": "success"}],
        [{"text": "Broadcast", "icon_custom_emoji_id": "5789428375261023681", "callback_data": "broadcast_msg", "style": "success"},
         {"text": "System", "icon_custom_emoji_id": "5420155432272438703", "callback_data": "system_settings", "style": "primary"}],
        [{"text": "User Management", "icon_custom_emoji_id": "5193063022226086560", "callback_data": "user_management", "style": "primary"},
         {"text": "Premium Emoji", "icon_custom_emoji_id": "5352552689983067014", "callback_data": "manage_emojis", "style": "success"}],
        [{"text": "🎨 Menu Design", "icon_custom_emoji_id": "5190751148704833975", "callback_data": "menu_design_list", "style": "primary"}],
        [{"text": "Close", "icon_custom_emoji_id": "5420130255174145507", "callback_data": "close_msg", "style": "danger"}]
    ]}

def system_settings_keyboard():
    return {"inline_keyboard": [
        [{"text": "Force Join System", "icon_custom_emoji_id": "5420517437885943844", "callback_data": "manage_fj", "style": "primary"},
         {"text": "Admin Management", "icon_custom_emoji_id": "5420145051336485498", "callback_data": "manage_admins", "style": "danger"}],
        [{"text": "OTP Group", "icon_custom_emoji_id": "5190447043545438788", "callback_data": "manage_otp_groups", "style": "danger"},
         {"text": "User Management", "icon_custom_emoji_id": "5193063022226086560", "callback_data": "user_management", "style": "primary"}],
        [{"text": "DXA Control", "icon_custom_emoji_id": "5193100774988617665", "callback_data": "dxa_control", "style": "primary"},
         {"text": "Premium Emoji", "icon_custom_emoji_id": "5352552689983067014", "callback_data": "manage_emojis", "style": "success"}],
        [{"text": "🎨 Menu Design", "icon_custom_emoji_id": "5190751148704833975", "callback_data": "menu_design_list", "style": "primary"}],
        [{"text": "Back", "icon_custom_emoji_id": "5267490665117275176", "callback_data": "back_to_admin", "style": "danger"}]
    ]}

def get_user_management_text():
    total = len(all_known_users)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    txt = f"""➖➖➖➖➖➖➖➖
《 👋 USER VIEW 》
➖➖➖➖➖➖➖➖
📊 LIVE STATISTICS:
➖➖➖➖➖➖➖➖
🫂 TOTAL USERS: {total}
➖➖➖➖➖➖➖➖
⌛ UPDATED: {now_str}"""
    return render_body_text(txt)

def user_management_keyboard():
    return {"inline_keyboard": [
        [{"text": "Manage Balance", "icon_custom_emoji_id": "5190576863226933563", "callback_data": "um_manage_balance", "style": "primary"},
         {"text": "Ban/Unban User", "icon_custom_emoji_id": "5334807341109908955", "callback_data": "um_ban_unban", "style": "danger"}],
        [{"text": "User Profile", "icon_custom_emoji_id": "5352861489541714456", "callback_data": "um_user_profile", "style": "success"}],
        [{"text": "Back", "icon_custom_emoji_id": "5267490665117275176", "callback_data": "system_settings", "style": "primary"}]
    ]}

# ==================== 🎨 MENU DESIGN (সম্পূর্ণ) ====================
def menu_design_list_keyboard():
    return {"inline_keyboard": [
        [{"text": "Edit /start Menu", "icon_custom_emoji_id": "5395444784611480792", "callback_data": "md_edit_start", "style": "primary"}],
        [{"text": "Edit TEMP MAIL", "icon_custom_emoji_id": "5337132498965010628", "callback_data": "md_edit_temp_mail", "style": "success"}],
        [{"text": "Edit SUPPORT", "icon_custom_emoji_id": "5420145051336485498", "callback_data": "md_edit_support", "style": "danger"}],
        [{"text": "Reset Defaults", "icon_custom_emoji_id": "5192812028632274956", "callback_data": "md_reset_defaults", "style": "success"}],
        [{"text": "Back", "icon_custom_emoji_id": "5267490665117275176", "callback_data": "system_settings", "style": "primary"}]
    ]}

def menu_edit_options_keyboard(menu_key):
    return {"inline_keyboard": [
        [{"text": "Edit Body (Text)", "icon_custom_emoji_id": "5395444784611480792", "callback_data": f"md_text_{menu_key}", "style": "primary"}],
        [{"text": "Edit Inline Buttons", "icon_custom_emoji_id": "5420155432272438703", "callback_data": f"md_btns_{menu_key}", "style": "success"}],
        [{"text": "Back to Menus", "icon_custom_emoji_id": "5267490665117275176", "callback_data": "menu_design_list", "style": "danger"}]
    ]}

def menu_buttons_list_keyboard(menu_key):
    kb = []
    btns = bot_settings["custom_messages"].get(menu_key, {}).get("buttons", [])
    for idx, btn in enumerate(btns):
        kb.append([{"text": f"Del: {btn['text']}", "icon_custom_emoji_id": "5420130255174145507", "callback_data": f"md_delbtn_{menu_key}_{idx}", "style": "danger"}])
    kb.append([{"text": "Add Inline Button", "icon_custom_emoji_id": "5420323438508155202", "callback_data": f"md_addbtn_{menu_key}", "style": "success"}])
    kb.append([{"text": "Back", "icon_custom_emoji_id": "5267490665117275176", "callback_data": f"md_edit_{menu_key}", "style": "primary"}])
    return {"inline_keyboard": kb}

def emoji_settings_keyboard():
    return {"inline_keyboard": [
        [{"text": "Upload Flags (TXT)", "icon_custom_emoji_id": "5353001161878182134", "callback_data": "up_flags_txt", "style": "primary"},
         {"text": "Download Flags", "icon_custom_emoji_id": "5257969839313526622", "callback_data": "dl_flags_txt", "style": "success"}],
        [{"text": "Upload Services (TXT)", "icon_custom_emoji_id": "5353001161878182134", "callback_data": "up_apps_txt", "style": "primary"},
         {"text": "Download Services", "icon_custom_emoji_id": "5257969839313526622", "callback_data": "dl_apps_txt", "style": "success"}],
        [{"text": "Delete All Flags", "icon_custom_emoji_id": "5422557736330106570", "callback_data": "del_all_flags", "style": "danger"},
         {"text": "Add Single Emoji", "icon_custom_emoji_id": "5420323438508155202", "callback_data": "add_single_emoji", "style": "success"}],
        [{"text": "Back", "icon_custom_emoji_id": "5267490665117275176", "callback_data": "system_settings", "style": "danger"}]
    ]}

def fj_settings_keyboard():
    status_text = 'ON' if bot_settings['fj_on'] else 'OFF'
    status_icon = "5352694861990501856" if bot_settings['fj_on'] else "5318840353510408444"
    kb = [[{"text": f"STATUS: {status_text}", "icon_custom_emoji_id": status_icon, "callback_data": "toggle_fj", "style": "primary"}]]
    for idx, ch in enumerate(bot_settings["fj_channels"]):
        kb.append([{"text": f"Delete: {ch}", "icon_custom_emoji_id": "5420130255174145507", "callback_data": f"del_fj_{idx}", "style": "danger"}])
    kb.append([{"text": "Add Channel", "icon_custom_emoji_id": "5420323438508155202", "callback_data": "add_fj", "style": "success"}])
    kb.append([{"text": "Back", "icon_custom_emoji_id": "5267490665117275176", "callback_data": "system_settings", "style": "primary"}])
    return {"inline_keyboard": kb}

def admin_settings_keyboard():
    kb = []
    for idx, adm in enumerate(bot_settings["admins"]):
        text_btn = f"Owner: {adm}" if adm == OWNER_ID else f"Delete: {adm}"
        icon_id = "5353032893096567467" if adm == OWNER_ID else "5420130255174145507"
        cb_data = "ignore" if adm == OWNER_ID else f"del_adm_{idx}"
        kb.append([{"text": text_btn, "icon_custom_emoji_id": icon_id, "callback_data": cb_data, "style": "danger" if adm != OWNER_ID else "primary"}])
    kb.append([{"text": "Add Admin", "icon_custom_emoji_id": "5420323438508155202", "callback_data": "add_adm", "style": "success"}])
    kb.append([{"text": "Back", "icon_custom_emoji_id": "5267490665117275176", "callback_data": "system_settings", "style": "primary"}])
    return {"inline_keyboard": kb}

def otp_groups_list_keyboard():
    kb = [[{"text": "Edit OTP Button Link", "icon_custom_emoji_id": "5420517437885943844", "callback_data": "edit_otp_link", "style": "primary"}]]
    for idx, fg in enumerate(bot_settings["fw_groups"]):
        kb.append([{"text": f"Group: {fg['chat_id']}", "icon_custom_emoji_id": "5193063022226086560", "callback_data": f"manage_fw_{idx}", "style": "primary"}])
    kb.append([{"text": "Add Forward Group", "icon_custom_emoji_id": "5420323438508155202", "callback_data": "add_fw", "style": "success"}])
    kb.append([{"text": "Back", "icon_custom_emoji_id": "5267490665117275176", "callback_data": "system_settings", "style": "danger"}])
    return {"inline_keyboard": kb}

def dxa_control_keyboard():
    w_status = "ON" if bot_settings["withdraw_on"] else "OFF"
    return {"inline_keyboard": [
        [{"text": f"WITHDRAW: {w_status}", "icon_custom_emoji_id": "5348469219761626211", "callback_data": "dxa_toggle_w", "style": "primary"}],
        [{"text": f"MIN WITHDRAW: {bot_settings['min_withdraw']}", "icon_custom_emoji_id": "5352877703043258544", "callback_data": "dxa_min_w", "style": "success"},
         {"text": f"OTP REWARD: {bot_settings['otp_reward']}", "icon_custom_emoji_id": "5190576863226933563", "callback_data": "dxa_otp_r", "style": "primary"}],
        [{"text": f"REFER REWARD: {bot_settings['refer_reward']}", "icon_custom_emoji_id": "5420396762189831222", "callback_data": "dxa_ref_r", "style": "success"},
         {"text": f"COOLDOWN: {bot_settings['cooldown']}s", "icon_custom_emoji_id": "5337172996211648018", "callback_data": "dxa_cool", "style": "primary"}],
        [{"text": f"NUM/REQ: {bot_settings['num_req']}", "icon_custom_emoji_id": "5337132498965010628", "callback_data": "dxa_num_req", "style": "success"},
         {"text": f"NUM/SHARE: {bot_settings['num_share']}", "icon_custom_emoji_id": "5352862640592949843", "callback_data": "dxa_num_share", "style": "primary"}],
        [{"text": f"SUPPORT LINK: {'ON' if bot_settings.get('support_link') else 'OFF'}", "icon_custom_emoji_id": "5420145051336485498", "callback_data": "dxa_sup_link", "style": "success"},
         {"text": "W. METHODS", "icon_custom_emoji_id": "5190899075968441286", "callback_data": "manage_w_methods", "style": "primary"}],
        [{"text": f"W. GROUP: {'ON' if bot_settings.get('w_group') else 'OFF'}", "icon_custom_emoji_id": "5420517437885943844", "callback_data": "dxa_w_group", "style": "success"},
         {"text": f"PROOF GROUP: {'ON' if bot_settings.get('proof_group') else 'OFF'}", "icon_custom_emoji_id": "5420517437885943844", "callback_data": "dxa_proof_group", "style": "success"}],
        [{"text": "BACK", "icon_custom_emoji_id": "5267490665117275176", "callback_data": "system_settings", "style": "danger"}]
    ]}

def w_methods_keyboard():
    kb = []
    for idx, m in enumerate(bot_settings["w_methods"]):
        kb.append([{"text": f"Delete: {m}", "icon_custom_emoji_id": "5420130255174145507", "callback_data": f"del_wm_{idx}", "style": "danger"}])
    kb.append([{"text": "Add Method", "icon_custom_emoji_id": "5420323438508155202", "callback_data": "add_wm", "style": "success"}])
    kb.append([{"text": "Back", "icon_custom_emoji_id": "5267490665117275176", "callback_data": "dxa_control", "style": "primary"}])
    return {"inline_keyboard": kb}

# ==================== PANEL RELATED (ব্যাকগ্রাউন্ড) ====================
def typed_panels_list_keyboard(p_type):
    return {"inline_keyboard": [[{"text": "Back", "callback_data": "system_settings"}]]}
def panel_config_keyboard(idx):
    return {"inline_keyboard": [[{"text": "Back", "callback_data": "system_settings"}]]}
def build_traffic_ui():
    return "📊 Traffic", {"inline_keyboard": [[{"text": "Close", "callback_data": "close_msg"}]]}

# ==================== HELPERS (বাকি) ====================
def parse_panel_response(response_text, p_config=None):
    return []

def fetch_cpt_panel_cdrs(p, session, check_url):
    return [], ""

def attempt_auto_login(p, idx):
    return False

def panel_monitor_thread():
    while True:
        time.sleep(5)

def global_sms_listener():
    while True:
        time.sleep(5)

def voltx_sms_listener():
    while True:
        time.sleep(5)

def voltx_console_listener():
    while True:
        time.sleep(10)

def detect_service(text):
    return None

def get_service_info_html(service_text, msg_text=""):
    return "Service", "📱"

def detect_language(text):
    return "#EN"

LANG_MAP = {"#EN": "English"}

def iso_to_unicode_flag(iso):
    if not iso or len(iso) != 2 or not iso.isalpha(): return "🌍"
    iso = iso.upper()
    return chr(0x1F1E6 + (ord(iso[0]) - ord('A'))) + chr(0x1F1E6 + (ord(iso[1]) - ord('A')))

def get_flag_info_from_num(num):
    return "🌍", "XX", None

def get_flag_and_code(num):
    return "🌍", "XX"

def get_flag_info_html(num_or_iso, return_full_name=False):
    return "🌍"

def mask_number(num):
    return num

def render_body_text(text):
    if not text: return str(text)
    parts = re.split(r'(<tg-emoji.*?</tg-emoji>)', str(text))
    for i in range(len(parts)):
        if not parts[i].startswith('<tg-emoji'):
            for normal_emj, prem_id in GLOBAL_BODY_EMOJIS.items():
                if normal_emj in parts[i]:
                    parts[i] = parts[i].replace(normal_emj, f'<tg-emoji emoji-id="{prem_id}">{normal_emj}</tg-emoji>')
    return "".join(parts)

def parse_chat_id(text):
    text = text.strip()
    if text.startswith("-100") or (text.startswith("-") and text[1:].isdigit()):
        return text
    if "t.me/" in text:
        parts = text.split("/")
        username = parts[-1]
        if username: return "@" + username if not username.startswith("@") else username
    if text.startswith("@"):
        return text
    return "@" + text

def is_admin(user_id):
    return user_id in bot_settings["admins"] or user_id == OWNER_ID

def check_force_join(user_id):
    if not bot_settings["fj_on"] or not bot_settings["fj_channels"]: return True
    if is_admin(user_id): return True
    for ch in bot_settings["fj_channels"]:
        res = api_call("getChatMember", {"chat_id": ch, "user_id": user_id})
        if res.get("ok") and res["result"]["status"] not in ["left", "kicked"]: continue
        else: return False
    return True

def send_force_join_msg(chat_id):
    kb = []
    for ch in bot_settings["fj_channels"]:
        url = f"https://t.me/{ch.replace('@', '')}" if ch.startswith("@") else ch
        kb.append([{"text": f"Join Channel", "icon_custom_emoji_id": "5789428375261023681", "url": url, "style": "primary"}])
    kb.append([{"text": "Check Joined", "icon_custom_emoji_id": "5352694861990501856", "callback_data": "check_fj", "style": "success"}])
    send_message(chat_id, render_body_text(f"{PEM['warn']} <b>Please join our channels to use the bot!</b>"), reply_markup={"inline_keyboard": kb})

def is_user_banned(user_id):
    if is_admin(user_id): return False
    if user_id in user_banned_cache and time.time() - user_banned_cache[user_id]['time'] < 60:
        return user_banned_cache[user_id]['banned']
    try:
        conn = get_db_conn()
        cursor = conn.execute("SELECT banned FROM users WHERE user_id = ?", (str(user_id),))
        row = cursor.fetchone()
        banned = bool(row['banned']) if row else False
    except:
        banned = False
    user_banned_cache[user_id] = {'banned': banned, 'time': time.time()}
    return banned

all_known_users = set()
def sync_users_list():
    global all_known_users
    try:
        if os.path.exists("users_list.json"):
            with open("users_list.json", "r") as f:
                all_known_users = set(json.load(f))
        if not all_known_users:
            conn = get_db_conn()
            cursor = conn.execute("SELECT user_id FROM users")
            for row in cursor.fetchall():
                all_known_users.add(row['user_id'])
            with open("users_list.json", "w") as f:
                json.dump(list(all_known_users), f)
    except: pass
threading.Thread(target=sync_users_list, daemon=True).start()

def _save_users_list():
    try:
        with open("users_list.json", "w") as f:
            json.dump(list(all_known_users), f)
    except: pass

def register_user_local(uid):
    uid_str = str(uid)
    if uid_str not in all_known_users:
        all_known_users.add(uid_str)
        threading.Thread(target=_save_users_list, daemon=True).start()

user_active_sessions = {}

# ==================== MESSAGE HANDLER ====================
def handle_message(msg):
    try:
        _handle_message_inner(msg)
    except Exception as e:
        import traceback
        print(f"💥 handle_message CRASH: {e}\n{traceback.format_exc()}")

def _handle_message_inner(msg):
    global total_uploaded_stats
    chat_id = msg["chat"]["id"]
    chat_type = msg["chat"].get("type", "private")
    if chat_type != "private":
        return
    text = msg.get("text", "")
    print(f"🔍 Processing: chat_id={chat_id}, text={text[:30]!r}")
    register_user_local(chat_id)
    if is_user_banned(chat_id):
        send_message(chat_id, render_body_text("🚫 <b>You are banned from using this bot!</b>\nIf you think this is a mistake, please contact support."))
        return
    if text.startswith("/start"):
        parts = text.split()
        if len(parts) > 1 and parts[1].isdigit():
            inviter = int(parts[1])
            if inviter != chat_id:
                conn = get_db_conn()
                row = conn.execute("SELECT 1 FROM users WHERE user_id=?", (str(chat_id),)).fetchone()
                if not row:
                    get_user(chat_id)
                    conn.execute("UPDATE users SET referred_by=?, ref_paid=0 WHERE user_id=?", (str(inviter), str(chat_id)))
                    conn.commit()
                    if str(chat_id) in user_cache:
                        user_cache[str(chat_id)]["referred_by"] = str(inviter)
                        user_cache[str(chat_id)]["ref_paid"] = False
    if not check_force_join(chat_id):
        send_force_join_msg(chat_id)
        return
    MAIN_MENU_CMDS = ["📧 TEMP MAIL", "SUPPORT", "Admin Panel"]
    is_main_cmd = False
    if text in MAIN_MENU_CMDS or text.startswith("/start"):
        if chat_id in user_states: del user_states[chat_id]
        if chat_id in temp_data: del temp_data[chat_id]
        is_main_cmd = True

    if chat_id in user_states and not is_main_cmd:
        state = user_states[chat_id]
        # স্টেট হ্যান্ডলিং (মেনু ডিজাইন, অ্যাডমিন অ্যাড, ব্রডকাস্ট)
        if state == "wait_for_menu_text":
            try:
                menu_key = temp_data[chat_id]["menu_key"]
                formatted_html_text = extract_premium_html(msg)
                bot_settings["custom_messages"][menu_key]["text"] = formatted_html_text
                save_db()
                delete_message(chat_id, msg["message_id"])
                preview_text = render_body_text(formatted_html_text)
                success_text = f"{PEM['ok']} <b>Message Body Updated successfully!</b>\n\n🎨 <b>Editing: {menu_key.upper()}</b>\n\nPreview of current Text:\n{preview_text}"
                edit_message(chat_id, temp_data[chat_id]["msg_id"], render_body_text(success_text), reply_markup=menu_edit_options_keyboard(menu_key))
            except Exception as e:
                send_message(chat_id, f"❌ Error saving text: {e}")
            finally:
                if chat_id in user_states: del user_states[chat_id]
                if chat_id in temp_data: del temp_data[chat_id]
            return

        elif state == "wait_for_menu_btn":
            try:
                menu_key = temp_data[chat_id]["menu_key"]
                if "-" in text:
                    parts = text.split("-", 1)
                    btn_text = parts[0].strip()
                    btn_url = parts[1].strip()
                    emoji_id = None
                    emoji_char = ""
                    for ent in msg.get("entities", []):
                        if ent.get("type") == "custom_emoji":
                            emoji_id = ent.get("custom_emoji_id")
                            offset = ent.get("offset", 0)
                            length = ent.get("length", 0)
                            b_text = text.encode('utf-16-le')
                            emoji_char = b_text[offset*2:(offset+length)*2].decode('utf-16-le')
                            break
                    if emoji_char:
                        btn_text = btn_text.replace(emoji_char, "").strip()
                    btn_data = {"text": btn_text, "url": btn_url, "style": "primary"}
                    if emoji_id:
                        btn_data["icon_custom_emoji_id"] = emoji_id
                    bot_settings["custom_messages"][menu_key]["buttons"].append(btn_data)
                    save_db()
                    delete_message(chat_id, msg["message_id"])
                    edit_message(chat_id, temp_data[chat_id]["msg_id"], render_body_text(f"{PEM['gear']} <b>Edit Inline Buttons: {menu_key.upper()}</b>"), reply_markup=menu_buttons_list_keyboard(menu_key))
                else:
                    send_message(chat_id, render_body_text(f"{PEM['no']} Invalid format. Use <code>Button Text - https://link.com</code>"))
            except Exception as e:
                pass
            finally:
                if chat_id in user_states: del user_states[chat_id]
                if chat_id in temp_data: del temp_data[chat_id]
            return

        elif state == "wait_for_admin_id":
            if text and text.isdigit():
                new_admin = int(text)
                if new_admin not in bot_settings["admins"]:
                    bot_settings["admins"].append(new_admin)
                    save_db()
                    send_message(chat_id, render_body_text(f"✅ Admin added successfully!\nUser ID: {new_admin}"))
                else:
                    send_message(chat_id, render_body_text(f"⚠️ User {new_admin} is already an admin."))
            else:
                send_message(chat_id, render_body_text("❌ Invalid User ID! Please send a numeric ID."))
            del user_states[chat_id]
            if chat_id in temp_data: del temp_data[chat_id]
            return

        elif state == "wait_for_broadcast":
            msg_id = msg["message_id"]
            send_message(chat_id, render_body_text(f"{PEM['ok']} Broadcast started..."))
            threading.Thread(target=broadcast_copymessage, args=(chat_id, msg_id)).start()
            del user_states[chat_id]
            return

        elif state == "wait_for_add_fj":
            bot_settings["fj_channels"].append(parse_chat_id(text))
            save_db()
            delete_message(chat_id, msg["message_id"])
            edit_message(chat_id, temp_data[chat_id]["msg_id"], render_body_text("🔗 <b>FORCE JOIN SYSTEM</b>\nManage channels below:"), reply_markup=fj_settings_keyboard())
            del user_states[chat_id]
            del temp_data[chat_id]
            return

        elif state == "wait_for_add_wm":
            bot_settings["w_methods"].append(text.strip())
            save_db()
            delete_message(chat_id, msg["message_id"])
            edit_message(chat_id, temp_data[chat_id]["msg_id"], render_body_text("💳 <b>WITHDRAWAL METHODS</b>"), reply_markup=w_methods_keyboard())
            del user_states[chat_id]
            del temp_data[chat_id]
            return

        elif state == "wait_for_add_fw_id":
            bot_settings["fw_groups"].append({"chat_id": text.strip(), "buttons": []})
            save_db()
            delete_message(chat_id, msg["message_id"])
            edit_message(chat_id, temp_data[chat_id]["msg_id"], render_body_text("🛡 <b>OTP GROUP MANAGEMENT</b>"), reply_markup=otp_groups_list_keyboard())
            del user_states[chat_id]
            del temp_data[chat_id]
            return

        elif state == "wait_for_otp_link":
            bot_settings["otp_link"] = text.strip()
            save_db()
            delete_message(chat_id, msg["message_id"])
            edit_message(chat_id, temp_data[chat_id]["msg_id"], render_body_text("🛡 <b>OTP GROUP MANAGEMENT</b>"), reply_markup=otp_groups_list_keyboard())
            del user_states[chat_id]
            del temp_data[chat_id]
            return

        elif state == "wait_for_add_fw_btn":
            fw_idx = temp_data[chat_id]["fw_idx"]
            if "-" in text:
                parts = text.split("-", 1)
                btn_text = parts[0].strip()
                btn_url = parts[1].strip()
                emoji_id = None
                emoji_char = ""
                for ent in msg.get("entities", []):
                    if ent.get("type") == "custom_emoji":
                        emoji_id = ent.get("custom_emoji_id")
                        offset = ent.get("offset", 0)
                        length = ent.get("length", 0)
                        b_text = text.encode('utf-16-le')
                        emoji_char = b_text[offset*2:(offset+length)*2].decode('utf-16-le')
                        break
                if emoji_char:
                    btn_text = btn_text.replace(emoji_char, "").strip()
                btn_data = {"text": btn_text, "url": btn_url}
                if emoji_id:
                    btn_data["icon_custom_emoji_id"] = emoji_id
                bot_settings["fw_groups"][fw_idx]["buttons"].append(btn_data)
                save_db()
            delete_message(chat_id, msg["message_id"])
            edit_message(chat_id, temp_data[chat_id]["msg_id"], render_body_text(f"🛡 <b>Manage Group:</b> {bot_settings['fw_groups'][fw_idx]['chat_id']}"), reply_markup=specific_fw_group_keyboard(fw_idx))
            del user_states[chat_id]
            del temp_data[chat_id]
            return

        elif state == "wait_for_2fa_key":
            # 2FA স্টেট (পুরনো)
            pass

    # ---- Commands ----
    if text.startswith("/start"):
        get_user(chat_id)
        u_data = get_user(chat_id)
        if u_data.get("referred_by") and not u_data.get("ref_paid"):
            inviter = u_data["referred_by"]
            conn = get_db_conn()
            conn.execute("UPDATE users SET ref_paid=1 WHERE user_id=?", (str(chat_id),))
            conn.commit()
            if str(chat_id) in user_cache: user_cache[str(chat_id)]["ref_paid"] = True
            reward = bot_settings.get("refer_reward", 0.2)
            get_user(inviter)
            update_balance(inviter, reward)
            increment_total_refers(inviter)
            ref_msg = (
                f"{PEM['gift']} <b>New Referral !</b>\n"
                f"------------------\n"
                f"🔥 <b>You Received {reward} TK</b>\n"
                f"------------------\n"
                f"{PEM['user']} <b>From User ID:</b> <code>{chat_id}</code>"
            )
            send_message(inviter, render_body_text(ref_msg))
        c_msg = bot_settings["custom_messages"].get("start", {})
        txt = render_body_text(c_msg.get("text", f"{PEM['hi']} Welcome!"))
        kb = []
        for b in c_msg.get("buttons", []):
            b_copy = b.copy()
            if "style" not in b_copy: b_copy["style"] = "primary"
            kb.append([b_copy])
        if kb:
            send_message(chat_id, txt, reply_markup={"inline_keyboard": kb})
            send_message(chat_id, render_body_text(f"{PEM['gear']} Navigation Menu:"), reply_markup=main_menu(chat_id))
        else:
            send_message(chat_id, txt, reply_markup=main_menu(chat_id))

    elif text == "📧 TEMP MAIL":
        show_temp_mail_menu(chat_id)

    elif text == "SUPPORT":
        c_msg = bot_settings["custom_messages"].get("support", {})
        txt = render_body_text(c_msg.get("text", f"{PEM['msg']} Support"))
        if not txt.strip(): txt = render_body_text(f"{PEM['msg']} Support")
        kb = []
        for b in c_msg.get("buttons", []):
            b_copy = b.copy()
            if "style" not in b_copy: b_copy["style"] = "primary"
            kb.append([b_copy])
        sup_link = bot_settings.get("support_link", "")
        if sup_link:
            kb.insert(0, [{"text": "Contact Support", "icon_custom_emoji_id": "5337302974806922068", "url": sup_link, "style": "success"}])
        kb.append([{"text": "Close", "icon_custom_emoji_id": "5420130255174145507", "callback_data": "close_msg", "style": "danger"}])
        send_message(chat_id, txt, reply_markup={"inline_keyboard": kb} if kb else None)

    elif text == "Admin Panel" and is_admin(chat_id):
        send_message(chat_id, get_admin_text(), reply_markup=admin_panel_keyboard())

# ==================== CALLBACK HANDLER ====================
def handle_callback(call):
    global total_assigned_stats
    chat_id = call["message"]["chat"]["id"]
    chat_type = call["message"]["chat"].get("type", "private")
    data = call.get("data", "")
    if not data.startswith("test_p_conn_") and not data.startswith("c_n_") and not data.startswith("g_c_"):
        try: threading.Thread(target=answer_callback, args=(call["id"],)).start()
        except: pass
    if chat_type != "private" and not (data.startswith("wapp_") or data.startswith("wrej_")):
        return
    msg_id = call["message"]["message_id"]
    if chat_type == "private":
        if is_user_banned(chat_id):
            answer_callback(call["id"], "🚫 You are banned from using this bot!", show_alert=True)
            return
        if not check_force_join(chat_id) and data != "check_fj":
            send_force_join_msg(chat_id)
            return

    # ---------- EMAIL FEATURE ----------
    if data == "email_gen":
        answer_callback(call["id"], "⏳ Creating new email...", show_alert=False)
        delete_email_data(chat_id)
        email, token = create_mail_tm_account(chat_id)
        if email and token:
            save_email_data(chat_id, email, token)
            send_message(chat_id, render_body_text(f"{PEM['ok']} Email created successfully!\n📧 <code>{email}</code>"))
            show_temp_mail_menu(chat_id, edit_msg_id=msg_id)
        else:
            send_message(chat_id, render_body_text(f"{PEM['no']} Failed to create email. Please try again."))

    elif data == "email_del":
        delete_email_data(chat_id)
        answer_callback(call["id"], "🗑 Email deleted!", show_alert=True)
        show_temp_mail_menu(chat_id, edit_msg_id=msg_id)

    elif data == "email_refresh":
        show_temp_mail_menu(chat_id, edit_msg_id=msg_id)
        answer_callback(call["id"], "🔄 Inbox refreshed!", show_alert=False)

    # ---------- 🎨 MENU DESIGN ----------
    elif data == "menu_design_list":
        edit_message(chat_id, msg_id, render_body_text(f"🎨 <b>Menu Design Editor</b>\n\nSelect a menu block to edit its Body Text and Inline Buttons."), reply_markup=menu_design_list_keyboard())

    elif data == "md_reset_defaults":
        bot_settings["custom_messages"] = DEFAULT_CUSTOM_MESSAGES.copy()
        save_db()
        answer_callback(call["id"], "✅ Resetted to Defaults!", show_alert=True)

    elif data.startswith("md_edit_"):
        answer_callback(call["id"])
        if chat_id in user_states: del user_states[chat_id]
        if chat_id in temp_data: del temp_data[chat_id]
        key = data.replace("md_edit_", "")
        cm_text = render_body_text(bot_settings["custom_messages"].get(key, {}).get("text", "..."))
        try:
            edit_message(chat_id, msg_id, render_body_text(f"🎨 <b>Editing: {key.upper()}</b>\n\nPreview of current Text:\n{cm_text}"), reply_markup=menu_edit_options_keyboard(key))
        except: pass

    elif data.startswith("md_text_"):
        key = data.replace("md_text_", "")
        user_states[chat_id] = "wait_for_menu_text"
        temp_data[chat_id] = {"msg_id": msg_id, "menu_key": key}
        edit_message(chat_id, msg_id, render_body_text(f"📝 <b>Edit Body: {key.upper()}</b>\n\nSend the new text.\n(Use HTML like <b>bold</b>, <i>italic</i>)"), reply_markup={"inline_keyboard": [[{"text": "Cancel", "callback_data": f"md_edit_{key}", "style": "danger"}]]})

    elif data.startswith("md_btns_"):
        answer_callback(call["id"])
        if chat_id in user_states: del user_states[chat_id]
        if chat_id in temp_data: del temp_data[chat_id]
        key = data.replace("md_btns_", "")
        try:
            edit_message(chat_id, msg_id, render_body_text(f"⚙️ <b>Edit Inline Buttons: {key.upper()}</b>"), reply_markup=menu_buttons_list_keyboard(key))
        except: pass

    elif data.startswith("md_addbtn_"):
        key = data.replace("md_addbtn_", "")
        user_states[chat_id] = "wait_for_menu_btn"
        temp_data[chat_id] = {"msg_id": msg_id, "menu_key": key}
        edit_message(chat_id, msg_id, render_body_text(f"➕ <b>Add Button: {key.upper()}</b>\n\nSend in format:\n<code>Button Text - https://link.com</code>"), reply_markup={"inline_keyboard": [[{"text": "Cancel", "callback_data": f"md_btns_{key}", "style": "danger"}]]})

    elif data.startswith("md_delbtn_"):
        parts = data.split("_")
        key = parts[2]
        b_idx = int(parts[3])
        if b_idx < len(bot_settings["custom_messages"][key]["buttons"]):
            del bot_settings["custom_messages"][key]["buttons"][b_idx]
            save_db()
            answer_callback(call["id"], "✅ Button Deleted!", show_alert=True)
            edit_message(chat_id, msg_id, render_body_text(f"⚙️ <b>Edit Inline Buttons: {key.upper()}</b>"), reply_markup=menu_buttons_list_keyboard(key))

    # ---------- OTHER CALLBACKS ----------
    elif data == "check_fj":
        if check_force_join(chat_id):
            delete_message(chat_id, msg_id)
            send_message(chat_id, render_body_text(f"{PEM['ok']} Thanks for joining! You can now use the bot."), reply_markup=main_menu(chat_id))
            u_data = get_user(chat_id)
            if u_data.get("referred_by") and not u_data.get("ref_paid"):
                inviter = u_data["referred_by"]
                conn = get_db_conn()
                conn.execute("UPDATE users SET ref_paid=1 WHERE user_id=?", (str(chat_id),))
                conn.commit()
                if str(chat_id) in user_cache: user_cache[str(chat_id)]["ref_paid"] = True
                reward = bot_settings.get("refer_reward", 0.2)
                get_user(inviter)
                update_balance(inviter, reward)
                increment_total_refers(inviter)
                ref_msg = (
                    f"{PEM['gift']} <b>New Referral !</b>\n"
                    f"------------------\n"
                    f"🔥 <b>You Received {reward} TK</b>\n"
                    f"------------------\n"
                    f"{PEM['user']} <b>From User ID:</b> <code>{chat_id}</code>"
                )
                send_message(inviter, render_body_text(ref_msg))
        else:
            answer_callback(call["id"], "❌ You haven't joined all channels yet!", show_alert=True)

    elif data == "close_msg":
        delete_message(chat_id, msg_id)

    elif data == "cancel_state":
        if chat_id in user_states: del user_states[chat_id]
        if chat_id in temp_data: del temp_data[chat_id]
        delete_message(chat_id, msg_id)

    elif data == "cancel_2fa":
        if chat_id in user_states: del user_states[chat_id]
        if chat_id in temp_data: del temp_data[chat_id]
        txt = "━━━━━━━━━━━━━━━\n《 🔐 <b>2FA ONLINE</b> 》\n━━━━━━━━━━━━━━━\n<i>Generate your 2FA security code instantly using your secret key.</i>\n━━━━━━━━━━━━━━━"
        kb = [[{"text": "Generate 2fa code", "icon_custom_emoji_id": "5353022963132174959", "callback_data": "gen_2fa", "style": "success"}],
              [{"text": "Close", "icon_custom_emoji_id": "5420130255174145507", "callback_data": "close_msg", "style": "danger"}]]
        edit_message(chat_id, msg_id, render_body_text(txt), reply_markup={"inline_keyboard": kb})
        answer_callback(call["id"])

    elif data == "gen_2fa":
        user_states[chat_id] = "wait_for_2fa_key"
        temp_data[chat_id] = {"msg_id": msg_id}
        txt = "━━━━━━━━━━━━━━━\n《 🔑 <b>ENTER 2FA KEY</b> 》\n━━━━━━━━━━━━━━━\n📝 <b>SEND YOUR 2FA SECRET KEY</b>\n━━━━━━━━━━━━━━━"
        kb = {"inline_keyboard": [[{"text": "Cancel", "icon_custom_emoji_id": "5267490665117275176", "callback_data": "cancel_2fa", "style": "danger"}]]}
        edit_message(chat_id, msg_id, render_body_text(txt), reply_markup=kb)
        answer_callback(call["id"])

    elif data.startswith("ref_2fa_"):
        secret = data.replace("ref_2fa_", "")
        try:
            totp = pyotp.TOTP(secret)
            code = totp.now()
            remaining_time = 30 - (int(time.time()) % 30)
            success_txt = (
                f"━━━━━━━━━━━━━━━\n"
                f"《 🔐 <b>2FA CODE</b> 》\n"
                f"━━━━━━━━━━━━━━━\n"
                f"🔐 <b>CODE:</b> <code>{code}</code>\n"
                f"━━━━━━━━━━━━━━━\n"
                f"🕓 <b>EXPIRES IN:</b> {remaining_time}s\n"
                f"━━━━━━━━━━━━━━━"
            )
            kb = [[{"text": f"Click to copy {code}", "icon_custom_emoji_id": "5353022963132174959", "copy_text": {"text": code}, "style": "success"}],
                  [{"text": "Refresh", "icon_custom_emoji_id": "5420155432272438703", "callback_data": f"ref_2fa_{secret}", "style": "primary"},
                   {"text": "New Code", "icon_custom_emoji_id": "5352552689983067014", "callback_data": "gen_2fa", "style": "danger"}],
                  [{"text": "Close", "icon_custom_emoji_id": "5420130255174145507", "callback_data": "close_msg", "style": "danger"}]]
            edit_message(chat_id, msg_id, render_body_text(success_txt), reply_markup={"inline_keyboard": kb})
        except:
            answer_callback(call["id"], "❌ Error refreshing code!", show_alert=True)

    # ---- Admin callbacks ----
    elif data == "lb_main":
        pass
    elif data == "broadcast_msg":
        user_states[chat_id] = "wait_for_broadcast"
        edit_message(chat_id, msg_id, render_body_text("📢 <b>Broadcast Mode</b>"), reply_markup={"inline_keyboard": [[{"text": "Cancel", "callback_data": "back_to_admin"}]]})
    elif data == "back_to_admin":
        edit_message(chat_id, msg_id, get_admin_text(), reply_markup=admin_panel_keyboard())
    elif data == "system_settings":
        edit_message(chat_id, msg_id, render_body_text(f"{PEM['gear']} System Settings"), reply_markup=system_settings_keyboard())
    elif data == "manage_fj":
        edit_message(chat_id, msg_id, render_body_text("🔗 Force Join"), reply_markup=fj_settings_keyboard())
    elif data == "toggle_fj":
        bot_settings["fj_on"] = not bot_settings["fj_on"]
        save_db()
        edit_message(chat_id, msg_id, render_body_text("🔗 Force Join"), reply_markup=fj_settings_keyboard())
    elif data == "add_fj":
        user_states[chat_id] = "wait_for_add_fj"
        temp_data[chat_id] = {"msg_id": msg_id}
        edit_message(chat_id, msg_id, render_body_text("📝 Send Channel Username or Invite Link:"))
    elif data.startswith("del_fj_"):
        idx = int(data.split("_")[2])
        if 0 <= idx < len(bot_settings["fj_channels"]):
            del bot_settings["fj_channels"][idx]
            save_db()
            answer_callback(call["id"], "✅ Channel deleted!", show_alert=True)
            edit_message(chat_id, msg_id, render_body_text("🔗 Force Join"), reply_markup=fj_settings_keyboard())
    elif data == "manage_admins":
        edit_message(chat_id, msg_id, render_body_text("👥 Admin Management"), reply_markup=admin_settings_keyboard())
    elif data == "add_adm":
        user_states[chat_id] = "wait_for_admin_id"
        temp_data[chat_id] = {"msg_id": msg_id}
        edit_message(chat_id, msg_id, render_body_text("📝 Send the User ID of the new Admin:"))
    elif data.startswith("del_adm_"):
        idx = int(data.split("_")[2])
        if 0 <= idx < len(bot_settings["admins"]):
            if bot_settings["admins"][idx] != OWNER_ID:
                del bot_settings["admins"][idx]
                save_db()
                answer_callback(call["id"], "✅ Admin deleted!", show_alert=True)
                edit_message(chat_id, msg_id, render_body_text("👥 Admin Management"), reply_markup=admin_settings_keyboard())
    elif data == "manage_otp_groups":
        edit_message(chat_id, msg_id, render_body_text("🛡 OTP Group Management"), reply_markup=otp_groups_list_keyboard())
    elif data == "add_fw":
        user_states[chat_id] = "wait_for_add_fw_id"
        temp_data[chat_id] = {"msg_id": msg_id}
        edit_message(chat_id, msg_id, render_body_text("📝 Send the Group ID/Username:"))
    elif data.startswith("manage_fw_"):
        idx = int(data.split("_")[2])
        if 0 <= idx < len(bot_settings["fw_groups"]):
            edit_message(chat_id, msg_id, render_body_text(f"🛡 <b>Manage Group:</b> {bot_settings['fw_groups'][idx]['chat_id']}"), reply_markup=specific_fw_group_keyboard(idx))
    elif data.startswith("add_fwbtn_"):
        idx = int(data.split("_")[2])
        user_states[chat_id] = "wait_for_add_fw_btn"
        temp_data[chat_id] = {"msg_id": msg_id, "fw_idx": idx}
        edit_message(chat_id, msg_id, render_body_text("📝 Send format:\n<code>Button Text - https://link.com</code>"))
    elif data.startswith("del_fwbtn_"):
        parts = data.split("_")
        idx, b_idx = int(parts[2]), int(parts[3])
        if 0 <= idx < len(bot_settings["fw_groups"]):
            if 0 <= b_idx < len(bot_settings["fw_groups"][idx]["buttons"]):
                del bot_settings["fw_groups"][idx]["buttons"][b_idx]
                save_db()
                answer_callback(call["id"], "✅ Button deleted!", show_alert=True)
                edit_message(chat_id, msg_id, render_body_text(f"🛡 <b>Manage Group:</b> {bot_settings['fw_groups'][idx]['chat_id']}"), reply_markup=specific_fw_group_keyboard(idx))
    elif data.startswith("del_fw_"):
        idx = int(data.split("_")[2])
        if 0 <= idx < len(bot_settings["fw_groups"]):
            del bot_settings["fw_groups"][idx]
            save_db()
            answer_callback(call["id"], "✅ Group deleted!", show_alert=True)
            edit_message(chat_id, msg_id, render_body_text("🛡 OTP Group Management"), reply_markup=otp_groups_list_keyboard())
    elif data == "edit_otp_link":
        user_states[chat_id] = "wait_for_otp_link"
        temp_data[chat_id] = {"msg_id": msg_id}
        edit_message(chat_id, msg_id, render_body_text("📝 Send the new OTP Group Link:"))
    elif data == "user_management":
        edit_message(chat_id, msg_id, get_user_management_text(), reply_markup=user_management_keyboard())
    elif data == "um_manage_balance":
        user_states[chat_id] = "wait_for_um_bal_uid"
        temp_data[chat_id] = {"msg_id": msg_id}
        edit_message(chat_id, msg_id, render_body_text("📝 Send the User ID to Manage Balance:"), reply_markup=get_cancel_kb())
    elif data == "um_ban_unban":
        user_states[chat_id] = "wait_for_um_ban_uid"
        temp_data[chat_id] = {"msg_id": msg_id}
        edit_message(chat_id, msg_id, render_body_text("📝 Send the User ID to Ban or Unban:"), reply_markup=get_cancel_kb())
    elif data == "um_user_profile":
        user_states[chat_id] = "wait_for_um_prof_uid"
        temp_data[chat_id] = {"msg_id": msg_id}
        edit_message(chat_id, msg_id, render_body_text("📝 Send the User ID to View Profile:"), reply_markup=get_cancel_kb())
    elif data == "dxa_control":
        edit_message(chat_id, msg_id, render_body_text("🕹 DXA Control"), reply_markup=dxa_control_keyboard())
    elif data == "dxa_toggle_w":
        bot_settings["withdraw_on"] = not bot_settings["withdraw_on"]
        save_db()
        edit_message(chat_id, msg_id, render_body_text("🕹 DXA Control"), reply_markup=dxa_control_keyboard())
    elif data.startswith("dxa_"):
        key = data.replace("dxa_", "")
        key_map = {"min_w": "min_withdraw", "otp_r": "otp_reward", "ref_r": "refer_reward", "cool": "cooldown", "num_req": "num_req", "num_share": "num_share", "sup_link": "support_link", "w_group": "w_group", "proof_group": "proof_group"}
        if key in key_map:
            user_states[chat_id] = "set_dxa"
            temp_data[chat_id] = {"msg_id": msg_id, "key": key_map[key]}
            edit_message(chat_id, msg_id, render_body_text(f"📝 Please send the new value for <code>{key_map[key]}</code>:"), reply_markup={"inline_keyboard": [[{"text": "Cancel", "callback_data": "cancel_dxa_edit", "style": "danger"}]]})
    elif data == "manage_w_methods":
        edit_message(chat_id, msg_id, render_body_text("💳 Withdrawal Methods"), reply_markup=w_methods_keyboard())
    elif data == "add_wm":
        user_states[chat_id] = "wait_for_add_wm"
        temp_data[chat_id] = {"msg_id": msg_id}
        edit_message(chat_id, msg_id, render_body_text("📝 Send the name of the new Withdrawal Method:"))
    elif data.startswith("del_wm_"):
        idx = int(data.split("_")[2])
        if 0 <= idx < len(bot_settings["w_methods"]):
            del bot_settings["w_methods"][idx]
            save_db()
            answer_callback(call["id"], "✅ Method deleted!", show_alert=True)
            edit_message(chat_id, msg_id, render_body_text("💳 Withdrawal Methods"), reply_markup=w_methods_keyboard())
    elif data == "manage_emojis":
        edit_message(chat_id, msg_id, render_body_text("✨ Premium Emoji Management"), reply_markup=emoji_settings_keyboard())
    elif data == "up_flags_txt":
        user_states[chat_id] = "wait_for_flag_txt"
        edit_message(chat_id, msg_id, render_body_text("📂 Upload Flag Emojis .txt file."), reply_markup={"inline_keyboard": [[{"text": "Cancel", "callback_data": "manage_emojis", "style": "danger"}]]})
    elif data == "dl_flags_txt":
        answer_callback(call["id"], "Download feature active.")
    elif data == "del_all_flags":
        bot_settings["premium_flags"] = {}
        save_db()
        answer_callback(call["id"], "✅ All Flags Deleted!", show_alert=True)
    else:
        answer_callback(call["id"], "Unknown action.", show_alert=False)

# ==================== BROADCAST ====================
def broadcast_copymessage(from_chat_id, msg_id):
    success = 0
    failed = 0
    users = list(all_known_users)
    b_session = requests.Session()
    url = f"{BASE_URL}/copyMessage"
    for user_id in users:
        payload = {"chat_id": user_id, "from_chat_id": from_chat_id, "message_id": msg_id}
        try:
            res = b_session.post(url, json=payload, timeout=5).json()
            if res.get("ok"): success += 1
            else: failed += 1
        except:
            failed += 1
        time.sleep(0.035)
    send_message(from_chat_id, render_body_text(f"📢 <b>Broadcast Completed!</b>\n✅ Success: {success}\n❌ Failed: {failed}\n👥 Total Sent: {len(users)}"))

# ==================== EXTRACT PREMIUM HTML ====================
def extract_premium_html(msg):
    text = msg.get("text", msg.get("caption", ""))
    entities = msg.get("entities", msg.get("caption_entities", []))
    if not entities: return text
    try:
        b_text = text.encode('utf-16-le')
        c_entities = [e for e in entities if e.get("type") == "custom_emoji"]
        c_entities.sort(key=lambda x: x["offset"], reverse=True)
        for ent in c_entities:
            offset = ent["offset"] * 2
            length = ent["length"] * 2
            eid = ent["custom_emoji_id"]
            emoji_char = b_text[offset:offset+length].decode('utf-16-le')
            html_tag = f'<tg-emoji emoji-id="{eid}">{emoji_char}</tg-emoji>'
            replacement = html_tag.encode('utf-16-le')
            b_text = b_text[:offset] + replacement + b_text[offset+length:]
        return b_text.decode('utf-16-le')
    except Exception as e:
        return text

def specific_fw_group_keyboard(idx):
    group = bot_settings["fw_groups"][idx]
    kb = []
    for b_idx, btn in enumerate(group.get("buttons", [])):
        kb.append([{"text": f"Del: {btn['text']}", "icon_custom_emoji_id": "5420130255174145507", "callback_data": f"del_fwbtn_{idx}_{b_idx}", "style": "danger"}])
    kb.append([{"text": "Add Inline Button", "icon_custom_emoji_id": "5420323438508155202", "callback_data": f"add_fwbtn_{idx}", "style": "success"}])
    kb.append([{"text": "Delete Entire Group", "icon_custom_emoji_id": "5422557736330106570", "callback_data": f"del_fw_{idx}", "style": "danger"}])
    kb.append([{"text": "Back to Groups", "icon_custom_emoji_id": "5267490665117275176", "callback_data": "manage_otp_groups", "style": "primary"}])
    return {"inline_keyboard": kb}

# ==================== MAIN LOOP ====================
def main():
    global BOT_USERNAME
    res = api_call("getMe")
    if res.get("ok"): BOT_USERNAME = res["result"]["username"]
    print(f"🤖 Bot is starting... @{BOT_USERNAME}")
    threading.Thread(target=panel_monitor_thread, daemon=True).start()
    threading.Thread(target=global_sms_listener, daemon=True).start()
    threading.Thread(target=voltx_sms_listener, daemon=True).start()
    threading.Thread(target=voltx_console_listener, daemon=True).start()
    threading.Thread(target=auto_email_checker, daemon=True).start()
    print("📡 All background threads started.")

    executor = ThreadPoolExecutor(max_workers=500)
    offset = None
    while True:
        try:
            params = {"timeout": 50, "allowed_updates": ["message", "callback_query"]}
            if offset is not None:
                params["offset"] = offset
            updates = api_call("getUpdates", params)
            if updates and "result" in updates:
                for update in updates["result"]:
                    offset = update["update_id"] + 1
                    if "message" in update:
                        msg = update["message"]
                        print(f"📨 MSG from {msg['chat']['id']} ({msg['chat'].get('type')}): {msg.get('text','')[:50]}")
                        executor.submit(handle_message, msg)
                    elif "callback_query" in update:
                        cq = update["callback_query"]
                        print(f"🔘 CALLBACK from {cq['from']['id']}: {cq.get('data','')[:50]}")
                        executor.submit(handle_callback, cq)
            elif updates and not updates.get("ok"):
                print(f"⚠️ getUpdates error: {updates}")
        except Exception as e:
            print(f"❌ Main loop error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        print("❌ FATAL STARTUP ERROR:", flush=True)
        traceback.print_exc()