import psycopg2
from datetime import date

# Database connection parameters, Use details of the DB you have set up
db_params = {
    "database": "postgres",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": "5432",
}

try:
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    current_date = date.today()
    first_day_of_the_month = date(current_date.year, current_date.month, 1)

    query = """
        SELECT s.a_id, s.a_name, b.a_budget_amount, b.a_amount_spent
        FROM t_shops s
        INNER JOIN t_budgets b ON s.a_id = b.a_shop_id
        WHERE b.a_month = %s
    """

    cursor.execute(query, (first_day_of_the_month,))
    shop_data = cursor.fetchall()

    for shop in shop_data:
        shop_id, shop_name, budget_amount, amount_spent = shop
        expenditure_percentage = (amount_spent / budget_amount) * 100

        # Check if the expenditure has reached 50% or 100% of the budget
        if expenditure_percentage >= 50 and expenditure_percentage < 100:
            # Check if a notification of this type has already been sent in the current month
            cursor.execute(
                "SELECT a_id FROM t_notifications WHERE a_shop_id = %s AND a_notification_type = 50 AND a_notification_date >= %s",
                (shop_id, first_day_of_the_month),
            )
            existing_notification = cursor.fetchone()
            if not existing_notification:
                print(
                    f"{current_date}: Shop ID {shop_id} ({shop_name}) - Expenditure: {amount_spent}, Budget: {budget_amount}, "
                    f"Expenditure Percentage: {expenditure_percentage:.2f}% - Send notification (50%)"
                )
                # Insert a notification record
                cursor.execute(
                    "INSERT INTO t_notifications (a_shop_id, a_notification_type, a_notification_date) VALUES (%s, %s, %s)",
                    (shop_id, 50, current_date),
                )
                conn.commit()  # Commit the transaction if a notification is inserted
        elif expenditure_percentage >= 100:
            # Check if a notification of this type has already been sent in the current month
            cursor.execute(
                "SELECT a_id FROM t_notifications WHERE a_shop_id = %s AND a_notification_type = 100 AND a_notification_date >= %s",
                (shop_id, first_day_of_the_month),
            )
            existing_notification = cursor.fetchone()
            if not existing_notification:
                print(
                    f"{current_date}: Shop ID {shop_id} ({shop_name}) - Expenditure: {amount_spent}, Budget: {budget_amount}, "
                    f"Expenditure Percentage: {expenditure_percentage:.2f}% - Send notification (100%) and set shop offline"
                )
                # Set the shop offline
                cursor.execute("UPDATE t_shops SET a_online = FALSE WHERE a_id = %s",(shop_id,))
                # Insert a notification record
                cursor.execute(
                    "INSERT INTO t_notifications (a_shop_id, a_notification_type, a_notification_date) VALUES (%s, %s, %s)",
                    (shop_id, 100, current_date),
                )
                conn.commit()  # Commit the transaction if a notification is inserted

except psycopg2.Error as e:
    print(f"Error connecting to the database: {e}")

finally:
    if conn is not None:
        conn.close()
