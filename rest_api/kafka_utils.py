"""Create and return AIOKafkaProducer."""
from asyncio import get_event_loop, set_event_loop_policy
from asyncio.events import AbstractEventLoop
from json import dumps
from ssl import SSLContext

from aiokafka import AIOKafkaProducer
from aiokafka.helpers import create_ssl_context

from config import kafka_compression, kafka_host, kafka_port, \
    kafka_sasl_mechanism, kafka_sasl_plain_password, \
    kafka_sasl_plain_username, kafka_ssl, kafka_ssl_cafile, \
    kafka_ssl_certfile, kafka_ssl_keyfile, kafka_ssl_password

from uvloop import EventLoopPolicy

set_event_loop_policy(EventLoopPolicy())
loop: AbstractEventLoop = get_event_loop()


def create_kafka_ssl_context() -> SSLContext:
    """Create and return ssl_context needed by Kafka when SSL is activated."""
    return create_ssl_context(
        cafile=kafka_ssl_cafile, certfile=kafka_ssl_certfile,
        keyfile=kafka_ssl_keyfile, password=kafka_ssl_password
    ) if len(kafka_ssl_password) > 0 else create_ssl_context(
        cafile=kafka_ssl_cafile, certfile=kafka_ssl_certfile,
        keyfile=kafka_ssl_keyfile)


def create_aio_producer() -> AIOKafkaProducer:
    """Create and return AIOKafkaProducer."""
    return AIOKafkaProducer(
        loop=loop, bootstrap_servers=f'{kafka_host}:{kafka_port}',
        value_serializer=lambda v: dumps(v).encode('utf-8'),
        compression_type=kafka_compression,
        ssl_context=create_kafka_ssl_context(),
        security_protocol='SSL', sasl_mechanism=kafka_sasl_mechanism,
        sasl_plain_username=kafka_sasl_plain_username,
        sasl_plain_password=kafka_sasl_plain_password) if kafka_ssl else \
        AIOKafkaProducer(
            loop=loop, bootstrap_servers=f'{kafka_host}:{kafka_port}',
        value_serializer=lambda v: dumps(v).encode('utf-8'),
        compression_type=kafka_compression, security_protocol='PLAINTEXT',
        sasl_mechanism=kafka_sasl_mechanism,
        sasl_plain_username=kafka_sasl_plain_username,
        sasl_plain_password=kafka_sasl_plain_password)
