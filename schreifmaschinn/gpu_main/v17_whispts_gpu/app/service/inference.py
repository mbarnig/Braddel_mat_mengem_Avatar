#!/usr/bin/env python3
#
#  Copyright © 2023 ZLS. All rights reserved.
#


import os
import re
import numpy as np
import time

import datetime
import ffmpeg
import math
from collections import Counter
import uuid

import transformers
import torch
import whisper_timestamped as whisper
from typing import Optional, Dict, List, Any

from app.core.config import settings



def asr_pipe(validated_data,model):


    

    #result = pipe("vad_chunks/temp_" + out_uuid + str(i) + ".wav",return_timestamps=True, chunk_length_s=30,stride_length_s=[6,0])

    starttime = time.time()
    wholetext= []
    wholetext_cc= []
    wholetext_raw= []
    dict1 = {}
    dict1["words"] = []

    chunk_limit = settings.AUDIO_SAMPLE_RATE*30
    chunks = math.ceil(len(validated_data)/chunk_limit)

    print(f">>>>> start ASR. duration of audiofile: {len(validated_data)/settings.AUDIO_SAMPLE_RATE:.2f}s.")

    for chunk in range(chunks):
        print(f"processing chunk {chunk}/{chunks}")
        
        relativeStartTime = chunk*30
        

        if chunk==chunks-1:
            validated_data1 = torch.as_tensor(validated_data[relativeStartTime*settings.AUDIO_SAMPLE_RATE:])
            #print(f"chunkStartTime: {chunk*30*16000}. chunkEndTime: {lendata}")
        else:
            validated_data1 = torch.as_tensor(validated_data[relativeStartTime*settings.AUDIO_SAMPLE_RATE:(chunk+1)*30*settings.AUDIO_SAMPLE_RATE])
            #print(f"chunkStartTime: {chunk*30*16000}. chunkEndTime: {(chunk+1)*30*16000}")

        if torch.cuda.is_available():
            validated_data1 = validated_data1.to(torch.device("cuda"))
            print("Tensor moved to GPU")

        try:
            result = whisper.transcribe(model, validated_data1, language="lb")
        except Exception as e:
            print(f"ERROR DURING COMPUTATION: {e}")
            print("computing again:")
            
            try:
                validated_data1 = torch.as_tensor(validated_data[relativeStartTime*settings.AUDIO_SAMPLE_RATE:(chunk+1)*30*settings.AUDIO_SAMPLE_RATE-int(0.25*settings.AUDIO_SAMPLE_RATE)])
                result = whisper.transcribe(model, validated_data1, language="lb")
            except Exception as e:
                print(f"AGAIN ERROR DURING COMPUTATION: {e}")
                print("not considering this transcription.")
                continue

        for segments in result['segments']:
            for wordinfo in segments['words']:
                wholetext_raw.append(wordinfo['text'])
                if wordinfo['confidence']<0.8:
                    #print(wordinfo)
                    if wordinfo['end']-wordinfo['start']>0.03:
                        dict2 = {}
                        dict2["word"] = wordinfo['text']
                        dict2["startTime"] = wordinfo['start']+relativeStartTime
                        dict2["endTime"] = wordinfo['end']+relativeStartTime
                        dict2["confidence"] = wordinfo['confidence']
                        dict1["words"].append(dict2)
                        wholetext.append(wordinfo['text'])
                        
                    else:
                        if wordinfo['end']%30>28:
                            dict2 = {}
                            dict2["word"] = wordinfo['text']
                            dict2["startTime"] = wordinfo['start']+relativeStartTime
                            dict2["endTime"] = wordinfo['end']+relativeStartTime
                            dict2["confidence"] = wordinfo['confidence']
                            dict1["words"].append(dict2)
                            wholetext.append(wordinfo['text'])
                            
                else:
                    if wordinfo['end']-wordinfo['start']>0.03:
                        dict2 = {}
                        dict2["word"] = wordinfo['text']
                        dict2["startTime"] = wordinfo['start']+relativeStartTime
                        dict2["endTime"] = wordinfo['end']+relativeStartTime
                        dict2["confidence"] = wordinfo['confidence']
                        dict1["words"].append(dict2)
                        wholetext.append(wordinfo['text'])
                        
                
    dict1["text"] = ' '.join(wholetext)
    # dict1["wholetext_raw"] = ' '.join(wholetext_raw)

    # dict1.keys: "words" (list of dict2), "text"
    # dict2.keys: "word", "startTime", "endTime", "confidence"
    print('>>>>>>>>>>>>>>>>>>')
    print(dict1)
    print(f"audio duration: {len(validated_data)/settings.AUDIO_SAMPLE_RATE:.2f}s. computation done in {time.time()-starttime:.2f}s.")
    print('DONE')
    return dict1

