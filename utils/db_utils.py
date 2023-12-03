from config_app import db, app
import argparse

parser = argparse.ArgumentParser(prog="Init/Destroy database", description="Create or delete the database")

parser.add_argument('config', choices=["init","destroy"])

args = parser.parse_args()

with app.app_context():
    if args.config == "init":
        db.create_all()
    elif args.config == "destroy":
        db.destroy()
