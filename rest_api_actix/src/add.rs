use actix_web::Result;
use ipaddress::IPAddress;
use log::info;
use paperclip::actix::web::{post, resource, Json, ServiceConfig};
use paperclip::actix::{api_v2_operation, Apiv2Schema};
use serde::{Deserialize, Serialize};

#[derive(Deserialize, Apiv2Schema)]
pub struct AddPost {
    ip_range: String,
}

#[derive(Debug, Serialize, Apiv2Schema)]
pub struct AddResp {
    result: String,
}

fn create_json(data: String) {
    info!("{}", Json(AddResp { result: data }).result)
}

#[api_v2_operation(
    description = "Add the range to the queue.",
    consumes = "application/json",
    produces = "application/json"
)]
pub async fn add(data: Json<AddPost>) -> Result<Json<AddResp>> {
    let ipr = IPAddress::parse(data.ip_range.to_string()).unwrap();
    if !ipr.to_string().contains("/32") {
        ipr.each_host(|ip| create_json(ip.to_string()))
    } else {
        create_json(ipr.to_string())
    }
    Ok(Json(AddResp {
        result: format!("Success, new IP range added: {}", ipr.to_string()),
    }))
}

pub fn init_routes(cfg: &mut ServiceConfig) {
    cfg.service(resource("/add").route(post().to(add)));
}
