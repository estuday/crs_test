from .dto import CRSExtractResponse, CRSExtractResponseCode, CRSTRResponse
from .template import (
    BASE_EXTRACT_TEMPLATE,
    COMPLEXITY_CONSTRAINT_TEMPLATE,
    JP_SOURECE_QUESTION_TEMPLATE,
    JP_SOURECE_CONSTRAINT_TEMPLATE,
    JP_DESCRIPTION_EXTRACT_TEMPLATE,
    JS_DESCRIPTION_EXTRACT_TEMPLATE,
    LIST_CONSTRAINT_TEMPLATE,
    JS_KEYWORDS_EXTRACT_TEMPLATE,
    JS_CASE_EXTRACT_TEMPLATE,
    JS_COMPLEXITY_EXTRACT_TEMPLATE,
    JS_LEVEL_CONSTRAINT_TEMPLATE,
    JS_LEVEL_EXTRACT_TEMPLATE,
    JS_TYPE_CONSTRAINT_TEMPLATE,
    JS_TYPE_EXTRACT_TEMPLATE,
    TC_DESCRIPTION_EXTRACT_TEMPLATE,
    TC_COMPLEXITY_EXTRACT_TEMPLATE,
    TC_CREDITS_EXTRACT_TEMPLATE,
    TC_DEPARTMENT_EXTRACT_TEMPLATE,
    TC_EXAMINE_CONSTRAINT_TEMPLATE,
    TC_EXAMINE_EXTRACT_TEMPLATE,
    TC_HOURS_EXTRACT_TEMPLATE,
    TC_HOURS_OF_PRACTICE_EXTRACT_TEMPLATE,
    TC_HOURS_OF_THEORY_EXTRACT_TEMPLATE,
    TC_IDEA_AND_POLICY_EXTRACT_TEMPLATE,
    TC_LANGUAGE_CONSTRAINT_TEMPLATE,
    TC_LANGUAGE_EXTRACT_TEMPLATE,
    TC_LEVEL_CONSTRAINT_TEMPLATE,
    TC_LEVEL_EXTRACT_TEMPLATE,
    TC_MAJOR_EXTRACT_TEMPLATE,
    TC_METHOD_EXTRACT_TEMPLATE,
    TC_MODE_CONSTRAINT_TEMPLATE,
    TC_MODE_EXTRACT_TEMPLATE,
    TC_STANDARD_EXTRACT_TEMPLATE,
    TC_TARGET_EXTRACT_TEMPLATE,
    TC_TERMS_EXTRACT_TEMPLATE,
    TC_TYPE_CONSTRAINT_TEMPLATE,
    TC_TYPE_EXTRACT_TEMPLATE,
    TC_UNIVERSITY_EXTRACT_TEMPLATE,
    TCC_COMPLEXITY_EXTRACT_TEMPLATE,
    TCC_DESCRIPTION_EXTRACT_TEMPLATE,
    TCC_HOURS_EXTRACT_TEMPLATE,
    TCC_IDEA_AND_POLICY_EXTRACT_TEMPLATE,
    TCC_INSTRUCTION_EXTRACT_TEMPLATE,
    TCC_MODE_CONSTRAINT_TEMPLATE,
    TCC_MODE_EXTRACT_TEMPLATE,
    TCC_TARGET_EXTRACT_TEMPLATE,
    TP_SUBJECT_CATEGORY_EXTRACT_TEMPLATE,
    TP_BACHELOR_EXTRACT_TEMPLATE,
    TP_CERTIFICATE_EXTRACT_TEMPLATE,
    TP_DEPARTMENT_EXTRACT_TEMPLATE,
    TP_DURATION_EXTRACT_TEMPLATE,
    TP_GRADUATE_REQUIREMENTS_EXTRACT_TEMPLATE,
    TP_DESCRIPTION_EXTRACT_TEMPLATE,
    TP_JOB_EXTRACT_TEMPLATE,
    TP_MAJOR_CODE_EXTRACT_TEMPLATE,
    TP_MAJOR_TYPE_EXTRACT_TEMPLATE,
    TP_TRAINING_TARGET_EXTRACT_TEMPLATE,
)
import requests
from .const import EMBEDDING_URL, DOCUMENT_PARSER_REQUEST_URL
import json
from .dao import doc_retriver
from nova.data.logos import Logos
from .crs_properties import JPProperty, JSProperty, TCProperty, TCCProperty, TPProperty
from enum import Enum
import os


class BaseExtracter:
    def __init__(self, llm, doc_id):
        self.llm = llm
        self.doc_id = doc_id

    def retriver(self, text: str) -> list[str]:
        embeddings = json.loads(
            requests.post(EMBEDDING_URL, json={"texts": [text]}).text
        )["data"][0]
        doc_contents = doc_retriver(embeddings, self.doc_id)
        return doc_contents

    async def ask(self, content: str):
        message = Logos(role=Logos.Role.USER, content=content)
        response = await self.llm.acall([message])
        return response.content

    async def get_rag_response(self, query: str, constraint: str = None):
        doc_contents = self.retriver(query)
        bet = BASE_EXTRACT_TEMPLATE.render(
            document=doc_contents,
            need=query,
            constraint=constraint,
        )
        response = await self.ask(bet)
        return response


class JPExtracter(BaseExtracter):
    def __init__(self, llm, doc_id):
        super().__init__(llm, doc_id)

    async def jp_extract(self, payload: dict):
        job_name = payload.name
        if job_name is None:
            return CRSExtractResponse(
                code=CRSExtractResponseCode.LACK_PARAM,
                message="JP服务必须提供参数name(岗位名称)",
            )
        job_properties = payload.property
        # 不提供属性则抽取全部
        if not job_properties:
            job_properties = [jp.value for jp in JPProperty]
        extract_result = {}
        for property in job_properties:
            match property:
                case JPProperty.INTRODUCTION:
                    jp_intro_template = JP_DESCRIPTION_EXTRACT_TEMPLATE.render(
                        job_name=job_name
                    )
                    response = await self.get_rag_response(jp_intro_template)
                    extract_result.update({property: response})
                case JPProperty.SOURCE_FROM:
                    jp_source_template = JP_SOURECE_QUESTION_TEMPLATE.render(
                        job_name=job_name
                    )
                    constraint = JP_SOURECE_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(
                        jp_source_template, constraint
                    )
                    extract_result.update({property: response})
        return CRSExtractResponse(data=extract_result, doc_id=self.doc_id)


class JSExtracter(BaseExtracter):
    def __init__(self, llm, doc_id):
        super().__init__(llm, doc_id)

    async def js_extract(self, payload: dict) -> CRSExtractResponse:
        skill_name = payload.name
        if skill_name is None:
            return CRSExtractResponse(
                code=CRSExtractResponseCode.LACK_PARAM,
                message="JS服务必须提供参数name(技能名称)",
            )

        skill_properties =  payload.property
        if not skill_properties:
            skill_properties = [js.value for js in JSProperty]
        extract_dict = {}
        for property in skill_properties:
            match property:
                case JSProperty.INTRODUCTION:
                    js_intro_template = JS_DESCRIPTION_EXTRACT_TEMPLATE.render(
                        skill_name=skill_name
                    )
                    response = await self.get_rag_response(js_intro_template)
                    extract_dict.update({property: response})
                case JSProperty.KEYWORDS:
                    skill_description = (
                        payload.get("description", None)
                        if payload.get("description", None)
                        else extract_dict.get(JSProperty.INTRODUCTION, None)
                    )
                    if skill_description is None:
                        continue
                    js_keywords_template = JS_KEYWORDS_EXTRACT_TEMPLATE.render(
                        skill_name=skill_name, skill_description=skill_description
                    )
                    response = await self.ask(content=js_keywords_template)
                    extract_dict.update({property: response})
                case JSProperty.COMPLEXITY:
                    js_complexity_template = JS_COMPLEXITY_EXTRACT_TEMPLATE.render(
                        skill_name=skill_name
                    )
                    constraint = COMPLEXITY_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(
                        js_complexity_template, constraint
                    )
                    extract_dict.update({property: response})
                case JSProperty.LEVEL:
                    js_level_template = JS_LEVEL_EXTRACT_TEMPLATE.render(
                        skill_name=skill_name
                    )
                    constraint = JS_LEVEL_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(
                        js_level_template, constraint
                    )
                    extract_dict.update({property: response})
                case JSProperty.TYPE:
                    js_type_template = JS_TYPE_EXTRACT_TEMPLATE.render(
                        skill_name=skill_name
                    )
                    constraint = JS_TYPE_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(js_type_template, constraint)
                    extract_dict.update({property: response})
                case JSProperty.CASE:
                    js_case_template = JS_CASE_EXTRACT_TEMPLATE.render(
                        skill_name=skill_name
                    )
                    constraint = LIST_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(js_case_template, constraint)
                    extract_dict.update({property: response})
        return CRSExtractResponse(data=extract_dict, doc_id=self.doc_id)


class TCExtracter(BaseExtracter):

    def __init__(self, llm, doc_id):
        super().__init__(llm, doc_id)

    async def tc_extract(self, payload: dict):
        course_name = payload.name
        if course_name is None:
            return CRSExtractResponse(
                code=CRSExtractResponseCode.LACK_PARAM,
                message="TC服务必须提供参数name(课程名称)",
            )

        course_properties =  payload.property
        if not course_properties:
            course_properties = [tc.value for tc in TCProperty]
        extract_result = {}
        for property in course_properties:
            match property:
                case TCProperty.INTRODUCTION:
                    tc_intro_template = TC_DESCRIPTION_EXTRACT_TEMPLATE.render(
                        course_name=course_name
                    )
                    response = await self.get_rag_response(tc_intro_template)
                    extract_result.update({property: response})
                case TCProperty.LANGUAGE:
                    tc_language_template = TC_LANGUAGE_EXTRACT_TEMPLATE.render(
                        course_name=course_name
                    )
                    constraint = TC_LANGUAGE_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(
                        tc_language_template, constraint
                    )
                    extract_result.update({property: response})
                case TCProperty.COMPLEXITY:
                    tc_complexity_template = TC_COMPLEXITY_EXTRACT_TEMPLATE.render(
                        course_name=course_name
                    )
                    constraint = COMPLEXITY_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(
                        tc_complexity_template, constraint
                    )
                    extract_result.update({property: response})
                case TCProperty.CREDITS:
                    tc_credits_template = TC_CREDITS_EXTRACT_TEMPLATE.render(
                        course_name=course_name
                    )
                    response = await self.get_rag_response(tc_credits_template)
                    extract_result.update({property: response})
                case TCProperty.HOURS:
                    tc_hours_template = TC_HOURS_EXTRACT_TEMPLATE.render(
                        course_name=course_name
                    )
                    response = await self.get_rag_response(tc_hours_template)
                    extract_result.update({property: response})
                case TCProperty.HOURS_OF_THEORY:
                    tc_hours_of_theory_template = (
                        TC_HOURS_OF_THEORY_EXTRACT_TEMPLATE.render(
                            course_name=course_name
                        )
                    )
                    response = await self.get_rag_response(tc_hours_of_theory_template)
                    extract_result.update({property: response})
                case TCProperty.HOURS_OF_PRACTICE:
                    tc_hours_of_practice_template = (
                        TC_HOURS_OF_PRACTICE_EXTRACT_TEMPLATE.render(
                            course_name=course_name
                        )
                    )
                    response = await self.get_rag_response(
                        tc_hours_of_practice_template
                    )
                    extract_result.update({property: response})
                case TCProperty.TERMS:
                    tc_terms_template = TC_TERMS_EXTRACT_TEMPLATE.render(
                        course_name=course_name
                    )
                    response = await self.get_rag_response(tc_terms_template)
                    extract_result.update({property: response})
                case TCProperty.UNIVERSITY:
                    tc_university_template = TC_UNIVERSITY_EXTRACT_TEMPLATE.render(
                        course_name=course_name
                    )
                    response = await self.get_rag_response(tc_university_template)
                    extract_result.update({property: response})
                case TCProperty.DEPARTMENT:
                    tc_department_template = TC_DEPARTMENT_EXTRACT_TEMPLATE.render(
                        course_name=course_name
                    )
                    constraint = LIST_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(
                        tc_department_template, constraint
                    )
                    extract_result.update({property: response})
                case TCProperty.MAJOR:
                    tc_major_template = TC_MAJOR_EXTRACT_TEMPLATE.render(
                        course_name=course_name
                    )
                    constraint = LIST_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(
                        tc_major_template, constraint
                    )
                    extract_result.update({property: response})
                case TCProperty.LEVEL:
                    tc_level_template = TC_LEVEL_EXTRACT_TEMPLATE.render(
                        course_name=course_name
                    )
                    constraint = TC_LEVEL_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(
                        tc_level_template, constraint
                    )
                    extract_result.update({property: response})
                case TCProperty.TYPE:
                    tc_type_template = TC_TYPE_EXTRACT_TEMPLATE.render(
                        course_name=course_name
                    )
                    constraint = TC_TYPE_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(tc_type_template, constraint)
                    extract_result.update({property: response})
                case TCProperty.MODE:
                    tc_mode_template = TC_MODE_EXTRACT_TEMPLATE.render(
                        course_name=course_name
                    )
                    constraint = TC_MODE_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(tc_mode_template, constraint)
                    extract_result.update({property: response})
                case TCProperty.METHOD:
                    tc_method_tempalte = TC_METHOD_EXTRACT_TEMPLATE.render(
                        course_name=course_name
                    )
                    constraint = LIST_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(
                        tc_method_tempalte, constraint
                    )
                    extract_result.update({property: response})
                case TCProperty.EXAMINE:
                    tc_examine_template = TC_EXAMINE_EXTRACT_TEMPLATE.render(
                        course_name=course_name
                    )
                    constraint = TC_EXAMINE_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(
                        tc_examine_template, constraint
                    )
                    extract_result.update({property: response})
                case TCProperty.STANDARD:
                    tc_standard_template = TC_STANDARD_EXTRACT_TEMPLATE.render(
                        course_name=course_name
                    )
                    constraint = LIST_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(
                        tc_standard_template, constraint
                    )
                    extract_result.update({property: response})
                case TCProperty.TARGET:
                    tc_target_template = TC_TARGET_EXTRACT_TEMPLATE.render(
                        course_name=course_name
                    )
                    constraint = LIST_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(
                        tc_target_template, constraint
                    )
                    extract_result.update({property: response})
                case TCProperty.IDEA_AND_POLICY:
                    tc_idea_and_policy_template = (
                        TC_IDEA_AND_POLICY_EXTRACT_TEMPLATE.render(
                            course_name=course_name
                        )
                    )
                    constraint = LIST_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(
                        tc_idea_and_policy_template, constraint
                    )
                    extract_result.update({property: response})
        return CRSExtractResponse(data=extract_result, doc_id=self.doc_id)


class TCCExtracter(BaseExtracter):
    def __init__(self, llm, doc_id):
        super().__init__(llm, doc_id)

    async def tcc_extract(self, payload: dict) -> CRSExtractResponse:
        chapter_name = payload.name
        if chapter_name is None:
            return CRSExtractResponse(
                code=CRSExtractResponseCode.LACK_PARAM,
                message="缺少章节名称",
            )
        chapter_properties =  payload.property
        if not chapter_properties:
            chapter_properties = [tcc.value for tcc in TCCProperty]
        extract_result = {}
        for property in chapter_properties:
            match property:
                case TCCProperty.INTRODUCTION:
                    tcc_introduction_template = TCC_DESCRIPTION_EXTRACT_TEMPLATE.render(
                        chapter_name=chapter_name
                    )
                    response = await self.get_rag_response(tcc_introduction_template)
                    extract_result.update({property: response})
                case TCCProperty.COMPLEXITY:
                    tcc_complexity_template = TCC_COMPLEXITY_EXTRACT_TEMPLATE.render(
                        chapter_name=chapter_name
                    )
                    constraint = COMPLEXITY_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(
                        tcc_complexity_template, constraint
                    )
                    extract_result.update({property: response})
                case TCCProperty.MODE:
                    tcc_mode_template = TCC_MODE_EXTRACT_TEMPLATE.render(
                        chapter_name=chapter_name
                    )
                    constraint = TCC_MODE_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(
                        tcc_mode_template, constraint
                    )
                    extract_result.update({property: response})
                case TCCProperty.HOURS:
                    tcc_hours_template = TCC_HOURS_EXTRACT_TEMPLATE.render(
                        chapter_name=chapter_name
                    )
                    response = await self.get_rag_response(tcc_hours_template)
                    extract_result.update({property: response})
                case TCCProperty.INSTRUCTION:
                    tcc_instruction_template = TCC_INSTRUCTION_EXTRACT_TEMPLATE.render(
                        chapter_name=chapter_name
                    )
                    constraint = LIST_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(
                        tcc_instruction_template, constraint
                    )
                    extract_result.update({property: response})
                case TCCProperty.TARGET:
                    tcc_target_template = TCC_TARGET_EXTRACT_TEMPLATE.render(
                        chapter_name=chapter_name
                    )
                    constraint = LIST_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(
                        tcc_target_template, constraint
                    )
                    extract_result.update({property: response})
                case TCCProperty.IDEA_AND_POLICY:
                    tcc_idea_and_policy_template = (
                        TCC_IDEA_AND_POLICY_EXTRACT_TEMPLATE.render(
                            chapter_name=chapter_name
                        )
                    )
                    constraint = LIST_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(
                        tcc_idea_and_policy_template, constraint
                    )
                    extract_result.update({property: response})
        return CRSExtractResponse(data=extract_result, doc_id=self.doc_id)


class TPExtracter(BaseExtracter):

    def __init__(self, llm, doc_id):
        super().__init__(llm, doc_id)

    async def tp_extract(self, payload: dict) -> CRSExtractResponse:
        major_name = payload.name
        if major_name is None:
            return CRSExtractResponse(
                code=CRSExtractResponseCode.LACK_PARAM,
                message="缺少专业名称",
            )
        properties = payload.property
        if not properties:
            properties = [tp.value for tp in TPProperty]
        extract_result = {}
        for property in properties:
            match property:
                case TPProperty.INTRODUCTION:
                    tp_introduction_template = TP_DESCRIPTION_EXTRACT_TEMPLATE.render(
                        major_name=major_name
                    )
                    response = await self.get_rag_response(tp_introduction_template)
                    extract_result.update({property: response})
                case TPProperty.DEPARTMENT:
                    tp_department_template = TP_DEPARTMENT_EXTRACT_TEMPLATE.render(
                        major_name=major_name
                    )
                    constraint = LIST_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(
                        tp_department_template, constraint
                    )
                    extract_result.update({property: response})
                case TPProperty.MAJOR_CODE:
                    tp_major_code_template = TP_MAJOR_CODE_EXTRACT_TEMPLATE.render(
                        major_name=major_name
                    )
                    response = await self.get_rag_response(tp_major_code_template)
                    extract_result.update({property: response})
                case TPProperty.MAHOR_TYPE:
                    tp_major_type_template = TP_MAJOR_TYPE_EXTRACT_TEMPLATE.render(
                        major_name=major_name
                    )
                    response = await self.get_rag_response(tp_major_type_template)
                    extract_result.update({property: response})
                case TPProperty.SUBJECT_CATEGORY:
                    tp_subject_category_template = (
                        TP_SUBJECT_CATEGORY_EXTRACT_TEMPLATE.render(
                            major_name=major_name
                        )
                    )
                    response = await self.get_rag_response(tp_subject_category_template)
                    extract_result.update({property: response})
                case TPProperty.BACHELOR:
                    tp_bachelor_template = TP_BACHELOR_EXTRACT_TEMPLATE.render(
                        major_name=major_name
                    )
                    response = await self.get_rag_response(tp_bachelor_template)
                    extract_result.update({property: response})
                case TPProperty.DURATION:
                    tp_duration_template = TP_DURATION_EXTRACT_TEMPLATE.render(
                        major_name=major_name
                    )
                    response = await self.get_rag_response(tp_duration_template)
                    extract_result.update({property: response})
                case TPProperty.GRADUATE_REQUIREMENTS:
                    tp_graduate_requirements_template = (
                        TP_GRADUATE_REQUIREMENTS_EXTRACT_TEMPLATE.render(
                            major_name=major_name
                        )
                    )
                    constraint = LIST_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(
                        tp_graduate_requirements_template, constraint
                    )
                    extract_result.update({property: response})
                case TPProperty.TRAINING_TARGET:
                    tp_training_target_template = (
                        TP_TRAINING_TARGET_EXTRACT_TEMPLATE.render(
                            major_name=major_name
                        )
                    )
                    constraint = LIST_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(
                        tp_training_target_template, constraint
                    )
                case TPProperty.CERTIFICATE:
                    tp_certificate_template = TP_CERTIFICATE_EXTRACT_TEMPLATE.render(
                        major_name=major_name
                    )
                    constraint = LIST_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(
                        tp_certificate_template, constraint
                    )
                    extract_result.update({property: response})
                case TPProperty.JOB:
                    tp_job_template = TP_JOB_EXTRACT_TEMPLATE.render(
                        major_name=major_name
                    )
                    constraint = LIST_CONSTRAINT_TEMPLATE.render()
                    response = await self.get_rag_response(tp_job_template, constraint)
                    extract_result.update({property: response})
        return CRSExtractResponse(data=extract_result, doc_id=self.doc_id)


class TRExtracter:
    class SupportFormat(str, Enum):
        DOCX = ".docx"
        PPTX = ".pptx"
        MP4 = ".mp4"

    SUPPORT_FORMAT = [sf.value for sf in SupportFormat]

    def parser_document(self, files):
        _parser = requests.post(DOCUMENT_PARSER_REQUEST_URL, files=files).text
        parser_rsp = json.loads(_parser)
        # 处理文档解析后的结果
        if parser_rsp["code"] == 200:
            descriptions = []
            texts = []
            for res in parser_rsp["data"]["result"]:
                texts.append(res.get("content", [""])[0])
                if len(texts) < 3 and res.get("content_type") == "text":
                    descriptions.append(res.get("content", [""])[0])
            return "".join(descriptions), "".join(texts)
        else:
            raise ValueError("文档解析接口失败")

    def analyze_keywords_and_description(self, files) -> list[str]:
        from .textrank4zh import TextRank4Keyword

        description, text = self.parser_document(files)
        t2w = TextRank4Keyword()
        t2w.analyze(text, lower=True, window=2)
        keywords = [item.word for item in t2w.get_keywords(3, word_min_len=2)]
        return keywords, description

    async def tr_extract(self, file) -> CRSExtractResponse:
        file_content = await file.read()
        filename = file.filename
        file_extension = os.path.splitext(filename)[1]
        filesize = round(len(file_content) / (1024 * 1024), 2)
        tr_rsp = CRSTRResponse(name=filename, filesize=filesize)
        match file_extension:
            case self.SupportFormat.DOCX:
                tr_rsp.resourcetype = CRSTRResponse.ResourceType.HANDOUTS
                files = {"file": (filename, file_content, file.content_type)}
                try:
                    keywords, description = self.analyze_keywords_and_description(files)
                    tr_rsp.description = description
                    tr_rsp.keywords = keywords
                except:
                    pass
            case self.SupportFormat.PPTX:
                tr_rsp.resourcetype = CRSTRResponse.ResourceType.COURSEWARE
                files = {"file": (filename, file_content, file.content_type)}
                try:
                    keywords, description = self.analyze_keywords_and_description(files)
                    tr_rsp.description = description
                    tr_rsp.keywords = keywords
                except:
                    pass
            case self.SupportFormat.MP4:
                from moviepy.editor import VideoFileClip
                tr_rsp.resourcetype = CRSTRResponse.ResourceType.VIDEO
                file_location = f"./temp/{filename}"
                with open(file_location, "wb") as f:
                    f.write(file_content)
                clip = VideoFileClip(file_location)
                duration = clip.duration
                clip.close()
                os.remove(file_location)
                tr_rsp.videotime = duration
            case _:
                tr_rsp.resourcetype = CRSTRResponse.ResourceType.OTHERS
        return CRSExtractResponse(
            data=tr_rsp.model_dump(exclude_none=True, exclude_defaults=True)
        )
