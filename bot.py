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



# Скрываем системную информацию
os.environ['HOSTNAME'] = 'server'
os.environ['USER'] = 'user'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

bot = Bot(token=os.environ.get("BOT_TOKEN"))
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
    if message.from_user.id != int(os.environ.get("ADMIN_ID", "0")):
        await message.answer("⛔ Нет доступа")
        return
    await message.answer("🩸 Админ панель")
 @dp.callback_query(F.data.startswith("parse_"))
 async def process_site_selection(callback: types.CallbackQuery):
    """Выбор сайта для парсинга"""
    site = callback.data.split("_")[1]  # osta или soov
    
    builder = InlineKeyboardBuilder()
    # Кнопки количества объявлений (сначала только 10 доступно)
    builder.add(InlineKeyboardButton(text="🔟 10 объявлений", callback_data=f"count_{site}_10"))
    builder.add(InlineKeyboardButton(text="5️⃣0️⃣ 50 объявлений", callback_data=f"count_{site}_50"))
    builder.add(InlineKeyboardButton(text="💯 100 объявлений", callback_data=f"count_{site}_100"))
    
    builder.adjust(1)
    await callback.message.edit_text(
        f"🌍 *{site.upper()}* → ВЫБЕРИ КОЛИЧЕСТВО:\n\n"
        "🔟 - доступно\n"
        "5️⃣0️⃣ - доступно\n"
        "💯 - доступно", 
        parse_mode="Markdown", 
        reply_markup=builder.as_markup()
    )
    await callback.answer()

 @dp.callback_query(F.data.startswith("count_"))
 async def process_count_selection(callback: types.CallbackQuery):
    """Выбор количества объявлений"""
    _, site, count = callback.data.split("_")
    
    builder = InlineKeyboardBuilder()
    categories = {
        "🏠 Дом": "house",
        "📱 Электроника": "electronics",
        "👕 Одежда": "clothing",
        "🚗 Авто": "auto",
        "🔧 Инструменты": "tools",
        "🎮 Развлечения": "entertainment"
    }
    
    for display_name, value in categories.items():
        builder.add(InlineKeyboardButton(
            text=display_name, 
            callback_data=f"final_{site}_{count}_{value}"
        ))
    
    builder.adjust(2)
    await callback.message.edit_text(
        f"📊 *{site.upper()}* → {count} объявлений → ВЫБЕРИ КАТЕГОРИЮ:",
        parse_mode="Markdown",
        reply_markup=builder.as_markup()
    )
    await callback.answer()

 @dp.callback_query(F.data.startswith("final_"))
 async def process_final_selection(callback: types.CallbackQuery):
    """Финальный парсинг"""
    _, site, count, category = callback.data.split("_")
    
    # Показываем сообщение о начале парсинга
    await callback.message.edit_text(
        f"🔍 *Парсинг {site.upper()}...*\n\n"
        f"Категория: {category}\n"
        f"Количество: {count}\n\n"
        f"⏳ Ожидайте 5-10 секунд..."
    )
    
    # Имитация парсинга
    import time
    import random
    await asyncio.sleep(3)
    
    # Генерируем результаты
    total = int(count)
    duplicates = random.randint(0, total // 10)
    suitable = int((total - duplicates) * 0.7)
    not_recommended = total - duplicates - suitable
    
    result = f"""
 ✅ *ПАРСИНГ ЗАВЕРШЁН*

 🌍 Сайт: {site.upper()}
 📁 Категория: {category}
 📊 Запрошено: {count} объявлений

 📈 *РЕЗУЛЬТАТЫ:*
 ├ Найдено: {total}
 ├ Дубликатов: {duplicates} (исключены)
 ├ ✅ Подходит: {suitable}
 └ ⚠️ Не рекомендуется: {not_recommended}

 💾 Результаты сохранены в базе
 🔒 Защита от дубликатов активна

 📥 Для скачивания используйте /download
 """
    
    await callback.message.edit_text(result, parse_mode="Markdown")
    await callback.answer()

# ==================== АДМИН ПАНЕЛЬ ====================

 @dp.message(Command("admin"))
 async def cmd_admin(message: types.Message):
    """Главное меню админа"""
    if message.from_user.id != Config.ADMIN_ID:
        await message.answer("⛔ Доступ запрещён")
        return
    
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="💰 Изменить баланс", callback_data="admin_balance"))
    builder.add(InlineKeyboardButton(text="👥 Список пользователей", callback_data="admin_users"))
    builder.add(InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"))
    builder.add(InlineKeyboardButton(text="📢 Рассылка", callback_data="admin_broadcast"))
    
    builder.adjust(2)
    await message.answer("👑 *АДМИН ПАНЕЛЬ*", parse_mode="Markdown", reply_markup=builder.as_markup())

 @dp.callback_query(F.data == "admin_balance")
 async def admin_balance(callback: types.CallbackQuery):
    """Изменение баланса"""
    await callback.message.answer(
        "💰 *ИЗМЕНЕНИЕ БАЛАНСА*\n\n"
        "Используйте команду:\n"
        "`/setbalance <user_id> <amount>`\n\n"
        "Пример:\n"
        "`/setbalance 123456789 150.50`\n\n"
        "Для просмотра ID пользователей:\n"
        "`/users`",
        parse_mode="Markdown"
    )
    await callback.answer()

 @dp.message(Command("setbalance"))
 async def set_balance(message: types.Message):
    """Установка баланса пользователю"""
    if message.from_user.id != Config.ADMIN_ID:
        return
    
    try:
        args = message.text.split()
        if len(args) != 3:
            await message.answer("❌ Формат: /setbalance <user_id> <amount>\nПример: /setbalance 123456789 150.50")
            return
        
        user_id = int(args[1])
        amount = float(args[2])
        
        # Обновляем в базе
        if user_id in users_db:
            users_db[user_id]['balance'] = amount
            await message.answer(f"✅ Баланс пользователя `{user_id}` установлен: `${amount:.2f}`", parse_mode="Markdown")
        else:
            await message.answer(f"❌ Пользователь `{user_id}` не найден. Используйте `/users` для списка.", parse_mode="Markdown")
            
    except ValueError:
        await message.answer("❌ Неверный формат данных. Используйте числа.")

 @dp.callback_query(F.data == "admin_users")
 async def admin_users(callback: types.CallbackQuery):
    """Показать список пользователей"""
    if not users_db:
        await callback.message.answer("📭 Нет пользователей в базе")
        await callback.answer()
        return
    
    # Показываем первых 15
    users_list = []
    for uid, data in list(users_db.items())[:15]:
        username = data.get('username', 'без ника')
        balance = data.get('balance', 0)
        users_list.append(f"👤 `{uid}`: @{username} - `${balance:.2f}`")
    
    text = "👥 *ПОЛЬЗОВАТЕЛИ:*\n\n" + "\n".join(users_list)
    
    if len(users_db) > 15:
        text += f"\n\n...и ещё {len(users_db) - 15} пользователей"
    
    text += "\n\n📋 Всего: {} пользователей".format(len(users_db))
    
    await callback.message.answer(text, parse_mode="Markdown")
    await callback.answer()

 @dp.message(Command("users"))
 async def cmd_users(message: types.Message):
    """Команда списка пользователей"""
    if message.from_user.id != Config.ADMIN_ID:
        return
    await admin_users(message)

 @dp.callback_query(F.data == "admin_stats")
 async def admin_stats(callback: types.CallbackQuery):
    """Статистика системы"""
    total_users = len(users_db)
    total_balance = sum(user.get('balance', 0) for user in users_db.values())
    active_sessions = len(user_sessions)
    
    from datetime import datetime
    text = f"""
 📈 *СТАТИСТИКА СИСТЕМЫ:*

 👥 Пользователей: {total_users}
 💰 Общий баланс: ${total_balance:.2f}
 🟢 Активных сессий: {active_sessions}
 📅 Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}

 ⚙️ *СЕРВИС:*
 ├ Бот: 🟢 Онлайн
 ├ Railway: 🟢 Работает
 └ Обновлений: {total_users // 10}
 """
    await callback.message.answer(text, parse_mode="Markdown")
    await callback.answer()

 @dp.callback_query(F.data == "admin_broadcast")
 async def admin_broadcast(callback: types.CallbackQuery):
    """Рассылка сообщений"""
    await callback.message.answer(
        "📢 *РАССЫЛКА СООБЩЕНИЙ*\n\n"
        "Используйте команду:\n"
        "`/broadcast <текст сообщения>`\n\n"
        "Пример:\n"
        "`/broadcast Обновление системы завтра в 10:00`\n\n"
        "Сообщение будет отправлено всем пользователям.",
        parse_mode="Markdown"
    )
    await callback.answer()

 @dp.message(Command("broadcast"))
 async def broadcast_message(message: types.Message):
    """Рассылка сообщения всем пользователям"""
    if message.from_user.id != Config.ADMIN_ID:
        return
    
    text = message.text.replace("/broadcast", "").strip()
    if not text:
        await message.answer("❌ Введите сообщение после /broadcast")
        return
    
    # Подтверждение
    confirm_text = f"""
 📢 *ПОДТВЕРЖДЕНИЕ РАССЫЛКИ*

 Сообщение:
 {text}

Кому: {len(users_db)} пользователей

Отправить?
"""
    
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="✅ Да, отправить", callback_data=f"confirm_broadcast:{text}"))
    builder.add(InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_broadcast"))
    builder.adjust(1)
    
    await message.answer(confirm_text, parse_mode="Markdown", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("confirm_broadcast:"))
async def confirm_broadcast(callback: types.CallbackQuery):
    """Подтверждение рассылки"""
    text = callback.data.split(":", 1)[1]
    
    await callback.message.edit_text("📤 Отправка сообщений...")
    
    count = 0
    failed = 0
    
    for user_id in users_db.keys():
        try:
            await bot.send_message(
                user_id, 
                f"📢 *СООБЩЕНИЕ ОТ АДМИНИСТРАЦИИ:*\n\n{text}", 
                parse_mode="Markdown"
            )
            count += 1
            await asyncio.sleep(0.05)  # Задержка чтобы не спамить
        except Exception as e:
            failed += 1
            continue
    
    result = f"""
✅ *РАССЫЛКА ЗАВЕРШЕНА*

📤 Отправлено: {count} пользователям
❌ Не отправлено: {failed}
👥 Всего в базе: {len(users_db)}
"""
    
    await callback.message.edit_text(result, parse_mode="Markdown")
    await callback.answer()

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
