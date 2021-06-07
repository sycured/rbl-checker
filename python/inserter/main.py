"""Consumes message from Kafka, check in RBL and insert positive IP."""
from asyncio import run, set_event_loop_policy

from aiokafka import AIOKafkaConsumer

from aiopg import Pool

from db_utils import create_db_pool, insert_result

from kafka_utils import create_aio_consumer

from uvloop import EventLoopPolicy

set_event_loop_policy(EventLoopPolicy())


async def app():
    """Take message from the queue and insert in the database."""
    aio_consumer: AIOKafkaConsumer = await create_aio_consumer()
    db_pool: Pool = await create_db_pool()
    await aio_consumer.start()
    async for msg in aio_consumer:
        if msg is None:
            continue
        await insert_result(db_pool, msg.value['date'],
                            msg.value['ip'], msg.value['rblname'])


run(app())
