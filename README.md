# Stock Service

Flask microservice for managing product inventory. Handles product creation, stock updates, and availability checks. Uses Celery for async stock reservation and release.

## Structure

```
stock_service/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration
│   ├── models/stock.py      # MongoDB model
│   ├── routes/stock_routes.py # API endpoints
│   ├── services/stock_service.py # Business logic
│   └── utils/               # Decorators, error handlers, logging
├── celery_app.py            # Celery worker
├── run.py                   # Entry point
├── Dockerfile
├── Jenkinsfile
└── requirements.txt
```

## Requirements

- Python 3.9+
- MongoDB
- Redis

## Local Development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run --host=0.0.0.0 --port=5000

# Celery worker (separate terminal)
celery -A celery_app worker -n stock_worker --loglevel=info -Q stock_queue
```

## Environment Variables

```env
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DB=devopsshowcase
MONGODB_USER=appuser
MONGODB_PASSWORD=apppassword
CELERY_BROKER_URL=redis://localhost:6379/0
```

## Celery Tasks

### Worker Setup

The Stock Service worker listens on `stock_queue` and registers tasks from `celery_app.py`.

```bash
celery -A celery_app worker -n stock_worker --loglevel=info -Q stock_queue
```

### Tasks Exposed by Stock Service

| Task Name | Purpose | Triggered By |
|-----------|---------|--------------|
| `stock.reserve_stock` | Temporarily reserves inventory during checkout | Cart Service |
| `stock.unreserve_stock` | Releases previously reserved inventory after a failed checkout or cart rollback | Cart Service |
| `stock.finalise_stock_purchase` | Finalizes inventory deduction after a successful checkout | Cart Service |
| `stock.add_stock` | Restores inventory during refund handling | Cart Service |

### External Tasks Sent by Stock Service

No outbound Celery tasks are sent by the Stock Service in the current codebase.

## API Endpoints

Base URL: `/api/stocks`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Get all products |
| GET | `/<product_id>` | Get specific product |
| POST | `/` | Create product |
| PUT | `/<product_id>` | Update product |
| DELETE | `/<product_id>` | Delete product |
## Docker

```bash
docker build -t stock_service .
docker run -p 5000:5000 --env-file .env stock_service
```

## License

MIT License
