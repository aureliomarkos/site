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


if __name__ == "__main__":
    unittest.main()
