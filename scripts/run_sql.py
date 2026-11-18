
import sqlite3
import pandas as pd

connection = sqlite3.connect("electricity_analytics.db")

queries = {
    "Total Consumption": """
        SELECT SUM(units_consumed) AS total_units
        FROM consumption;
    """,

    "City-wise Consumption": """
        SELECT c.city,
               SUM(co.units_consumed) AS total_units
        FROM customers c
        JOIN consumption co
        ON c.customer_id = co.customer_id
        GROUP BY c.city
        ORDER BY total_units DESC;
    """,

    "Payment Analysis": """
        SELECT payment_status,
               COUNT(*) AS number_of_bills,
               ROUND(SUM(total_bill), 2) AS total_amount
        FROM consumption
        GROUP BY payment_status;
    """,

    "Collection Efficiency" : """
        SELECT
            ROUND(
                SUM(CASE
                    WHEN payment_status = 'Paid'
                    THEN total_bill ELSE 0
                END) * 100.0 / SUM(total_bill),
                2
            ) AS collection_percentage,

            ROUND(
                SUM(CASE
                    WHEN payment_status IN ('Pending', 'Overdue')
                    THEN total_bill ELSE 0
                END),
                2
            ) AS outstanding_amount

        FROM consumption;
    """,

    "Top 5 Customers": """
        SELECT
            c.customer_id,
            c.city,
            SUM(co.units_consumed) AS total_units
        FROM customers c
        JOIN consumption co
            ON c.customer_id = co.customer_id
        GROUP BY c.customer_id, c.city
        ORDER BY total_units DESC
        LIMIT 5;
    """,

    "Monthly Consumption Ranking": """
        SELECT
            billing_month,
            SUM(units_consumed) AS monthly_units,
            RANK() OVER (
                ORDER BY SUM(units_consumed) DESC
            ) AS consumption_rank
        FROM consumption
        GROUP BY billing_month;
    """,

    "City Contribution Percentage": """
        WITH city_usage AS (
            SELECT
                c.city,
                SUM(co.units_consumed) AS total_units
            FROM customers c
            JOIN consumption co
                ON c.customer_id = co.customer_id
            GROUP BY c.city
        )
        SELECT
            city,
            total_units,
            ROUND(
                total_units * 100.0 /
                SUM(total_units) OVER (),
                2
            ) AS contribution_percentage
        FROM city_usage
        ORDER BY total_units DESC;
    """,


    "Connection Type Analysis": """
        SELECT
            c.connection_type,
            COUNT(DISTINCT c.customer_id) AS total_customers,
            SUM(co.units_consumed) AS total_units,
            ROUND(AVG(co.units_consumed), 2) AS avg_monthly_units,
            ROUND(SUM(co.total_bill), 2) AS total_billing
        FROM customers c
        JOIN consumption co
            ON c.customer_id = co.customer_id
        GROUP BY c.connection_type
        ORDER BY total_units DESC;
    """,


    "Average Consumption Per Customer Type": """
        SELECT
            c.connection_type,
            COUNT(DISTINCT c.customer_id) AS customers,
            ROUND(
                SUM(co.units_consumed) * 1.0 /
                COUNT(DISTINCT c.customer_id) / 12,
                2
            ) AS avg_units_per_customer_month
        FROM customers c
        JOIN consumption co
            ON c.customer_id = co.customer_id
        GROUP BY c.connection_type
        ORDER BY avg_units_per_customer_month DESC;
    """




}

for title, query in queries.items():
    print("\n==========", title, "==========")
    result = pd.read_sql_query(query, connection)
    print(result.to_string(index=False))

connection.close()


