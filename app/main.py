from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Deribit Price Collector API")
app.include_router(router)
