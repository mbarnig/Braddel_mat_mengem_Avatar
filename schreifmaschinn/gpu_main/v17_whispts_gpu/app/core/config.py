#!/usr/bin/env python3
#
#  Copyright © 2023 ZLS. All rights reserved.
#

import os

from typing import List
from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    MODEL_PATH: str = "./app/service/zls-whisper/"
    AUDIO_SAMPLE_RATE: int = 16000
    AUDIO_LENGTH_RESTRICTION: int = 0 #30*AUDIO_SAMPLE_RATE
    AUDIO_CHANNELS: int = 1
    ORIGINS: List[str] = ["*"]

settings = Settings()

# ORIGINS: List[str] = [
#         "https://dev.braddel.net",
#         "https://neischreifmaschinn.braddel.net",
#         "https://asr-frontend-whisperts-cloudrunbe-v01-g47egm2hya-ez.a.run.app",
#         "https://asr-frontend-whisperts-v01-g47egm2hya-ez.a.run.app",
#         "158.64.182.62",
#         "0.0.0.0"
#     ]