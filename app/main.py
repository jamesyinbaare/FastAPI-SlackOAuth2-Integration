from __future__ import annotations

from dataclasses import dataclass, field

from fastapi import FastAPI



@dataclass
class Item:
    name: str
    price: float
    tags: list[str] = field(default_factory=list)
    description: str | None = None
    tax: float | None = None


app = FastAPI()



@app.get("/items/next", response_model=Item)
async def read_next_item():
    return {
        "name": "Island In The Moon",
        "price": 14.6,
        "description": "A place to be playin and having fun",
        "tags": ["breater"],
    }
