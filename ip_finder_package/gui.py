import os
import sys
import tkinter as tk
from tkinter import scrolledtext

# Получаем абсолютный путь к директории ip_finder_package
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Импортируем необходимые функции из core
from core import find_ip_and_switch_by_mac, switch_data

class IPFinderGUI:
    def __init__(self, master):
        self.master = master
        master.title("IP Finder")

        # Устанавливаем цвет фона
        master.configure(bg="#C8E2F8")

        # Устанавливаем размер окна на половину экрана
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        master.geometry(f"{screen_width // 2}x{screen_height // 2}")

        # Создаем виджеты
        self.label = tk.Label(master, text="Введите MAC-адрес:", bg="#C8E2F8", font=("Arial", 16))
        self.label.pack(pady=10)

        # Создаем валидатор для ввода
        self.validate_command = master.register(self.validate_input)

        self.mac_entry = tk.Entry(master, font=("Arial", 16), validate="key", validatecommand=(self.validate_command, '%P'))
        self.mac_entry.pack(pady=10)

        self.search_button = tk.Button(master, text="НАЙТИ", command=self.search_ip, font=("Arial", 16), bg="#A1C6E7")
        self.search_button.pack(pady=10)

        # Используем виджет Text для отображения результатов
        self.result_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, font=("Arial", 14), height=5, width=50)
        self.result_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.result_text.config(state=tk.DISABLED)  # Делаем текстовое поле только для чтения

        # Добавляем информацию о источнике входных данных
        self.source_label = tk.Label(master, text="Входные данные берутся из файла 'switch_data.json'", bg="#C8E2F8", font=("Arial", 12))
        self.source_label.pack(pady=10)

    def validate_input(self, new_value):
        """
        Проверяет, является ли введенное значение допустимым (только цифры, латинские буквы и двоеточия).
        """
        if all(c.isalnum() or c == ':' for c in new_value) or new_value == "":
            self.mac_entry.config(fg="black")  # Устанавливаем цвет текста в черный
            return True
        else:
            self.mac_entry.config(fg="red")  # Устанавливаем цвет текста в красный
            return True

    def search_ip(self):
        mac_address = self.mac_entry.get()
        ip_address, path = find_ip_and_switch_by_mac(mac_address, switch_data)

        self.result_text.config(state=tk.NORMAL)  # Разрешаем редактирование, чтобы вставить текст
        self.result_text.delete(1.0, tk.END)  # Очищаем текстовое поле перед выводом нового результата

        if ip_address and path:
            result_text = f"IP-адрес устройства с MAC-адресом {mac_address}: {ip_address}\n"
            result_text += f"Путь до устройства: {' -> '.join(path)}"
        else:
            result_text = f"Не удалось найти IP-адрес и путь для MAC-адреса {mac_address}"

        self.result_text.insert(tk.END, result_text)  # Вставляем текст в текстовое поле
        self.result_text.config(state=tk.DISABLED)  # Снова делаем текстовое поле только для чтения

if __name__ == "__main__":
    root = tk.Tk()
    app = IPFinderGUI(root)
    root.mainloop()
