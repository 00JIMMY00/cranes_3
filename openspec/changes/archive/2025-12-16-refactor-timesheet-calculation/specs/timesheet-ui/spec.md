# Spec: Timesheet UI

## ADDED Requirements

### Requirement: Monthly Detail View Columns
The monthly detail view table MUST be simplified.

#### Scenario: Hidden Columns
- **GIVEN** the monthly detail page
- **WHEN** the table is rendered
- **THEN** the "Trips", "Hourly Rate", and "Daily Total" columns should not be visible.

### Requirement: Shift Divisor Input
The monthly detail view MUST provide an input for the shift divisor.

#### Scenario: Input Field
- **GIVEN** the monthly detail page
- **WHEN** the page loads
- **THEN** an input field for "Shift Divisor" (or "Shift Hours") should be visible near the totals.
