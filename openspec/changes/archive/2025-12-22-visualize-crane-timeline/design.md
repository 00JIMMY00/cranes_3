# Design: Visualize Crane Timeline

## Architecture
- **Backend**: Update `crane_detail` view in `backend/cranes/views.py` to serialize assignment data (start_date, end_date, client_name, status) into a JSON format that can be consumed by the frontend.
- **Frontend**:
    - Add a container for the timeline in `backend/templates/cranes/crane_detail.html` above the Assignment History tables.
    - Include `vis-timeline` library (via CDN or static file).
    - Write JavaScript to initialize the timeline with the data provided by the backend.

## Data Structure
The backend will pass a list of objects:
```json
[
  {
    "id": 1,
    "content": "Client Name",
    "start": "2023-10-01",
    "end": "2023-10-15",
    "className": "status-past"
  },
  ...
]
```

## UI/UX
- **Placement**: Top of the page, below the header and above the "Assignment History" section.
- **Styling**:
    - Use the project's existing color palette (Bootstrap colors: success, info, secondary).
    - "Past" assignments: Secondary (Gray)
    - "Present" assignments: Success (Green)
    - "Future" assignments: Info (Blue)
- **Interactivity**: Users can scroll horizontally to see past/future assignments.
