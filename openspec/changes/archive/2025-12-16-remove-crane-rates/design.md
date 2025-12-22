# Design: Remove Crane Rates

## Problem
The `Crane` model currently couples pricing (rates) with the asset (crane). This is incorrect as pricing is dynamic based on client and location.

## Solution
Remove the following fields from the `Crane` model:
- `rate_8h`
- `rate_9h`
- `rate_12h`

## Impact
- **Database**: Columns dropped.
- **UI**: "Rate Configuration" section removed from Crane form.
- **Logic**: Any logic using `crane.rate_*` must be updated (checked: none found so far, but will verify).
