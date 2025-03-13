# Leads - Backend application publicaly availble for prospect clients to fill in.

## Table of Contents

- [Running the Application Locally](#running-the-application-locally)
- [Design Document](#design-document)
- [Features](#features) 

---

## Running the Application Locally

To run the application locally on your machine, follow the steps below:

### Steps to Run Locally

1. **Clone the repository**:

   ```bash
   git clone [https://github.com/yourusername/your-repository-name.git](https://github.com/Rediet8abere/leads.git)
   cd leads
   ```
 2. ** create a virtual environment and activate it**:

  ```bash
  # Create a virtual environment (optional)

  python -m venv venv
  # Activate the virtual environment
  # For Windows
  venv\Scripts\activate
  # For macOS/Linux
  source venv/bin/activate
  ```
 3. **Run cmd below to start server**:
  ```bash
  uvicorn main:app --reload --log-level debug
  ```
 4. **To access fast api swagger go to**:
   ```bash http://127.0.0.1:8000/docs
   ```
   Fetch all Clients API requires a secret key to run the application. The secret key can be obtained from the Author.
   
   <img width="1415" alt="Screenshot 2025-03-13 at 12 59 08 PM" src="https://github.com/user-attachments/assets/641125a4-83f1-4716-885a-e05355c2a699" />

   
   
   
  <img width="1437" alt="Screenshot 2025-03-12 at 11 53 28 AM" src="https://github.com/user-attachments/assets/89082537-d07c-4cf1-aaae-aea0ad961bae" />
 6. **Note: API Limitation**

## Design Document 
   [Tech Spec](https://docs.google.com/document/d/1wiy8QHlNwsQVWUJy8v7UhPlPr-pxdRsS7Xq_xe9g-q0/edit?tab=t.0#heading=h.e1d7h350587m)

## Features 
  1. CRU(D - no delete fun) operation for prospective clients 
  2. Create operation for attorney 
  3. Email Notification for prospect clients and attorneys 
   <img width="656" alt="Screenshot 2025-03-12 at 11 58 01 AM" src="https://github.com/user-attachments/assets/39510064-25ed-457d-bb02-2e948179db4d" />
   
