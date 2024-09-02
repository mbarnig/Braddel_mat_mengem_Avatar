#!/usr/bin/env python3
#
#  Copyright © 2023 ZLS. All rights reserved.
#

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.endpoints.v1 import api_router


app = FastAPI(
    title="ZLS GPU Schreifmaschinn Backend",
    openapi_url=f"{settings.API_V1_STR}/openapi_url.json",
    # docs_url=None,
    # redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
