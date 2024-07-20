import os
import sys
import tkinter as tk

# Получаем абсолютный путь к директории ip_finder_package
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Импортируем необходимые функции из core
from core import find_ip_and_switch_by_mac, switch_data

class IPFinderGUI:
    def __init__(self, master):
        self.master = master
        master.title("IP Finder")
        
        # Создаем виджеты
        self.label = tk.Label(master, text="Введите MAC-адрес:")
        self.label.pack()
        
        self.mac_entry = tk.Entry(master)
        self.mac_entry.pack()
        
        self.search_button = tk.Button(master, text="Найти", command=self.search_ip)
        self.search_button.pack()
        
        self.result_label = tk.Label(master, text="")
        self.result_label.pack()
        
        # Добавляем информацию о источнике входных данных
        self.source_label = tk.Label(master, text="Входные данные берутся из файла 'switch_data.json'")
        self.source_label.pack()
    
    def search_ip(self):
        mac_address = self.mac_entry.get()
        ip_address, path = find_ip_and_switch_by_mac(mac_address, switch_data)
        
        if ip_address and path:
            result_text = f"IP-адрес устройства с MAC-адресом {mac_address}: {ip_address}\n"
            result_text += f"Путь до устройства: {' -> '.join(path)}"
        else:
            result_text = f"Не удалось найти IP-адрес и путь для MAC-адреса {mac_address}"
        
        self.result_label.config(text=result_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = IPFinderGUI(root)
    root.mainloop()