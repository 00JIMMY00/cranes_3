# Track Customer Financials and Stats

## Summary
This proposal introduces financial tracking and usage statistics for customers. It enables the system to track how many services a customer has used, how many machines (tow trucks/cranes) they currently have rented, and supports a ledger system for payments (Cash, Bank Transfer, Cheque) to handle deferred payments and outstanding balances.

## Motivation
Currently, the system tracks time and revenue per timesheet but does not provide a consolidated view of a customer's financial standing or engagement history. The business needs to know:
1.  **Customer Loyalty/Usage**: Total services used.
2.  **Current Engagement**: Number of active machines.
3.  **Financial Health**: Outstanding balance and payment history, supporting partial payments.

## Proposed Solution
1.  **Customer Stats**: Add computed fields to the Client profile to show total timesheets (services) and active timesheets (current rentals).
2.  **Payments System**: Introduce a `Payment` model linked to Clients to record incoming funds.
3.  **Balance Calculation**: Compute customer balance dynamically (Total Revenue from Timesheets - Total Payments).

## Risks
*   **Data Migration**: Existing clients will have 0 payments, so they might appear to have huge debts if we count all past timesheets as "unpaid". We might need a "Initial Balance" field or a migration strategy to mark past sheets as paid or create a "Legacy Balance" adjustment. *Decision: We will add an `initial_balance` field to Client to handle legacy states if needed, or assume 0 start and let users backfill payments.*
