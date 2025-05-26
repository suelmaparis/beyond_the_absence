import csv
from app import app, db
from models import Resource

with app.app_context():
    with open('beyond_resources_full.csv', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            resource = Resource(**row)
            db.session.add(resource)
        db.session.commit()

print("✔️ Recursos importados com sucesso!")
