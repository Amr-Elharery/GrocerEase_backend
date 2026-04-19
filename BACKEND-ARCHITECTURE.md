# Backend Architecture Overview - GrocerEase

## Summary

The backend follows a **feature-based clean architecture** using **FastAPI**.
It is a **single application** with a **single shared database**, while domains are separated into independent modules.

Goals:

- high maintainability
- clear ownership by feature
- easy testing

---

## High-Level Architecture

- Single FastAPI app
- Single repository
- PostgreSQL database
- Multiple feature modules (auth, users, products, orders, etc.)
- Clean architecture boundaries inside each module

---

## Architectural Style

Each feature is implemented as a vertical slice and contains its own layers:

1. **Presentation Layer**

- FastAPI routers
- controllers
- request/response DTOs (Pydantic)
- dependency wiring for services

2. **Application Layer**

- services (application services)
- orchestration of business flows
- transaction boundaries

3. **Domain Layer**

- entities
- value objects
- domain services and rules
- domain exceptions

4. **Infrastructure Layer**

- SQLAlchemy repositories
- external services (e.g. email, payment)
- adapters for framework and DB concerns

Dependency rule:

- Outer layers depend on inner layers.
- Domain layer depends on nothing external.
- FastAPI and SQLAlchemy stay in presentation/infrastructure only.

---

## Module Boundaries (Feature-Based)

Each feature module is isolated and owns:

- its API endpoints
- its services
- its domain models/rules
- its repository interfaces and implementations

Shared code is limited to cross-cutting components only (auth, config, db session, common exceptions, logging).

---

## Suggested Folder Structure (FastAPI, Single App)

```txt
app/
├─ main.py
├─ core/
│  ├─ config.py
│  ├─ security.py
│  ├─ exceptions.py
│  └─ logging.py
├─ db/
│  ├─ session.py
│  ├─ base.py
│  └─ migrations/
├─ modules/
│  ├─ users/
│  │  ├─ presentation/
│  │  │  ├─ router.py
│  │  │  ├─ controller.py
│  │  │  └─ schemas.py
│  │  ├─ application/
│  │  │  ├─ services/
│  │  │  │  └─ user_service.py
│  │  ├─ domain/
│  │  │  ├─ entities.py
│  │  │  ├─ value_objects.py
│  │  │  ├─ repositories.py
│  │  │  └─ errors.py
│  │  └─ infrastructure/
│  │     ├─ models.py
│  │     └─ repository_sqlalchemy.py
│  ├─ products/
│  │  └─ ...
│  ├─ cart/
│  │  └─ ...
│  └─ orders/
│     └─ ...
└─ tests/
   ├─ unit/
   └─ integration/
```

---

## Request Flow

```txt
FastAPI Router -> Controller -> Service -> Domain Rules -> Repository Interface -> SQLAlchemy Repository -> PostgreSQL
```

Notes:

- Router binds endpoint paths and dependencies.
- Controller handles request/response orchestration.
- Service contains business workflow.
- Repository interface lives in domain/application boundary.
- Repository implementation lives in infrastructure.

### Where Are Controller and Service?

They are explicit and feature-scoped:

- Controller: `modules/<feature>/presentation/controller.py`
- Service: `modules/<feature>/application/services/*`

No global root-level `controllers/` or `services/` folders are used.

---

## Layer Responsibilities

### Schemas vs Entities

- Schemas (`presentation/schemas.py`) define API request/response contracts and transport validation.
- Entities (`domain/entities.py`) represent core business objects and enforce domain rules.

### Presentation (Router + Controller + Schemas)

Responsibilities:

- define endpoints (router)
- orchestrate request/response (controller)
- validate input/output via Pydantic
- call services
- map exceptions to HTTP responses

Rules:

- no direct SQL queries
- no core business logic

### Application (Services)

Responsibilities:

- execute business scenarios
- coordinate repositories/services
- enforce transaction boundaries

Rules:

- no HTTP objects
- no ORM models in signatures

### Domain

Responsibilities:

- business invariants
- entity behavior
- domain-specific exceptions

Rules:

- framework-agnostic
- persistence-agnostic

### Infrastructure

Responsibilities:

- DB models and queries
- mapping between DB models and domain entities
- external integrations

Rules:

- must implement interfaces defined by inner layers

---

## Database Strategy (Single DB)

- One PostgreSQL database for all modules
- Module tables are separated by naming convention (or schema if needed)
- Foreign keys allowed across modules when required
- Migrations are centralized (Alembic)
- Keep strong constraints and indexes in DB

---

## Cross-Cutting Concerns

### Authentication and Authorization

- JWT/OAuth2 in FastAPI dependencies
- role/permission checks at router/controller/service boundary

### Validation

- transport validation with Pydantic schemas
- business validation in domain and services
- DB constraints as final guard

### Error Handling

- domain/application exceptions raised internally
- global FastAPI exception handlers convert to API errors

### Configuration

- centralized settings via environment variables
- no hardcoded secrets

---

## Minimal Example (Users Module)

### Router

```python
from fastapi import APIRouter, Depends, status
from app.modules.users.presentation.schemas import CreateUserRequest, UserResponse
from app.modules.users.presentation.controller import UserController

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: CreateUserRequest, controller: UserController = Depends()):
    return controller.create_user(payload)
```

### Controller

```python
from app.modules.users.application.services.user_service import UserService


class UserController:
    def __init__(self, service: UserService):
        self.service = service

    def create_user(self, payload):
        return self.service.create_user(payload)
```

### Service

```python
from app.modules.users.domain.errors import EmailAlreadyExistsError


class UserService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def create_user(self, payload):
        if self.user_repo.exists_by_email(payload.email):
            raise EmailAlreadyExistsError()
        return self.user_repo.create(payload)
```

### Repository Interface (Domain)

```python
from abc import ABC, abstractmethod


class UserRepository(ABC):
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        ...

    @abstractmethod
    def create(self, payload):
        ...
```

---

## Practical Rules for This Project

- Keep one FastAPI app and one DB until clear scaling pressure exists.
- Separate by feature module, not by technical layer at root level.
- Do not let routers call SQLAlchemy directly.
- Do not put HTTP concerns inside services/domain.
- Expose each module through its own router and register in `main.py`.

---

## Final Verdict

This architecture is **single-app, single-DB, module-separated, feature-based, and clean-architecture compliant**.

It gives MVP speed now and keeps a clean path for future scaling.
