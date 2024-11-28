from enum import Enum


class JPProperty(str, Enum):
    INTRODUCTION = "介绍说明"
    SOURCE_FROM = "岗位需求来源"


class JSProperty(str, Enum):
    INTRODUCTION = "介绍说明"
    KEYWORDS = "关键词"
    COMPLEXITY = "复杂度"
    LEVEL = "技能层次"
    TYPE = "技能类型"
    CASE = "技能工作案例"


class TCProperty(str, Enum):
    INTRODUCTION = "介绍说明"
    LANGUAGE = "语言"
    COMPLEXITY = "复杂度"
    CREDITS = "学分"
    HOURS = "学时"
    HOURS_OF_THEORY = "理论学时"
    HOURS_OF_PRACTICE = "实践学时"
    TERMS = "学期"
    UNIVERSITY = "学校"
    DEPARTMENT = "院系"
    MAJOR = "专业"
    LEVEL = "课程层次"
    TYPE = "课程类型"
    MODE = "教学模式"
    METHOD = "授课方法"
    EXAMINE = "考核模式"
    STANDARD = "考核标准"
    TARGET = "课程目标"
    IDEA_AND_POLICY = "教学思政"


class TCCProperty(str, Enum):
    INTRODUCTION = "介绍说明"
    COMPLEXITY = "复杂度"
    MODE = "教学模式"
    HOURS = "学时"
    INSTRUCTION = "章节教学说明"
    TARGET = "章节教学目标"
    IDEA_AND_POLICY = "教学思政"


class TPProperty(str, Enum):
    INTRODUCTION = "介绍说明"
    DEPARTMENT = "院系"
    MAJOR_CODE = "专业代码"
    MAHOR_TYPE = "专业类别"
    SUBJECT_CATEGORY = "学科门类"
    BACHELOR = "学位"
    DURATION = "学制"
    GRADUATE_REQUIREMENTS = "毕业要求"
    TRAINING_TARGET = "培养目标"
    CERTIFICATE = "专业相关证书"
    JOB = "专业相关职业"


class TRProperty(str, Enum):
    RESOURCETYPE = "资源类型"
    NAME = "资源名称"
    DESCRIPTION = "资源描述"
    KEYWORDS = "关键词"
    FILESIZE = "资源大小"
