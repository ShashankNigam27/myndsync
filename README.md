# Suraksha Setu (MyndSync)

Suraksha Setu is an AI-powered psychological distress monitoring and decision-support platform designed to safeguard victims and witnesses under the Scheduled Castes and Scheduled Tribes (Prevention of Atrocities) Act. The system ingests multi-channel check-ins (Chatbot, IVRS, SMS, App, Web), performs multilingual NLP sentiment analysis, and calculates an auditable Dynamic Distress Score (DDS) to provide proactive early-warning risk alerts and intervention workflows for counsellors and district officials without replacing human clinical oversight.

---

## 🚀 Quickstart for Fresh Clone

Follow these steps to set up and run the backend locally on your machine.

### 1. Prerequisites
- **Python 3.10+** (Python 3.11 - 3.13 recommended)
- **Git**

---

### 2. Setup Virtual Environment & Install Dependencies

Navigate to the `backend` directory:

```bash
cd backend
```

Create a virtual environment:

```bash
# On Windows
python -m venv venv

# On Linux/macOS
python3 -m venv venv
```

Activate the virtual environment:

```bash
# On Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# On Windows (Command Prompt)
.\venv\Scripts\activate.bat

# On Linux/macOS
source venv/bin/activate
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables

Copy the provided `.env.example` template to `.env`:

```bash
# On Windows (PowerShell)
Copy-Item .env.example .env

# On Linux/macOS or Git Bash
cp .env.example .env
```

*(By default, `.env` is pre-configured with a local SQLite database `sqlite:///myndsync.db` and development JWT secrets)*.

---

### 4. Run Database Migrations & Seed Data

Apply the latest Alembic database migrations:

```bash
alembic upgrade head
```

*(Optional but recommended)* Seed initial demo authorities, staff users, sample cases, and active/pending victims:

```bash
python scripts/seed_data.py
```

---

### 5. Start the Development Server

Launch the FastAPI application with auto-reload:

```bash
uvicorn app.main:app --reload --port 8000
```

The API will now be accessible at `http://localhost:8000`.

---

## 🔍 Verifying the Installation

Open your browser or run curl to verify that the server is active:

1. **Health Check**:
   - URL: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)
   - Expected Response: `{"status": "ok"}`

2. **Interactive Swagger UI**:
   - URL: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Use Swagger's **Authorize 🔓** button with any seeded account:
     - **Admin**: `admin@myndsync.gov.in` / `Password123!`
     - **District Official**: `district.officer@delhi.gov.in` / `Password123!`
     - **Counsellor**: `counsellor.ananya@delhi.gov.in` / `Password123!`
     - **State Director**: `state.director@delhi.gov.in` / `Password123!`

---

## 🧪 Running Automated Tests

Run the full pytest suite from the `backend/` directory:

```bash
pytest
```

---

## 📑 Frontend & API Contract

> [!IMPORTANT]
> The current, real API contract reflecting all implemented endpoints is located at:
> - **YAML Specification**: [`docs/api-spec.yaml`](docs/api-spec.yaml)
> - **JSON Specification**: [`docs/api-spec.json`](docs/api-spec.json)
>
> Anyone building or integrating frontend clients (React/TypeScript dashboard or Flutter victim app) should treat `docs/api-spec.yaml` as the source of truth for request/response schemas.

### Re-exporting API Specifications
Whenever backend endpoints or schemas are updated, refresh the OpenAPI contract by running:

```bash
# Inside backend/
python scripts/export_openapi.py
```

---

## 📂 Project Structure

```
myndsync/
├── docs/
│   ├── engineering-master-spec.md   # Architectural & engineering master spec
│   ├── api-spec.yaml                # Real exported OpenAPI YAML specification
│   └── api-spec.json                # Real exported OpenAPI JSON specification
├── backend/
│   ├── alembic/                     # Database migrations
│   ├── app/
│   │   ├── ai/                      # AI/ML modules (NLP sentiment, DDS scoring)
│   │   ├── api/v1/routers/          # FastAPI routers (auth, victims, interactions, cases)
│   │   ├── core/                    # Security, auth dependencies, exceptions, config
│   │   ├── db/                      # SQLAlchemy session and Base
│   │   ├── models/                  # Database models (User, Authority, Victim, Case, Interaction, Assessment, DistressScore)
│   │   ├── repositories/            # Data access layer
│   │   ├── schemas/                 # Pydantic schemas
│   │   └── services/                # Business logic
│   ├── scripts/
│   │   ├── seed_data.py             # Development database seeder
│   │   └── export_openapi.py        # OpenAPI export script
│   ├── tests/                       # Pytest test suite
│   ├── requirements.txt
│   └── .env.example
├── .gitignore
└── README.md
```
