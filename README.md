# CodeGen — AI-Native Development Pipeline

CodeGen is a spec-driven AI development pipeline that takes a structured feature specification, validates it, generates an implementation plan, waits for approval, generates backend code, creates automated tests, runs quality checks, and shows the final pipeline status in a simple web dashboard.

![CodeGen Dashboard](https://github.com/YowzaK/Code-gen/blob/7084bcd140154f76833998dcf159f8af5f033d9d/Code-gen.png)

## Features

- Feature specification intake using structured JSON
- Backend validation with Pydantic
- Pipeline state tracking with PostgreSQL/Neon
- AI-generated implementation planning using OpenRouter
- Human approval checkpoint before implementation
- AI-generated backend code artifacts
- Generated code saved into a local `generated/` folder
- Automated test generation
- Quality checks for syntax, formatting, linting, tests, and security scanning
- Simple Next.js dashboard for running the pipeline

## Tech Stack

**Backend**

- FastAPI
- SQLModel / SQLAlchemy
- PostgreSQL via Neon
- Pydantic
- OpenRouter LLM API
- Ruff, Pytest, Bandit

**Frontend**

- Next.js
- TypeScript
- Tailwind CSS
- shadcn/ui
- Axios

---

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <your-repository-name>
```

---

## Backend Setup

### 2. Open the backend folder

```bash
cd backend
```

### 3. Create a `.env` file

Create a `.env` file inside the `backend` folder and add the following values:

```env
DATABASE_URL=your_neon_database_connection_string
OPENROUTER_API_KEY=your_openrouter_api_key
MODEL_NAME=openrouter/free
```

`MODEL_NAME` can be changed if you have access to a better or paid model.

Example:

```env
MODEL_NAME=openrouter/free
```

### 4. Create and activate the virtual environment

#### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\activate
```

If PowerShell blocks activation, run this first:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.\venv\Scripts\activate
```

#### Windows CMD

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

#### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
```

### 5. Install backend dependencies

Install the required packages using the provided instructions file:

```bash
pip install -r requirements.txt
```

### 6. Start the backend server

Run the backend on port `8000`:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The backend must run on port `8000` because the frontend API client expects:

```text
http://127.0.0.1:8000
```

Backend API docs will be available at:

```text
http://127.0.0.1:8000/docs
```

> Note: When testing the full AI pipeline, avoid running Uvicorn with `--reload` because generated files may trigger automatic backend restarts.

---

## Frontend Setup

### 7. Open the frontend folder

Open a new terminal from the repository root and run:

```bash
cd frontend
```

### 8. Install frontend dependencies

```bash
pnpm install
```

### 9. Start the frontend development server

```bash
pnpm dev
```

The frontend should now be available at:

```text
http://localhost:3000
```

---

## Pipeline Flow

The application follows this workflow:

```text
1. Submit feature specification
2. Validate and save specification
3. Generate implementation plan
4. Approve generated plan
5. Automatically generate code
6. Save generated code files
7. Generate automated tests
8. Run quality checks
9. Display passed and failed checks
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | Neon PostgreSQL database connection string |
| `OPENROUTER_API_KEY` | API key for OpenRouter LLM access |
| `MODEL_NAME` | LLM model name. Default recommendation: `openrouter/free` |

---

## Quality Checks

The backend quality check stage can run validations such as:

- Python syntax check
- Ruff formatting
- Ruff linting
- Pytest execution
- Bandit security scan

The UI displays which checks passed and which checks failed.

---

## Notes

- Free OpenRouter models may be rate-limited.
- If rate limits occur, wait and retry or change `MODEL_NAME` to another available model.
- The generated files are written into the `generated/` folder.
- Keep the backend running on port `8000` for the frontend to connect correctly.
