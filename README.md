## Project Report – Part 1: Design Decisions

This section outlines key design decisions made while building the Selwyn Ticketing web application.

### 1. Template Inheritance Using `base.html`
To avoid repetitive code, I used template inheritance via `base.html`, which contains the navigation bar and header. All other templates extend this base file using `{% extends 'base.html' %}`. This ensures consistency and reduces maintenance effort.

### 2. Navigation Bar Design
The navigation bar appears on all pages and provides links to the Home, Events, Customer Search, and Add Customer pages. This improves usability and allows users to move easily between sections.

### 3. GET vs POST Methods
I chose GET for displaying data (like event lists and customer ticket summaries) and POST for form submissions (e.g., buying tickets or adding customers). This follows standard web development practice and improves user experience by avoiding unintended form resubmissions.

### 4. Page Layout with Bootstrap
I used Bootstrap grid layout for consistent and responsive formatting. For instance, forms are styled with `form-group`, `btn`, and `form-control` classes to ensure a professional look without custom CSS.

### 5. Buying Tickets via Dropdown Selection
In the ticket purchase form, I used dropdown menus to allow users to select both the event and the customer. This minimises errors and ensures only valid options are shown (e.g., only future events with available tickets).

### 6. Sorting and Filtering in SQL
To display customers alphabetically by last name (and by youngest first when the same last name occurs), I used `ORDER BY` clauses in the SQL query. This sorting was done in the database layer to reduce complexity in the Flask view logic.

### 7. Age Restriction Handling in Python
Instead of relying on client-side JavaScript, I implemented age restriction validation in the backend using Python. This ensures data integrity and complies with COMP636 constraints (no JS except provided script).

### 8. Future Events Page Logic
Only future events with remaining tickets are shown. I added filtering conditions in SQL to check both the event date and ticket availability (`event_date > CURDATE()` and `capacity > tickets_sold`).

### 9. Ticket Summary Page Aggregation
To display total tickets per customer across all events, I used SQL aggregation (`SUM`) and grouped by event. This allowed for clear reporting and reduced redundant calculations in Python.

---

*Note: All routes use parameterised queries with `%s` to prevent SQL injection and comply with best practice.*
