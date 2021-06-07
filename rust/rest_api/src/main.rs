use actix_web::{
    middleware::{Compress, Logger},
    web::Data,
    App, HttpServer,
};
use env_logger::{Builder, Env};
use paperclip::actix::OpenApiExt;
use std::{io::Result, sync::Mutex};

mod add;
use add::init_routes;

mod configuration;
use configuration::{app_ip, app_port};

mod utils;
use utils::create_kafka_producer;

#[actix_web::main]
async fn main() -> Result<()> {
    Builder::from_env(Env::default().default_filter_or("info")).init();
    let producer = create_kafka_producer().await;
    let producer = Data::new(Mutex::new(producer));
    HttpServer::new(move || {
        App::new()
            .wrap_api()
            .wrap(Compress::default())
            .wrap(Logger::default())
            .configure(init_routes)
            .app_data(producer.clone())
            .with_json_spec_at("/openapi.json")
            .build()
    })
    .bind(format!(
        "{ip}:{port}",
        ip = app_ip().await,
        port = app_port().await
    ))?
    .run()
    .await
}
