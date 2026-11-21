# Smart Service Desk Management System

A Python command-line application for managing employee IT support requests. The system provides a simple way to register and log in, create service requests, view and search requests, and resolve open requests. Request data is stored locally in JSON files so it remains available after the application is restarted.

## Features

### User authentication
- Register a new account and log in with existing credentials.
- Enforce unique usernames (case-insensitive).
- Require passwords to contain at least 8 characters.
- Store passwords as salted PBKDF2-HMAC-SHA256 hashes rather than plain text.
- Log out and return to the welcome screen.
- Create the first account through the application; no default account is provided.

### Service request management
- Create requests with a request ID, employee name, issue description, and priority.
- Assign the initial status `OPEN` automatically.
- View all saved service requests.
- Search for a request by its ID and view its details.
- Resolve requests that are currently `OPEN`.
- Prevent duplicate request IDs and attempts to resolve an already resolved request.
- Validate priority values (`LOW`, `MEDIUM`, `HIGH`) and status values (`OPEN`, `RESOLVED`).

### Data persistence
- Store service requests in `data/requests.json`.
- Store user account records in `data/users.json`.
- Load saved data when the application starts.
- Save changes when requests are created or resolved.
- Handle missing or empty data files safely.

## Technology and concepts

- **Python** – application language.
- **Object-oriented programming (OOP)** – classes, objects, attributes, methods, and encapsulated business behavior.
- **Exception handling** – custom exceptions for application and domain errors.
- **JSON file handling** – local data storage using Python's `json` and `pathlib` modules.
- **Layered architecture** – separation of domain, application, infrastructure, and presentation responsibilities.
- **SOLID principles** – separate responsibilities across classes and layers; repository dependencies are injected into application services.
- **Domain-Driven Design (DDD) concepts** – core request rules are kept in the domain layer.
- **Git and GitHub** – version control and collaboration.

## Project structure

```text
smart-service-desk/
├── domain/
│   ├── __init__.py
│   ├── service_request.py
│   └── exceptions.py
├── application/
│   ├── __init__.py
│   ├── request_service.py
│   └── auth_service.py
├── infrastructure/
│   ├── __init__.py
│   ├── file_repository.py
│   └── user_repository.py
├── data/
│   ├── requests.json
│   └── users.json
├── main.py
├── README.md
└── .gitignore
```

### Layer responsibilities

| Layer | Responsibility |
|---|---|
| **Domain** | Defines the `ServiceRequest` model, request validation, and business behavior such as resolving a request. Contains custom exceptions. |
| **Application** | Implements use cases through `RequestService` and `AuthService`, coordinating business operations. |
| **Infrastructure** | Handles JSON file storage and retrieval through `FileRepository` and `UserRepository`. |
| **Presentation** | `main.py` provides the command-line interface, menus, user input, and output. |

The domain model is kept independent of JSON file operations. Storage concerns are handled by the infrastructure layer.

## Requirements

- Python 3.9 or later
- No third-party Python packages required

## Getting started

### 1. Clone the repository

```bash
git clone <repository-url>
```

Replace `<repository-url>` with the URL of the GitHub repository.

### 2. Open the project folder

```bash
cd smart-service-desk
```

Open a terminal in the project root—the folder containing `main.py`.

### 3. Run the application

```bash
python main.py
```

On the first run, register a user account from the welcome screen. Use that account to log in on subsequent runs.

## Application menu

After a successful login, the application provides these options:

```text
SMART SERVICE DESK SYSTEM

1. Create Service Request
2. View All Requests
3. Search Request
4. Resolve Request
5. Exit
6. Logout
```

## Data files

The application uses JSON files for local persistence:

- `data/users.json` stores registered user account records.
- `data/requests.json` stores service request information.

These files are read when the application starts and updated when relevant data changes.

## Git workflow

The project uses `main` and `development` branches. Development work is carried out in `development`, with meaningful commits made as features are implemented. After testing, the completed changes are merged into `main`.

Useful commands:

```bash
# Check the current branch and working tree
git status
git branch

# Review commit history
git log --oneline --graph --all

# Switch to the development branch
git switch development

# After testing, merge development into main
git switch main
git merge development
```
