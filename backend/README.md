# Server Monitoring Dashboard Backend

A robust, extensible backend service for monitoring server status (online/offline, tags, history, etc.) built with FastAPI and MongoDB.

## Features

- **JWT Authentication** (optionally extensible to Google/Email)
- **Server CRUD** with tagging, description, and metadata
- **Bulk import/export** (CSV/JSON)
- **Last status API** for all servers, with filtering by tag or status
- **Status history** (with timestamps)
- **Event notifications** (email/Telegram, optional)
- **Ready for integration with dashboards and front-end clients**
- **Comprehensive API documentation via Swagger/OpenAPI**

---

## Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/your-org/your-repo.git
cd your-repo
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the project root with:

```env
MONGO_URI=mongodb://localhost:27017/monitor
SECRET_KEY=your_strong_secret
NOTIFY_EMAIL_ADDRESS=your_email@gmail.com
NOTIFY_EMAIL_PASSWORD=your_app_password
TELEGRAM_BOT_TOKEN=bot_token
TELEGRAM_CHAT_ID=chat_id
```

### 3. Run MongoDB

Make sure MongoDB is running locally or update `MONGO_URI` accordingly.

### 4. Launch the API

```bash
uvicorn app.main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

---

## API Overview

### Authentication

- **Login**: `POST /auth/token`  
  Returns JWT access token.  
  Example with [httpie](https://httpie.io/):
  ```bash
  http -f POST http://localhost:8000/auth/token username=admin password=admin
  ```

- **Using JWT**:  
  Set `Authorization: Bearer <token>` header in all requests.

---

### Server Management

- **Create Server**: `POST /servers/`
  ```json
  {
    "name": "App Server 1",
    "ip": "10.0.0.1",
    "description": "Production server",
    "tags": ["prod", "web"]
  }
  ```

- **List Servers**: `GET /servers/`

---

### Tagging

- **Add Tag**: `POST /servers/{server_id}/tags?tag=prod`
- **Remove Tag**: `DELETE /servers/{server_id}/tags?tag=prod`

---

### Status APIs

- **Get Last Status All Servers**:  
  `GET /server-status/latest`  
  Optional filters: `?tag=prod`, `?online=true`
- **Get Status History**:  
  `GET /server-status/history/{server_id}`

---

### Import/Export

- **Import CSV**: `POST /servers/import/csv`  
  Upload a CSV file with fields:  
  `name,ip,description,tags` (tags as comma separated string)

- **Import JSON**: `POST /servers/import/json`  
  Upload a JSON array of server objects.

- **Export CSV**: `GET /servers/export/csv`
- **Export JSON**: `GET /servers/export/json`

---

## Example Usage

### Add a Server

```bash
http POST http://localhost:8000/servers/ \
  'Authorization: Bearer <TOKEN>' \
  name="DB Server" ip="192.168.1.2" description="Postgres" tags:='["prod","db"]'
```

### Get All Servers with Tag

```bash
http GET http://localhost:8000/server-status/latest?tag=prod \
  'Authorization: Bearer <TOKEN>'
```

### Import Servers from CSV

```bash
http --form POST http://localhost:8000/servers/import/csv \
  'Authorization: Bearer <TOKEN>' \
  file@servers.csv
```

---

## CSV Import Example

```csv
name,ip,description,tags
AppServer1,10.0.0.1,Production app,"prod,web"
DBServer,10.0.0.2,Database server,"prod,db"
TestServer,10.0.0.3,Testing,"test"
```

---

## Developer Notes

- All endpoints are `async` and optimized for performance.
- For production, use a production-ready ASGI server (e.g., Gunicorn with Uvicorn workers).
- Extend user model and authentication as needed (see FastAPI Users for Google/Email OAuth).
- For notifications, configure `.env` accordingly or disable if not needed.

---

## API Documentation

Interactive documentation is always available at:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)