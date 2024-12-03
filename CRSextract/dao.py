from nova.engine.storage.postgres import Postgres

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, VARCHAR
from pgvector.sqlalchemy import VECTOR
from uuid import uuid4

_dbname = "CRS"


class CRSCommonPropertyORM(DeclarativeBase):
    pass


class DocumentORM(CRSCommonPropertyORM):
    __tablename__ = "document"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    doc_id: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    content: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    embedding: Mapped[list] = mapped_column(VECTOR(768), nullable=False)


_client = Postgres(
    user="pgvector", password="pgvector", host="172.31.99.9", port="54329"
)
_client.init(CRSCommonPropertyORM, _dbname)


def create_new_document(content: list[str], embedding: list[list[float]]):
    if len(content) != len(embedding):
        raise ValueError("content and embedding must have the same length")
    doc_id = uuid4().hex
    with _client.sync_session(_dbname) as session:
        for c, e in zip(content, embedding):
            session.add(
                DocumentORM(
                    doc_id=doc_id,
                    content=c,
                    embedding=e,
                )
            )
            session.commit()
    return doc_id


def doc_retriver(query_embed: list[float], doc_id: str):
    with _client.sync_session(_dbname) as session:
        doc = (
            session.query(DocumentORM)
            .filter_by(doc_id=doc_id)
            .order_by(DocumentORM.embedding.cosine_distance(query_embed))
            .limit(3)
        )
        contents = [_doc.content[:1000] for _doc in doc]
        return contents
