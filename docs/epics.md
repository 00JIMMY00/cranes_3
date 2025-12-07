# cranes_3 - Epic Breakdown

**Author:** Ahmedgamal
**Date:** 2025-12-06

---

## Overview

This document provides the complete epic and story breakdown for cranes_3, decomposing the requirements from the [PRD](./prd.md) into implementable stories.

## Functional Requirements Inventory

### FR1: Core Data Management
- **FR1.1**: Manage Driver Profiles (Create, Read, Update, Delete)
- **FR1.2**: Manage Crane Profiles with multi-rate logic
- **FR1.3**: Manage Client Profiles

### FR2: Time Sheet Processing
- **FR2.1**: Digital Time Sheet Entry Form
- **FR2.2**: Automatic Hours Calculation (Total & Overtime)
- **FR2.3**: Automatic Rate Selection (8/9/12h logic)
- **FR2.4**: Automatic Commission Calculation

### FR3: Financial Management
- **FR3.1**: Driver Loan Recording
- **FR3.2**: Driver Balance Tracking (Wages - Loans)

### FR4: Reporting & Output
- **FR4.1**: Generate PDF Client Invoice
- **FR4.2**: Generate PDF Driver Wage Slip

---

## Epic 1: Foundation & Core Data Setup
**Goal:** Establish the technical foundation (Django/React) and enable the Owner to manage the static entities (Drivers, Cranes, Clients) required for daily operations.

### Story 1.1: Project Initialization & Infrastructure
As a Developer, I want to set up the Django backend and React frontend with PostgreSQL, So that the application has a stable environment to run.

**Acceptance Criteria:**
- **Given** a fresh environment
- **When** I run the setup script
- **Then** a Django 4.x project is created with a connected PostgreSQL database
- **And** a React frontend is initialized with TailwindCSS
- **And** the `.env` file handles configuration secrets
- **And** I can access the admin panel at `/admin`

**Technical Notes:**
- Stack: Django, DRF, React, PostgreSQL.
- Create `requirements.txt` and `package.json`.

### Story 1.2: Driver Management (CRUD)
As the Owner, I want to add and edit driver profiles, So that I can track who is operating my cranes.

**Acceptance Criteria:**
- **Given** I am on the "Drivers" page
- **When** I click "Add Driver" and enter "Name" and "Base Salary"
- **Then** the driver is saved to the database
- **And** I see them in the Driver List
- **And** their initial "Current Balance" is 0

**Technical Notes:**
- Model: `Driver(name, base_salary, current_balance)`.
- API: `POST /api/drivers`, `GET /api/drivers`.

### Story 1.3: Crane Management with Rate Logic
As the Owner, I want to define cranes with their specific daily rates (8/9/12 hours), So that the system knows how to bill them later.

**Acceptance Criteria:**
- **Given** I am on the "Cranes" page
- **When** I add a crane "Liebherr 50t"
- **And** I set rates: 8h=3000, 9h=3500, 12h=5000
- **And** I check "Is Sub-rented?" and set "Owner Cost=2000"
- **Then** the crane is saved with all rate configurations

**Technical Notes:**
- Model: `Crane(name, rate_8h, rate_9h, rate_12h, is_subrented, owner_cost)`.
- Frontend: Form with numeric inputs for all 3 rates.

### Story 1.4: Client Management
As the Owner, I want to store client details, So that invoices can be addressed correctly.

**Acceptance Criteria:**
- **Given** I am on the "Clients" page
- **When** I enter Client Name and Address
- **Then** the client is stored for future dropdown selection

---

## Epic 2: The Logic Engine (Time Sheets)
**Goal:** Enable the "Single Source of Truth" workflow where the Owner enters daily logs and the system handles all the complex math automatically.

### Story 2.1: Time Sheet Entry Form
As the Owner, I want a unified form to enter daily work logs, So that I don't have to use paper notebooks.

**Acceptance Criteria:**
- **Given** I am on the "New Entry" page
- **When** I select Date, Driver, Crane, Client
- **And** I enter Start Time (08:00) and End Time (20:00)
- **Then** the system automatically displays "Total Hours: 12"
- **And** calculates "Overtime: 4 hours" (assuming 8h standard)

**Technical Notes:**
- Frontend: DateTime pickers.
- Real-time calculation on frontend before submit is nice, but backend validation is mandatory.

### Story 2.2: Automated Rate & Wage Calculation
As the Owner, I want the system to calculate the billing amount and driver wage instantly, So that I avoid mental math errors.

**Acceptance Criteria:**
- **Given** I submit a Time Sheet for 12 hours
- **When** the system processes the entry
- **Then** it looks up the Crane's "12h Rate" and saves it as `revenue`
- **And** it calculates Driver Wage = (Base Rate + Overtime Rate)
- **And** if the crane is sub-rented, it calculates Commission = (Revenue - Owner Cost)

**Technical Notes:**
- Backend Logic: `TimeSheet.save()` method or Service layer should handle this logic.
- Do not rely on frontend for financial calculations.

---

## Epic 3: Financials & Reporting
**Goal:** Close the loop by tracking money (Loans/Balances) and generating the final artifacts (PDFs) for external stakeholders.

### Story 3.1: Driver Loan Recording
As the Owner, I want to record cash loans given to drivers, So that I don't forget to deduct them later.

**Acceptance Criteria:**
- **Given** I am on a Driver's profile
- **When** I click "Add Loan" and enter "1000 EGP"
- **Then** the Driver's "Current Balance" decreases by 1000
- **And** a Loan record is created with the date

**Technical Notes:**
- Model: `Loan(driver, amount, date)`.
- Trigger: Update `Driver.current_balance` signal.

### Story 3.2: PDF Invoice Generation
As the Owner, I want to download a professional PDF invoice for a client, So that I can get paid faster.

**Acceptance Criteria:**
- **Given** I select a Client and a Month (e.g., "Orascom", "November")
- **When** I click "Generate Invoice"
- **Then** a PDF is downloaded containing:
    - Client Name/Address
    - Table of all Time Sheet entries for that month (Date, Crane, Hours, Price)
    - Total Amount Due

**Technical Notes:**
- Library: `ReportLab` (Python) or `WeasyPrint`.
- API: `GET /api/reports/invoice/...` returns `application/pdf`.

### Story 3.3: Driver Wage Slip Generation
As the Owner, I want to print a wage slip that shows the net payout, So that the driver understands their pay and loan deductions.

**Acceptance Criteria:**
- **Given** I select a Driver and Month
- **When** I click "Generate Wage Slip"
- **Then** a PDF shows:
    - Total Earned (from Time Sheets)
    - Less: Total Loans (taken this month)
    - Net Payable Amount

---

## Summary
This breakdown delivers the MVP scope:
1.  **Epic 1** builds the data foundation.
2.  **Epic 2** automates the core operational logic.
3.  **Epic 3** delivers the financial value and final outputs.
