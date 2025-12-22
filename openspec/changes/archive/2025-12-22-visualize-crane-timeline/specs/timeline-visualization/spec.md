# Spec: Timeline Visualization

## ADDED Requirements

### Requirement: Display Horizontal Timeline
The Crane Details page MUST display a horizontal timeline of assignments at the top of the page.

#### Scenario: Viewing the timeline
Given a crane with past, present, and future assignments
When I visit the Crane Details page
Then I see a timeline visualization at the top
And the timeline shows bars for each assignment
And each bar displays the Client's name
And the bars are positioned according to their start and end dates

### Requirement: Color-code Assignments
Assignments on the timeline MUST be color-coded based on their status (Past, Present, Future).

#### Scenario: Color coding
Given the timeline is displayed
When I look at a past assignment
Then it appears in a gray color (Secondary)
When I look at a current assignment
Then it appears in a green color (Success)
When I look at a future assignment
Then it appears in a blue color (Info)

### Requirement: Timeline Navigation
The timeline MUST allow horizontal scrolling or panning to view different time periods.

#### Scenario: Scrolling
Given the timeline displays a limited time range
When I drag or scroll the timeline
Then I can see assignments outside the initial view
