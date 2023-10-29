# Budget Notifications Application

This Python CLI application checks shops' budgets and expenditures, sending notifications when certain thresholds are reached and marking shops as offline when their budget is exhausted. This README provides details on the database system, schema changes, and how to run the application.

## Database System

We have chosen to use **PostgreSQL version 16.0** for this project. PostgreSQL is a powerful, open-source relational database management system.

### Schema Changes

Instead of using the provided `db.sql` file, we have made some schema changes in a separate file named `postgres-db.sql`:

1. Changed the data type of `a_id` in the `t_shops` table to `SERIAL`. In PostgreSQL, we use `SERIAL` to create auto-incrementing columns.

2. Changed the values of `a_online` in the `t_shops` table from `1`/`0` to `True`/`False` to use the Boolean data type.

## Running the Application

To set up the database and schema, follow these steps:

1. Create a PostgreSQL database using the PostgreSQL command-line utility or a GUI tool.

2. Run `postgres-db.sql` to initialize the schema and make the necessary changes.

3. Run `migration.sql` file for the following tasks:
   - Add a new column `a_notification_sent` to the `t_shops` table, which is a boolean indicating whether a notification has been sent.
   - Create a new table `t_notifications` to store notification records.
   - Insert sample data into the `t_budgets` table for testing.

4. Run the Python CLI application to check shops' budgets and send notifications when thresholds are reached. The application performs the following tasks:
   - Connects to the PostgreSQL database using the specified parameters.
   - Retrieves the current date and the first day of the current month.
   - Executes a SQL query to get shops' budgets and expenditures for the current month, joining data from the t_shops and t_budgets tables.
   - Iterates through the retrieved shop data and calculates the expenditure percentage.
   - Checks if the expenditure has reached 50% or 100% of the budget and whether a notification of the same type has already been sent in the current month.
   - If the expenditure is at 50%, it sends a notification (50%) and inserts a corresponding notification record into the t_notifications table.
   - If the expenditure is at 100%, it sends a notification (100%), sets the shop as offline, and updates the a_notification_sent flag in the t_shops table.
   - Commits the transaction if a notification is inserted.

By running the Python application, you can manage shop budgets, send notifications, and update the t_shops table to reflect their online/offline status as needed.
