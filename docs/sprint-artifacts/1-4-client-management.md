# Story 1.4: Client Management

**Epic:** 1: Foundation & Core Data Setup
**Story ID:** 1.4
**Status:** complete

## User Story
As the Owner, I want to store client details, So that invoices can be addressed correctly.

## Acceptance Criteria
- [x] **Given** I am on the "Clients" page
- [x] **When** I enter Client Name and Address
- [x] **Then** the client is stored for future dropdown selection

## Technical Implementation Guide

### Architecture Alignment
- **Model:** `Client(name, address, phone, email)`
- **API:** `GET /api/clients/`, `POST /api/clients/`, `PUT /api/clients/{id}/`, `DELETE /api/clients/{id}/`
- **Frontend:** React component with form and table

### Tasks
- [x] **Task 1:** Create Django App `clients`
- [x] **Task 2:** Create Client Model
- [x] **Task 3:** Create DRF Serializer & ViewSet
- [x] **Task 4:** Frontend - Client List Component
- [x] **Task 5:** Frontend - Add Client Form

## Dev Agent Record
**Files Created/Modified:**
- `backend/clients/` (new Django app)
- `backend/clients/models.py` - Client model
- `backend/clients/serializers.py` - ClientSerializer
- `backend/clients/views.py` - ClientViewSet
- `backend/clients/urls.py` - API routes
- `backend/core/settings.py` - Added clients to INSTALLED_APPS
- `backend/core/urls.py` - Added API routes
- `frontend/src/api/clients.js` - API client
- `frontend/src/components/ClientList.jsx` - Client management UI
- `frontend/src/App.jsx` - Added ClientList to navigation
