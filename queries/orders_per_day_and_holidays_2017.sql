SELECT 
    strftime('%s', DATE(order_purchase_timestamp)) * 1000 as date,
    COUNT(*) as order_count
FROM 
    olist_orders
WHERE 
    strftime('%Y', order_purchase_timestamp) = '2017'
GROUP BY 
    DATE(order_purchase_timestamp)
ORDER BY 
    date;
