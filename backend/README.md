# Backend Project

## Structure

- **app/**: Main application package
  - **api/**: API endpoints
    - **auth/**: Authentication endpoints (Hassan)
    - **summarization/**: Summarization endpoints (Hamza)
    - **profile/**: Profile endpoints (Mohamed)
    - **collections/**: Collections endpoints (Mohamed)
    - **analytics/**: Analytics endpoints (Mehdi)
  - **core/**: Core utilities
    - **config.py**: Configuration (Hassan)
    - **security.py**: Security utilities (Hassan)
    - **database.py**: Database configuration (Hassan)
  - **models/**: Data models (Tous)
  - **schemas/**: Pydantic schemas (Tous)
  - **services/**: Business logic services
    - **nip_service.py**: NIP service (Hamza)
    - **file_service.py**: File service (Hamza)
    - **email_service.py**: Email service (Mehdi)
    - **analytics_service.py**: Analytics service (Mehdi)
- **tests/**: Test suite
- **main.py**: Application entry point (Hassan)
- **requirements.txt**: Python dependencies
