# Refactor Timesheet Calculation and UI

## Context
The current timesheet implementation tracks daily entries with specific financial fields (hourly rate, daily total) and trips. The user wants to simplify this by removing these financial and trip columns and instead focusing on "Shift Units" calculated from total working hours divided by a configurable shift duration (8, 9, 10, or 12 hours).

## Goals
1.  **Simplify Data Entry**: Remove `hourly_rate`, `daily_total`, and `trips` from the daily timesheet view.
2.  **Flexible Shift Calculation**: Allow the user to define a "Shift Divisor" (8, 9, 10, 12) for the crane.
3.  **New Calculation Logic**: Calculate "Shift Days" = `Total Working Hours` / `Shift Divisor`.

## Scope
-   **Backend**:
    -   Modify `DailyEntry` model to remove/deprecate `trips`, `daily_total`, `hourly_rate`.
    -   Add logic to calculate `shift_units` based on a dynamic divisor.
    -   Update `MonthlyTimeSheet` to aggregate these new units.
-   **Frontend (Templates)**:
    -   Update `timesheets/monthly_detail.html` to remove columns and add the shift divisor input.
    -   Update JavaScript for real-time calculation.

## Risks
-   **Data Migration**: Existing data with `trips` and `daily_totals` might need preservation or migration strategy if we drop columns. For now, we might just hide them or make them nullable.
-   **Financial Calculation**: Removing `hourly_rate` from daily entries implies revenue is calculated differently (e.g., globally per sheet or just tracking hours). We need to clarify if revenue calculation is still needed at the sheet level.
