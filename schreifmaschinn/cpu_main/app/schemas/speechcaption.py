#!/usr/bin/env python3
#
#  Copyright © 2023 ZLS. All rights reserved.
#

from pydantic import BaseModel


class WordTimestamp(BaseModel):
    word: str
    startTime: float
    endTime: float
    confidence: float

class SpeechCaption(BaseModel):
    text: str
    words: list[WordTimestamp]
