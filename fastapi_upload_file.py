import os
from os import stat_result
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


app: FastAPI = FastAPI()

@app.post("/upload_file")
async def upload (request: Request) -> dict[str, str]:
    file_name: str = "upload.png"

    current_file_size: int = 0
    if os.path.exists(file_name):
        file_stat: stat_result = os.stat(file_name)
        current_file_size = file_stat.st_size

    headers: dict[str, str] = {}
    response: dict[str, str] = {"status": "failed"}

    if "content-range" in request.headers:
        content_range: dict[str, int] = parse_content_range_request_header(request.headers["content-range"])

        if current_file_size < content_range["size"]:
            writen_bytes: int = 0

            with open(file_name, "ab") as file:
                data: bytes = await request.body()
                writen_bytes = file.write(data)

            if writen_bytes > 0:
                response["status"] = "success"
                headers["Range"] = f"bytes={current_file_size + writen_bytes}-"

    return JSONResponse(response, headers=headers)


def parse_content_range_request_header (header: str) -> dict[str, int]:
    content_range: str = header.split(" ")[1]
    range_size: list = content_range.split("/")
    range: list = range_size[0].split("-")
    return {
        "range_start": int(range[0]),
        "range_end": int(range[1]),
        "size": int(range_size[1]),
    }



