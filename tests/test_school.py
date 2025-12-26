import pytest

async def create_citta_helper(client):
    response = await client.post(
        "/api/v1/citta/",
        json={
            "nome": "Roma",
            "cap": "00100",
            "provincia": "RM",
            "regione": "Lazio"
        }
    )
    assert response.status_code == 200
    return response.json()

async def create_school_helper(client, citta_id, nome="Liceo Scientifico"):
    response = await client.post(
        "/api/v1/schools/",
        json={
            "nome": nome,
            "tipo": "Liceo",
            "indirizzo": "Via Roma 1",
            "email_contatto": "info@liceo.it",
            "telefono_contatto": "0612345678",
            "citta_id": citta_id
        }
    )
    return response

@pytest.mark.anyio
async def test_create_school(client):
    citta = await create_citta_helper(client)
    response = await create_school_helper(client, citta["id"])
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Liceo Scientifico"
    assert "id" in data
    assert data["città"] == "Roma"

@pytest.mark.anyio
async def test_get_schools(client):
    citta = await create_citta_helper(client)
    await create_school_helper(client, citta["id"], nome="School A")
    await create_school_helper(client, citta["id"], nome="School B")
    
    response = await client.get("/api/v1/schools/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    names = [s["nome"] for s in data["scuole"]]
    assert "School A" in names
    assert "School B" in names

@pytest.mark.anyio
async def test_get_school_by_id(client):
    citta = await create_citta_helper(client)
    school_res = await create_school_helper(client, citta["id"])
    assert school_res.status_code == 200
    school_id = school_res.json()["id"]
    
    response = await client.get(f"/api/v1/schools/{school_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Liceo Scientifico"

@pytest.mark.anyio
async def test_update_school(client):
    citta = await create_citta_helper(client)
    school_res = await create_school_helper(client, citta["id"])
    school_id = school_res.json()["id"]
    
    response = await client.put(
        f"/api/v1/schools/{school_id}",
        json={
            "nome": "Liceo Classico",
            "tipo": "Liceo",
            "indirizzo": "Via Milano 2",
            "email_contatto": "info@classico.it",
            "telefono_contatto": "0687654321",
            "citta_id": citta["id"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Liceo Classico"

@pytest.mark.anyio
async def test_delete_school(client):
    citta = await create_citta_helper(client)
    school_res = await create_school_helper(client, citta["id"])
    school_id = school_res.json()["id"]
    
    response = await client.delete(f"/api/v1/schools/{school_id}")
    assert response.status_code == 200
    
    # Try to get it
    # Depending on implementation, might return 404 or something else
