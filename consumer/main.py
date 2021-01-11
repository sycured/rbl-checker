"""Consumes message from Kafka, check in RBL and insert positive IP."""
from asyncio import get_event_loop, set_event_loop_policy
from asyncio.events import AbstractEventLoop
from datetime import datetime

from aiokafka import AIOKafkaConsumer

from aiopg import Pool

from db_utils import create_db_pool, insert_result

from dns.resolver import resolve

from kafka_utils import create_aio_consumer

from rbls import rbls

from uvloop import EventLoopPolicy

set_event_loop_policy(EventLoopPolicy())
loop: AbstractEventLoop = get_event_loop()


def check(rip, rblname):
    """Do and return the result of the query."""
    try:
        dns_query = f'{rip}.{rblname}'
        return resolve(dns_query, 'A')
    except Exception as e:
        print(f'{e=}')
        return None


async def app():
    """Do the check of the IP across the list and insert positive IP."""
    aio_consumer: AIOKafkaConsumer = await create_aio_consumer(loop)
    db_pool: Pool = await create_db_pool(loop)
    await aio_consumer.start()
    async for msg in aio_consumer:
        if msg is None:
            continue
        ip = msg.value['ip']
        rip = '.'.join(reversed(ip.split('.')))
        for rblname in rbls:
            date = datetime.now().isoformat()
            result = check(rip, rblname)
            if result is not None:
                await insert_result(db_pool, date, ip, rblname)


loop.run_until_complete(app())
