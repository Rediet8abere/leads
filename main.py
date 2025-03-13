from fastapi import FastAPI, HTTPException, Depends, status, Header
from typing_extensions import Annotated, Optional
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv

import models
from modelbase import ClientBase, AttorneyBase, ClientUpdateBase, ClientStateUpdateBase
from database import engine, SessionLocal
from sendemail import send_email
from auth import api_key_auth
from database import db_dependency

# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Create a logger instance
logger = logging.getLogger(__name__)

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

@app.post("/attorney/", status_code=status.HTTP_201_CREATED)
async def create_attorney(attorney: AttorneyBase, db: db_dependency):
    db_attorney = models.Attorney(**attorney.dict())
    try:
        db.add(db_attorney)
        db.commit()
        db.refresh(db_attorney)
        return {"id": db_attorney.id, "name": db_attorney.firstname, "email": db_attorney.email}
    except IntegrityError:
        db.rollback()  # Rollback the transaction if there's an integrity error
        raise HTTPException(status_code=409, detail="Client with this email already exists")

@app.post("/client/", status_code=status.HTTP_201_CREATED)
async def create_client(client: ClientBase, db: db_dependency):
    db_client = models.Client(**client.dict())
    # consts
    subject = "Client Application Submitted"
    client_body = "Thank you for submitting your application. Please keep an eye out for further updates"
    attorney_body = "New client has submitted their application"

    try:
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        # TODO: once submitted send email to client and attorney
        logger.info(f"GET request received - email={db_client.email}")
        # send email for client
        send_email(
            subject=subject,
            body=client_body,
            to_email=db_client.email
        )
        attorneys = db.query(models.Attorney).all()
        for attorney in attorneys:
            # send email for attorney
            send_email(
                subject=subject,
                body=attorney_body,
                to_email=attorney.email
            )
        return {"id": db_client.id, "name": db_client.firstname, "email": db_client.email}
    except IntegrityError:
        db.rollback()  # Rollback the transaction if there's an integrity error
        raise HTTPException(status_code=409, detail="Client with this email already exists")

@app.get("/clients", status_code=status.HTTP_200_OK)
async def fetch_all_clients(db: db_dependency, api_key: str = Depends(api_key_auth)):
    # TODO: guard with auth - maybe use apikey instead of token
    client = db.query(models.Client).all()
    if client is None:
        raise HTTPException(status_code=404, detail='client not found')
    return client

@app.patch("/client/{client_id}", status_code=status.HTTP_200_OK)
async def update_client(client_id: str, clientUpdate: ClientUpdateBase, db: db_dependency):
    client_to_update = db.query(models.Client).filter(models.Client.id == client_id).first()
    if client_to_update:
        client_to_update.firstname = clientUpdate.firstname
        client_to_update.lastname = clientUpdate.lastname
        client_to_update.email = clientUpdate.email
        client_to_update.resume = clientUpdate.resume
        db.commit()
        db.refresh(client_to_update)
        return {"message": "Client updated"}
    else:
        raise HTTPException(status_code=404, detail='client not found')

@app.patch("/client/state/{client_id}", status_code=status.HTTP_200_OK)
async def update_client_state(client_id: str, clientStateUpdate: ClientStateUpdateBase, db: db_dependency):
    # TODO: enable this api only for an attorney
    client_state_to_update = db.query(models.Client).filter(models.Client.id == client_id).first()
    if client_state_to_update:
        client_state_to_update.state = clientStateUpdate.state
        db.commit()
        db.refresh(client_state_to_update)
        return {"message": "Client state updated"}
    else:
        raise HTTPException(status_code=404, detail='client not found')




