from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

from file_cache import settings

if settings.CACHE == "MEMORY":
    from file_cache.memory_cache import default_file_path, get_file_path

app = FastAPI(title="文件缓存系统")


class FileID(BaseModel):
    file_id: str


class FilePath(BaseModel):
    file_path: str


@app.post("/file/{project_id}", response_model=FileID)
async def write_file(project_id: str, file: UploadFile = File(...,)):
    """
    写入文件
    """
    file_id = await default_file_path(project_id, file)
    return FileID(file_id=file_id)


@app.get("/file/{project_id}/{file_id}", response_model=FilePath)
async def file_path(project_id: str, file_id: str):
    file_path = await get_file_path(project_id, file_id)
    return FilePath(file_path=file_path)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
