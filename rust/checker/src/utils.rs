use super::{
    configuration::{kafka_compression, kafka_hosts},
    reverse_ip,
    structs::Result,
};

use dns_lookup::lookup_host;
use log::info;
use rdkafka::{
    client::DefaultClientContext,
    config::ClientConfig,
    consumer::stream_consumer::StreamConsumer,
    consumer::DefaultConsumerContext,
    producer::{FutureProducer, FutureRecord},
    util::{DefaultRuntime, Timeout},
};

pub async fn create_kafka_consumer() -> StreamConsumer<DefaultConsumerContext, DefaultRuntime> {
    let consumer: StreamConsumer = ClientConfig::new()
        .set("group.id", "checker")
        .set("bootstrap.servers", kafka_hosts().await)
        .set("enable.auto.commit", "true")
        .create()
        .expect("Consumer creation failed");
    consumer
}

pub async fn create_kafka_producer() -> FutureProducer<DefaultClientContext, DefaultRuntime> {
    let producer: &FutureProducer = &ClientConfig::new()
        .set("bootstrap.servers", kafka_hosts().await)
        .set("message.timeout.ms", "5000")
        .set("compression.codec", kafka_compression().await)
        .set("request.required.acks", "1")
        .set("request.timeout.ms", "1000")
        .create()
        .unwrap();
    producer.clone()
}

pub async fn lookup(date: String, ip: String, rbl: String, producer: &mut FutureProducer) {
    let resolved = lookup_host(&*format!("{}.{}", ip, rbl)).unwrap_or_default();
    match resolved.is_empty() {
        true => info!("{} on {} : clean", ip, rbl),
        false => {
            let ip_orig = reverse_ip(ip).await;
            let message = serde_json::to_string(&Result {
                date,
                ip: ip_orig,
                rbl,
            })
            .unwrap();
            let record: FutureRecord<String, String> = FutureRecord::to("result").payload(&message);
            producer.send(record, Timeout::Never).await;
        }
    }
}
