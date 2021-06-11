use actix_web::Result;
use futures::{stream, StreamExt};
use ipaddress::IPAddress;
use paperclip::actix::{
    api_v2_operation,
    web::{post, resource, Data, Json, ServiceConfig},
    Apiv2Schema,
};
use rdkafka::{
    producer::{FutureProducer, FutureRecord},
    util::Timeout,
};
use serde::{Deserialize, Serialize};
use std::{
    ops::DerefMut,
    sync::{Arc, Mutex},
};

#[derive(Deserialize, Apiv2Schema)]
pub struct AddPost {
    ip_range: String,
}

#[derive(Serialize, Apiv2Schema)]
pub struct AddIpToKafka {
    ip: String,
}

#[derive(Serialize, Apiv2Schema)]
pub struct Response {
    status: String,
}

async fn create_json(data: String, producer: &mut FutureProducer) {
    let message = serde_json::to_string(&AddIpToKafka { ip: data }).unwrap();
    let record: FutureRecord<String, String> = FutureRecord::to("rbl").payload(&message);
    producer.send(record, Timeout::Never).await;
}

#[api_v2_operation(
    description = "Add the range to the queue.",
    consumes = "application/json",
    produces = "application/json"
)]
pub async fn add(
    data: Json<AddPost>,
    producer: Data<Mutex<FutureProducer>>,
) -> Result<Json<Response>> {
    let ipr = IPAddress::parse(data.ip_range.to_string()).unwrap();
    match ipr.to_string().contains("/32") {
        true => create_json(ipr.to_s(), producer.lock().unwrap().deref_mut()).await,
        false => {
            let mut hosts: Vec<String> = vec![];
            let mut hosts_mutex = Arc::new(Mutex::new(hosts));
            ipr.each_host(|ip| hosts_mutex.lock().unwrap().push(ip.to_s()));
            let mut stream = stream::iter(hosts_mutex.lock().unwrap().to_vec());
            while let Some(ip) = stream.next().await {
                let value = String::from(ip);
                create_json(value, producer.lock().unwrap().deref_mut()).await;
            }
        }
    }
    Ok(Json(Response {
        status: format!("Success, new IP range added: {}", ipr.to_string()),
    }))
}

pub fn init_routes(cfg: &mut ServiceConfig) {
    cfg.service(resource("/add").route(post().to(add)));
}
