import os
from typing import AsyncGenerator


def search_file(file_hash: str) -> str:
    """
    Search file in store

    :param file_hash: str - File hash
    :return: str - full path to file

    # TODO: improve search method (bu hash and etc.)
    """
    list_files = os.listdir(f'store/{file_hash[:2]}')
    for filename in list_files:
        if file_hash in filename:
            return f"store/{filename[:2]}/{filename}"


def mkdir(path: str) -> None:
    """
    Make directory if not exist

    :param path: str - path to dirs
    :return: none
    """
    directory = os.path.dirname(path)
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)


async def file_provider(file_path: str) -> AsyncGenerator[bytes]:
    """
    File provider with chunks

    :param file_path: str - path to file
    :return: AsyncGenerator[bytes]
    """
    with open(file_path, 'rb') as f:
        chunk = True
        while chunk:
            chunk = f.read(2 ** 16)
            yield chunk