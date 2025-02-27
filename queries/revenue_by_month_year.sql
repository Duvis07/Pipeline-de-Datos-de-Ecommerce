-- TODO: Esta consulta devolverá una tabla con los ingresos por mes y año.
-- Tendrá varias columnas: month_no, con los números de mes del 01 al 12;
-- month, con las primeras 3 letras de cada mes (ej. Ene, Feb);
-- Year2016, con los ingresos por mes de 2016 (0.00 si no existe);
-- Year2017, con los ingresos por mes de 2017 (0.00 si no existe); y
-- Year2018, con los ingresos por mes de 2018 (0.00 si no existe).

WITH RECURSIVE months(month_no) AS (
  SELECT '01'
  UNION ALL
  SELECT printf('%02d', CAST(month_no AS INTEGER) + 1)
  FROM months
  WHERE CAST(month_no AS INTEGER) < 12
),
MonthNames AS (
  SELECT 
    month_no,
    CASE month_no
      WHEN '01' THEN 'Jan'
      WHEN '02' THEN 'Feb'
      WHEN '03' THEN 'Mar'
      WHEN '04' THEN 'Apr'
      WHEN '05' THEN 'May'
      WHEN '06' THEN 'Jun'
      WHEN '07' THEN 'Jul'
      WHEN '08' THEN 'Aug'
      WHEN '09' THEN 'Sep'
      WHEN '10' THEN 'Oct'
      WHEN '11' THEN 'Nov'
      WHEN '12' THEN 'Dec'
    END as month
  FROM months
),
OrderRevenue AS (
  SELECT 
    strftime('%m', o.order_purchase_timestamp) as month_no,
    strftime('%Y', o.order_purchase_timestamp) as year,
    SUM(oi.price + oi.freight_value) as revenue
  FROM 
    olist_orders o
    JOIN olist_order_items oi ON o.order_id = oi.order_id
  WHERE 
    o.order_status != 'cancelled'
  GROUP BY 
    strftime('%Y-%m', o.order_purchase_timestamp)
)
SELECT 
  m.month_no,
  m.month,
  COALESCE(SUM(CASE WHEN r.year = '2016' THEN r.revenue END), 0.00) as Year2016,
  COALESCE(SUM(CASE WHEN r.year = '2017' THEN r.revenue END), 0.00) as Year2017,
  COALESCE(SUM(CASE WHEN r.year = '2018' THEN r.revenue END), 0.00) as Year2018
FROM 
  MonthNames m
  LEFT JOIN OrderRevenue r ON m.month_no = r.month_no
GROUP BY 
  m.month_no
ORDER BY 
  m.month_no;
