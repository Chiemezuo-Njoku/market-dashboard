from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import stock_routes, news_routes, dashboard_routes

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "API is runing"}
app.include_router(stock_routes.router, prefix="/stocks")   
app.include_router(news_routes.router, prefix="/news")
app.include_router(dashboard_routes.router, prefix="/dashboard")