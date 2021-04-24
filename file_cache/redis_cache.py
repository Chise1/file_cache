import asyncio
from typing import Optional

from fastapi import UploadFile
from . import settings
from aioredis import Redis, create_redis_pool, Channel
import logging
from .common import get_file_info
from .remove_file import remove_file
from .write_file import write_to_file

logger = logging.Logger(__file__)
redis: Optional[Redis] = None


async def write_file(project_id: str, file: UploadFile) -> str:
    """
    文件信息存储到内存
    """

    file_id, file_path = await get_file_info(file, project_id)
    await redis.set(file_id, file_path, expire=settings.EXPIRE_TIME)
    await redis.hset(project_id, file_id, file_path)
    await write_to_file(file, file_path)
    return file_id


async def check_expired_key(ch_key: str, channel):
    """
    获取过期键并删除对应文件
    启动redis过期回调方法: redis-cli config set notify-keyspace-events KEA
    """
    ch_key_b = ch_key.encode('utf-8')
    async for ch, message in channel.iter(encoding='utf-8'):
        if ch == ch_key_b:
            project_id = message.split("&")[-1]
            file_path = await redis.hget(project_id, message)
            remove_file(file_path)
            await redis.hdel(project_id, message)
        else:
            logger.warning(f"Couldn't found {message} file.")


async def get_file_path(file_id)->Optional[str]:
    """
    获取并固定文件
    :param project_id:
    :param file_id:
    :return:
    """
    project_id = file_id.split("&")[-1]
    file_path = await redis.hget(project_id, file_id)
    if file_path:
        await redis.delete(file_id)
        await redis.hdel(project_id, file_id)
    return file_path


async def init(host, db, password):
    global redis
    redis = await create_redis_pool(
        f'redis://{host}', password=password, encoding='utf-8')
    ch_key = f'__keyevent@{db}__:expired'
    ch, = await redis.psubscribe(ch_key)
    assert isinstance(ch, Channel)
    asyncio.create_task(check_expired_key(ch_key, ch))


async def close():
    global redis
    redis.close()
    await redis.wait_closed()
