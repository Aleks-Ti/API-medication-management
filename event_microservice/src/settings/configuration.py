import os
from dataclasses import dataclass
from os import getenv
from pathlib import Path

from sqlalchemy.engine import URL

BASE_DIR_PROJECT: Path = Path(__file__).resolve().parent.parent.parent
"""
project/                  < - указывает BASE_DIR_PROJECT
├── pyproject.toml
├── README.md
├── .gitignore
├── ... прочее
├── src/                  # Основная директория для кодовой базы проекта
│   └── main.py           # Основной файл приложения
│   └── __init__.py
│   └── <другие модули и файлы проекта>
└── tests/                # Директория с тестами
    └── __init__.py       # Индикатор пакета для тестов
"""


@dataclass
class DBConfig:
    name: str | None = getenv("PG_DB_NAME")
    user: str | None = getenv("PG_USER")
    passwd: str | None = getenv("PG_PASSWORD", None)
    port: int = int(getenv("PG_PORT", 5432))
    host: str = getenv("PG_HOST", "db")

    driver: str = "asyncpg"
    database_system: str = "postgresql"

    def __post_init__(self):
        required_vars = ["name", "user", "passwd", "port", "host"]
        for var in required_vars:
            value = getattr(self, var)
            if value is None:
                raise ValueError(f"Environment variable for {var} is not set")

    def build_connection(self) -> str:
        return URL.create(
            drivername=f"{self.database_system}+{self.driver}",
            username=self.user,
            database=self.name,
            password=self.passwd,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)


@dataclass
class MQEnvs:
    network_port: int | None = int(getenv("RMQ_NETWOTK_PORT"))
    user: str | None = str(getenv("RMQ_USER"))
    password: str | None = str(getenv("RMQ_PASSWORD"))
    host: str = os.getenv("RMQ_HOST") if os.getenv("DEV") == "prod" else "host.docker.internal"

    def __post_init__(self):
        required_vars = ["network_port", "user", "password", "host"]
        for var in required_vars:
            value = getattr(self, var)
            if value is None:
                raise ValueError(f"Environment variable for <{var}> is not set")

    def build_connection(self):
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.network_port}/"


@dataclass
class Configuration:
    debug: bool = getenv("DEBUG", False) == "yes"
    postgres_db = DBConfig()
    rabbit_mq = MQEnvs()


config_project = Configuration()
