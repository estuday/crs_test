from mongoengine import Document, StringField, ListField


class KnowledgeODM(Document):
    id = StringField(required=True, primary_key=True)
    name = StringField(required=True)
    description = StringField(required=True)
    data = ListField(StringField(), required=True)
    level = StringField(choices=["领域层", "学科层", "单元层", "节点层"])
    type = StringField(choices=["识记", "理解", "应用"])
    difficulty = StringField(choices=["简单", "较简单", "中等", "较难", "困难"])
    keywords = ListField(StringField())
    meta = {"collection": "knowledge"}


class KnowledgeBetaODM(Document):
    id = StringField(required=True, primary_key=True)
    name = StringField(required=True)
    description = StringField(required=True)
    data = ListField(StringField(), required=True)
    level = StringField(choices=["领域层", "学科层", "单元层", "节点层"])
    type = StringField(choices=["识记", "理解", "应用"])
    difficulty = StringField(choices=["简单", "较简单", "中等", "较难", "困难"])
    keywords = ListField(StringField())
    meta = {"collection": "knowledge_beta"}
