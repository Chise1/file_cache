import asyncio
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
import aioredis


async def check_expired_key(ch_key: str, channel):
    """
    获取过期键并删除对应文件
    启动redis过期回调方法: redis-cli config set notify-keyspace-events KEA
    """
    ch_key_b = ch_key.encode('utf-8')
    async for ch, message in channel.iter(encoding='utf-8'):
        if ch == ch_key_b:
            print("Got message in channel:", ch, ":", message)


async def main(host, db, password):
    redis = await aioredis.create_redis_pool(f'redis://{host}',
                                             password=password,
                                             encoding='utf-8')
    ch_key = f'__keyevent@{db}__:expired'
    ch, = await redis.psubscribe(ch_key)
    assert isinstance(ch, aioredis.Channel)
    asyncio.create_task(check_expired_key(ch_key, ch))
    await redis.publish('channel:1', 'Hello')
    await redis.publish('channel:2', 'World')
    await asyncio.sleep(100)
    redis.close()
    await redis.wait_closed()


asyncio.run(main('localhost', 1, None))
