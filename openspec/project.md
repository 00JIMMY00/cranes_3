# Project Context

## Purpose
A comprehensive management system for a crane and construction logistics business. The system is designed to manage:
- **Clients**: Customer relationship management.
- **Cranes**: Machinery tracking and management.
- **Drivers**: Personnel management for operators.
- **Kitchen**: Catering or supply management.
- **Timesheets**: Tracking work hours and operations.
- **Reports**: Generating operational and financial reports (PDFs).

## Tech Stack
- **Frontend**:
    - React 19
    - Vite 7
    - JavaScript/JSX
    - ESLint
- **Backend**:
    - Python
    - Django 4.2
    - Django REST Framework 3.16
    - ReportLab (for PDF generation)
    - Pillow (for image processing)
- **Database**:
    - PostgreSQL
- **Infrastructure**:
    - Docker (implied by typical setup, though running locally via scripts currently)
    - python-dotenv for configuration

## Project Conventions

### Code Style
- **Frontend**: ESLint configuration is present (`eslint.config.js`). Follow standard React/Vite patterns.
- **Backend**: Follows standard Django application structure. Apps are modularized (`clients`, `cranes`, `drivers`, etc.). Settings are located in `backend/core/settings.py`.

### Architecture Patterns
- **Backend**: Monolithic Django application serving a REST API via Django REST Framework.
- **Frontend**: Single Page Application (SPA) built with React and Vite, consuming the Django API.

### Testing Strategy
[Explain your testing approach and requirements - e.g., Django tests for backend, Vitest/Jest for frontend]

### Git Workflow
[Describe your branching strategy and commit conventions - e.g., Feature branching, PR reviews]

## Domain Context
- The system deals with the logistics of heavy machinery (cranes).
- Key entities include Drivers, Cranes, and Clients.
- Operational tracking involves Timesheets and Reporting.

## Important Constraints
- **Database**: Must use PostgreSQL.
- **Environment**: Configuration managed via `.env` files.

## External Dependencies
- **PostgreSQL**: Primary data store.
