import db as _db
import models as _models
from typing import TYPE_CHECKING, List

import schemas
import schemas as _schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def _add_tables():
    return _db.Base.metadata.create_all(bind=_db.engine)


def get_db():
    db = _db.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_contact(contact: _schemas.CreateContact, db: "Session") -> _schemas.Contact:
    contact = _models.Contact(**contact.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return _schemas.Contact.from_orm(contact)


async def get_all_contacts(db: "Session") -> List[schemas.Contact]:
    contacts = db.query(_models.Contact).all()
    print(contacts)
    return list(map(schemas.Contact.from_orm, contacts))


async def get_contact(contact_id: int, db: "Session"):
    contact = db.query(_models.Contact).filter(_models.Contact.id == contact_id).first()
    return contact


async def delete_contact(contact: _models.Contact, db: "Session"):
    db.delete(contact)
    db.commit()


async def update_contact(contact_data: _schemas.CreateContact, contact: _models.Contact,
                         db: "Session") -> schemas.Contact:
    contact.first_name = contact_data.first_name
    contact.last_name = contact_data.last_name
    contact.email = contact_data.email
    contact.phone_number = contact_data.phone_number

    db.commit()
    db.refresh(contact)
    return schemas.Contact.from_orm(contact)
