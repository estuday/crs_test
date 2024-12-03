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
    class Payload(BaseModel):
        name: Annotated[str,Field(description="名称")]
        property: Annotated[list[str], Field(default=[],description="需要抽取的属性，不输入则抽取全部")]
    payload: Annotated[Payload, Field(description="请求内容")]
    doc_id: Annotated[str, Field(default=None, description="文档ID")]


class CRSTRResponse(BaseModel):
    class ResourceType(str, Enum):
        HANDOUTS = "讲义"
        COURSEWARE = "课件"
        EXPERIMENT = "实验"
        VIDEO = "视频"
        DATASET = "数据集"
        BOOKS = "教材"
        OTHERS = "其他"

    class Complexity(str, Enum):
        EASY = "简单"
        LITTLE_EASY = "较简单"
        MEDIUM = "中等"
        LITTLE_HARD = "较难"
        HARD = "困难"

    class SourceFrom(str, Enum):
        SELF_MAKE = "自研制作"
        BUY = "购买"
        PRIVATE = "内部私有数据"
        OFFICIAL = "组织官方发布"
        PUBLIC = "大众开源"
        UNKNOW = "未知来源"

    resourcetype: Annotated[
        ResourceType, Field(default=None,description="资源类型")
    ]
    name: Annotated[str, Field(description="资源名称")]
    description: Annotated[str, Field(default=None, description="资源描述")]
    keywords: Annotated[list[str], Field(default=[], description="关键词列表")]
    complexity: Annotated[
        Complexity, Field(default=Complexity.MEDIUM, description="复杂度")
    ]
    studyhour: Annotated[int, Field(default=0, description="学时")]
    theorystudyhour: Annotated[int, Field(default=0, description="理论学时")]
    practicalstudyhour: Annotated[int, Field(default=0, description="实践学时")]
    sourcefrom: Annotated[
        list[SourceFrom], Field(default=[SourceFrom.UNKNOW], description="来源")
    ]
    expandinfo: Annotated[list[str], Field(default=None, description="补充信息")]
    filesize: Annotated[float, Field(description="资源大小，MB")]
    filepage: Annotated[int, Field(default=None, description="资源页数")]
    videotime: Annotated[int, Field(default=None, description="视频时长")]
    resourcepath: Annotated[str, Field(default=None, description="资源本地路径")]
