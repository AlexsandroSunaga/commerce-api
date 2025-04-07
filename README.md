# Commerce API (FastAPI)

A Shopify-like storefront API by **Alexsandro Sunaga**: product catalog (loaded from `data/products.json`), in-memory carts and orders, and a Stripe Checkout session endpoint.

There are two entry points in this repo:

| Entry | Location | Contents |
|---|---|---|
| Legacy | `app.main:app` (repo root, `app/`) | health, products, cart |
| Backend (current) | `backend/` (`src.main:backend_app`) | health, products, cart, orders, checkout, integrations |

## Run

Legacy entry (from the repo root):

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8020
```

Backend entry:

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
mkdir data                                           # SQLite file location (./data/app.db)
PYTHONPATH=src uvicorn src.main:backend_app --reload --port 8020   # PowerShell: $env:PYTHONPATH="src"
```

Interactive docs: http://127.0.0.1:8020/docs. The Docker image is built from the repository root (`docker compose up --build`, or `docker build -f backend/Dockerfile -t commerce-api .`) and serves the backend entry on port 8000. The image bundles `data/products.json`. The data directory can be overridden with the `DATA_DIR` environment variable.

Optional environment variables: `CORS_ORIGINS` (default `http://localhost:3000`), `STRIPE_SECRET_KEY` (live Checkout; the `stripe` package must be installed, otherwise a demo session is returned), `CHECKOUT_SUCCESS_URL`, `CHECKOUT_CANCEL_URL`.

## Endpoints

Backend entry (the legacy entry has `GET /health`, `GET /api/v1/products`, `GET /api/v1/products/{product_id}` and `POST /api/v1/cart`):

- `GET /health`
- `GET /api/v1/products` (optional `?tag=`), `GET /api/v1/products/{product_id}`
- `POST /api/v1/cart`
- `GET /api/v1/orders`, `POST /api/v1/orders`
- `POST /api/v1/checkout/session`
- `GET /api/v1/integrations/status`

## Examples

```bash
curl "http://127.0.0.1:8020/api/v1/products"

curl -X POST http://127.0.0.1:8020/api/v1/cart \
  -H "Content-Type: application/json" \
  -d '{"line":{"productId":"<id from /products>","quantity":2}}'

curl -X POST http://127.0.0.1:8020/api/v1/orders \
  -H "Content-Type: application/json" \
  -d '{"email":"buyer@example.com","items":[{"sku":"demo","price_cents":2500}]}'
```

## Tests

Covers both the legacy entry (`app.main:app`) and the backend entry (`src.main:backend_app`).

```bash
pip install -r requirements.txt -r backend/requirements.txt -r requirements-dev.txt
python -m pytest -q
```

## Author

**Alexsandro Sunaga**

## License

MIT License — see [LICENSE](LICENSE).
