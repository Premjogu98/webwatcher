from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def create_app():
    app = FastAPI(
        title="Web Watcher api's",
        # description="Contains Web Watcher info and Web settings",
        version="1.0.0",
        # openapi_url="/api/v1/camera/openapi.json",
        docs_url="/api/v1/web/watcher/docs",
        # docs_url=None,
        # redoc_url=None,
    )
    from .routes import router as service_router
    app.include_router(service_router, prefix="/api/v1/web/watcher")
    return app

app = create_app()
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)