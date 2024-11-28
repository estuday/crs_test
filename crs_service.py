from fastapi import FastAPI
from CRSextract import common_extract_router
from CRSknowledge import knowledge_router
import uvicorn

app = FastAPI()

app.include_router(common_extract_router)
app.include_router(knowledge_router)

if __name__ == "__main__":
    uvicorn.run(
        app="crs_service:app",
        host="172.31.99.9",
        port=8011,
        reload=True,
        reload_dirs=["/data/weizhang105/personal/multiAgent"],
    )
