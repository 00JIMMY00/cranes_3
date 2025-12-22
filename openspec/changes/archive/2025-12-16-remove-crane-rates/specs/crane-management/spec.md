# Crane Management Specs

## ADDED Requirements

### Requirement: Crane Configuration
The system MUST allow creating and editing Cranes with a name, sub-rented status, and optional owner cost.

#### Scenario: Add New Crane
- **Given** I am on the "Add New Crane" page
- **Then** I should see inputs for "Crane Name", "Is Sub-rented?", and "Owner Cost" (if sub-rented)
- **And** I should NOT see inputs for hourly rates
