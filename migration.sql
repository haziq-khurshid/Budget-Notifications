CREATE TABLE t_notifications (
    a_id SERIAL PRIMARY KEY,
    a_shop_id INT NOT NULL,
    a_notification_type INT NOT NULL,
    a_notification_date DATE NOT NULL,
    FOREIGN KEY (a_shop_id) REFERENCES t_shops (a_id)
);


INSERT INTO t_budgets (a_shop_id, a_month, a_budget_amount, a_amount_spent)
VALUES
    (1, '2023-10-01', 1000.00, 1100.00),
    (2, '2023-10-01', 800.00, 750.00),
    (3, '2023-10-01', 1200.00, 900.00),
    (4, '2023-10-01', 750.00, 600.00),
    (5, '2023-10-01', 1500.00, 1450.00),
    (6, '2023-10-01', 600.00, 250.00),
    (7, '2023-10-01', 900.00, 800.00),
    (8, '2023-10-01', 1100.00, 900.00);
