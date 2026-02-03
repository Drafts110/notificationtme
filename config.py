"""
Конфигурационный файл бота для Railway
"""
import os

class Config:
    # Токен из переменных окружения Railway
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    
    # Проверяем что токен есть
    if not BOT_TOKEN:
        print("⚠️ ОШИБКА: BOT_TOKEN не установлен!")
        print("Установи в Railway Dashboard: BOT_TOKEN=твой_токен")
        exit(1)
    
    # Твой ID
    try:
        ADMIN_ID = int(os.environ.get("ADMIN_ID", "7259419425"))
    except:
        ADMIN_ID = 7259419425
    
    # Чат-ссылки
    TEAM_CHAT_LINK = "https://t.me/+xuScRpBN9wA3YzU8"
    GENERAL_CHAT_LINK = "https://t.me/+Ck59B4YJOjRhOGQ0"
    
    # Настройки
    DB_NAME = 'bot_database.db'
    PROJECT_NAME = "TARGET"
    VERSION = "1.0.0"
    
    # Логи
    LOG_LEVEL = "INFO"

# Проверка при импорте
if __name__ == "__main__":
    print("✅ Config проверен")
    print(f"👑 Admin ID: {Config.ADMIN_ID}")
    print(f"🤖 Token: {Config.BOT_TOKEN[:15]}...")
