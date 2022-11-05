import paho.mqtt.client as mqtt
import xmltodict
import json
from datetime import datetime


# Параметры подключения к MQTT-брокеру
HOST = "192.168.2.25"  # IP чемодана
PORT = 1883  # Стандартный порт подключения для Mosquitto
KEEPALIVE = 60  # Время ожидания доставки сообщения, если при отправке оно будет прeвышено, брокер будет считаться недоступным

# Словарь с топиками и собираемыми из них параметрами
SUB_TOPICS = {
    '/devices/wb-ms_11/controls/Illuminance': 'illuminance',
    '/devices/wb-msw-v3_21/controls/CO2': 'CO2',
    '/devices/power_status/controls/Vin': 'Vin'
}

# Создание словаря для хранения данных JSON
JSON_DICT = {}
JSON_LIST = []


def on_connect(client, userdata, flags, rc):
    """ Функция, вызываемая при подключении к брокеру

    Arguments:
    client - Экземпляр класса Client, управляющий подключением к брокеру
    userdata - Приватные данные пользователя, передаваемые при подключениии
    flags - Флаги ответа, возвращаемые брокером
    rc - Результат подключения, если 0, всё хорошо, в противном случае идем в документацию
    """
    print("Connected with result code " + str(rc))

    # Подключение ко всем заданным выше топикам
    for topic in SUB_TOPICS.keys():
        client.subscribe(topic)


def on_message(client: mqtt.Client, userdata, msg):
    """ Функция, вызываемая при получении сообщения от брокера по одному из отслеживаемых топиков

    Arguments:
    client - Экземпляр класса Client, управляющий подключением к брокеру
    userdata - Приватные данные пользователя, передаваемые при подключениии
    msg - Сообщение, приходящее от брокера, со всей информацией
    """
    payload = msg.payload.decode()  # Основное значение, приходящее в сообщение, например, показатель температуры
    topic = msg.topic  # Топик, из которого пришло сообщение, поскольку функция обрабатывает сообщения из всех топиков

    param_name = SUB_TOPICS[topic]
    JSON_DICT[param_name] = payload
    JSON_DICT['time'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    JSON_LIST.append(JSON_DICT)
    print(topic + " " + payload)

    # Запись данных в файл
    with open('../data.json', 'w') as file:
        json_string = json.dumps({'data': JSON_LIST})  # Формирование строки JSON из словаря
        file.write(json_string)
    with open('../data.xml', 'w') as file:
        unparsed = xmltodict.unparse({'data': JSON_LIST}, pretty=True)
        file.write(unparsed)

def main(subtopics=None):
    SUB_TOPICS = SUB_TOPICS if subtopics is None else subtopics
    for value in SUB_TOPICS.values():
        JSON_DICT[value] = 0
    # Создание и настройка экземпляра класса Client для подключения в Mosquitto
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOST, PORT, KEEPALIVE)

    client.loop_forever()  # Бесконечный внутренний цикл клиента в ожидании сообщений


if __name__ == "__main__":
    main()
