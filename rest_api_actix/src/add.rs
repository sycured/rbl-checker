use actix_web::Result;
use ipaddress::IPAddress;
use kafka::producer::{Producer, Record};
use paperclip::actix::{
    api_v2_operation,
    web::{post, resource, Data, Json, ServiceConfig},
    Apiv2Schema,
};
use serde::{Deserialize, Serialize};
use std::{ops::DerefMut, sync::Mutex};

#[derive(Deserialize, Apiv2Schema)]
pub struct AddPost {
    ip_range: String,
}

#[derive(Debug, Serialize, Apiv2Schema)]
pub struct AddResp {
    result: String,
}

fn create_json(data: String, producer: &mut Producer) {
    producer
        .send(&Record::from_value(
            "rbl",
            format!("{}", Json(AddResp { result: data }).result),
        ))
        .unwrap();
}

#[api_v2_operation(
    description = "Add the range to the queue.",
    consumes = "application/json",
    produces = "application/json"
)]
pub async fn add(data: Json<AddPost>, producer: Data<Mutex<Producer>>) -> Result<Json<AddResp>> {
    let ipr = IPAddress::parse(data.ip_range.to_string()).unwrap();
    if !ipr.to_string().contains("/32") {
        ipr.each_host(|ip| create_json(ip.to_string(), producer.lock().unwrap().deref_mut()))
    } else {
        create_json(ipr.to_string(), producer.lock().unwrap().deref_mut());
    }
    Ok(Json(AddResp {
        result: format!("Success, new IP range added: {}", ipr.to_string()),
    }))
}

pub fn init_routes(cfg: &mut ServiceConfig) {
    cfg.service(resource("/add").route(post().to(add)));
}
