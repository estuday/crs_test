from fastapi import APIRouter, UploadFile, File
from .dto import CRSExtractRequest, CRSExtractResponse, CRSExtractResponseCode
from spire.doc import Document

from .utils import text_split
import requests
from .const import EMBEDDING_URL
import json
from .dao import create_new_document
from nova.sdk.llm.spark.client import Spark
import shutil
import os
from .extracter import (
    JPExtracter,
    JSExtracter,
    TCExtracter,
    TCCExtracter,
    TPExtracter,
    TRExtracter,
)
import PyPDF2

llm = Spark()
common_extract_router = APIRouter()

@common_extract_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"./temp/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if file_location.endswith(".docx"):
        doc = Document(file_location)
        text = doc.GetText()
    elif file_location.endswith(".pdf"):
        with open(file_location, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page_obj = pdf_reader.pages[page_num]
                text += page_obj.extract_text()
    else:
        os.remove(file_location)
        return CRSExtractResponse(
            code=CRSExtractResponseCode.UNSUPPORTED_FILE_TYPE,
            message="不支持的文件类型",
        )
    os.remove(file_location)
    texts = text_split(text)
    embedding_rsp = requests.post(EMBEDDING_URL, json={"texts": texts}).text
    doc_embeddings = json.loads(embedding_rsp)["data"]
    doc_id = create_new_document(texts, doc_embeddings)
    return CRSExtractResponse(doc_id=doc_id)


@common_extract_router.post("/crs/{crs_type}")
async def common_extract(crs_type: str, request: CRSExtractRequest):
    try:
        payload = request.payload
        doc_id = request.doc_id if request.doc_id else None
    except:
        return CRSExtractResponse(
            code=CRSExtractResponseCode.MISFORMAT_PARAM,
            message="请求参数格式不正确",
        )

    if doc_id is None:
        return CRSExtractResponse(
            code=CRSExtractResponseCode.LACK_PARAM,
            message="doc_id 不可为空",
        )

    if crs_type == "jp":
        extracter = JPExtracter(llm, doc_id)
        rsp = await extracter.jp_extract(payload)
    elif crs_type == "js":
        extracter = JSExtracter(llm, doc_id)
        rsp = await extracter.js_extract(payload)
    elif crs_type == "tc":
        extracter = TCExtracter(llm, doc_id)
        rsp = await extracter.tc_extract(payload)
    elif crs_type == "tcc":
        extracter = TCCExtracter(llm, doc_id)
        rsp = await extracter.tcc_extract(payload)
    elif crs_type == "tp":
        extracter = TPExtracter(llm, doc_id)
        rsp = await extracter.tp_extract(payload)
    return rsp


@common_extract_router.post("/tr")
async def upload_file(file: UploadFile = File(...)):
    extracter = TRExtracter()
    rsp = await extracter.tr_extract(file)
    return rsp
