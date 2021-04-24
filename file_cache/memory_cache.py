import asyncio
import datetime
import os
import uuid
from multiprocessing import Process, Queue
from typing import Dict

import aiofiles
from fastapi import UploadFile

from file_cache import settings

PROJECT_FILE_DICT: Dict[str, Dict[str, str]] = {}
queue = Queue()


def remove_file():
    while True:
        file_path = queue.get()
        # file_path = PROJECT_FILE_DICT[project_id].pop(file_id)['path']
        os.remove(file_path)


p = Process(target=remove_file)
p.start()


async def wait_remove_file(project_id, file_id):
    await asyncio.sleep(int(settings.EXPIRE_TIME))
    file_path = PROJECT_FILE_DICT[project_id].pop(file_id)
    if file_path:
        queue.put(file_path)
    else:
        pass


async def default_file_path(project_id: str, file: UploadFile) -> str:
    """
    文件信息存储到内存
    :param project_id:
    :param file:
    :return:
    """

    file_id = str(uuid.uuid4())
    file_path = os.path.join(
        settings.MEDIA_ROOT,
        project_id,
        str(datetime.datetime.utcnow().date()),
        file_id + "." + file.filename.split(".")[-1],
    )
    if PROJECT_FILE_DICT.get(project_id):
        PROJECT_FILE_DICT[project_id][file_id] = file_path
    else:
        PROJECT_FILE_DICT[project_id] = {file_id: file_path}

    file_dir, file_name = os.path.split(file_path)
    file_dir = os.path.abspath(file_dir)
    print(os.path.exists(file_dir))
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    try:
        # 异步保存文件
        async with aiofiles.open(
            os.path.join(settings.BASE_DIR, file_dir, file_name), "wb"
        ) as afp:
            await afp.write(await file.read())
        asyncio.create_task(wait_remove_file(project_id, file_id))
    except Exception as e:
        PROJECT_FILE_DICT[project_id].pop(file_id)
        raise e
    return file_id


async def get_file_path(project_id: str, file_id: str) -> str:
    """
    获取文件id
    :param project_id:
    :param file_id:
    :return:
    """
    file_path = PROJECT_FILE_DICT[project_id].pop(file_id)
    return file_path
