# Tasks: Enforce Crane Availability

## Backend
- [x] **Implement Overlap Validation** <!-- id: 0 -->
    - Modify `MonthlyTimeSheet.clean()` in `backend/timesheets/models.py`.
    - Query for other `MonthlyTimeSheet` records for the same `crane`.
    - Check if `(start_date <= other.end_date) and (end_date >= other.start_date)`.
    - Exclude `self.pk` from the query.
    - Raise `ValidationError` if overlap found.
- [x] **Test Overlap Validation** <!-- id: 1 -->
    - Create tests in `backend/timesheets/tests/test_models.py` (or similar).
    - Test cases: exact match, partial overlap, inside, enclosing, no overlap, update self.
- [x] **Expose Assignments in API** <!-- id: 2 -->
    - Update `CraneSerializer` in `backend/cranes/serializers.py` (or create a specific serializer).
    - Add a field (e.g., `assignments` or `history`) that returns `MonthlyTimeSheet` data (id, client name, location, start_date, end_date).
    - Alternatively, ensure `monthly_sheets` are accessible and filterable.
    - *Decision*: Add a read-only `assignments` field to `CraneSerializer` that returns a list of simple assignment objects.

## Frontend
- [x] **Update Crane Details Page** <!-- id: 3 -->
    - Modify `frontend/src/pages/cranes/CraneDetails.jsx` (check actual path).
    - Add a section for "Assignment History".
    - Fetch crane details (which now includes assignments).
    - Group assignments into Present, Future, History based on current date.
    - Display as a list or timeline.
- [x] **Handle Validation Errors** <!-- id: 4 -->
    - Verify that the Timesheet form (where assignments are created) displays the specific validation error message when an overlap occurs.

