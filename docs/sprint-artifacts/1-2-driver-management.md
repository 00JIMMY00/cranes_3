# Story 1.2: Driver Management (CRUD)

**Epic:** 1: Foundation & Core Data Setup
**Story ID:** 1.2
**Status:** ready-for-dev

## User Story
As the Owner, I want to add and edit driver profiles, So that I can track who is operating my cranes.

## Acceptance Criteria
- [ ] **Given** I am on the "Drivers" page
- [ ] **When** I click "Add Driver" and enter "Name" and "Base Salary"
- [ ] **Then** the driver is saved to the database
- [ ] **And** I see them in the Driver List
- [ ] **And** their initial "Current Balance" is 0

## Technical Implementation Guide

### Architecture Alignment
- **Model:** `Driver(name, base_salary, current_balance)`
- **API:** `GET /api/drivers/`, `POST /api/drivers/`, `PUT /api/drivers/{id}/`, `DELETE /api/drivers/{id}/`
- **Frontend:** React component with form and table

### Tasks
- [x] **Task 1:** Create Django App `drivers`
    - [x] Run `python manage.py startapp drivers`
    - [x] Add `drivers` to INSTALLED_APPS
- [x] **Task 2:** Create Driver Model
    - [x] Define `Driver` model with fields: `name`, `base_salary`, `current_balance`
    - [x] Run migrations
- [x] **Task 3:** Create DRF Serializer & ViewSet
    - [x] Create `DriverSerializer`
    - [x] Create `DriverViewSet` with CRUD operations
    - [x] Register routes in `urls.py`
- [x] **Task 4:** Frontend - Driver List Component
    - [x] Create `DriverList.jsx` component
    - [x] Fetch and display drivers from API
- [x] **Task 5:** Frontend - Add Driver Form
    - [x] Create form with Name and Base Salary fields
    - [x] POST to API on submit
    - [x] Refresh list after adding

## Dev Agent Record
**Files Created/Modified:**
- `backend/drivers/` (new Django app)
- `backend/drivers/models.py` - Driver model
- `backend/drivers/serializers.py` - DriverSerializer
- `backend/drivers/views.py` - DriverViewSet
- `backend/drivers/urls.py` - API routes
- `backend/core/settings.py` - Added drivers to INSTALLED_APPS
- `backend/core/urls.py` - Added API routes
- `frontend/src/api/drivers.js` - API client
- `frontend/src/components/DriverList.jsx` - Driver management UI
- `frontend/src/App.jsx` - Updated to use DriverList
- `frontend/tailwind.config.js` - Tailwind configuration
- `frontend/postcss.config.js` - PostCSS configuration
