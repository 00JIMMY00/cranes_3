# timesheet-drivers Specification

## Purpose
TBD - created by archiving change enable-multi-driver-timesheets. Update Purpose after archive.
## Requirements
### Requirement: Driver Count Configuration
The system SHALL allow users to specify the "Number of Drivers" (defaulting to 1) when creating or editing a Monthly Timesheet. Setting this count greater than 1 enables multi-driver features.

#### Scenario: Set Multiple Drivers
Given I am creating a new Monthly Timesheet
When I set the "Number of Drivers" to 2
Then the created timesheet should allow assigning different drivers to different daily entries

### Requirement: Driver Assignment per Entry
When the driver count is greater than 1, the system SHALL provide a mechanism to select a specific driver for each daily entry row. The default selection SHALL be the primary driver assigned to the timesheet.

#### Scenario: Assign Driver to Daily Entry
Given I am viewing a Timesheet with "Number of Drivers" set to 2
When I look at the daily entries table
Then I should see a "Driver" dropdown for each entry
And the default selected driver should be the Timesheet's main driver

### Requirement: Multiple Shifts per Day
The system SHALL allow users to add multiple entry rows for the same calendar day to represent split shifts or multiple drivers working on the same day.

#### Scenario: Split Day into Multiple Shifts
Given I am viewing a Multi-Driver Timesheet
And I want to record two drivers for Day 1 (e.g. 8am-12pm and 12pm-4pm)
When I click "Add Shift" for Day 1
Then a new row for Day 1 should appear
And I can set different times and drivers for each row

### Requirement: Multi-Driver Calculations
The system SHALL calculate financial totals (wages) by summing the calculated wage for each individual entry, respecting the specific driver assigned to that entry and their rate.

#### Scenario: Calculate Totals with Multiple Drivers
Given a timesheet has multiple drivers across different shifts
When the totals are calculated
Then the "Total Driver Wage" should be the sum of wages for all entries (calculating each entry's wage based on its assigned driver's rate)
And "Total Operating Hours" should be the sum of all entries' hours

### Requirement: Robust Entry Saving
The system SHALL identify and update daily entries using their unique database ID rather than their day number, to support multiple entries sharing the same day number.

#### Scenario: Save All Entries
Given I have a timesheet with multiple rows for the same day
When I click "Save"
Then all entries should be saved correctly
And the system should identify entries by their unique ID, not just the day number

