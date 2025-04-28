import os
from sqlmodel import create_engine, Session


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(f"BASE_DIR: {BASE_DIR}")
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'database.db')}"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    return Session(engine)
