# Design: Enforce Crane Availability

## Architecture
- **Validation Layer**: Model-level validation in Django (`clean()` method). This ensures that whether data comes from API, Admin, or Shell, the integrity is maintained.
- **API Layer**: `CraneSerializer` will be enriched with assignment data to avoid multiple round-trips from the frontend.

## Data Model Changes
- No schema changes (migrations) required if `start_date` and `end_date` already exist.
- Logic change only in `MonthlyTimeSheet`.

## Algorithm: Overlap Check
For a given range `[S1, E1]` and existing range `[S2, E2]`:
Overlap exists if `S1 <= E2` AND `E1 >= S2`.
*Note*: Dates are inclusive.

## UI Design
- **Crane Details Page**:
    - Add a new container/card below the main details.
    - Title: "Assignment History".
    - Content:
        - **Active**: Highlighted box with current assignment details.
        - **Upcoming**: List of future assignments.
        - **Past**: Collapsible or scrollable list of past assignments.
