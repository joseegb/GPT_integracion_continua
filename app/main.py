from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="Demo API - GPTIC P02",
    description="Aplicación demostradora para el pipeline CI/CD con GitHub Actions",
    version="0.1.0",
)

# Almacenamiento en memoria (sin BD externa para mantener el entorno simple)
items_db: list[dict] = []


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Endpoint de verificación de estado para despliegues y rollback."""
    return {"status": "ok", "version": "0.1.0"}


@app.get("/items")
def list_items() -> list[dict]:
    """Devuelve todos los elementos registrados."""
    return items_db


@app.post("/items", status_code=201)
def create_item(item: ItemCreate) -> dict:
    """Crea un nuevo elemento en memoria y lo devuelve."""
    new_item = {
        "id": len(items_db) + 1,
        "name": item.name,
        "price": item.price,
    }
    items_db.append(new_item)
    return new_item