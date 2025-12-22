# Driver Hours Breakdown

## ADDED Requirements

### Requirement: Calculate Total Hours Per Driver
The system MUST calculate the sum of `operating_hours` for each unique driver present in the timesheet's daily entries.

#### Scenario: Single Driver
- **Given** a timesheet with 1 driver and 10 entries of 8 hours each.
- **When** the sheet is viewed.
- **Then** the system shows "Driver A: 80 hours".

#### Scenario: Multiple Drivers
- **Given** a timesheet with 2 drivers (Driver A and Driver B).
- **And** Driver A has 5 entries of 10 hours.
- **And** Driver B has 5 entries of 10 hours.
- **When** the sheet is viewed.
- **Then** the system shows:
  - "Driver A: 50 hours"
  - "Driver B: 50 hours"

### Requirement: Display Driver Hours in Summary
The breakdown of hours per driver MUST be displayed in the timesheet detail view, preferably in the summary section or a new "Driver Totals" section.

#### Scenario: Summary Display
- **Given** a timesheet with Driver A (50h) and Driver B (30h).
- **When** the user views the summary section.
- **Then** they see "Driver A: 50" and "Driver B: 30" clearly listed.
