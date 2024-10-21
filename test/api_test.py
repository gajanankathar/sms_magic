import pytest
from httpx import AsyncClient

from main import app
from sms_magic_app.database import DB
from sms_magic_app.utils import get_next_sequence_id

client = AsyncClient(app=app, base_url="http://test")


@pytest.mark.asyncio
async def test_default_route():
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello SMS-Magic E-commerce App!"}


@pytest.mark.asyncio
async def test_create_user():
    next_id = await get_next_sequence_id("users")
    response = await client.post("/api/v1/users", json={"name": "Rohit"})
    assert response.status_code == 201
    assert response.json() == {
        "name": "Rohit",
        "id": next_id
    }


@pytest.mark.asyncio
async def test_get_all_users():
    response = await client.get("/api/v1/users")
    assert response.status_code == 200
    assert response.json() == DB["users"]


@pytest.mark.asyncio
async def test_get_user_by_id():
    user_id = 1
    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == list(filter(lambda user: user["id"] == user_id, DB["users"]))[0]


@pytest.mark.asyncio
async def test_get_user_by_id_if_not_found():
    user_id = 199999
    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found!"}


@pytest.mark.asyncio
async def test_get_user_by_id_if_invalid_user_id():
    user_id = "user_id_str"
    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 422
    assert "detail" in response.json()
