-- 1. Mostra tutti i dati
SELECT *
FROM sales;

-- 2. Fatturato totale
SELECT
    SUM(revenue) AS total_revenue
FROM sales;

-- 3. Fatturato totale per prodotto
SELECT
    product,
    SUM(revenue) AS total_revenue
FROM sales
GROUP BY product;

-- 4. Quantità totale venduta per prodotto
SELECT
    product,
    SUM(quantity) AS total_quantity
FROM sales
GROUP BY product;

-- 5. Prodotto più venduto
SELECT
    product,
    SUM(quantity) AS total_quantity
FROM sales
GROUP BY product
ORDER BY total_quantity DESC
LIMIT 1;