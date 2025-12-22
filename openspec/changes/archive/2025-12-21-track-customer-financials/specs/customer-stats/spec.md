# Spec: Customer Stats

## ADDED Requirements

### Requirement: Track Total Services Used
The system MUST calculate and display the total number of services (timesheets) a customer has utilized over time.

#### Scenario: Viewing customer history
Given a customer "Acme Corp"
And "Acme Corp" has 5 completed monthly timesheets
When I view the "Acme Corp" profile
Then I should see "Total Services: 5"

### Requirement: Track Active Tow Trucks
The system MUST calculate and display the number of tow trucks (cranes) currently rented by the customer.

#### Scenario: Viewing active rentals
Given a customer "Acme Corp"
And "Acme Corp" has a timesheet for the current month for "Crane A"
And "Acme Corp" has a timesheet for the current month for "Crane B"
When I view the "Acme Corp" profile
Then I should see "Active Trucks: 2"
