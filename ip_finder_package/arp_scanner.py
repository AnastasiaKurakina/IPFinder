import subprocess
import re
import os

def get_arp_table():
    """
    Получает ARP-таблицу из локальной сети, вызывая команду arp -a.

    Returns:
        str: Вывод команды arp -a, содержащий IP и MAC адреса.
    """
    try:
        # Получаем вывод команды arp -a
        output = subprocess.check_output(['arp', '-a'], universal_newlines=True, encoding='cp866')
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def save_ip_mac_to_file(filename):
    """
    Сохраняет IP и MAC адреса в файл.

    Args:
        filename (str): Имя файла для сохранения данных.
    """
    arp_table = get_arp_table()
    if arp_table:
        # Проверяем, существует ли файл
        file_exists = os.path.isfile(filename)

        # Открываем файл для записи (перезаписываем, если файл не пуст)
        with open(filename, 'w', encoding='cp866') as file:
            # Регулярное выражение для извлечения IP и MAC адресов
            ip_mac_pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+)\s+([\da-fA-F-]+)')
            
            # Обрабатываем вывод ARP-таблицы
            for line in arp_table.splitlines():
                match = ip_mac_pattern.search(line)
                if match:
                    ip_address = match.group(1)
                    mac_address = match.group(2)
                    file.write(f"{ip_address} {mac_address}\n")  # Записываем в формате IP MAC

        if not file_exists:
            print(f"Файл {filename} был создан и заполнен.")
        else:
            print(f"Файл {filename} был перезаписан новыми данными.")
    else:
        print("Не удалось получить ARP-таблицу.")

if __name__ == "__main__":
    output_file = "arp_table.txt"
    save_ip_mac_to_file(output_file)






