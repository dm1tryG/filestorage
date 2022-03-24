import os
import uuid
import shutil
import hashlib

from aiohttp import web
from aiohttp.web import Request
from aiohttp import streamer
from helpers import mkdir, search_file



async def file_reader(file_path=None):
    """ File streamer """
    with open(file_path, 'rb') as f:
        chunk = f.read(2 ** 16)
        while chunk:
            yield chunk
            chunk = f.read(2 ** 16)



async def upload(request: Request):
    """ Upload method """

    md5sum = hashlib.md5()
    reader = await request.multipart()
    field = await reader.next()

    ext = field.filename.split(".")[-1]
    session = uuid.uuid4()
    session_path = f'store/sessions/{session}'
    mkdir(session_path)

    with open(session_path, 'wb') as f:
        while True:
            chunk = await field.read_chunk()
            if not chunk:
                file_hash = md5sum.hexdigest()
                path = f'store/{file_hash[:2]}/{file_hash}{"." + ext if ext else ""}'
                mkdir(path)
                shutil.copyfile(session_path, path)
                os.remove(session_path)
                break

            f.write(chunk)
            md5sum.update(chunk)

    return web.json_response({"id": file_hash})


async def download(request: Request):
    """ Download method """

    file_hash = f'{request.match_info["hash"]}'
    file_path = search_file(file_hash=file_hash)



    if file_path:
        stream = web.StreamResponse(headers={"Content-Disposition": f"attachment; filename={file_path.split('/')[-1]}"})
        await stream.prepare(request)

        async for i in file_reader(file_path):
            if stream.task.done() or stream.task.cancelled():
                break
            await stream.write(bytearray(f'no: {i} ', 'utf-8'))

        await stream.write_eof()
        return stream
    else:
        return web.Response(
            text='File not found',
            status=404
        )


async def delete(request: Request):
    """ Delete method """

    file_hash = request.match_info["hash"]
    file_path = search_file(file_hash=file_hash)
    if file_path:
        os.remove(file_path)
        return web.Response(
            text='File deleted',
            status=404
        )
    else:
        return web.Response(
            text='File not found',
            status=404
        )


app = web.Application()
app.add_routes([web.post('/', upload),
                web.get('/{hash}', download),
                web.delete('/{hash}', delete),])


if __name__ == '__main__':
    web.run_app(app)
