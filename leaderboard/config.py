# config.py
import os
from dotenv import load_dotenv

load_dotenv()

def get_redis_config():
    redis_host = os.getenv("REDIS_HOST")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    redis_password = os.getenv("REDIS_PASSWORD")
    redis_ssl = os.getenv("REDIS_SSL", "True").lower() in ["true", "1", "yes"]
    redis_ssl_cert_reqs = os.getenv("REDIS_SSL_CERT_REQS")
    if redis_ssl_cert_reqs == "None":
        redis_ssl_cert_reqs = None
    return {
        "host": redis_host,
        "port": redis_port,
        "password": redis_password,
        "ssl": redis_ssl,
        "ssl_cert_reqs": redis_ssl_cert_reqs,
    }
