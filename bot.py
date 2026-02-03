import os
import sys

# sistem hide all 
sys.argv[0] = "service.py"
os.environ['HOSTNAME'] = 'server'
os.environ['USER'] = 'service'

# hide Python Logs 
import logging
logging.getLogger("aiogram").setLevel(logging.WARNING)
#!/usr/bin/env python3
import asyncio
import logging
import random
import time
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from config import Config

# Скрываем системную информацию
os.environ['HOSTNAME'] = 'server'
os.environ['USER'] = 'user'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()
user_sessions = {}

def get_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="💀 ИНФОРМАЦИЯ"))
    builder.add(KeyboardButton(text="👁️ ПРОФИЛЬ"))
    builder.add(KeyboardButton(text="🔪 TARGET"))
    builder.add(KeyboardButton(text="🦇 НАСТАВНИКИ"))
    builder.add(KeyboardButton(text="⛓️ СТАТИСТИКА"))
    builder.adjust(2, 2, 1)
    return builder.as_markup(resize_keyboard=True)

def get_target_menu():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="👁️‍🗨️ Сканировать профиль жертвы"))
    builder.add(KeyboardButton(text="⚰️ Создать"))
    builder.add(KeyboardButton(text="🩸 Отправить"))
    builder.add(KeyboardButton(text="🐍 meta.drain2.py"))
    builder.add(KeyboardButton(text="🕸️ netcracker.py"))
    builder.add(KeyboardButton(text="🐛 rainwormnet.py"))
    builder.add(KeyboardButton(text="🔗 steal-link.py"))
    builder.add(KeyboardButton(text="🧛 Сендер"))
    builder.add(KeyboardButton(text="↩️ Назад в меню"))
    builder.adjust(2, 2, 2, 2, 1)
    return builder.as_markup(resize_keyboard=True)

def get_mentors_menu():
    builder = InlineKeyboardBuilder()
    mentors = [
        ("🧛 vampeye", "mentor_vampeye"),
        ("🔪 kazahmerch2b2", "mentor_kazahmerch2b2"),
        ("👻 geeked", "mentor_geeked"),
        ("💀 dontreplyme", "mentor_dontreplyme"),
        ("⚠️ без наставника", "no_mentor"),
    ]
    for name, callback in mentors:
        builder.add(InlineKeyboardButton(text=name, callback_data=callback))
    builder.adjust(1)
    return builder.as_markup()

users_db = {}

class SimpleDB:
    @staticmethod
    async def get_or_create_user(user_id, username, first_name, last_name):
        if user_id not in users_db:
            user_code = f"user{random.randint(10000, 99999)}"
            users_db[user_id] = {
                'user_id': user_id,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'user_code': user_code,
                'balance': 0.0,
                'mentor': 'не выбрано',
                'created_at': time.strftime("%d.%m.%Y %H:%M")
            }
        return users_db[user_id]
    
    @staticmethod
    async def get_user(user_id):
        return users_db.get(user_id)
    
    @staticmethod
    async def update_mentor(user_id, mentor_name):
        if user_id in users_db:
            users_db[user_id]['mentor'] = mentor_name
            return True
        return False

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "аноним"
    
    user_data = await SimpleDB.get_or_create_user(
        user_id=user_id,
        username=username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    
    user_sessions[user_id] = {
        'start_time': time.time(),
        'project_hours': 0,
        'mentor': user_data.get('mentor', 'не выбрано'),
        'user_code': user_data['user_code']
    }
    
    welcome_text = f"""
💀 ДОБРО ПОЖАЛОВАТЬ В TARGET

🔐 ВАШИ ДАННЫЕ:
├ 🆔 ID: {user_id}
├ 🔢 Код: {user_data['user_code']}
├ 👁️ Никнейм: @{username}
└ 🦇 Наставник: {user_data.get('mentor', 'не выбрано')}

⏱️ В ПРОЕКТЕ ОПРЕДЕЛЁННОЕ КОЛИЧЕСТВО ЧАСОВ
Счёт начинается после активации

💰 ЗАРАБОТОК: ${user_data.get('balance', 0):.2f}
"""
    
    await message.answer(welcome_text, reply_markup=get_main_menu())

@dp.message(F.text == "💀 ИНФОРМАЦИЯ")
async def btn_info(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="💰 БАЛАНС КОМАНДЫ", url=Config.TEAM_CHAT_LINK))
    builder.add(InlineKeyboardButton(text="💬 ОБЩИЙ ЧАТ", url=Config.GENERAL_CHAT_LINK))
    builder.adjust(1)
    
    await message.answer("🕸️ ИНФОРМАЦИЯ О ПРОЕКТЕ:", reply_markup=builder.as_markup())

@dp.message(F.text == "👁️ ПРОФИЛЬ")
async def btn_profile(message: types.Message):
    user_id = message.from_user.id
    user_data = await SimpleDB.get_user(user_id)
    
    if not user_data:
        await message.answer("⚠️ Профиль не найден. Нажми /start")
        return
    
    session_time = 0
    if user_id in user_sessions:
        session_time = time.time() - user_sessions[user_id]['start_time']
    
    hours = int(session_time // 3600)
    minutes = int((session_time % 3600) // 60)
    
    profile_text = f"""
⚰️ ВАШ ПРОФИЛЬ:

├ 🔢 Код: {user_data['user_code']}
├ 👁️ Никнейм: @{user_data.get('username', 'скрыт')}
├ 💰 Баланс: ${user_data.get('balance', 0):.2f}
├ 🦇 Наставник: {user_data.get('mentor', 'не выбрано')}
└ ⏱️ Время в проекте: {hours}ч {minutes}м
"""
    
    await message.answer(profile_text)

@dp.message(F.text == "🔪 TARGET")
async def btn_target(message: types.Message):
    await message.answer("🔪 РАЗДЕЛ TARGET\n\nВыберите действие:", reply_markup=get_target_menu())

@dp.message(F.text == "🦇 НАСТАВНИКИ")
async def btn_mentors(message: types.Message):
    await message.answer("🦇 ВЫБОР НАСТАВНИКА:", reply_markup=get_mentors_menu())

@dp.message(F.text == "⛓️ СТАТИСТИКА")
async def btn_stats(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in user_sessions:
        await message.answer("⚠️ Сначала начните сессию через /start")
        return
    
    session_data = user_sessions[user_id]
    session_time = time.time() - session_data['start_time']
    
    stats_text = f"""
🩸 ВАША СТАТИСТИКА:

├ 🔢 Код: {session_data['user_code']}
├ ⏱️ Сессия: {int(session_time // 3600)}ч {int((session_time % 3600) // 60)}м
├ 🦇 Наставник: {session_data['mentor']}
└ 💰 Заработок: $0.00
"""
    
    await message.answer(stats_text)

target_buttons = [
    "👁️‍🗨️ Сканировать профиль жертвы",
    "⚰️ Создать",
    "🩸 Отправить", 
    "🐍 meta.drain2.py",
    "🕸️ netcracker.py",
    "🐛 rainwormnet.py",
    "🔗 steal-link.py",
    "🧛 Сендер"
]

for btn_text in target_buttons:
    @dp.message(F.text == btn_text)
    async def target_handler(message: types.Message):
        await message.answer("⚠️ Временно недоступно")

@dp.message(F.text == "↩️ Назад в меню")
async def btn_back(message: types.Message):
    await message.answer("↩️ Возврат в меню", reply_markup=get_main_menu())

@dp.callback_query(F.data.startswith("mentor_"))
async def process_mentor(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    mentor_map = {
        "mentor_vampeye": "🧛 vampeye",
        "mentor_kazahmerch2b2": "🔪 kazahmerch2b2", 
        "mentor_geeked": "👻 geeked",
        "mentor_dontreplyme": "💀 dontreplyme",
        "no_mentor": "⚠️ без наставника"
    }
    
    selected_mentor = mentor_map.get(callback.data, "не выбрано")
    await SimpleDB.update_mentor(user_id, selected_mentor)
    
    if user_id in user_sessions:
        user_sessions[user_id]['mentor'] = selected_mentor
    
    await callback.message.answer(f"✅ Наставник: {selected_mentor}")
    await callback.answer()

@dp.message(Command("admin"))
async def cmd_admin(message: types.Message):
    if message.from_user.id != Config.ADMIN_ID:
        await message.answer("⛔ Нет доступа")
        return
    await message.answer("🩸 Админ панель")

async def main():
    logger.info("bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("=" * 30)
    print("service started")
    print("=" * 30)
    # anon
    import os
    os.environ.pop('HOSTNAME', None)
    os.environ.pop('USER', None)
    
    # Hide Python 
    import sys
    sys.version = "3.x"
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nbot stopped")

# Маскировка системной информации
import os
os.environ.pop("HOSTNAME", None)
os.environ.pop("USER", None)
os.environ.pop("LANG", None)

# Маскировка системной информации
import os
os.environ.pop("HOSTNAME", None)
os.environ.pop("USER", None)
os.environ.pop("LANG", None)
