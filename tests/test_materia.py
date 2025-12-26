import pytest

async def create_materia_helper(client, nome="Matematica"):
    response = await client.post(
        "/api/v1/materie/",
        json={
            "nome": nome,
            "descrizione": "Corso di matematica"
        }
    )
    return response

@pytest.mark.anyio
async def test_create_materia(client):
    response = await create_materia_helper(client)
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Matematica"
    assert "id" in data

@pytest.mark.anyio
async def test_get_materie(client):
    await create_materia_helper(client, "Matematica")
    await create_materia_helper(client, "Fisica")
    
    response = await client.get("/api/v1/materie/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    names = [m["nome"] for m in data["materie"]]
    assert "Matematica" in names
    assert "Fisica" in names

@pytest.mark.anyio
async def test_get_materia_by_id(client):
    materia_res = await create_materia_helper(client)
    materia_id = materia_res.json()["id"]
    
    response = await client.get(f"/api/v1/materie/{materia_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Matematica"

@pytest.mark.anyio
async def test_update_materia(client):
    materia_res = await create_materia_helper(client)
    materia_id = materia_res.json()["id"]
    
    response = await client.put(
        f"/api/v1/materie/{materia_id}",
        json={
            "nome": "Matematica Avanzata",
            "descrizione": "Analisi 1"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Matematica Avanzata"

@pytest.mark.anyio
async def test_delete_materia(client):
    materia_res = await create_materia_helper(client)
    materia_id = materia_res.json()["id"]
    
    response = await client.delete(f"/api/v1/materie/{materia_id}")
    assert response.status_code == 200
