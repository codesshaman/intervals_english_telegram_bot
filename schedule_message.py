import os
import re
import asyncio
import shutil
from datetime import datetime
from dotenv import load_dotenv
from aiogram import Bot

# Загружаем переменные из .env
load_dotenv()
token = os.getenv("token")
group = os.getenv("group")

# Функция для экранирования текста в формате MarkdownV2, кроме скрытого текста
def escape_markdown_v2(text):
    """Экранирует символы MarkdownV2 для безопасной отправки в Telegram, кроме скрытого текста."""
    text = re.sub(r'([_\*\[\]\(\)\~\`\>\#\+\-\=\|\,\.\!\&])', r'\\\1', text)
    text = text.replace(r'\|\|', '||')
    return text

async def schedule_message(bot, group, message, schedule_time):
    """Отправляет отложенное сообщение в указанный момент."""
    now = datetime.now()
    delay = (schedule_time - now).total_seconds()

    if delay > 0:
        await asyncio.sleep(delay)

    try:
        await bot.send_message(group, message, parse_mode="MarkdownV2")
        print(f"Сообщение отправлено: {message[:20]}")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

async def process_files():
    """Обрабатывает файлы из директории .msgs, отправляет сообщения и перемещает файлы."""
    input_dir = "./.msgs"
    old_dir = os.path.join(input_dir, "old")

    # Инициализируем бота
    bot = Bot(token)

    try:
        # Проверяем наличие директорий
        if not os.path.exists(input_dir):
            print(f"Директория '{input_dir}' не найдена.")
            return

        if not os.path.exists(old_dir):
            os.makedirs(old_dir)

        # Получаем текущую дату
        today = datetime.now().strftime("%Y-%m-%d")

        # Считываем файлы
        files = [
            os.path.join(input_dir, f)
            for f in os.listdir(input_dir)
            if os.path.isfile(os.path.join(input_dir, f)) and f.startswith(today)
        ]

        if not files:
            print(f"На текущую дату ({today}) файлы не найдены.")
            return

        tasks = []

        for file_path in files:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read().strip()

            if not content:
                content = " "

            # Экранируем содержимое
            formatted_text = escape_markdown_v2(content)

            # Извлекаем время из имени файла
            try:
                time_part = os.path.basename(file_path).split(" ")[1].replace(".txt", "")
                schedule_time = datetime.strptime(f"{today} {time_part}", "%Y-%m-%d %H:%M:%S")
            except Exception as e:
                print(f"Ошибка при разборе времени из файла {file_path}: {e}")
                continue

            # Планируем отправку
            tasks.append(schedule_message(bot, group, formatted_text, schedule_time))

            # Перемещаем файл в папку old
            shutil.move(file_path, os.path.join(old_dir, os.path.basename(file_path)))

        # Выполняем задачи отправки сообщений
        if tasks:
            await asyncio.gather(*tasks)
    finally:
        # Закрываем сессию бота
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(process_files())
