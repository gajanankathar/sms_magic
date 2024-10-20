from fastapi import FastAPI

from sms_magic_app import api

app = FastAPI(
    title="Recommendation System",
    description="Recommendation system for ecommerce website"
)

app.include_router(
    api.user_route,
    prefix="/api",
    tags=["Accounts"],
    responses={418: {"description": "I'm a teapot"}},
)
app.include_router(
    api.product_route,
    prefix="/api",
    tags=["Product Catalogue"],
    responses={418: {"description": "I'm a teapot"}},
)
app.include_router(
    api.order_route,
    prefix="/api",
    tags=["Orders"],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello SMS-Magic E-commerce App!"}
