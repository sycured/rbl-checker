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


def create_kafka_ssl_context(ca=kafka_ssl_cafile,
                             cert=kafka_ssl_certfile,
                             key=kafka_ssl_keyfile,
                             pwd=kafka_ssl_password) -> SSLContext:
    """Create and return ssl_context needed by Kafka when SSL is activated."""
    return create_ssl_context(cafile=ca, certfile=cert, keyfile=key,
                              password=pwd) if len(pwd) > 0 else \
        create_ssl_context(cafile=ca, certfile=cert, keyfile=key)


def create_aio_producer(ssl=kafka_ssl, eventloop=loop, host=kafka_host,
                        port=kafka_port, compression=kafka_compression,
                        saslmechanism=kafka_sasl_mechanism,
                        saslplainusername=kafka_sasl_plain_username,
                        saslplainpassword=kafka_sasl_plain_password
                        ) -> AIOKafkaProducer:
    """Create and return AIOKafkaProducer."""
    return AIOKafkaProducer(
        loop=eventloop, bootstrap_servers=f'{host}:{port}',
        value_serializer=lambda v: dumps(v).encode('utf-8'),
        compression_type=compression, ssl_context=create_kafka_ssl_context(),
        security_protocol='SSL', sasl_mechanism=saslmechanism,
        sasl_plain_username=saslplainusername,
        sasl_plain_password=saslplainpassword) if ssl else AIOKafkaProducer(
        loop=loop, bootstrap_servers=f'{kafka_host}:{kafka_port}',
        value_serializer=lambda v: dumps(v).encode('utf-8'),
        compression_type=kafka_compression, security_protocol='PLAINTEXT',
        sasl_mechanism=saslmechanism, sasl_plain_username=saslplainusername,
        sasl_plain_password=saslplainpassword)
