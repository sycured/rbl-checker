#!/usr/bin/env python3
# coding: utf-8

"""RBL-Checker: rest api to add new range to check."""
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


@app.post('/add', status_code=200)
async def add(body: AddReqJson):
    """Add the range to the queue."""
    await aio_producer.send(topic=kafka_topic, value=body.json())
    return Response()
