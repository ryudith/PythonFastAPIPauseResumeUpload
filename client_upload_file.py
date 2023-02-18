import os
from os import stat_result
import time
import requests
from requests import Response


if __name__ == "__main__":
    url: str = "http://127.0.0.1:8000/upload_file"
    file_name: str = "youtube_banner.png"
    file_stat: stat_result = os.stat(file_name)
    file_size: int = file_stat.st_size

    with open(file_name, "rb") as file:
        chunk_size: int = 1024

        headers: dict[str, str] = {"Content-Range": f"bytes 0-{chunk_size}/{file_size}"}

        # for prevent endless loop
        max_loop: int = 10_000
        loop_count: int = 0

        current_byte: int = 0
        while file_size > current_byte and loop_count < max_loop:
            headers["Content-Range"] = f"bytes {current_byte}-{current_byte + chunk_size}/{file_size}"

            file.seek(current_byte)
            chunk: bytes = file.read(chunk_size)

            response: Response = requests.post(url, headers=headers, data=chunk)
            response_headers: dict[str, str] = response.headers

            # skip range end for simple code testing
            # counter from Range header
            #
            # header example -> Range: Bytes=0-
            if "Range" in response_headers:
                range_chunk: list = response_headers["Range"].split("=")[1].split("-")
                current_byte = int(range_chunk[0])

            print(response_headers)

            # simulate pause resume
            # sleep 5 second
            percent_upload: float = current_byte / float(file_size) * 100
            if percent_upload >= 60:
                time.sleep(5)

            loop_count += 1