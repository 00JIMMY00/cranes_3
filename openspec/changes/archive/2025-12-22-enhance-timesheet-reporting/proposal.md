# Enhance Timesheet Reporting and UI

## Problem
1. The timesheet currently shows total operating hours for the entire sheet, but when multiple drivers are involved, there is no breakdown of hours per driver.
2. There is a display issue in the timesheet UI where the template tag `{{ sheet.total_shift_days|floatformat:2 }}` is visible to the user as raw code instead of the rendered value.

## Solution
1.  **Driver Hours Breakdown**: Calculate and display the total operating hours for each driver assigned to entries in the timesheet. This will be shown in the summary section or a dedicated table.
2.  **UI Fixes**: Investigate and fix the template rendering issue for `total_shift_days` to ensure it displays the numeric value correctly.

## Risks
- Minimal risk. The driver hours calculation is a read-only aggregation. The UI fix is cosmetic.
