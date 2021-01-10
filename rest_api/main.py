#!/usr/bin/env python3
# coding: utf-8

"""RBL-Checker: rest api to add new range to check."""
from ipaddress import ip_network

from aiokafka import AIOKafkaProducer

from config import kafka_topic

from fastapi import FastAPI
from fastapi.responses import Response

from kafka_utils import create_aio_producer

from pydantic import BaseModel


app: FastAPI = FastAPI(title='RBL-Checker', docs_url='/')

aio_producer: AIOKafkaProducer = create_aio_producer()


class AddReqJson(BaseModel):
    """Defines the JSON schema used by /add."""

    ip_range: str


@app.on_event('startup')
async def startup_event():
    """Start aio_producer using asyncio with uvloop on statup."""
    await aio_producer.start()


@app.on_event('shutdown')
async def shutdown_event():
    """Stop aio_producer using asyncio with uvloop on shutdown."""
    await aio_producer.stop()


async def send_msg(msg):
    """Send msg to Kafka."""
    await aio_producer.send(topic=kafka_topic, value=msg)


async def split_range(ip_range):
    """Split network range to individual ip."""
    for ip in ip_network(ip_range).hosts():
        msg = {'ip': str(ip)}
        await send_msg(msg)


@app.post('/add', status_code=200)
async def add(body: AddReqJson):
    """Add the range to the queue."""
    if '/32' in body.ip_range:
        msg = {'ip': body.ip_range.split('/')[0]}
        await send_msg(msg)
    else:
        await split_range(body.ip_range)
    return Response()
