import os

import aiofiles
from .import settings
from .remove_file import remove_file

async def write_to_file(file, file_path):
    file_dir, file_name = os.path.split(file_path)
    file_dir = os.path.abspath(file_dir)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    try:
        # 异步保存文件
        async with aiofiles.open(
            os.path.join(settings.BASE_DIR, file_dir, file_name), "wb"
        ) as afp:
            await afp.write(await file.read())
    except Exception as e:
        remove_file(file_path)
        raise e
