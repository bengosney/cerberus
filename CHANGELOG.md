## Unreleased

### Feat

- **invoice**: form to invoice uninvoiced charges
- **charges**: queryset with some helpers for charges
- **fields**: grouped multiple model choice field
- **invoice**: invoice actions don't update the url as you can't really go back anyway
- **dashboard**: remove the time-frame label, it seamed redundant
- **htmx**: add a loading pulse animation
- **completable-bookings**: set empty text
- **CheckboxTable**: add empty text
- **booking**: create a completeable booking widget with selectable timeframe
- **charges**: chargeable bookings form view can now take a date
- **css**: add another grid template
- **bookings**: complete bookings form
- **CheckboxTable**: support for overriding column names
- **CheckboxTable**: simple join if the last item is iterable
- **bookings**: add upcoming and past headings for the booking list
- **bookings**: enquiries go stright to confirmed
- **bookings**: add icons and sort orders to the transition actions
- **bookings**: merge the customer upcoming and previous booking lists
- **icon**: add a calendar plus icon to booking fab
- **booking**: Update list on invoice actions
- **bookings**: allow any confirmed booking and prelim bookings in the past to be completed
- **bookings**: add a past bookings list to customer page
- **deps**: update the decencies

### Fix

- **checkbox-table**: don't join string values
- **checkbox-table**: ensure we set the column titles
- **checkbox-table**: don't join string values
- **checkbox-table**: ensure we set the column titles
- **completable-booking**: today filter now starts at the begining of the day
- **completable-booking**: change this month to 30 days
- **completable-booking**: this week starts on monday
- **CheckboxTable**: remove mutable default arg
- **urls**: add trailing slash for completeable urls
- **css**: remove overflow styling around tables
- rename invalid module name

### Refactor

- **UninvoicedCharges**: rename the UninvoicedChargesForm to better reflect its use
