import tkinter as tk
from tkinter import font, messagebox
from core import get_arp_table, extract_ip_mac, get_ip_from_mac, load_switch_data, load_arp_data
import re
import subprocess

class ARPLookupGUI:
    def __init__(self, master):
        self.master = master
        master.title("ARP Lookup")
        
        # Установка размера окна на половину экрана
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        master.geometry(f"{screen_width // 2}x{screen_height // 2}")

        # Установка цвета фона
        master.configure(bg="#C8E2F8")
        
        # Установка шрифта
        self.custom_font = font.Font(family="Arial", size=16)
        
        # Создаем флаг для выбора источника данных
        self.use_file = tk.BooleanVar()
        
        # Создаем чекбокс для выбора источника данных
        self.checkbox = tk.Checkbutton(master, text="Считывать данные из файла (JSON)", variable=self.use_file, bg="#C8E2F8")
        self.checkbox.pack(pady=10)
        
        # Создаем поле ввода для MAC-адреса
        self.label = tk.Label(master, text="Введите MAC-адрес:", bg="#C8E2F8", font=self.custom_font)
        self.label.pack()
        self.mac_entry = tk.Entry(master, font=self.custom_font)
        self.mac_entry.pack(pady=10)
        
        # Создаем кнопку для поиска IP-адреса
        self.search_button = tk.Button(master, text="Найти IP-адрес", command=self.find_ip, font=self.custom_font)
        self.search_button.pack(pady=10)
        
        # Создаем поле вывода для IP-адреса
        self.label2 = tk.Label(master, text="IP-адрес:", bg="#C8E2F8", font=self.custom_font)
        self.label2.pack()
        self.ip_label = tk.Label(master, bg="#C8E2F8", font=self.custom_font)
        self.ip_label.pack(pady=10)

        # Привязываем событие к полю ввода для проверки символов
        self.mac_entry.bind("<KeyRelease>", self.validate_input)

        # Вызываем функционал arp_scanner для обновления arp_table.txt при запуске
        self.update_arp_table()

    def update_arp_table(self):
        """Вызывает arp_scanner для обновления arp_table.txt."""
        try:
            subprocess.run(['python', 'arp_scanner.py'], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить ARP-таблицу: {e}")

    def find_ip(self):
        mac_address = self.mac_entry.get().strip()
        
        if self.use_file.get():
            # Считываем данные из JSON файла
            try:
                json_file_path = 'switch_data.json'
                ip_mac_list = load_switch_data(json_file_path)
            except FileNotFoundError:
                messagebox.showerror("Ошибка", "Файл switch_data.json не найден.")
                return
        else:
            # Считываем данные из текстового файла
            txt_file_path = 'arp_table.txt'
            ip_mac_list = load_arp_data(txt_file_path)
        
        ip_address = get_ip_from_mac(mac_address, ip_mac_list)
        
        if ip_address:
            self.ip_label.config(text=ip_address)
        else:
            self.ip_label.config(text="Не найдено")

    def validate_input(self, event):
        # Регулярное выражение для проверки корректности ввода
        valid_pattern = re.compile(r'^[0-9a-fA-F:-]*$')  # Добавлено тире в допустимые символы
        input_text = self.mac_entry.get()
        
        if not valid_pattern.match(input_text):
            # Подсвечиваем некорректные символы
            self.mac_entry.config(bg="red")
        else:
            # Возвращаем цвет фона, если ввод корректен
            self.mac_entry.config(bg="white")

root = tk.Tk()
app = ARPLookupGUI(root)
root.mainloop()



