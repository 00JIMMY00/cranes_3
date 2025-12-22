# prevent-overlapping-assignments Specification

## Purpose
TBD - created by archiving change enforce-crane-availability. Update Purpose after archive.
## Requirements
### Requirement: Enforce Unique Crane Assignment Periods
The system MUST ensure that a crane is not assigned to multiple contexts (Clients/Locations) simultaneously. An assignment is defined by a `MonthlyTimeSheet` record.

#### Scenario: Blocking Overlapping Assignments
- **Given** a `MonthlyTimeSheet` exists for "Crane A" with `start_date="2024-01-01"` and `end_date="2024-01-15"`.
- **When** a user attempts to create or update a `MonthlyTimeSheet` for "Crane A" with `start_date="2024-01-10"` and `end_date="2024-01-20"`.
- **Then** the system should reject the save operation with a validation error indicating the crane is already assigned during that period.

#### Scenario: Allowing Sequential Assignments
- **Given** a `MonthlyTimeSheet` exists for "Crane A" with `start_date="2024-01-01"` and `end_date="2024-01-15"`.
- **When** a user attempts to create a `MonthlyTimeSheet` for "Crane A" with `start_date="2024-01-16"` and `end_date="2024-01-31"`.
- **Then** the system should accept the assignment.

#### Scenario: Ignoring Self in Overlap Check
- **Given** a `MonthlyTimeSheet` exists for "Crane A" with `start_date="2024-01-01"` and `end_date="2024-01-15"`.
- **When** the user updates this specific `MonthlyTimeSheet` (e.g., changing the client or notes) without changing dates to overlap with another DIFFERENT sheet.
- **Then** the system should accept the update.

### Requirement: Date Range Validity
The validation MUST rely on `start_date` and `end_date`.

#### Scenario: Missing Dates
- **Given** a `MonthlyTimeSheet` is being saved without `start_date` or `end_date`.
- **Then** the system should either enforce these fields are present (if that's the new standard) or derive them from `month`/`year` for validation purposes if legacy support is needed. (For this change, we assume `start_date` and `end_date` are populated as they are essential for the "specific time period" requirement).

