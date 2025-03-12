# Leads - Backend application publicaly availble for prospect clients to fill in.

## Table of Contents

- [Running the Application Locally](#running-the-application-locally)
- [Design Document](#design-document)
- [Additional Documentation](#additional-documentation)

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
  <img width="1437" alt="Screenshot 2025-03-12 at 11 53 28 AM" src="https://github.com/user-attachments/assets/89082537-d07c-4cf1-aaae-aea0ad961bae" />
 6. **Note: API Limitation**
   
