import subprocess
import re
import json

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

def extract_ip_mac(arp_table):
    """
    Извлекает IP и MAC адреса из ARP-таблицы.

    Args:
        arp_table (str): Вывод команды arp -a, содержащий ARP-таблицу.

    Returns:
        list: Список кортежей, где каждый кортеж содержит IP и MAC адрес.
    """
    ip_mac_pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+)\s+([\da-fA-F-]+)')
    matches = ip_mac_pattern.findall(arp_table)
    return matches

def normalize_mac(mac_address):
    """
    Нормализует MAC-адрес, заменяя тире на двоеточия.

    Args:
        mac_address (str): MAC-адрес для нормализации.

    Returns:
        str: Нормализованный MAC-адрес.
    """
    return mac_address.replace('-', ':')

def get_ip_from_mac(mac_address, ip_mac_list):
    """
    Находит соответствующий IP-адрес для заданного MAC-адреса.

    Args:
        mac_address (str): MAC-адрес, для которого необходимо найти IP-адрес.
        ip_mac_list (list): Список кортежей, содержащих IP и MAC адреса.

    Returns:
        str or None: Соответствующий IP-адрес, если найден, иначе None.
    """
    normalized_mac = normalize_mac(mac_address)
    for ip, mac in ip_mac_list:
        if normalize_mac(mac) == normalized_mac:
            return ip
    return None

def load_switch_data(file_path):
    """
    Загружает данные коммутаторов из JSON файла.

    Args:
        file_path (str): Путь к JSON файлу.

    Returns:
        list: Список устройств с их IP и MAC адресами.
    """
    devices = []

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

        # Добавляем устройства из корневого уровня
        for device in data.get('connected_devices', []):
            devices.append((device['ip_address'], device['mac_address']))

        # Рекурсивно добавляем устройства из дочерних коммутаторов
        def add_devices(switch):
            for device in switch.get('connected_devices', []):
                devices.append((device['ip_address'], device['mac_address']))
            for child_switch in switch.get('child_switches', []):
                add_devices(child_switch)

        add_devices(data)

    return devices

def load_arp_data(file_path):
    """
    Загружает данные ARP-таблицы из текстового файла.

    Args:
        file_path (str): Путь к текстовому файлу.

    Returns:
        list: Список кортежей, где каждый кортеж содержит IP и MAC адрес.
    """
    ip_mac_list = []

    try:
        with open(file_path, 'r', encoding='cp866') as file:
            for line in file:
                ip, mac = line.strip().split()
                ip_mac_list.append((ip, mac))
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except ValueError:
        print("Ошибка в формате файла. Ожидается: IP MAC")

    return ip_mac_list

