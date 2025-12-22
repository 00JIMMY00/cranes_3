# Crane Assignment History

## ADDED Requirements

### Requirement: View Crane Assignment Timeline
The Crane Details view MUST display the assignment history of the crane, categorized by time relative to the current date.

#### Scenario: Displaying Assignments
- **Given** "Crane A" has the following `MonthlyTimeSheet` records:
    - Sheet 1: Jan 1 - Jan 15 (Past)
    - Sheet 2: Feb 1 - Feb 28 (Current, assuming today is Feb 10)
    - Sheet 3: Mar 1 - Mar 15 (Future)
- **When** the user views the details page for "Crane A".
- **Then** the page should display these sheets categorized as:
    - **Present**: Sheet 2 (showing Client, Location, Dates)
    - **Future**: Sheet 3
    - **History**: Sheet 1

### Requirement: Assignment Details
For each assignment in the list, key details MUST be visible.

#### Scenario: Assignment Information
- **When** viewing an assignment in the list.
- **Then** the user should see:
    - Client Name
    - Location
    - Start Date
    - End Date
    - Link to the full Timesheet (optional but recommended)
