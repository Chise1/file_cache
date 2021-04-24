import os
from multiprocessing import Process, Queue
from typing import Dict

PROJECT_FILE_DICT: Dict[str, Dict[str, str]] = {}
queue = Queue()


def _remove_file():
    while True:
        file_path = queue.get()
        os.remove(file_path)


p = Process(target=_remove_file)
p.start()


def remove_file(file_path: str):
    queue.put(file_path)
