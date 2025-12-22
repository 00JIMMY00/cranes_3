# Design: Customer Financials

## Database Schema Changes

### 1. New Model: `Payment` (in `clients` app)
Represents a payment made by a client.

*   `client`: ForeignKey to `Client`
*   `amount`: Decimal (10, 2)
*   `date`: DateField
*   `method`: CharField (Choices: 'CASH', 'BANK_TRANSFER', 'CHEQUE')
*   `reference`: CharField (Optional, for cheque number or transaction ID)
*   `notes`: TextField
*   `created_at`, `updated_at`

### 2. Updates to `Client` Model (or Service Layer)
We need to expose the following computed properties (likely via annotations or properties on the model/serializer):

*   `total_services_count`: Count of `MonthlyTimeSheet` objects associated with the client.
*   `active_rentals_count`: Count of `MonthlyTimeSheet` objects where `end_date` is >= today (or null/active logic).
*   `total_revenue`: Sum of `total_revenue` from all `MonthlyTimeSheet`s.
*   `total_paid`: Sum of `amount` from all `Payment`s.
*   `outstanding_balance`: `total_revenue` - `total_paid`.

## Logic

### "Tow Truck" Terminology
The user requested "Tow Truck" stats. The system currently uses `Crane`. We will assume `Crane` entities represent the "Tow Trucks". The UI labels can be adjusted, but the backend model remains `Crane`.
"Services Used" will be interpreted as the number of `MonthlyTimeSheet` records, as each sheet represents a rental engagement.

### Active Rentals
A rental is "active" if there is a `MonthlyTimeSheet` for the current month/period or if the specific `end_date` on the sheet is in the future.
Given the `MonthlyTimeSheet` structure (month/year based), "Active" might mean "Has a sheet for the current month".

### Deferred Payments
The system will not link payments 1:1 to Timesheets (Invoices). Instead, it will use a **Ledger** approach (Balance Forward).
*   **Debit**: `MonthlyTimeSheet` completion adds to the debt.
*   **Credit**: `Payment` reduces the debt.
*   **Balance**: Net of Debts and Credits.
This naturally supports partial payments (deferred payments).

## API Changes
*   `GET /api/clients/`: Include `balance`, `active_rentals`, `services_count` in the list/detail response.
*   `POST /api/clients/{id}/payments/`: Endpoint to record a payment.
*   `GET /api/clients/{id}/payments/`: Endpoint to list payment history.
