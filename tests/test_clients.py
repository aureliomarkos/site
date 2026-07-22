import os
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient


db_dir = Path(tempfile.mkdtemp())
db_path = db_dir / "test_clients.db"
os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

from app.database import SessionLocal, Base, engine
from app.main import app
from app import models


class ClientRegistrationTests(unittest.TestCase):
    def setUp(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.client = TestClient(app)

    def test_create_client_persists_to_database(self):
        payload = {
            "name": "Maria Silva",
            "email": "maria@example.com",
            "phone": "(11) 99999-9999",
            "password": "123456",
            "company": "Acme"
        }

        response = self.client.post("/api/clients", json=payload)

        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertEqual(body["email"], payload["email"])
        self.assertEqual(body["name"], payload["name"])

        db = SessionLocal()
        try:
            saved = db.query(models.Client).filter(models.Client.email == payload["email"]).first()
            self.assertIsNotNone(saved)
            self.assertEqual(saved.name, payload["name"])
            self.assertEqual(saved.company, payload["company"])
        finally:
            db.close()

    def test_duplicate_email_returns_friendly_message(self):
        payload = {
            "name": "Maria Silva",
            "email": "maria@example.com",
            "phone": "(11) 99999-9999",
            "password": "123456",
            "company": "Acme"
        }

        first_response = self.client.post("/api/clients", json=payload)
        self.assertEqual(first_response.status_code, 201)

        second_response = self.client.post("/api/clients", json=payload)
        self.assertEqual(second_response.status_code, 409)
        self.assertEqual(second_response.json()["detail"], "email já existe")

    def test_client_login_and_message_crud(self):
        payload = {
            "name": "Maria Silva",
            "email": "maria@example.com",
            "phone": "(11) 99999-9999",
            "password": "123456",
            "company": "Acme"
        }

        self.client.post("/api/clients", json=payload)

        login_response = self.client.post(
            "/api/clients/login",
            json={"email": payload["email"], "password": payload["password"]},
        )
        self.assertEqual(login_response.status_code, 200)
        client_data = login_response.json()
        self.assertEqual(client_data["email"], payload["email"])

        create_response = self.client.post(
            f"/api/clients/{client_data['id']}/messages",
            json={"title": "Pedido de revisão", "message": "Preciso de ajuda", "status": "pendente"},
        )
        self.assertEqual(create_response.status_code, 201)
        message_id = create_response.json()["id"]

        list_response = self.client.get(f"/api/clients/{client_data['id']}/messages")
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.json()), 1)

        update_response = self.client.put(
            f"/api/clients/{client_data['id']}/messages/{message_id}",
            json={"status": "respondido"},
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json()["status"], "respondido")

        delete_response = self.client.delete(f"/api/clients/{client_data['id']}/messages/{message_id}")
        self.assertEqual(delete_response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
