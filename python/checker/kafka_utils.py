"""Create and return AIOKafkaProducer."""
from json import dumps, loads
from ssl import SSLContext

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.helpers import create_ssl_context

from config import kafka_compression, kafka_host, kafka_port, \
    kafka_sasl_mechanism, kafka_sasl_plain_password, \
    kafka_sasl_plain_username, kafka_ssl, kafka_ssl_cafile, \
    kafka_ssl_certfile, kafka_ssl_keyfile, kafka_ssl_password, kafka_topic_rbl


def create_kafka_ssl_context() -> SSLContext:
    """Create and return ssl_context needed by Kafka when SSL is activated."""
    return create_ssl_context(
        cafile=kafka_ssl_cafile, certfile=kafka_ssl_certfile,
        keyfile=kafka_ssl_keyfile, password=kafka_ssl_password
    ) if len(kafka_ssl_password) > 0 else create_ssl_context(
        cafile=kafka_ssl_cafile, certfile=kafka_ssl_certfile,
        keyfile=kafka_ssl_keyfile)


async def create_aio_consumer() -> AIOKafkaConsumer:
    """Create and return AIOKafkaConsumer."""
    return AIOKafkaConsumer(
        kafka_topic_rbl, group_id='rbl_consumer',
        bootstrap_servers=f'{kafka_host}:{kafka_port}',
        ssl_context=create_kafka_ssl_context(), security_protocol='SSL',
        sasl_mechanism=kafka_sasl_mechanism,
        sasl_plain_username=kafka_sasl_plain_username,
        sasl_plain_password=kafka_sasl_plain_password,
        value_deserializer=lambda v: loads(v)
    ) if kafka_ssl else AIOKafkaConsumer(
        kafka_topic_rbl, group_id='rbl_consumer',
        bootstrap_servers=f'{kafka_host}:{kafka_port}',
        security_protocol='PLAINTEXT', sasl_mechanism=kafka_sasl_mechanism,
        sasl_plain_username=kafka_sasl_plain_password,
        sasl_plain_password=kafka_sasl_plain_password,
        value_deserializer=lambda v: loads(v))


async def create_aio_producer() -> AIOKafkaProducer:
    """Create and return AIOKafkaProducer."""
    return AIOKafkaProducer(
        bootstrap_servers=f'{kafka_host}:{kafka_port}',
        value_serializer=lambda v: dumps(v).encode('utf-8'),
        enable_idempotence=True, compression_type=kafka_compression,
        ssl_context=create_kafka_ssl_context(),
        security_protocol='SSL', sasl_mechanism=kafka_sasl_mechanism,
        sasl_plain_username=kafka_sasl_plain_username,
        sasl_plain_password=kafka_sasl_plain_password
    ) if kafka_ssl else AIOKafkaProducer(
        bootstrap_servers=f'{kafka_host}:{kafka_port}',
        value_serializer=lambda v: dumps(v).encode('utf-8'),
        enable_idempotence=True, compression_type=kafka_compression,
        security_protocol='PLAINTEXT', sasl_mechanism=kafka_sasl_mechanism,
        sasl_plain_username=kafka_sasl_plain_username,
        sasl_plain_password=kafka_sasl_plain_password)
