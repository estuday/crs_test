from nova.data.logos import Logos
from .const import CUT_LEN
import re


def get_knowledge_msg(title: str, paras: list[str]):
    from .template import GENERATE_KNOWLEDGE_AND_DESCRIPTION_TEMPLATE

    _para = "".join(paras)
    para = _para if len(_para) < CUT_LEN else _para[:CUT_LEN]
    return Logos(
        role=Logos.Role.USER,
        content=GENERATE_KNOWLEDGE_AND_DESCRIPTION_TEMPLATE.render(
            title=title, content=para
        ),
    )


def get_cluster_msg(title_list: list[str]):
    from .template import CLUSTER_TEMPLATE

    n_title = len(title_list) - 1
    title_info = ""
    for i in range(n_title + 1):
        title_info += f"{i}. {title_list[i]}\n"
    return Logos(
        role=Logos.Role.USER,
        content=CLUSTER_TEMPLATE.render(title=title_info, n_title=n_title),
    )


def get_description_msg(knowledge: str, sub_title: list[str]):
    from .template import GENERATE_DESCRIPTION_BY_KNOWLEDGE_TEMPLATE

    return Logos(
        role=Logos.Role.USER,
        content=GENERATE_DESCRIPTION_BY_KNOWLEDGE_TEMPLATE.render(
            knowledge=knowledge, title_list=sub_title
        ),
    )


def extract_content(input_string: str, symbol_pair: tuple[str]):
    start_index = input_string.find(symbol_pair[0])
    end_index = input_string.rfind(symbol_pair[1])
    if start_index != -1 and end_index != -1 and start_index < end_index:
        return input_string[start_index : end_index + 1]
    else:
        return None


def remove_digits_and_dots(text: str) -> str:
    # 使用正则表达式匹配所有阿拉伯数字 [0-9] 和点 [.]
    # 然后用空字符串替换它们
    cleaned_text = re.sub(r"[0-9.]", "", text)
    return cleaned_text
