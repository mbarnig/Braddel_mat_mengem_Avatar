#!/usr/bin/env python3
#
#  Copyright © 2023 ZLS. All rights reserved.
#

# import os
from fastapi import File
from fastapi import UploadFile
from fastapi.routing import APIRouter

from app import schemas
from app.core.config import settings
from app.service.inference import asr_pipe
from app.service.audio_validation import validate_audio

import transformers
import torch
import whisper_timestamped as whisper

import os
import time

router = APIRouter()

print('model loading.....')
#model = whisper.load_model("ZLSCompLing/whisper_large_v2_lb_ZLS_a", device="cpu")
model = whisper.load_model(settings.MODEL_PATH)

if torch.cuda.is_available():
    print("GPU is available and being used")
    device = torch.device("cuda")
    model.to(device)
    
else:
    device = torch.device("cpu")
    print("GPU is not available, using CPU instead")


@router.post("", response_model=schemas.SpeechCaption)
async def listen(audio_file: UploadFile):
    validated_data = await validate_audio(audio_file)
    output = asr_pipe(validated_data,model)
    return output