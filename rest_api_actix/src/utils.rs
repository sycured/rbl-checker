use super::configuration::kafka_hosts;

use kafka::producer::{
    Compression::SNAPPY, DefaultHasher, DefaultPartitioner, Producer, RequiredAcks::One,
};
use std::{hash::BuildHasherDefault, time::Duration};

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
