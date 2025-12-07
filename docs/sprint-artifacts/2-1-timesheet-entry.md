# Story 2.1: Time Sheet Entry Form (Monthly Sheet Format)

**Epic:** 2: The Logic Engine (Time Sheets)
**Story ID:** 2.1
**Status:** complete

## User Story
As the Owner, I want a monthly time sheet form that matches my hard copy sheets, So that I can digitize my existing workflow without changing how I record data.

## Acceptance Criteria
- [x] **Given** I am on the "New Time Sheet" page
- [x] **When** I select Date, Driver, Crane, Client
- [x] **And** I enter Start Time and End Time
- [x] **Then** the system automatically displays "Total Hours"
- [x] **And** calculates "Overtime" (assuming 8h standard)
- [x] **Given** I create a new monthly time sheet
- [x] **When** I specify Project/Client, Crane, Driver, Location, and Month
- [x] **Then** a 31-row table is generated for daily entries
- [x] **And** each row has: Day#, Weekday, Date, From, To, Operating Hours, Trips, Notes, Attendance Hours
- [x] **Given** I fill in daily entries in the monthly sheet
- [x] **When** I save the sheet
- [x] **Then** all daily data is processed and stored
- [x] **And** totals are calculated for the month

## Technical Implementation Guide

### Architecture Alignment
Based on hard copy sheet format:

**Header Fields:**
- Project/Customer Name (Client FK)
- Machine Type/Equipment (Crane FK)
- Operator Name (Driver FK)
- Location/Site (text field)
- Month/Year (date field)

**Daily Entry Table (31 rows):**
| Column | Arabic | Field Type |
|--------|--------|------------|
| No. | م | Auto (1-31) |
| Day | اليوم | Auto (weekday name) |
| Date | التاريخ | Auto (calendar date) |
| From | من | Time input |
| To | إلى | Time input |
| Operating Hours | إجمالي ساعات التشغيل | Calculated |
| Trips | رحلات | Integer input |
| Notes | البيان | Text input |
| Attendance Hours | إجمالي ساعات الحضور | Decimal input |

**Footer:**
- Supervisor signature field
- Monthly totals (hours, trips)

### Tasks
- [x] **Task 1:** Create Django App `timesheets`
- [x] **Task 2:** Create TimeSheet Model (single entry)
- [x] **Task 3:** Create template views for list/create/edit
- [x] **Task 4:** Add real-time hour calculation in JavaScript
- [x] **Task 5:** Implement automated rate calculation on save
- [x] **Task 6:** Create MonthlyTimeSheet model (header info)
- [x] **Task 7:** Create DailyEntry model (31 rows per sheet)
- [x] **Task 8:** Create monthly sheet form template with 31-row table
- [x] **Task 9:** Add JavaScript for auto-calculating daily operating hours
- [x] **Task 10:** Create monthly sheet list and detail views
- [x] **Task 11:** Calculate monthly totals on save

## Dev Agent Record
**Files Created/Modified:**
- `backend/timesheets/` (new Django app)
- `backend/timesheets/models.py` - TimeSheet, MonthlyTimeSheet, DailyEntry models
- `backend/timesheets/views.py` - All CRUD views + AJAX endpoints
- `backend/timesheets/urls.py` - URL patterns for both formats
- `backend/templates/timesheets/timesheet_list.html` - Quick entry list
- `backend/templates/timesheets/timesheet_form.html` - Quick entry form
- `backend/templates/timesheets/monthly_list.html` - Monthly sheets list
- `backend/templates/timesheets/monthly_create.html` - Create monthly sheet
- `backend/templates/timesheets/monthly_detail.html` - 31-row table view
- `backend/templates/base.html` - Updated navigation with dropdown
- `backend/core/urls.py` - Added timesheet routes
- `backend/core/settings.py` - Added timesheets to INSTALLED_APPS

**Implementation Notes:**
- Implementing monthly sheet format to match hard copy workflow
- Each MonthlyTimeSheet has header info + 31 DailyEntry rows
- DailyEntry stores: from_time, to_time, operating_hours, trips, notes, attendance_hours
- Auto-calculates operating hours when from/to times are entered
- Monthly totals (hours, trips, revenue, wage) calculated on each entry save
- Bilingual support (English/Arabic) for column headers and weekday names
- Friday rows highlighted in yellow (common weekend in Egypt)
- Invalid days (e.g., day 31 in February) shown as disabled rows
