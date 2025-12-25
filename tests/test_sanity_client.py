import pytest

@pytest.mark.anyio
async def test_sanity_client(client):
    response = await client.get("/health")
    assert response.status_code == 200
