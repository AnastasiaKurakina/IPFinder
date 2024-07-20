import netaddr
import subprocess
import locale
import json
import os

def get_arp_data(ip_address):
    """
    Получает данные ARP для указанного IP-адреса.
    
    Args:
        ip_address (str): IP-адрес коммутатора или устройства.
    
    Returns:
        list: Список строк с данными ARP или None, если возникла ошибка.
    """
    try:
        # Получаем данные ARP и декодируем с использованием кодировки по умолчанию
        arp_output = subprocess.check_output(['arp', '-a', ip_address]).decode(errors='ignore').split('\n')
        return arp_output
    except subprocess.CalledProcessError:
        return None

def search_recursively(current_switch, mac_address):
    """
    Рекурсивная функция для поиска по дереву коммутаторов.
    
    Args:
        current_switch (dict): Словарь с информацией о текущем коммутаторе.
        mac_address (str): MAC-адрес устройства в формате XX:XX:XX:XX:XX:XX.
    
    Returns:
        tuple: (ip_address, path) или (None, None), если не найдено.
    """
    arp_output = get_arp_data(current_switch["ip_address"])
    if arp_output:
        for line in arp_output:
            if mac_address.upper() in line.upper():
                ip_address = line.split()[0]
                path = [current_switch["name"]]
                return ip_address, path
    
    for device in current_switch.get("connected_devices", []):
        if device["mac_address"].upper() == mac_address.upper():
            return device["ip_address"], [current_switch["name"]]
    
    for child_switch in current_switch.get("child_switches", []):
        ip_address, path = search_recursively(child_switch, mac_address)
        if ip_address:
            path.insert(0, current_switch["name"])
            return ip_address, path
    
    return None, None

def find_ip_and_switch_by_mac(mac_address, switch_data):
    """
    Находит IP-адрес устройства и путь до него от центрального коммутатора по его MAC-адресу.
    
    Args:
        mac_address (str): MAC-адрес устройства в формате XX:XX:XX:XX:XX:XX.
        switch_data (dict): Словарь с информацией о коммутаторах и подключенных устройствах.
    
    Returns:
        tuple: (ip_address, path) или (None, None), если не найдено.
    """
    # Проверяем, что MAC-адрес имеет правильный формат
    if not netaddr.valid_mac(mac_address):
        return None, None
    
    # Ищем IP-адрес и коммутатор, соответствующие заданному MAC-адресу, начиная с центрального коммутатора
    return search_recursively(switch_data, mac_address)

# Загружаем данные о коммутаторах из файла switch_data.json
current_dir = os.path.dirname(os.path.abspath(__file__))
switch_data_path = os.path.join(current_dir, 'switch_data.json')

with open(switch_data_path, 'r', encoding='utf-8') as f:
    switch_data = json.load(f)