#!/usr/bin/env python3
#
#  Copyright © 2023 ZLS. All rights reserved.
#

from fastapi import APIRouter

from . import listen


__all__ = [
    "api_router",
]

api_router = APIRouter()
api_router.include_router(listen.router, prefix="/listen", tags=["listen"])
