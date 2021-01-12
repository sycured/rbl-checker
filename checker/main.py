"""Consumes message from Kafka, check in RBL and insert positive IP."""
from asyncio import run, set_event_loop_policy
from datetime import datetime

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from config import kafka_topic_result

from dns.resolver import resolve

from kafka_utils import create_aio_consumer, create_aio_producer

from rbls import rbls

from uvloop import EventLoopPolicy


async def check(date, ip, rip, rblname):
    """Do and return the result of the query."""
    try:
        dns_query = f'{rip}.{rblname}'
        rst = resolve(dns_query, 'A')
        if rst is not None:
            return {'date': date, 'ip': ip, 'rblname': rblname}
    except Exception as e:
        print(e)
        return None


async def app():
    """Do the check of the IP across the list and insert positive IP."""
    consumer_rbl: AIOKafkaConsumer = await create_aio_consumer()
    producer_result: AIOKafkaProducer = await create_aio_producer()
    await consumer_rbl.start()
    await producer_result.start()
    async for msg in consumer_rbl:
        if msg is None:
            continue
        ip = msg.value['ip']
        rip = '.'.join(reversed(ip.split('.')))
        for rblname in rbls:
            date = datetime.now().isoformat()
            result = await check(date, ip, rip, rblname)
            if result is not None:
                await producer_result.send(topic=kafka_topic_result,
                                           value=result)


set_event_loop_policy(EventLoopPolicy())
run(app())
