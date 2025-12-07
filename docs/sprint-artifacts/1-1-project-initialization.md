# Story 1.1: Project Initialization & Infrastructure

**Epic:** 1: Foundation & Core Data Setup
**Story ID:** 1.1
**Status:** ready-for-dev

## User Story
As a Developer, I want to set up the Django backend and React frontend with PostgreSQL, So that the application has a stable environment to run.

## Acceptance Criteria
- [ ] **Given** a fresh environment
- [ ] **When** I run the setup script (or manual setup)
- [ ] **Then** a Django 4.x project is created with a connected PostgreSQL database
- [ ] **And** a React frontend is initialized with TailwindCSS
- [ ] **And** the `.env` file handles configuration secrets
- [ ] **And** I can access the admin panel at `/admin`

## Technical Implementation Guide

### Architecture Alignment
- **Backend:** Django + Django Rest Framework (DRF)
- **Frontend:** React + TailwindCSS
- **Database:** PostgreSQL
- **Configuration:** .env file for secrets

### Tasks
- [x] **Task 1:** Initialize Django Project
    - [x] Create virtual environment
    - [x] Install Django, psycopg2-binary, python-dotenv, djangorestframework, django-cors-headers
    - [x] Start project `backend`
    - [x] Configure settings.py for PostgreSQL and Environment Variables
- [x] **Task 2:** Initialize React Frontend
    - [x] Create React app `frontend` (using Vite recommended for speed)
    - [x] Install TailwindCSS and configure
- [x] **Task 3:** Database Setup
    - [x] Create PostgreSQL database `cranes`
    - [x] Run initial migrations
    - [x] Create superuser
- [x] **Task 4:** Integration Verification
    - [x] Ensure backend runs on port 8000
    - [x] Ensure frontend runs on port 5173 (Vite default)
    - [x] Verify Admin Panel access

## Dev Agent Record
<!-- To be filled by the developer during implementation -->
