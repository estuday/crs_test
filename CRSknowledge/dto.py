from pydantic import BaseModel, Field
from typing import Annotated
from enum import Enum


class KnowledgeStatusCode(int, Enum):
    SUCCESS = 200
    PARSER_FAILED = 501
    GENERATE_FAILED = 502
    PROPERTY_FAILED = 503


class KnowledgeResponse(BaseModel):
    code: Annotated[
        KnowledgeStatusCode,
        Field(default=KnowledgeStatusCode.SUCCESS, description="响应码"),
    ]

    message: Annotated[str, Field(default="处理成功", description="")]

    data: Annotated[dict, Field(default=None, description="")]


class Knowledge(BaseModel):
    name: Annotated[str, Field(description="知识点名称")]

    description: Annotated[str, Field(description="知识点描述")]

    keywords: Annotated[str, Field(default=None, description="关键词")]

    alias: Annotated[str, Field(default=None, description="别名")]

    level: Annotated[str, Field(default=None, description="知识点教学层次")]

    type: Annotated[str, Field(default=None, description="知识点教学类型")]

    difficulty: Annotated[str, Field(default=None, description="复杂度")]

    name_emb: Annotated[
        list[float], Field(default=None, description="知识点的embedding")
    ]
