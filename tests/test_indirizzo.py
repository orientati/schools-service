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
    return response.json()

async def create_school_helper(client, citta_id):
    response = await client.post(
        "/api/v1/schools/",
        json={
            "nome": "Liceo Scientifico",
            "tipo": "Liceo",
            "indirizzo": "Via Roma 1",
            "email_contatto": "info@liceo.it",
            "telefono_contatto": "0612345678",
            "citta_id": citta_id
        }
    )
    return response.json()

async def create_indirizzo_helper(client, school_id, nome="Informatica"):
    response = await client.post(
        "/api/v1/indirizzi/",
        json={
            "nome": nome,
            "descrizione": "Corso di informatica",
            "id_scuola": school_id
        }
    )
    return response

@pytest.mark.anyio
async def test_create_indirizzo(client):
    citta = await create_citta_helper(client)
    school = await create_school_helper(client, citta["id"])
    response = await create_indirizzo_helper(client, school["id"])
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Informatica"
    assert data["id_scuola"] == school["id"]

@pytest.mark.anyio
async def test_get_indirizzi(client):
    citta = await create_citta_helper(client)
    school = await create_school_helper(client, citta["id"])
    await create_indirizzo_helper(client, school["id"], "Informatica")
    await create_indirizzo_helper(client, school["id"], "Elettronica")
    
    response = await client.get("/api/v1/indirizzi/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    names = [i["nome"] for i in data["indirizzi"]]
    assert "Informatica" in names
    assert "Elettronica" in names

@pytest.mark.anyio
async def test_get_indirizzo_by_id(client):
    citta = await create_citta_helper(client)
    school = await create_school_helper(client, citta["id"])
    indirizzo_res = await create_indirizzo_helper(client, school["id"])
    indirizzo_id = indirizzo_res.json()["id"]
    
    response = await client.get(f"/api/v1/indirizzi/{indirizzo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Informatica"

@pytest.mark.anyio
async def test_update_indirizzo(client):
    citta = await create_citta_helper(client)
    school = await create_school_helper(client, citta["id"])
    indirizzo_res = await create_indirizzo_helper(client, school["id"])
    indirizzo_id = indirizzo_res.json()["id"]
    
    response = await client.put(
        f"/api/v1/indirizzi/{indirizzo_id}",
        json={
            "nome": "Informatica Avanzata",
            "descrizione": "Corso avanzato",
            "id_scuola": school["id"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Informatica Avanzata"

@pytest.mark.anyio
async def test_delete_indirizzo(client):
    citta = await create_citta_helper(client)
    school = await create_school_helper(client, citta["id"])
    indirizzo_res = await create_indirizzo_helper(client, school["id"])
    indirizzo_id = indirizzo_res.json()["id"]
    
    response = await client.delete(f"/api/v1/indirizzi/{indirizzo_id}")
    assert response.status_code == 200
