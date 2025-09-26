import asyncio
import json
import os
import re
import sys
import uuid
from abc import abstractmethod
from typing import Optional, Self, List

import dotenv
import httpx
from langchain_openai import OpenAIEmbeddings
from openpyxl.styles.builtins import output
from typing_extensions import TypedDict

from fastmcp import Client
from pydantic import BaseModel
from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field
from pathlib import Path

async def main():
    config = {"model": "Qwen3-Embedding-0.6B", "dimensions": 1024, "check_embedding_ctx_length": False}
    # config = {"model": "xiaobu-embedding-v2", "dimensions": 1792, "check_embedding_ctx_length": False}
    # config = {"model": "stella_en_400M_v5", "dimensions": 1024, "check_embedding_ctx_length": False}
    config["http_client"] = httpx.Client(
        limits=httpx.Limits(max_connections=1000, max_keepalive_connections=100),
        timeout=httpx.Timeout(timeout=600.0, connect=5.0),
        follow_redirects=True,
        verify=False,
    )
    config["http_async_client"] = httpx.AsyncClient(
        limits=httpx.Limits(max_connections=1000, max_keepalive_connections=100),
        timeout=httpx.Timeout(timeout=600.0, connect=5.0),
        follow_redirects=True,
        verify=False,
    )
    config['base_url'] = "http://10.185.233.128:38098/models/v1"
    embeddings = OpenAIEmbeddings.model_validate(config)

    result = await embeddings.aembed_query("你好jzzheng")
    print(result)
    print(len(result))

if __name__ == '__main__':
    os.environ.setdefault("OPENAI_API_KEY", '')
    asyncio.run(main())