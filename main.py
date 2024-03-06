from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers.get_stats import stats_router
from routers.upload_file import upload_file_router
from routers.get_log_extraction_parsing import parse_router

# app
app = FastAPI(
    title='A reboot a day can keep the ******** away',
    version='1.0.0',
    redoc_url='/api/v1/docs'
)

# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(upload_file_router)
app.include_router(parse_router)
app.include_router(stats_router)
