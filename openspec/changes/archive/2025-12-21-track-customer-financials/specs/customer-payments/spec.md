# Spec: Customer Payments

## ADDED Requirements

### Requirement: Record Payments
The system MUST allow recording payments from customers with a specified method (Cash, Bank Transfer, Cheque).

#### Scenario: Recording a cash payment
Given a customer "Acme Corp" with an outstanding balance of 1000
When I record a payment of 500 with method "Cash"
Then the payment should be saved in the history
And the customer's outstanding balance should become 500

### Requirement: Support Deferred Payments (Partial Payments)
The system MUST support partial payments, leaving the remaining amount as an outstanding balance.

#### Scenario: Partial payment
Given a customer "Acme Corp" with a total revenue/debt of 5000
When I record a payment of 2000
Then the "Outstanding Balance" should display 3000

### Requirement: Track Payment Method
The system MUST record the method of payment for each transaction.

#### Scenario: Payment methods
Given I am recording a payment
When I select the payment method
Then I should be able to choose between "Cash", "Bank Transfer", and "Cheque"
