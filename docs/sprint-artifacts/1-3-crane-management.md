# Story 1.3: Crane Management with Rate Logic

**Epic:** 1: Foundation & Core Data Setup
**Story ID:** 1.3
**Status:** complete

## User Story
As the Owner, I want to define cranes with their specific daily rates (8/9/12 hours), So that the system knows how to bill them later.

## Acceptance Criteria
- [ ] **Given** I am on the "Cranes" page
- [ ] **When** I add a crane "Liebherr 50t"
- [ ] **And** I set rates: 8h=3000, 9h=3500, 12h=5000
- [ ] **And** I check "Is Sub-rented?" and set "Owner Cost=2000"
- [ ] **Then** the crane is saved with all rate configurations

## Technical Implementation Guide

### Architecture Alignment
- **Model:** `Crane(name, rate_8h, rate_9h, rate_12h, is_subrented, owner_cost)`
- **API:** `GET /api/cranes/`, `POST /api/cranes/`, `PUT /api/cranes/{id}/`, `DELETE /api/cranes/{id}/`
- **Frontend:** React component with form and table

### Tasks
- [x] **Task 1:** Create Django App `cranes`
    - [x] Run `python manage.py startapp cranes`
    - [x] Add `cranes` to INSTALLED_APPS
- [x] **Task 2:** Create Crane Model
    - [x] Define `Crane` model with all fields
    - [x] Run migrations
- [x] **Task 3:** Create DRF Serializer & ViewSet
    - [x] Create `CraneSerializer`
    - [x] Create `CraneViewSet` with CRUD operations
    - [x] Register routes in `urls.py`
- [x] **Task 4:** Frontend - Crane List Component
    - [x] Create `CraneList.jsx` component
    - [x] Fetch and display cranes from API
- [x] **Task 5:** Frontend - Add Crane Form
    - [x] Create form with all fields including rates
    - [x] POST to API on submit
    - [x] Refresh list after adding

## Dev Agent Record
**Files Created/Modified:**
- `backend/cranes/` (new Django app)
- `backend/cranes/models.py` - Crane model
- `backend/cranes/serializers.py` - CraneSerializer
- `backend/cranes/views.py` - CraneViewSet
- `backend/cranes/urls.py` - API routes
- `backend/core/settings.py` - Added cranes to INSTALLED_APPS
- `backend/core/urls.py` - Added API routes
- `frontend/src/api/cranes.js` - API client
- `frontend/src/components/CraneList.jsx` - Crane management UI
- `frontend/src/App.jsx` - Added navigation tabs
- `frontend/postcss.config.js` - Fixed for Tailwind v4
