from jinja2 import Template

GENERATE_KNOWLEDGE_AND_DESCRIPTION_TEMPLATE = Template(
    """
下面是一段文本的标题和内容，请阅读并用一个知识点名词概括，并生成对应的描述。

文本标题:
{{title}}

文本内容：
{{content}}

输出格式：
{
"knowledge":xxx,
"description":xxx
}

注意点：
1. 生成的描述在100字左右。
2. 文本内容仅供参考，在生成描述的时候应该独立生成，不要出现根据文本内容之类的联系。
3. 如果该文本是参考文献、摘要、综述等宽泛性的内容，则视为无法概括。
4. 如果出现无法概括的情况，则只输出None。

现在请你开始概括，按输出格式输出，并且不要生成其他内容。
"""
)

CLUSTER_TEMPLATE = Template(
    """
在第一个和第二个“===”之间是一篇文档中的所有标题，你要判断哪些标题可以合并成一个知识点。

===
{{title}}
===

输出格式：
[
{
"title":[x,x,...],
"knowledge":xxx
},
...
]

输出格式说明：
title是你认为应该属于一个知识点的标题列表
knowledge是你用一个知识点名字来概括列表中的标题

注意点：
1. 在标题列表中，你只需填入0-{{n_title}}的标题序号，且每个序号只能使用一次
2. 只考虑介绍知识点的标题，例如：摘要、参考文献等泛用性的标题不要合并

现在请你开始合并，按输出格式输出，并且不要生成其他内容。
"""
)


GENERATE_DESCRIPTION_BY_KNOWLEDGE_TEMPLATE = Template(
    """
请为以下知识点生成一段100字左右的描述。
在第一个和第二个“===”之间的时该知识点相关文档所包含的标题，仅供表名知识点语义，在生成描述的时候请不要关联。

知识点：
{{knowledge}}

===
{{title_list}}
===

现在请开始生成描述。
"""
)


GENERATE_PROPERTY_TEMPLATE = Template(
    """
请根据提供的知识点信息，按要求生成属性。
知识点信息：
{{konwledge_info}}

需要生成的属性：
keywords: 可以代表知识点的关键词，关键词必须从description中提取。
level: 知识点的教学层次，可选值：[领域层,学科层,单元层,节点层]
type: 知识点的教学类型，可选值：[识记,理解,应用]
difficulty: 知识点的教学难度，可选值: [简单,较简单,中等,较难,困难]

输出格式：
{
"keywords":[xxx,xxx,...],
"level":xxx,
"type":xxx,
"difficulty":xxx
}

注意点：
1. 生成的属性如果有可选值，则只能从可选值中选择
2. 在选择type和difficulty的属性值时，必须考虑到授课对象为大学生
3. 关键词选择在2-3个即可

现在请你开始生成，按输出格式输出，并且不要生成其他内容。
"""
)

GENERATE_PROPERTY_RAG_TEMPLATE = Template(
    """
请根据提供的知识点信息，按要求生成属性。
知识点信息：
{{konwledge_info}}

需要生成的属性：
keywords: 可以代表知识点的关键词，关键词必须从description中提取。
level: 知识点的教学层次，可选值：[领域层,学科层,单元层,节点层]
type: 知识点的教学类型，可选值：[识记,理解,应用]
difficulty: 知识点的教学难度，可选值: [简单,较简单,中等,较难,困难]

在第一个和第二个“===”之间的是一些和本知识点相近的知识点信息，用于辅助判断level、type和difficulty的值
===
{{similarity_knowledge}}
===

输出格式：
{
"keywords":[xxx,xxx,...],
"level":xxx,
"type":xxx,
"difficulty":xxx
}

注意点：
1. 生成的属性如果有可选值，则只能从可选值中选择
2. 在选择type和difficulty的属性值时，必须考虑到授课对象为大学生
3. 关键词选择在2-3个即可

现在请你开始生成，按输出格式输出，并且不要生成其他内容。
"""
)
