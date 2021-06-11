use super::configuration::{kafka_compression, kafka_hosts};

use rdkafka::{
    client::DefaultClientContext, config::ClientConfig, producer::FutureProducer,
    util::DefaultRuntime,
};

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
