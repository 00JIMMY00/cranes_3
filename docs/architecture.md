# Technical Architecture - cranes_3

## 1. Technology Stack
- **Frontend**: React with TailwindCSS
- **Backend**: Django (Python)
- **Database**: PostgreSQL
- **Environment**: .env for configuration

## 2. Core Data Models
- **Driver**: id, name, base_salary, current_balance
- **Crane**: id, name, rate_8h, rate_9h, rate_12h, is_subrented, owner_cost (if subrented)
- **Client**: id, name, contact_info, address
- **TimeSheet**: id, date, driver_id, crane_id, client_id, start_time, end_time, total_hours, overtime_hours, calculated_wage, calculated_revenue, notes
- **Loan**: id, driver_id, amount, date, description
- **Invoice**: id, client_id, date_generated, total_amount, status
- **WageSlip**: id, driver_id, month, total_wage, total_loans_deducted, final_payout

## 3. Logic Engine (Backend Service)
- **Rate Calculator**: Logic to determine 8/9/12h rate based on `TimeSheet.total_hours`
- **Wage Calculator**: Logic for `(base_hours * rate) + (overtime * 1.5)`
- **Commission Calculator**: Logic for `(TimeSheet.revenue - Crane.owner_cost)`

## 4. API Design (REST)
- `GET /api/drivers`, `POST /api/drivers`
- `GET /api/cranes`, `POST /api/cranes`
- `GET /api/clients`, `POST /api/clients`
- `POST /api/timesheets` (Triggers calculation logic)
- `POST /api/loans` (Updates driver balance)
- `GET /api/reports/invoice/{client_id}/{month}` (Generates PDF)
- `GET /api/reports/wages/{driver_id}/{month}` (Generates PDF)

## 5. Frontend Components
- **Dashboard**: High-level stats (Revenue, Active Jobs)
- **TimeSheetEntry**: Form with dynamic rate lookup
- **DriverList**: Table with "Add Loan" action
- **CraneList**: Table with Rate configuration
- **Reports**: Selector for Month/Client to generate PDFs
