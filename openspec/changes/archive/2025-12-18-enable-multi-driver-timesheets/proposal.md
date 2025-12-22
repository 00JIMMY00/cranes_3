# Enable Multi-Driver Timesheets

## Why
Currently, a Monthly Timesheet is assigned to a single Driver. However, in practice, a Crane may be operated by multiple drivers during the same month or even during the same day (e.g., shifts). The user needs to be able to specify which driver worked during which hours.

## What Changes
We will enable a "Multi-Driver Mode" for Monthly Timesheets based on a driver count.
- **Model Changes**:
    - Add `driver_count` (PositiveInteger, default=1) to `MonthlyTimeSheet`.
    - Add `driver` (FK to Driver, nullable) to `DailyEntry`.
    - Remove `unique_together` constraint on `DailyEntry` (currently `['monthly_sheet', 'day_number']`) to allow multiple entries per day.
- **UI Changes**:
    - Add a number input "Number of Drivers" (default 1) when creating/editing a Timesheet.
    - If `driver_count > 1`:
        - Display a "Driver" column in the daily entries table.
        - Allow adding multiple rows for the same day (to split hours between drivers).
        - Use the Timesheet's main driver as the default for new rows.
    - Refactor the "Save All" form handling to identify rows by `entry.id` instead of `day_number` to support multiple rows per day.

## Impact
- **Database**: Migration required for `MonthlyTimeSheet` and `DailyEntry`.
- **Backend**: `monthly_sheet_save_all` view needs significant refactoring to handle dynamic rows and ID-based inputs.
- **Frontend**: `monthly_detail.html` needs to support dynamic row addition and the new "Driver" column.

## Risks
- **Data Integrity**: Removing `unique_together` means we must be careful not to accidentally duplicate days when not intended.
- **Backward Compatibility**: Existing timesheets should default to `is_multi_driver=False` and behave exactly as before.
