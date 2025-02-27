-- TODO: Esta consulta devolverá una tabla con las diferencias entre los tiempos 
-- reales y estimados de entrega por mes y año. Tendrá varias columnas: 
-- month_no, con los números de mes del 01 al 12; month, con las primeras 3 letras 
-- de cada mes (ej. Ene, Feb); Year2016_real_time, con el tiempo promedio de 
-- entrega real por mes de 2016 (NaN si no existe); Year2017_real_time, con el 
-- tiempo promedio de entrega real por mes de 2017 (NaN si no existe); 
-- Year2018_real_time, con el tiempo promedio de entrega real por mes de 2018 
-- (NaN si no existe); Year2016_estimated_time, con el tiempo promedio estimado 
-- de entrega por mes de 2016 (NaN si no existe); Year2017_estimated_time, con 
-- el tiempo promedio estimado de entrega por mes de 2017 (NaN si no existe); y 
-- Year2018_estimated_time, con el tiempo promedio estimado de entrega por mes 
-- de 2018 (NaN si no existe).
-- PISTAS:
-- 1. Puedes usar la función julianday para convertir una fecha a un número.
-- 2. order_status == 'delivered' AND order_delivered_customer_date IS NOT NULL
-- 3. Considera tomar order_id distintos.

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
      WHEN '01' THEN 'Ene'
      WHEN '02' THEN 'Feb'
      WHEN '03' THEN 'Mar'
      WHEN '04' THEN 'Abr'
      WHEN '05' THEN 'May'
      WHEN '06' THEN 'Jun'
      WHEN '07' THEN 'Jul'
      WHEN '08' THEN 'Ago'
      WHEN '09' THEN 'Sep'
      WHEN '10' THEN 'Oct'
      WHEN '11' THEN 'Nov'
      WHEN '12' THEN 'Dic'
    END as month
  FROM months
),
DeliveryTimes AS (
  SELECT 
    strftime('%m', order_purchase_timestamp) as month_no,
    strftime('%Y', order_purchase_timestamp) as year,
    ROUND(AVG(JULIANDAY(order_delivered_customer_date) - JULIANDAY(order_purchase_timestamp)), 2) as real_time,
    ROUND(AVG(JULIANDAY(order_estimated_delivery_date) - JULIANDAY(order_purchase_timestamp)), 2) as estimated_time
  FROM 
    olist_orders
  WHERE 
    order_status = 'delivered'
    AND order_delivered_customer_date IS NOT NULL
  GROUP BY 
    strftime('%Y-%m', order_purchase_timestamp)
)
SELECT 
  m.month_no,
  m.month,
  COALESCE(SUM(CASE WHEN d.year = '2016' THEN d.real_time END), NULL) as Year2016_real_time,
  COALESCE(SUM(CASE WHEN d.year = '2017' THEN d.real_time END), NULL) as Year2017_real_time,
  COALESCE(SUM(CASE WHEN d.year = '2018' THEN d.real_time END), NULL) as Year2018_real_time,
  COALESCE(SUM(CASE WHEN d.year = '2016' THEN d.estimated_time END), NULL) as Year2016_estimated_time,
  COALESCE(SUM(CASE WHEN d.year = '2017' THEN d.estimated_time END), NULL) as Year2017_estimated_time,
  COALESCE(SUM(CASE WHEN d.year = '2018' THEN d.estimated_time END), NULL) as Year2018_estimated_time
FROM 
  MonthNames m
  LEFT JOIN DeliveryTimes d ON m.month_no = d.month_no
GROUP BY 
  m.month_no
ORDER BY 
  m.month_no;
