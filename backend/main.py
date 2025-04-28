# backend/main.py

from fastapi import FastAPI, UploadFile, File, Form
from sqlmodel import SQLModel, create_engine, Session, select
import shutil
import os
from datetime import datetime

from backend.models import ImageEntry
from backend.database import engine, get_session
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/images", StaticFiles(directory="data/images"), name="images")

# İlk başta veritabanı tablolarını oluştur
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Ana sayfa
@app.get("/")
def read_root():
    return {"message": "PowerPrompt Backend Active!"}

# backend/main.py içinde

from fastapi import HTTPException

# Görsel yükleme endpointi
@app.post("/upload/")
async def upload_image(
    file: UploadFile = File(...),
    prompt: str = Form(...),
    model_type: str = Form(...),
    style_type: str = Form(...)
):
    try:
        # Görseller için klasör var mı, yoksa oluştur
        images_dir = "data/images"
        os.makedirs(images_dir, exist_ok=True)

        # Dosyayı kaydet
        filename = f"{datetime.utcnow().timestamp()}_{file.filename}"
        file_path = os.path.join(images_dir, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Veritabanına kayıt
        session = get_session()
        image_entry = ImageEntry(
            image_path=file_path,
            prompt=prompt,
            model_type=model_type,
            style_type=style_type
        )
        session.add(image_entry)
        session.commit()
        session.refresh(image_entry)

        return {"message": "Upload successful", "image_id": image_entry.id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# backend/main.py içine ekle (upload'ın altına)

from fastapi import Depends
from sqlalchemy.orm import Session

# backend/main.py içinde /search/ endpointini güncelle

from fastapi import Query


@app.get("/search/")
def search_images(
    query: str = Query(None),
    model_type: str = Query(None),
    style_type: str = Query(None),
    session: Session = Depends(get_session)
):
    statement = select(ImageEntry)

    # Eğer parametreler geldiyse, filtre uygulayalım
    if query:
        statement = statement.where(ImageEntry.prompt.contains(query))
    if model_type:
        statement = statement.where(ImageEntry.model_type == model_type)
    if style_type:
        statement = statement.where(ImageEntry.style_type == style_type)

    images = session.exec(statement).all()

    results = []
    for img in images:
        image_url = f"http://localhost:8000/images/{os.path.basename(img.image_path)}"

        results.append({
            "id": img.id,
            "prompt": img.prompt,
            "model_type": img.model_type,
            "style_type": img.style_type,
            "created_at": img.created_at,
            "image_url": image_url
        })

    return results





