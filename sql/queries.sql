-- ============================================================
-- Restaurant Operations Data Pipeline
-- Portfolio SQL Queries
-- ============================================================


-- 1. Rebuild enriched sales data using a SQL JOIN
SELECT
    sr.sale_id,
    sr.date,
    sr.product_id,
    p.product_name,
    p.category,
    sr.quantity,
    p.unit_price,
    p.unit_cost,
    sr.quantity * p.unit_price AS revenue,
    sr.quantity * p.unit_cost AS food_cost,
    sr.quantity * (p.unit_price - p.unit_cost) AS gross_profit
FROM sales_raw AS sr
JOIN products AS p
    ON sr.product_id = p.product_id;


-- 2. Overall business KPIs
SELECT
    COUNT(*) AS sales_records,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(food_cost), 2) AS total_food_cost,
    ROUND(SUM(gross_profit), 2) AS total_gross_profit,
    ROUND(
        SUM(food_cost) / SUM(revenue) * 100,
        2
    ) AS food_cost_pct,
    ROUND(
        SUM(gross_profit) / SUM(revenue) * 100,
        2
    ) AS gross_margin_pct
FROM sales;


-- 3. Monthly performance
SELECT
    strftime('%Y-%m', date) AS month,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(food_cost), 2) AS food_cost,
    ROUND(SUM(gross_profit), 2) AS gross_profit,
    ROUND(
        SUM(food_cost) / SUM(revenue) * 100,
        2
    ) AS food_cost_pct
FROM sales
GROUP BY month
ORDER BY month;


-- 4. Performance by category
SELECT
    category,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(food_cost), 2) AS food_cost,
    ROUND(SUM(gross_profit), 2) AS gross_profit,
    ROUND(
        SUM(gross_profit) / SUM(revenue) * 100,
        2
    ) AS gross_margin_pct
FROM sales
GROUP BY category
ORDER BY revenue DESC;


-- 5. Top products by revenue
SELECT
    product_name,
    category,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(gross_profit), 2) AS gross_profit
FROM sales
GROUP BY product_name, category
ORDER BY revenue DESC
LIMIT 10;


-- 6. Best-selling products by quantity
SELECT
    product_name,
    category,
    SUM(quantity) AS units_sold
FROM sales
GROUP BY product_name, category
ORDER BY units_sold DESC
LIMIT 10;


-- 7. Product profitability
SELECT
    product_name,
    category,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(food_cost), 2) AS food_cost,
    ROUND(SUM(gross_profit), 2) AS gross_profit,
    ROUND(
        SUM(gross_profit) / SUM(revenue) * 100,
        2
    ) AS gross_margin_pct
FROM sales
GROUP BY product_name, category
ORDER BY gross_profit DESC;


-- 8. Daily sales trend
SELECT
    date,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(gross_profit), 2) AS gross_profit
FROM sales
GROUP BY date
ORDER BY date;


-- 9. Revenue by day of week
SELECT
    CASE strftime('%w', date)
        WHEN '0' THEN 'Sunday'
        WHEN '1' THEN 'Monday'
        WHEN '2' THEN 'Tuesday'
        WHEN '3' THEN 'Wednesday'
        WHEN '4' THEN 'Thursday'
        WHEN '5' THEN 'Friday'
        WHEN '6' THEN 'Saturday'
    END AS day_of_week,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(gross_profit), 2) AS gross_profit
FROM sales
GROUP BY strftime('%w', date)
ORDER BY revenue DESC;


-- 10. Revenue contribution by product
SELECT
    product_name,
    ROUND(SUM(revenue), 2) AS product_revenue,
    ROUND(
        SUM(revenue) * 100.0 /
        (SELECT SUM(revenue) FROM sales),
        2
    ) AS revenue_share_pct
FROM sales
GROUP BY product_name
ORDER BY product_revenue DESC;


-- 11. Average revenue per sales record
SELECT
    ROUND(AVG(revenue), 2) AS avg_revenue_per_sale,
    ROUND(AVG(quantity), 2) AS avg_units_per_sale
FROM sales;


-- 12. Data quality check
SELECT
    COUNT(*) AS invalid_records
FROM sales
WHERE
    product_id IS NULL
    OR product_name IS NULL
    OR quantity <= 0
    OR unit_price < 0
    OR unit_cost < 0
    OR revenue < 0
    OR gross_profit < 0;