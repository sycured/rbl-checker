use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
pub struct IpFromKafka {
    pub ip: String,
}

#[derive(Serialize)]
pub struct Result {
    pub date: String,
    pub ip: String,
    pub rbl: String,
}
