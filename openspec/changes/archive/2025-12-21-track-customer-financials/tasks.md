# Tasks: Track Customer Financials

## Backend Implementation
- [x] Create `Payment` model in `clients/models.py` with fields: client, amount, date, method, reference, notes. <!-- id: create-payment-model -->
- [x] Create migration for `Payment` model. <!-- id: migrate-payment -->
- [x] Add `get_stats` methods to `Client` model (services_count, active_count, balance). <!-- id: client-stats-methods -->
- [x] Create `PaymentSerializer` and `PaymentViewSet`. <!-- id: payment-api -->
- [x] Update `ClientSerializer` to include financial stats and counts. <!-- id: client-serializer-update -->
- [x] Register Payment URLs in `clients/urls.py` (or main `urls.py`). <!-- id: payment-urls -->

## Frontend Implementation
- [x] Update Client List view to show "Balance" and "Active Rentals" columns. <!-- id: fe-client-list -->
- [x] Update Client Detail view to show:
    - [x] Summary Cards: Total Services, Active Trucks, Outstanding Balance.
    - [x] Payment History Table.
    - [x] "Add Payment" Button and Modal Form. <!-- id: fe-client-detail -->
- [x] Implement "Add Payment" form logic (handling Cash, Bank, Cheque types). <!-- id: fe-payment-form -->

## Validation
- [x] Test: Add a timesheet, verify balance increases. <!-- id: test-balance-increase -->
- [x] Test: Add a partial payment, verify balance decreases but remains positive. <!-- id: test-partial-payment -->
- [x] Test: Verify "Active Trucks" count updates when a new sheet is added for current month. <!-- id: test-active-count -->
