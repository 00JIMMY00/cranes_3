# Remove Crane Hourly Rates

## Goal
Remove the fixed 8, 9, and 12-hour rate fields from the Crane configuration.

## Context
The current system stores fixed hourly rates (8h, 9h, 12h) directly on the `Crane` model. However, pricing is actually determined by the location and the client, not just the crane itself. Therefore, these fields are misleading and unnecessary on the Crane model.

## Scope
- **Backend**: `Crane` model in `backend/cranes/models.py`.
- **Frontend**: `crane_form.html` template.
- **Database**: Migration to remove fields.

## Risks
- Any existing calculations relying on `crane.rate_Xh` will break. (Need to verify if any exist).
- Data in these fields will be lost. (Acceptable as per user request).
