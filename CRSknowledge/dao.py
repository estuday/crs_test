from nova.engine.storage.postgres import Postgres

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, VARCHAR
from pgvector.sqlalchemy import VECTOR
from dto import Knowledge


_dbname = "CRS"


class CRSKnowledgeORM(DeclarativeBase):
    pass


class KnowledgeORM(CRSKnowledgeORM):
    __tablename__ = "knowledge"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    description: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    keywords: Mapped[str] = mapped_column(VARCHAR)
    alias: Mapped[str] = mapped_column(VARCHAR)
    level: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    type: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    difficulty: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    name_embedding: Mapped[list] = mapped_column(VECTOR(768), nullable=False)


_client = Postgres(
    user="pgvector", password="pgvector", host="172.31.99.9", port="54329"
)
_client.init(CRSKnowledgeORM, _dbname)


def add_knowledge(knowledge: Knowledge) -> None:
    with _client.sync_session(_dbname) as session:
        session.add(
            KnowledgeORM(
                name=knowledge.name,
                description=knowledge.description,
                keywords=knowledge.keywords,
                alias=knowledge.alias,
                level=knowledge.level,
                type=knowledge.type,
                difficulty=knowledge.difficulty,
                name_embedding=knowledge.name_emb,
            )
        )
        session.commit()


def cosine_knowledge(query_embed: list[float]) -> list:
    with _client.sync_session(_dbname) as session:
        query_result = (
            session.query(KnowledgeORM)
            .order_by(KnowledgeORM.name_embedding.cosine_distance(query_embed))
            .limit(3)
        )
        similarity_knowledges = []
        for res in query_result:
            similarity_knowledges.append(
                {
                    "knowledge": res.name,
                    "level": res.level,
                    "type": res.type,
                    "difficulty": res.difficulty,
                }
            )
        return similarity_knowledges
