import os
import shutil
import csv
from datetime import datetime, timedelta

# Время начала повторений
time = "07"
# Директория с исходными файлами
input_dir = "input"
# Директория для сохранения выходных файлов
output_dir = "output"
# CSV файл с расписанием
csv_file = "schedule.csv"

# Убедимся, что выходная директория существует
os.makedirs(output_dir, exist_ok=True)

# Чтение CSV файла
with open(csv_file, "r") as file:
    reader = csv.reader(file)
    
    for row in reader:
        # Пропускаем пустые строки
        if not row:
            continue

        # Первая ячейка - дата
        date_str = row[0]
        try:
            base_datetime = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError as e:
            print(f"Ошибка в формате даты: {date_str}")
            continue

        # Каждая цифра в строке после даты - номер файла
        for i, file_number in enumerate(row[1:]):
            file_number = file_number.strip()

            # Формируем исходные имена файлов
            file_txt = f"file_{file_number}.txt"
            file_r_txt = f"file_{file_number}r.txt"

            # Формируем новое время
            new_datetime = base_datetime + timedelta(seconds=10 * i * 2)  # Увеличение на 10 секунд

            # Обрабатываем обычный файл (без 'r')
            if os.path.exists(os.path.join(input_dir, file_txt)):
                new_file_name = new_datetime.strftime("%Y-%m-%d " + time + ":%M:%S") + ".txt"
                shutil.copy(
                    os.path.join(input_dir, file_txt),
                    os.path.join(output_dir, new_file_name)
                )

            # Обрабатываем файл с 'r'
            new_datetime = new_datetime + timedelta(seconds=10)  # Следующий 10-секундный интервал
            if os.path.exists(os.path.join(input_dir, file_r_txt)):
                new_file_name = new_datetime.strftime("%Y-%m-%d " + time + ":%M:%S") + ".txt"
                shutil.copy(
                    os.path.join(input_dir, file_r_txt),
                    os.path.join(output_dir, new_file_name)
                )

print("Файлы успешно переименованы и сохранены в папке output.")
