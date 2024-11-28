from pydantic import BaseModel, Field
from typing import Annotated, Any
from enum import Enum


class CRSExtractResponseCode(int, Enum):
    SUCCESS = 200
    LACK_PARAM = 501
    MISFORMAT_PARAM = 502
    UNSUPPORTED_FILE_TYPE = 503


class CRSExtractResponse(BaseModel):
    code: Annotated[
        int, Field(default=CRSExtractResponseCode.SUCCESS, description="响应码")
    ]

    message: Annotated[
        str,
        Field(default="处理成功", description="响应消息"),
    ]
    data: Annotated[Any, Field(default=None, description="处理结果")]
    doc_id: Annotated[str, Field(default=None, description="文档ID")]


class CRSExtractRequest(BaseModel):
    payload: Annotated[dict, Field(description="请求内容")]
    doc_id: Annotated[str, Field(default=None, description="文档ID")]
