import os.path
import uuid
from contextlib import asynccontextmanager

import sqlalchemy
from alembic.config import Config as AlembicConfig
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


from config import db_engine_url


class _DbConfig:
    url = db_engine_url
    
    
@asynccontextmanager
async def make_session():
    engine = create_async_engine(_DbConfig.url)
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
    await engine.dispose()
    
    
def set_db_url(url: str):
    """
    Принудительно меняет адрес базы данных в make_session на указанный
    Полезно для текстов.
    :param url:
    :return:
    """
    _DbConfig.url = url
    

def get_alembic_config(db_url: str = db_engine_url) -> AlembicConfig:
    """
    Генерирует конфиг для Alembic на основе имеющегося файла настроек и данного URL бд
    :param db_url:
    :return:
    """
    config = AlembicConfig(
        file_="alembic.ini",
    )
    config.set_main_option('sqlalchemy.url', db_url)
    return config


@asynccontextmanager
async def use_temp_database(source_db_url: str):
    """
    Создаёт временную базу данных и отдаёт её через yield
    :param source_db_url: Адрес подключения
    :return:
    """
    temp_db_name = f"test_db_{uuid.uuid4().hex}"
    temp_db_url = f"{os.path.dirname(source_db_url)}/{temp_db_name}"

    await _create_database_async(source_db_url, temp_db_name)
    try:
        yield temp_db_url
    finally:
        await _drop_database_async(source_db_url, temp_db_name)


async def _create_database_async(url, database_name: str):
    """
    Создаёт новую БД в postgresql
    :param url: URL для подключения
    :param database_name: Название БД
    :return:
    """
    connect_url = f"{os.path.dirname(url)}/postgres"
    db_engine = create_async_engine(connect_url, isolation_level="AUTOCOMMIT")
    async with db_engine.begin() as conn:
        text = "CREATE DATABASE {}".format(database_name.replace("'", "\\'"))
        await conn.execute(sqlalchemy.text(text))


async def _drop_database_async(url, database_name: str):
    """
    Удаляет указанную БД в postgresql
    :param url: URL для подключения
    :param database_name: Название БД
    :return:
    """
    connect_url = f"{os.path.dirname(url)}/postgres"
    db_engine = create_async_engine(connect_url, isolation_level="AUTOCOMMIT")
    async with db_engine.begin() as conn:
        text = "DROP DATABASE {}".format(database_name.replace("'", "\\'"))
        await conn.execute(sqlalchemy.text(text))