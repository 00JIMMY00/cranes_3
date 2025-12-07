---
stepsCompleted: [1, 2, 3, 4]
inputDocuments:
  - product-brief-cranes_3-2025-12-06.md
workflowType: 'prd'
lastStep: 0
project_name: 'cranes_3'
user_name: 'Ahmedgamal'
date: '2025-12-06'
---

# Product Requirements Document - cranes_3

**Author:** Ahmedgamal
**Date:** 2025-12-06

## Executive Summary

**Cranes_3** is a specialized "ERP-lite" platform designed to digitize and automate the core operations of crane rental businesses. By centralizing the "Time Sheet" as the single source of truth, it eliminates the chaos of paper tracking and manual calculation. The system automatically propagates daily operational data into financial outcomes—calculating complex driver wages (including loans and overtime), generating professional client invoices, and tracking sub-renting commissions in real-time. It transforms a fragmented, error-prone manual process into a streamlined, digital workflow tailored specifically for the crane industry.

### What Makes This Special

Unlike generic invoicing tools or heavy enterprise ERPs, **Cranes_3** is built around the specific, non-standard logic of the crane rental niche:
*   **Variable Day-Rate Logic:** Native handling of 8, 9, and 12-hour shift pricing models.
*   **Commission Arbitrage:** Dedicated tracking for "Sub-rented" equipment that calculates profit based on the delta between Owner Cost and Client Price.
*   **Integrated Driver Financials:** A seamless link between operational hours, overtime, and loan deductions, treating the driver's wallet as a core system entity.

## Project Classification

**Technical Type:** saas_b2b
**Domain:** Business Operations/ERP-lite
**Complexity:** medium

This project is classified as a B2B SaaS application focused on operational efficiency. While it does not require high-risk regulatory compliance (like FinTech or HealthTech), it demands high calculation accuracy and data integrity characteristic of ERP systems.

## Success Criteria

### User Success
*   **Administrative Freedom:** The Business Owner reduces weekly paperwork from hours to minutes.
*   **Financial Clarity:** Owner has instant, 100% accurate visibility into driver balances and fleet profit.
*   **Professional Image:** Clients receive standardized, digital invoices instead of handwritten notes.

### Business Success
*   **Revenue Assurance:** 100% of billable hours are captured and invoiced.
*   **Cost Control:** Zero overpayment of driver wages due to missed loan deductions.
*   **Operational Scalability:** The system can handle 2x fleet growth without increasing administrative time.

### Technical Success
*   **Calculation Integrity:** 100% accuracy in split-shift and commission calculations.
*   **Performance:** PDF generation < 5 seconds.
*   **Reliability:** Zero data loss of entered time sheets.

### Measurable Outcomes
*   **Outcome 1:** Generate a monthly client invoice in under 30 seconds.
*   **Outcome 2:** Eliminate manual "end-of-month" wage reconciliation for drivers.

## Product Scope

### MVP - Minimum Viable Product
The initial release focuses on the "Single Source of Truth" workflow for the Owner:
1.  **Core Data Management:** CRUD operations for Drivers, Cranes, and Clients.
2.  **Digital Time Sheet:** A unified entry form for Date, Driver, Crane, Client, and Hours.
3.  **The Logic Engine:**
    *   Automatic Day Rate calculation (8/9/12-hour logic).
    *   Driver Wage calculation (Base + Overtime).
    *   Commission Calculation (Cost vs. Price).
4.  **Financial Management:**
    *   Driver Account Balance tracking (Wages - Loans).
    *   Simple Loan recording interface.
5.  **Reporting:**
    *   One-click PDF Invoice generation for Clients.
    *   Monthly Wage Sheet generation for Drivers.

### Growth Features (Post-MVP)
*   **Driver Self-Service:** Limited login for drivers to view their own hours/balance.
*   **Expense Tracking:** Tracking fuel and maintenance costs per crane.
*   **Dashboard Analytics:** Visual charts for utilization and profit trends.
*   **WhatsApp Integration:** Sending PDFs directly via WhatsApp API.

### Vision (Future)
To become the "Operating System" for crane rental SMEs, potentially expanding to marketplace features for sub-renting between different companies.

## User Journeys

### Journey 1: The "Friday Night" Reconciliation (Core Workflow)
**Persona:** The Owner
**Scenario:** It's Friday evening. The owner has a stack of loose paper notes and WhatsApp messages from 5 different drivers detailing their week's work. Usually, this triggers a 2-hour headache of manual calculation and cross-checking.
**Action:** He logs into **Cranes_3**. He opens the "Time Sheet" form. He selects `Driver: Mahmoud` -> `Crane: Liebherr 100` -> `Client: Orascom`. He types "08:00" to "20:00".
**System Response:** The system instantly flags this as "12 Hours" (Day Rate + Overtime) and calculates the wage. He clicks "Save" and moves to the next slip.
**Resolution:** In 15 minutes, all slips are entered. He clicks "Generate Invoices," downloads the PDFs, and sends them via WhatsApp to his clients. He closes his laptop, stress-free.

### Journey 2: The "Sub-Rent" Commission Check (Unique Value)
**Persona:** The Owner
**Scenario:** He sub-rented a crane from a partner to fulfill a contract for a major client. He's worried the partner's daily rate is eating into his margin.
**Action:** He opens the "Commission Report". He filters by "Sub-Rented Equipment".
**System Response:** The dashboard shows a clear breakdown: "Cost from Partner: 5000 EGP" vs "Price to Client: 6000 EGP". Net Commission: 1000 EGP/day.
**Resolution:** He sees that the deal is profitable and decides to extend the sub-rental for another week, confident in the numbers.

### Journey 3: The Driver Loan Request (Financial Control)
**Persona:** The Owner
**Scenario:** Driver "Ahmed" asks for an advance (1000 EGP) for a family emergency. In the past, the owner would write this in a notebook and often forget to deduct it later.
**Action:** He opens **Cranes_3** on his phone, goes to "Drivers" -> "Ahmed" -> "Loans". He enters "1000 EGP - Emergency".
**System Response:** The system records the transaction and updates Ahmed's "Current Balance".
**Resolution:** At the end of the month, when generating Ahmed's wage slip, the system *automatically* lists "Less: Loan Repayment (1000 EGP)" and calculates the final payout. No awkward conversations, no lost money.

### Journey Requirements Summary
These journeys reveal requirements for:
*   **Fast Data Entry:** Keyboard-friendly forms for rapid timesheet input.
*   **Automatic Logic:** Instant calculation of overtime and day-rates upon entry.
*   **Commission Analytics:** Visible "Cost vs. Revenue" fields for sub-rented assets.
*   **Driver Ledger:** A persistence balance tracking system for every driver (Wages + Overtime - Loans).
*   **PDF Generation:** Instant creation of client-facing invoices and internal wage slips.

## Functional Requirements

### Core Data & Forms
*   **Driver Profile:** Name, Base Salary (optional), Current Balance (calculated).
*   **Crane Profile:** Name, Day Rate (8hr), Day Rate (9hr), Day Rate (12hr), Is Sub-rented? (checkbox).
*   **Client Profile:** Name, Address, Contact Info.
*   **Time Sheet Form:** Date (calendar), Driver (dropdown), Crane (dropdown), Client (dropdown), Start Time, End Time, Notes (optional).

### The "Magic" - Calculations & Logic
*   **Hours Calculation:** `(End - Start) = Total Hours`. If > 8, calculate Overtime.
*   **Day Rate Logic:** Use the correct rate based on total hours (8/9/12).
*   **Driver Wage:** `(Standard Hours * Hourly Rate) + (Overtime Hours * 1.5x Rate)`.
*   **Commission:** If crane is "Sub-rented": `Client Price - Owner Cost = Commission`.
*   **Driver Balance:** `Previous Balance + New Wage - New Loans`.

### Financials & Outputs
*   **Loan Form:** Amount, Date, Description.
*   **Invoice PDF:** Client details, list of jobs (date, crane, hours, rate), total.
*   **Wage Sheet PDF:** Driver details, list of jobs, total wage, list of loans, final payout.



