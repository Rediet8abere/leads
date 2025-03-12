from fastapi import FastAPI, HTTPException, Depends, status, Header
from pydantic import BaseModel
from typing_extensions import Annotated, Optional
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Create a logger instance
logger = logging.getLogger(__name__)

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


# Load the .env file
load_dotenv()

# Get the secret key for JWT encoding/decoding from the environment variable
SECRET_KEY = os.getenv('SECRET_KEY')
EMAIL_SENDER_PASSWORD = os.getenv('EMAIL_SENDER_PASSWORD')
ALGORITHM = "HS256"

class ClientBase(BaseModel):
    firstname: str
    lastname: str
    email: str
    resume: str

class AttorneyBase(BaseModel):
    firstname: str
    lastname: str
    email: str

class ClientUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    resume: Optional[str] = None

class ClientStateUpdate(BaseModel):
    state: Optional[str] = None

def send_email(subject: str, body: str, to_email: str):
    # SMTP server configuration
    smtp_host = "smtp.gmail.com"  # Gmail SMTP server
    smtp_port = 587  # SMTP port for Gmail
    sender_email = "redietaberegesesse@gmail.com"
    sender_password = EMAIL_SENDER_PASSWORD

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Add email body
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Establish a connection to the SMTP server
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)  # Log in to the SMTP server

        # Send the email
        server.sendmail(sender_email, to_email, msg.as_string())
        logger.info("Email sent successfully!")

    except Exception as e:
        logger.info(f"Error: {e}")

    finally:
        # Close the server connection
        server.quit()

# Custom Dependency to extract token from Authorization header
def get_token_from_header(authorization: Optional[str] = Header(None)) -> str:
    logger.info(f"GET request received - authorization={authorization}")
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization token missing")

    token = authorization
    return token

# Function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to decode and validate the JWT token
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token is invalid")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token is invalid")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# TODO: internal api for create, get attorney
# TODO: Fix token expire limitation by refreshing token

@app.post("/attorney/", status_code=status.HTTP_201_CREATED)
async def create_attorney(attorney: AttorneyBase, db: db_dependency):
    db_attorney = models.Attorney(**attorney.dict())
    try:
        db.add(db_attorney)
        db.commit()
        db.refresh(db_attorney)
        # Generate JWT token
        access_token = create_access_token(data={"sub": db_attorney.email})
        return {"id": db_attorney.id, "name": db_attorney.firstname, "email": db_attorney.email, "access_token": access_token}
    except IntegrityError:
        db.rollback()  # Rollback the transaction if there's an integrity error
        raise HTTPException(status_code=409, detail="Client with this email already exists")

@app.post("/client/", status_code=status.HTTP_201_CREATED)
async def create_client(client: ClientBase, db: db_dependency):
    db_client = models.Client(**client.dict())
    try:
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        # Generate JWT token
        access_token = create_access_token(data={"sub": client.email})
        # TODO: once submitted send email to client and attorney
        # send email for client
        send_email(
            subject="Client Application Submitted",
            body="Thank you for submitting your application. Please keep an eye out for further updates",
            to_email=db_client.email
        )
        attorneys = db.query(models.Attorney).all()
        for attorney in attorneys:
            # send email for attorney
            send_email(
                subject="Client Application Submitted",
                body="New client has submitted their application",
                to_email=attorney.email
            )
        return {"id": db_client.id, "name": db_client.firstname, "email": db_client.email, "access_token": access_token}
    except IntegrityError:
        db.rollback()  # Rollback the transaction if there's an integrity error
        raise HTTPException(status_code=409, detail="Client with this email already exists")

@app.get("/client/{client_id}/", status_code=status.HTTP_200_OK)
async def fetch_client(client_id: int, db: db_dependency, token: str = Depends(get_token_from_header)):
    # Decode and validate the token
    email = decode_access_token(token)

    client = db.query(models.Client).filter(
        models.Client.id == client_id,
        models.Client.email == email
    ).first()
    if client is None:
        raise HTTPException(status_code=404, detail='client not found')
    return client

@app.patch("/client/{client_id}", status_code=status.HTTP_200_OK)
async def update_client(client_id: str, clientUpdate: ClientUpdate, db: db_dependency):
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
async def update_client_state(client_id: str, clientStateUpdate: ClientStateUpdate, db: db_dependency):
    # TODO: enable this api only for an attorney
    client_state_to_update = db.query(models.Client).filter(models.Client.id == client_id).first()
    if client_state_to_update:
        client_state_to_update.state = clientStateUpdate.state
        db.commit()
        db.refresh(client_state_to_update)
        return {"message": "Client state updated"}
    else:
        raise HTTPException(status_code=404, detail='client not found')



