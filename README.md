## Telegram bot для интервальных повторений наиболее распространённых слов английского языка

Бот заточен на интервальное повторение карточек. 

Развёртывание:

#### Шаг 1. Клонирование

Для пользовательского ключа:

``git clone https://github.com/codesshaman/intervals_english_telegram_bot.git``

Для корпоративного/специального ключа:

``git clone github-repo:codesshaman/intervals_english_telegram_bot.git``

Переход в каталог:

``cd intervals_english_telegram_bot``

#### Шаг 2. Создание .env-файла

Создать файл:

``make env``

Редактировать файл:

``nano .env``

Вставить в файл id группы (не забыть '-' или '-100') и токен бота рассылки.

Сохранить файл.

#### Шаг 3. Создание карточек

Удаляем старые карточки:

``rm -rf ./output/*``

Правим файл schedule.csv:

создаём два пустых столбца после столбца с датами

создаём формулу, которая увеличит дату начала повторений на нужное нам время

применяем формулу ко всему второму столбцу

копируем полученные дать как текст в следующий стоблец

Удаляем два первых столбца, оставляя только нужные нам даты

Далее запускаем names_changer.py:

``python3 names_changer.py``

и получаем список карточек с нужными нам датами в output

Перемещаем эти карточки в .msgs:

``rm -rf ./.msgs/* && cp -rf ./output/* ./.msgs``

#### Шаг 4. Создание сервиса и таймера:

``make service``

``make timer``

#### Шаг 5. Проверка работы сервиса:

``sudo service english_bot start``

``sudo service english_bot status``

Проверить логи:

``cat ./logfile.log``
