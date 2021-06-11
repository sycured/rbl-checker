use log::warn;
use std::env::var;

pub async fn get_from_env_or_default(env_name: &str, default: String) -> String {
    var(env_name).unwrap_or_else(|_| {
        let default = default;
        warn!(
            "Using default {name}: {value}",
            name = env_name,
            value = default
        );
        default
    })
}

pub async fn kafka_compression() -> String {
    get_from_env_or_default("KAFKA_COMPRESSION", "lz4".to_string()).await
}

pub async fn kafka_hosts() -> String {
    get_from_env_or_default("KAFKA_HOSTS", "127.0.0.1:9092".to_string()).await
}
