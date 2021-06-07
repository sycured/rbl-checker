"""Configuration need by the restapi."""
from distutils.util import strtobool
from os import getenv


kafka_compression: str = getenv(key='KAFKA_COMPRESSION', default='lz4')
kafka_host: str = getenv(key='KAFKA_ADDR', default='localhost')
kafka_port: int = getenv(key='KAFKA_PORT', default=9092)
kafka_sasl_mechanism: str = getenv(key='KAFKA_SASL_MECHANISM', default='PLAIN')
kafka_sasl_plain_username: str = getenv(key='KAFKA_SASL_PLAIN_USERNAME',
                                        default=None)
kafka_sasl_plain_password: str = getenv(key='KAFKA_SASL_PLAIN_PASSWORD',
                                        default=None)
kafka_ssl: bool = strtobool(getenv(key='KAFKA_SSL', default='false'))
kafka_ssl_cafile: str = getenv(key='KAFKA_SSL_CAFILE', default='')
kafka_ssl_certfile: str = getenv(key='KAFKA_SSL_CERTFILE', default='')
kafka_ssl_keyfile: str = getenv(key='KAFKA_SSL_KEYFILE', default='')
kafka_ssl_password: str = getenv(key='KAFKA_SSL_PASSWORD', default='')
kafka_topic_rbl: str = getenv(key='KAFKA_TOPIC', default='rbl')
