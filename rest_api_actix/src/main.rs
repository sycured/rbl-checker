use actix_web::middleware::{Compress, Logger};
use actix_web::{App, HttpServer};
use env_logger::Env;
use log::warn;
use paperclip::actix::OpenApiExt;
use std::env;
use std::io::Result;

mod add;
use add::init_routes;

#[actix_web::main]
async fn main() -> Result<()> {
    env_logger::Builder::from_env(Env::default().default_filter_or("info")).init();
    let ip = env::var("APP_IP").unwrap_or_else(|_| {
        let default_ip = "127.0.0.1".to_string();
        warn!("Using default IP: {}", default_ip);
        default_ip
    });
    let port = env::var("APP_PORT").unwrap_or_else(|_| {
        let default_port = "8080".to_string();
        warn!("Using default port: {}", default_port);
        default_port
    });
    HttpServer::new(|| {
        App::new()
            .wrap_api()
            .wrap(Compress::default())
            .wrap(Logger::default())
            .configure(init_routes)
            .with_json_spec_at("/openapi.json")
            .build()
    })
    .bind(format!("{ip}:{port}", ip = ip, port = port))?
    .run()
    .await
}
