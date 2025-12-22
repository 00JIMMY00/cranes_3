# Tasks

- [x] Create migration to add `driver_count` to `MonthlyTimeSheet` and `driver` to `DailyEntry` <!-- id: 0 -->
- [x] Create migration to remove `unique_together` constraint from `DailyEntry` <!-- id: 1 -->
- [x] Update `MonthlyTimeSheet` model logic (e.g. `calculate_totals`) to handle per-entry drivers if needed (wage calculation might differ per driver) <!-- id: 2 -->
- [x] Refactor `monthly_sheet_save_all` view to parse inputs using `entry_{id}_field` format instead of `entry_{day}_field` <!-- id: 3 -->
- [x] Update `monthly_detail.html` template to use `entry.id` for input names <!-- id: 4 -->
- [x] Update `monthly_detail.html` to show "Driver" column when `driver_count > 1` <!-- id: 5 -->
- [x] Add JavaScript to `monthly_detail.html` to allow adding/removing rows for a specific day (splitting shifts) <!-- id: 6 -->
- [x] Update `monthly_sheet_create` and `edit` forms to include `driver_count` number input <!-- id: 7 -->
- [x] Verify wage calculations sum up correctly across multiple drivers <!-- id: 8 -->
