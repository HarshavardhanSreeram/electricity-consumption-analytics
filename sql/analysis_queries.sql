-- ============================================================
-- Electricity Consumption & Billing Analytics (Synthetic Data, 2025)
-- Database: SQLite (electricity_analytics.db)
-- Tables:   customers(customer_id, customer_name, city, connection_type)
--           consumption(customer_id, billing_month, units_consumed,
--                       rate_per_unit, total_bill, payment_status)
-- ============================================================


-- 1. Total consumption
-- Question: How many units were consumed in total across 2025?
SELECT
    SUM(units_consumed) AS total_units_consumed
FROM consumption;


-- 2. City-wise consumption and billing
-- Question: Which cities consume and are billed the most?
SELECT
    c.city,
    SUM(co.units_consumed) AS total_units,
    ROUND(SUM(co.total_bill), 2) AS total_billing
FROM customers c
JOIN consumption co
    ON c.customer_id = co.customer_id
GROUP BY c.city
ORDER BY total_units DESC;


-- 3. Monthly trend
-- Question: How do consumption and billing change month by month?
SELECT
    billing_month,
    SUM(units_consumed) AS monthly_units,
    ROUND(SUM(total_bill), 2) AS monthly_billing
FROM consumption
GROUP BY billing_month
ORDER BY billing_month;


-- 4. Payment analysis
-- Question: How many bills and how much money sit in each payment status?
SELECT
    payment_status,
    COUNT(*) AS number_of_bills,
    ROUND(SUM(total_bill), 2) AS total_amount
FROM consumption
GROUP BY payment_status;


-- 5. Collection efficiency and outstanding amount (CASE WHEN)
-- Question: What share of billed money was collected, and how much is outstanding?
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


-- 6. Top 10 customers by consumption
-- Question: Which customers use and are billed the most?
SELECT
    c.customer_id,
    c.customer_name,
    c.city,
    SUM(co.units_consumed) AS total_units,
    ROUND(SUM(co.total_bill), 2) AS total_billing
FROM customers c
JOIN consumption co
    ON c.customer_id = co.customer_id
GROUP BY
    c.customer_id,
    c.customer_name,
    c.city
ORDER BY total_units DESC
LIMIT 10;


-- 7. Monthly consumption ranking (window function: RANK)
-- Question: Which months have the highest and lowest consumption?
SELECT
    billing_month,
    SUM(units_consumed) AS monthly_units,
    RANK() OVER (
        ORDER BY SUM(units_consumed) DESC
    ) AS consumption_rank
FROM consumption
GROUP BY billing_month;


-- 8. City contribution percentage (CTE + window function: SUM OVER)
-- Question: What percentage of total consumption does each city contribute?
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


-- 9. Connection type analysis
-- Question: How do customer count, consumption and billing differ by connection type?
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


-- 10. Average consumption per customer per month, by connection type
-- Question: On average, how much does one customer in each connection type use per month?
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
