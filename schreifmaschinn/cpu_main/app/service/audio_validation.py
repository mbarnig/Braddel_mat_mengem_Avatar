#!/usr/bin/env python3
#
#  Copyright © 2023 ZLS. All rights reserved.
#

import numpy as np
import subprocess
import time

from fastapi.exceptions import HTTPException
from fastapi import UploadFile
from starlette import status

from app.core.config import settings


async def validate_audio(audio_file: UploadFile) -> np.ndarray:
    print('>>>>> validate audio <<<<<')
    start = time.time()
    if audio_file.content_type.split("/")[0] != "audio":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="file type not supported!"
        )

    data = await audio_file.read()

    sr = str(settings.AUDIO_SAMPLE_RATE)
    ac = str(settings.AUDIO_CHANNELS)
    format_for_conversion = "f32le"

    ffmpeg_command = [
        "ffmpeg",
        "-i",
        "pipe:0",
        "-ac",
        ac,
        "-ar",
        sr,
        "-f",
        format_for_conversion,
        "-hide_banner",
        "-loglevel",
        "quiet",
        "pipe:1",
    ]

    try:
        ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    except FileNotFoundError:
        raise ValueError("ffmpeg was not found but is required to load audio files from filename")

    output_stream = ffmpeg_process.communicate(data)
    out_bytes = output_stream[0]
    audio = np.frombuffer(out_bytes, np.float32)

    if settings.AUDIO_LENGTH_RESTRICTION:
        audio = audio[:settings.AUDIO_LENGTH_RESTRICTION]
    print(f'>>>>> validated audio in {time.time()-start:.2f}s. <<<<<')
    return audio
