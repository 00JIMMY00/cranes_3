# Tasks

1.  [x] **Migration**: Make `trips`, `daily_total`, `hourly_rate` nullable or set defaults in `DailyEntry` model. *(Kept existing defaults, fields still in DB but hidden from UI)*
2.  [x] **Model Update**: Add `shift_divisor` to `MonthlyTimeSheet`.
3.  [x] **Backend Logic**: Update `calculate_totals` in `MonthlyTimeSheet` to use the new logic.
4.  [x] **Template Update**: Modify `timesheets/monthly_detail.html` table structure.
5.  [x] **Frontend Logic**: Update AJAX handlers in `views.py` and JS in template to support new calculation.
6.  [ ] **Verification**: Test with various shift divisors.
