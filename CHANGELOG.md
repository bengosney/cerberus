## Unreleased

### Refactor

- **deps**: zelot has been renamed to zeal

## v0.2.0 (2024-07-20)

### Feat

- **n+1**: add zealot to catch n+1 querys
- **charge-admin**: display more useful list columns
- **FAB**: add a fab container that makes the fab sticky
- **htmx**: update to htmx v2
- **htmx**: include and enable the plugins
- **htmx**: plugin to remove elements
- **htmx**: plugin to auto-target htmx based on the response
- **invoice**: make the send form work with HTMX
- **invoice**: use the transition action mixin
- **transition**: add a url option
- **bookings**: command to find invalid bookins
- **invoice**: create invoice fab
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

### Fix

- **charges**: don't allow charges to be created that are not assigned to a customer
- **js**: remove console.log
- **invoice**: fix the adding/editing of invoice lines
- **invoice-form**: use the default cursor on the total
- **invoice-form**: move the delete checkbox to the end
- **css**: make the inline gap scale with width
- **invoice**: move the invoice lines below the details
- **invoice-form**: sent to shouldn't be set or edited by a user
- **invoice**: use the inlineformset_factory so new lines are saved correctly
- **htmx**: auto targeting doesn't work with the boosted list sorting
- **htmx**: set the swap mode when setting the target
- **invoice**: list actions should update the list
- **invoice**: don't output the invoicable link when it's a HTMX request
- **invoice**: move the invoicable link to the base list
- **bookings**: incorectly refrenced charges
- **invoice**: add customer and disabled editing once it has been created
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

### Refactor

- **n+1**: move zelot to a normal dep so I can ignore some queries
- **invoice-forms**: shorten the long lines
- **htmx**: remove some now unessasary hx-targets
- **trasitions**: remove explicit url and add meta
- **invoice**: dry up the view logic
- **transitions**: extract the transition actions into a mixin
- **actions**: extract action icons into it's own css file
- **invoice**: move the invoice row into it's own template file
- **UninvoicedCharges**: rename the UninvoicedChargesForm to better reflect its use

### Perf

- **n+1**: prevent some n+1 queries

## v0.1.0 (2024-06-19)

### Feat

- **bookings**: add a past bookings list to customer page
- **deps**: update the decencies

### Fix

- rename invalid module name
