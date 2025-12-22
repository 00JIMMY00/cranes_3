# Design: Timesheet Refactoring

## Problem
The current system hardcodes financial calculations (rate * hours) into every daily entry and tracks "trips". The user wants a more operational view where they track "Shift Units" derived from total hours divided by a standard shift length (8, 9, 10, 12), without per-day pricing.

## Proposed Solution

### Data Model Changes
1.  **`MonthlyTimeSheet`**:
    -   Add `shift_divisor` (Integer, choices/validation for 8, 9, 10, 12, but user wants "write it", so maybe just IntegerField).
    -   Remove/Deprecate `total_trips`.
    -   Update `total_revenue` calculation logic (to be determined: is it `total_shift_units * rate`?).

2.  **`DailyEntry`**:
    -   Remove `trips`, `daily_total`, `hourly_rate` from the active UI.
    -   The `operating_hours` calculation remains the same.
    -   New concept: `calculated_shift_units` (virtual or stored).

### Calculation Logic
$$ \text{Shift Units} = \frac{\text{Operating Hours}}{\text{Shift Divisor}} $$

Example:
-   Operating Hours: 10
-   Shift Divisor: 8
-   Shift Units: 1.25

### UI Changes
-   **Monthly Detail View**:
    -   Remove columns: "Trips", "Hourly Rate", "Daily Total".
    -   Add input for "Shift Divisor" (defaulting to 8?).
    -   Show "Operating Hours" and potentially the calculated "Shift Units".

## Open Questions
1.  Do we still need to calculate Revenue? If so, where does the rate come from? (Likely `MonthlyTimeSheet.default_hourly_rate` or a new `shift_rate`).
2.  What happens to existing data? (We will keep fields in DB but hide in UI for now).
