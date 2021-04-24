import asyncio

import aioredis


# 死循环,不停的接收订阅的通知
async def start():
    # 连接redis数据库
    redis = await aioredis.create_redis_pool(
        f"redis://localhost:6379", db=1, )
    # 创建pubsub对象，该对象订阅一个频道并侦听新消息：
    pubsub = redis.pubsub_numpat()

    # 定义触发事件
    def event_handler(msg):
        print('Handler', msg)
        print(msg['data'])

    # 订阅redis键空间通知
    pubsub.psubscribe(**{'__keyevent@0__:expired': event_handler})

    while True:
        message = await pubsub.get_message()
        if message:
            print(message)
        else:
            await asyncio.sleep(0.01)


if __name__ == '__main__':
    asyncio.run(start())
