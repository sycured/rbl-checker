mod configuration;
mod rbls;
mod structs;
mod utils;

use chrono::Utc;
use env_logger::{Builder, Env};
use futures::{lock::Mutex, stream, StreamExt};
use log::warn;
use rbls::rbls;
use rdkafka::{consumer::Consumer, Message};
use std::{borrow::BorrowMut, sync::Arc};
use structs::IpFromKafka;
use utils::{create_kafka_consumer, create_kafka_producer, lookup};

async fn reverse_ip(ip: String) -> String {
    let mut vec_ip: Vec<String> = ip.split(".").map(str::to_string).collect();
    vec_ip.reverse();
    vec_ip.join('.'.to_string().as_ref())
}

#[tokio::main(flavor = "multi_thread", worker_threads = 4)]
async fn main() -> () {
    Builder::from_env(Env::default().default_filter_or("info")).init();
    let list_rbls = rbls().await;
    let mut kafka_producer = create_kafka_producer().await;
    let mut kafka_consumer = create_kafka_consumer().await;
    let producer = Arc::new(Mutex::new(kafka_producer));

    kafka_consumer
        .subscribe(&*vec!["rbl"])
        .expect("Can't subscribe to specified topic");

    loop {
        match kafka_consumer.recv().await {
            Err(e) => warn!("Kafka error: {}", e),
            Ok(m) => {
                let payload = match m.payload_view::<str>() {
                    None => {
                        warn!("Message payload was empty");
                        ""
                    }
                    Some(Ok(s)) => s,
                    Some(Err(e)) => {
                        warn!("Error while deserializing message payload: {:?}", e);
                        ""
                    }
                };
                let mesg: IpFromKafka = serde_json::from_str(payload).unwrap();
                let rev_ip = reverse_ip(mesg.ip).await;
                let mut stream = stream::iter(&list_rbls);
                while let Some(rbl) = stream.next().await {
                    lookup(
                        Utc::now().to_string(),
                        rev_ip.to_string(),
                        rbl.to_string(),
                        producer.lock().await.borrow_mut(),
                    )
                    .await
                }
            }
        };
    }
}
