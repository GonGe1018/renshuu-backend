from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.api.routers as router
import app.core.config as config

app = FastAPI(
    title=config.settings.app_name,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router.include_routers()  # 모든 엔드포인트 추가


@app.get("/")
def read_root():
    return {"Hello": "World"}