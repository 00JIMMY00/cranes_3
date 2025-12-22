# Timesheet UI Fixes

## ADDED Requirements

### Requirement: Correctly Render Total Shift Days
The `total_shift_days` value MUST be rendered as a number (formatted to 2 decimal places) in the timesheet summary and totals row, not as raw template code.

#### Scenario: View Timesheet
- **Given** a timesheet with `total_shift_days` = 10.5.
- **When** the user views the timesheet.
- **Then** they see "10.50" in the "Total Shift Days" field.
- **And** they do NOT see `{{ sheet.total_shift_days|floatformat:2 }}`.
