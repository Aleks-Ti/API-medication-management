import pika

from src.settings.configuration import config_project


def setup_queue():
    connection = pika.BlockingConnection(pika.URLParameters(config_project.rabbit_mq.build_connection()))
    channel = connection.channel()
    # Убеждаемся, что очередь существует (или создаем её, если отсутствует)
    channel.queue_declare(queue="send_tg_message", durable=True)
    connection.close()
