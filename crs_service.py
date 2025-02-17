from fastapi import FastAPI
from CRSextract import common_extract_router
from CRSknowledge import knowledge_router
import uvicorn
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

app.include_router(common_extract_router)
app.include_router(knowledge_router)

if __name__ == "__main__":
    uvicorn.run(
        app="crs_service:app",
        host="0.0.0.0",
        port=8011
    )
