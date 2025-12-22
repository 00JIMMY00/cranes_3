# Enforce Crane Availability and History

## Problem
Currently, the system allows a crane to be assigned to multiple clients or locations for the same time period. This leads to scheduling conflicts and data inconsistency. Additionally, there is no easy way to view the assignment history (past, present, future) of a crane to plan availability.

## Solution
1.  **Enforce Non-overlapping Assignments**: Add a constraint to the `MonthlyTimeSheet` model (or the relevant assignment entity) to ensure that for a given crane, the date ranges of assignments do not overlap.
2.  **Crane Assignment History**: Implement a view on the Crane details page that displays a timeline or list of all assignments (MonthlyTimeSheets) for that crane, categorized by status (History, Present, Future).

## Impact
- **Backend**:
    - Modify `MonthlyTimeSheet` validation logic to check for overlaps.
    - Ensure existing data is handled (or assume data is clean/provide migration path if needed - for now, we will enforce for new/updated records).
- **Frontend**:
    - Update Crane details page to fetch and display assignment history.
    - Show validation errors if a user tries to create an overlapping assignment.

## Risks
- Existing overlapping data might cause issues if we enforce strict validation on save without cleaning up data first. We will enforce this on *new* or *modified* records.
