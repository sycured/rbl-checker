use super::configuration::kafka_hosts;
use super::structs::Result;

use dns_lookup::lookup_host;
use kafka::producer::{
    Compression::SNAPPY, DefaultHasher, DefaultPartitioner, Producer, Record, RequiredAcks::One,
};
use log::info;
use rdkafka::consumer::DefaultConsumerContext;
use rdkafka::util::DefaultRuntime;
use rdkafka::{config::ClientConfig, consumer::stream_consumer::StreamConsumer};
use std::{hash::BuildHasherDefault, time::Duration};

pub async fn create_kafka_consumer() -> StreamConsumer<DefaultConsumerContext, DefaultRuntime> {
    let consumer: StreamConsumer = ClientConfig::new()
        .set("group.id", "checker")
        .set("bootstrap.servers", kafka_hosts().await)
        .set("enable.auto.commit", "true")
        .create()
        .expect("Consumer creation failed");
    consumer
}

pub async fn create_kafka_producer(
) -> Producer<DefaultPartitioner<BuildHasherDefault<DefaultHasher>>> {
    let producer = Producer::from_hosts(vec![kafka_hosts().await])
        .with_compression(SNAPPY)
        .with_ack_timeout(Duration::from_secs(1))
        .with_required_acks(One)
        .create()
        .unwrap();
    producer
}

pub fn lookup(date: String, ip: String, rbl: String, producer: &mut Producer) {
    let resolved = lookup_host(&*format!("{}.{}", ip, rbl)).unwrap_or_default();
    match resolved.is_empty() {
        true => info!("{} on {} : clean", ip, rbl),
        false => producer
            .send(&Record::from_value(
                "result",
                serde_json::to_string(&Result { date, ip, rbl }).unwrap(),
            ))
            .unwrap(),
    }
}
