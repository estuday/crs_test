from jinja2 import Template

BASE_EXTRACT_TEMPLATE = Template(
    """
    请阅读第一个和第二个“===”之间文本，然后解决需求。
    文本：
    ===
    {{document}}
    ===

    需求：
    {{need}}

    你需要遵循的约束：
    {{constraint}}

    你的回答只能基于提供的文本，不可做推理。如果你无法回答，则直接输出None。
    现在请解决需求，直接输出答案即可，不要输出无关内容。
    """
)

COMPLEXITY_CONSTRAINT_TEMPLATE = Template(
    """
    你的答案必须从下面这些选项中选择：
    ['简单', '较简单', '中等','较难', '困难']
    """
)

LIST_CONSTRAINT_TEMPLATE = Template(
    """
    输出格式：
    [xxx,xxx,...]
    """
)

JP_DESCRIPTION_EXTRACT_TEMPLATE = Template(
    """
文档中{{job_name}}岗位的介绍说明（描述）是什么？
"""
)

JP_SOURECE_QUESTION_TEMPLATE = Template(
    """
文档中{{job_name}}岗位的需求来源是什么？
"""
)
JP_SOURECE_CONSTRAINT_TEMPLATE = Template(
    """
    输出格式：
    [xxx,xxx,...]

    你的答案必须从下面这些选项中选择：
    ['内部推荐', '招聘网站', '内部私有数据', '招聘会', '猎头', '公司官网', '未知来源']
    """
)

JS_DESCRIPTION_EXTRACT_TEMPLATE = Template(
    """
    文档中{{skill_name}}技能的介绍说明（描述）是什么？
    """
)

JS_KEYWORDS_EXTRACT_TEMPLATE = Template(
    """
    以下是一个工作技能的名称和介绍，你需要从介绍中抽取关键词，并输出一个关键词列表。

    技能名称：
    {{skill_name}}

    技能介绍：
    {{skill_description}}

    输出格式：
    [xxx,xxx,...]

    关键词个数不超过3个
    """
)

JS_COMPLEXITY_EXTRACT_TEMPLATE = Template(
    """
    总结{{skill_name}}的复杂度。
    """
)

JS_LEVEL_EXTRACT_TEMPLATE = Template(
    """
    总结{{skill_name}}的技能层次。
    """
)
JS_LEVEL_CONSTRAINT_TEMPLATE = Template(
    """
    你的答案必须从下面这些选项中选择：
    ['领域层', '模块层', '方法层']
    """
)
JS_TYPE_EXTRACT_TEMPLATE = Template(
    """
    总结{{skill_name}}的技能类型。
    """
)
JS_TYPE_CONSTRAINT_TEMPLATE = Template(
    """
    你的答案必须从下面这些选项中选择：
    ['专业技术', '职业素养', '任职资格']
    """
)
JS_CASE_EXTRACT_TEMPLATE = Template(
    """
    总结{{skill_name}}的技能工作案例。
    """
)


TC_DESCRIPTION_EXTRACT_TEMPLATE = Template(
    """
    文档中{{course_name}}课程的介绍说明（描述）是什么？
    """
)

TC_LANGUAGE_EXTRACT_TEMPLATE = Template(
    """
    文档中{{course_name}}课程的教学语言是什么？
    """
)

TC_LANGUAGE_CONSTRAINT_TEMPLATE = Template(
    """
    你的答案必须从下面这些选项中选择：
    ['汉语', '英语', '双语']
    """
)

TC_COMPLEXITY_EXTRACT_TEMPLATE = Template(
    """
    总结{{course_name}}课程的复杂度。
    """
)

TC_CREDITS_EXTRACT_TEMPLATE = Template(
    """
    {{course_name}}课程的学分是多少
    """
)

TC_HOURS_EXTRACT_TEMPLATE = Template(
    """
    {{course_name}}课程的学时是多少
    """
)

TC_HOURS_OF_THEORY_EXTRACT_TEMPLATE = Template(
    """
    {{course_name}}课程的理论学时是多少
    """
)

TC_HOURS_OF_PRACTICE_EXTRACT_TEMPLATE = Template(
    """
    {{course_name}}课程的实践学时是多少
    """
)

TC_TERMS_EXTRACT_TEMPLATE = Template(
    """
    {{course_name}}课程的在哪个学期设置
    """
)

TC_UNIVERSITY_EXTRACT_TEMPLATE = Template(
    """
    {{course_name}}课程是哪个学校的课程
    """
)

TC_DEPARTMENT_EXTRACT_TEMPLATE = Template(
    """
    哪些院系设置{{course_name}}课程
    """
)

TC_MAJOR_EXTRACT_TEMPLATE = Template(
    """
    哪些专业设置{{course_name}}课程
    """
)

TC_LEVEL_EXTRACT_TEMPLATE = Template(
    """
    总结{{course_name}}课程的课程层次。
    """
)

TC_LEVEL_CONSTRAINT_TEMPLATE = Template(
    """
    你的答案必须从下面这些选项中选择：
    ['高职专科', '高职本科', '普通本科','重点本科','研究生']
    """
)

TC_TYPE_EXTRACT_TEMPLATE = Template(
    """
    总结{{course_name}}课程的课程类型。
    """
)

TC_TYPE_CONSTRAINT_TEMPLATE = Template(
    """
    你的答案必须从下面这些选项中选择：
    ['公共必修', '公共选修', '专业选修', '专业必修', '其他拓展']
    """
)

TC_MODE_EXTRACT_TEMPLATE = Template(
    """
    {{course_name}}课程的教学模式是什么。
    """
)

TC_MODE_CONSTRAINT_TEMPLATE = Template(
    """
    输出格式：
    [xxx,xxx,...]

    你的答案必须从下面这些选项中选择一个或多个：
    ['理论教学', '实践教学']
    """
)

TC_METHOD_EXTRACT_TEMPLATE = Template(
    """
    {{course_name}}课程的授课方法是什么。
    """
)

TC_EXAMINE_EXTRACT_TEMPLATE = Template(
    """
    {{course_name}}课程的考核模式是什么。
    """
)

TC_EXAMINE_CONSTRAINT_TEMPLATE = Template(
    """
    输出格式：
    [xxx,xxx,...]

    你的答案必须从下面这些选项中选择一个或多个：
    ['考查', '考试', '活动报告答辩']
    """
)

TC_STANDARD_EXTRACT_TEMPLATE = Template(
    """
    {{course_name}}课程的考核标准是什么。
    """
)

TC_TARGET_EXTRACT_TEMPLATE = Template(
    """
    {{course_name}}课程的课程目标是什么。
    """
)

TC_IDEA_AND_POLICY_EXTRACT_TEMPLATE = Template(
    """
    {{course_name}}课程的课程教学思政是什么。
    """
)

TCC_DESCRIPTION_EXTRACT_TEMPLATE = Template(
    """
    文档中{{chapter_name}}章节的介绍说明（描述）是什么？
    """
)

TCC_COMPLEXITY_EXTRACT_TEMPLATE = Template(
    """
    总结{{chapter_name}}章节的复杂度。
    """
)

TCC_MODE_EXTRACT_TEMPLATE = Template(
    """
    {{chapter_name}}章节的教学模式是什么。
    """
)

TCC_HOURS_EXTRACT_TEMPLATE = Template(
    """
    {{chapter_name}}章节的学时是多少
    """
)

TCC_MODE_CONSTRAINT_TEMPLATE = Template(
    """
    输出格式：
    [xxx,xxx,...]

    你的答案必须从下面这些选项中选择一个或多个：
    ['理论教学', '实践教学']
    """
)

TCC_INSTRUCTION_EXTRACT_TEMPLATE = Template(
    """
    {{chapter_name}}章节的章节教学说明是什么。
    """
)

TCC_TARGET_EXTRACT_TEMPLATE = Template(
    """
    {{chapter_name}}章节的章节教学目标是什么。
    """
)

TCC_IDEA_AND_POLICY_EXTRACT_TEMPLATE = Template(
    """
    {{chapter_name}}章节的章节教学思政是什么。
    """
)

TP_DESCRIPTION_EXTRACT_TEMPLATE = Template(
    """
    {{major_name}}的介绍说明（描述）是什么？
    """
)

TP_DEPARTMENT_EXTRACT_TEMPLATE = Template(
    """
    哪些院系设置{{major_name}}
    """
)

TP_MAJOR_CODE_EXTRACT_TEMPLATE = Template(
    """
    {{major_name}}的专业代码是什么？
    """
)

TP_MAJOR_TYPE_EXTRACT_TEMPLATE = Template(
    """
    {{major_name}}的专业类别是什么？
    """
)

TP_SUBJECT_CATEGORY_EXTRACT_TEMPLATE = Template(
    """
    {{major_name}}属于哪个学科门类？
    """
)

TP_BACHELOR_EXTRACT_TEMPLATE = Template(
    """
    {{major_name}}的学位是什么？
    """
)

TP_DURATION_EXTRACT_TEMPLATE = Template(
    """
    {{major_name}}的学制是什么？
    """
)

TP_GRADUATE_REQUIREMENTS_EXTRACT_TEMPLATE = Template(
    """
    {{major_name}}的毕业要求是什么？
    """
)

TP_TRAINING_TARGET_EXTRACT_TEMPLATE = Template(
    """
    {{major_name}}的培养目标是什么？
    """
)

TP_CERTIFICATE_EXTRACT_TEMPLATE = Template(
    """
    {{major_name}}有哪些相关证书？
    """
)

TP_JOB_EXTRACT_TEMPLATE = Template(
    """
    {{major_name}}有哪些相关职业？
    """
)
