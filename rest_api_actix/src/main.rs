use actix_web::middleware::{Compress, Logger};
use actix_web::{App, HttpServer};
use env_logger::Env;
use paperclip::actix::OpenApiExt;
use std::io::Result;

mod add;
use add::init_routes;

mod configuration;
use configuration::{app_ip, app_port};

// mod kafka;

#[actix_web::main]
async fn main() -> Result<()> {
    env_logger::Builder::from_env(Env::default().default_filter_or("info")).init();
    HttpServer::new(|| {
        App::new()
            .wrap_api()
            .wrap(Compress::default())
            .wrap(Logger::default())
            .configure(init_routes)
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
