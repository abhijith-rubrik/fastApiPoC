import fastapi
from fastapi import FastAPI
from typing import TYPE_CHECKING, List

import services
from schemas import Contact, CreateContact

import sqlalchemy.orm as _orm
import services as _services

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

app = FastAPI()


@app.post("/api/contacts/", response_model=Contact)
async def create_contact(contact: CreateContact, db: _orm.Session = fastapi.Depends(_services.get_db), ):
    return await _services.create_contact(contact=contact, db=db)


@app.get("/api/contacts/", response_model=List[Contact])
async def get_contacts(db: _orm.Session = fastapi.Depends(_services.get_db)):
    return await _services.get_all_contacts(db=db)


@app.get("/api/contacts/{contact_id}", response_model=Contact)
async def get_contact(contact_id: int, db: _orm.Session = fastapi.Depends(_services.get_db)):
    return await _services.get_contact(contact_id=contact_id, db=db)


@app.delete("/api/contacts/{contact_id}")
async def delete_contact(contact_id: int, db: _orm.Session = fastapi.Depends(_services.get_db)):
    contact = await services.get_contact(contact_id=contact_id, db=db)
    if contact is None:
        raise fastapi.HTTPException(status_code=404, detail="user does not exists")
    await services.delete_contact(contact=contact, db=db)
    return "successfully deleted the user"


@app.put("/api/contacts/{contact_id}", response_model=Contact)
async def update_contact(contact_id: int, contact_data: CreateContact,
                         db: _orm.Session = fastapi.Depends(_services.get_db),
                         ):
    contact = await services.get_contact(contact_id=contact_id, db=db)
    if contact is None:
        raise fastapi.HTTPException(status_code=404, detail="user does not exists")

    return await services.update_contact(contact_data=contact_data, contact=contact, db=db)
