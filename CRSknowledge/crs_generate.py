from nova.data.logos import Logos
from nova.sdk.llm.spark.client import Spark
import requests
import json
from fastapi.responses import StreamingResponse
import uuid
from .mongoODM import KnowledgeODM, KnowledgeBetaODM
from mongoengine import connect
from fastapi import APIRouter, File, UploadFile
from .dto import KnowledgeStatusCode, KnowledgeResponse
from .utils import (
    remove_digits_and_dots,
    get_cluster_msg,
    get_description_msg,
    get_knowledge_msg,
    extract_content,
)
from .const import (
    DOCUMENT_PARSER_REQUEST_URL,
    MONGO_DB_NAME,
    MONGO_DB_HOST,
    MONGO_DB_PASSWORD,
    MONGO_DB_USERNAME,
    EMBEDDING_URL,
)

knowledge_router = APIRouter()
connect(
    db=MONGO_DB_NAME,
    host=MONGO_DB_HOST,
    username=MONGO_DB_USERNAME,
    password=MONGO_DB_PASSWORD,
    authentication_source="admin",  # 指定认证数据库
)

spark = Spark()
llm = spark


def parser_document(files, beta=False):

    _parser = requests.post(DOCUMENT_PARSER_REQUEST_URL, files=files).text

    parser_rsp = json.loads(_parser)
    para_list = []
    # 处理文档解析后的结果
    if parser_rsp["code"] == 200:
        title = None
        sub_para_list = []
        for para_info in parser_rsp["data"]["result"]:
            if para_info.get("content_type") == "title":
                if beta:
                    if title:
                        para_list.append((title, sub_para_list))
                    title = para_info.get("content", [""])[0]
                elif title and sub_para_list:
                    para_list.append((title, sub_para_list))
                    sub_para_list = []
                title = para_info.get("content", [""])[0]
            elif title and para_info.get("content_type") == "text":
                sub_para_list += para_info.get("content", [])
        return para_list
    else:
        return None


async def generate_property(knowledge_info: dict[str]) -> dict[str] | None:
    from template import GENERATE_PROPERTY_TEMPLATE

    message = Logos(
        role=Logos.Role.USER,
        content=GENERATE_PROPERTY_TEMPLATE.render(konwledge_info=knowledge_info),
    )
    _rsp = await llm.acall([message])
    rsp = extract_content(_rsp.content, ("{", "}"))
    try:
        property = json.loads(rsp)
        return property
    except:
        return None


async def generate_property_with_rag(knowledge_info: dict[str]) -> dict[str] | None:
    from template import GENERATE_PROPERTY_RAG_TEMPLATE
    from dao import cosine_knowledge

    embedding_rsp = requests.post(
        EMBEDDING_URL, json={"texts": [knowledge_info["knowledge"]]}
    ).text
    query_name_embedding = json.loads(embedding_rsp)["data"][0]
    similarity_knowledge = cosine_knowledge(query_name_embedding)
    message = Logos(
        role=Logos.Role.USER,
        content=GENERATE_PROPERTY_RAG_TEMPLATE.render(
            konwledge_info=knowledge_info, similarity_knowledge=similarity_knowledge
        ),
    )
    _rsp = await llm.acall([message])
    rsp = extract_content(_rsp.content, ("{", "}"))
    try:
        property = json.loads(rsp)
        return property
    except:
        return None


@knowledge_router.post("/knowledge")
async def knowledge(file: UploadFile = File(...)):
    file_content = await file.read()
    # 调取文档解析接口
    files = {"file": (file.filename, file_content, file.content_type)}
    para_list = parser_document(files=files)

    async def generate_knowledge():
        if para_list:
            for t, paras in para_list:
                message = get_knowledge_msg(t, paras)
                _llm_resp = await llm.acall([message])
                if _llm_resp == "[]":
                    continue
                llm_resp = extract_content(_llm_resp.content, ("{", "}"))
                if llm_resp:
                    knowledge = json.loads(llm_resp)
                    # 生成属性
                    # property_rsp = await generate_property_with_rag(knowledge_info=knowledge)
                    property_rsp = None
                    if property_rsp:
                        knowledge.update(property_rsp)
                        knowledge["data_id"] = uuid.uuid4().hex
                        KnowledgeODM(
                            id=knowledge["data_id"],
                            name=knowledge["knowledge"],
                            description=knowledge["description"],
                            data=[t] + paras,
                            level=knowledge["level"],
                            type=knowledge["type"],
                            difficulty=knowledge["difficulty"],
                            keywords=knowledge["keywords"],
                        ).save()
                        yield KnowledgeResponse(data=knowledge).model_dump_json()
                    else:
                        knowledge["data_id"] = uuid.uuid4().hex
                        KnowledgeODM(
                            id=knowledge["data_id"],
                            name=knowledge["knowledge"],
                            description=knowledge["description"],
                            data=[t] + paras,
                        ).save()
                        yield KnowledgeResponse(data=knowledge).model_dump_json()
                else:
                    yield KnowledgeResponse(
                        code=KnowledgeStatusCode.GENERATE_FAILED,
                        message="知识点生成失败",
                    ).model_dump_json()
        else:
            yield KnowledgeResponse(
                code=KnowledgeStatusCode.PARSER_FAILED, message="文档解析失败"
            ).model_dump_json()

    response = StreamingResponse(generate_knowledge(), media_type="application/json")
    return response


@knowledge_router.post("/knowledge_beta")
async def knowledge_beta(file: UploadFile = File(...)):
    file_content = await file.read()
    files = {"file": (file.filename, file_content, file.content_type)}
    para_list = parser_document(files=files, beta=True)

    # 全部和逐个返回的差异：假设全部返回用时30s，但在30s期间用户看不到任何内容。逐个返回会用45s，但在这期间用户会看见一个知识点一个知识点的生成
    async def generate_knowledge_beta():
        if para_list:
            title_list = [remove_digits_and_dots(para[0]) for para in para_list]
            cluster_message = get_cluster_msg(title_list)
            _cluster_resp = await llm.acall([cluster_message])
            cluster_resp = extract_content(_cluster_resp.content, ("[", "]"))
            if cluster_resp:
                knowledge_list = json.loads(cluster_resp)
                for k in knowledge_list:
                    title_idx = k["title"]
                    sub_title = []
                    data = []
                    for idx in title_idx:
                        sub_title.append(title_list[idx])
                        data.extend([para_list[idx][0]] + para_list[idx][1])
                    des_message = get_description_msg(k["knowledge"], sub_title)
                    des_resp = await llm.acall([des_message])
                    knowledge = {
                        "knowledge": k["knowledge"],
                        "description": des_resp.content,
                    }
                    # property_rsp = await generate_property_with_rag(knowledge_info=knowledge)
                    property_rsp = None
                    if property_rsp:
                        knowledge["data_id"] = uuid.uuid4().hex
                        knowledge.update(property_rsp)
                        KnowledgeBetaODM(
                            id=knowledge["data_id"],
                            name=knowledge["knowledge"],
                            description=knowledge["description"],
                            data=data,
                            level=knowledge["level"],
                            type=knowledge["type"],
                            difficulty=knowledge["difficulty"],
                            keywords=knowledge["keywords"],
                        ).save()
                        yield KnowledgeResponse(data=knowledge).model_dump_json()
                    else:
                        knowledge["data_id"] = uuid.uuid4().hex
                        KnowledgeBetaODM(
                            id=knowledge["data_id"],
                            name=knowledge["knowledge"],
                            description=knowledge["description"],
                            data=data,
                        ).save()
                        yield KnowledgeResponse(data=knowledge).model_dump_json()
            else:
                yield KnowledgeResponse(
                    code=KnowledgeStatusCode.GENERATE_FAILED, message="标题聚类失败"
                ).model_dump_json()
        else:
            yield KnowledgeResponse(
                code=KnowledgeStatusCode.PARSER_FAILED, message="文档解析失败"
            ).model_dump_json()

    response = StreamingResponse(
        generate_knowledge_beta(), media_type="application/json"
    )
    return response


@knowledge_router.get("/getknowledge")
async def get_knowledge(id: str):
    query_result = KnowledgeODM.objects(id=id).first().to_mongo().to_dict()
    return KnowledgeResponse(data=query_result)


@knowledge_router.get("/getpara")
async def get_para(id: str):
    query_result = KnowledgeODM.objects(id=id).only("data").first().to_mongo().to_dict()
    return KnowledgeResponse(data=query_result)
