import uuid
from . import settings
import os
import datetime


async def get_file_info(file, project_id):
    file_id = str(uuid.uuid4()) + "&" + project_id
    file_path = os.path.join(
        settings.MEDIA_ROOT,
        project_id,
        str(datetime.datetime.utcnow().date()),
        file_id + "." + file.filename.split(".")[-1],
    )
    return file_id, file_path
