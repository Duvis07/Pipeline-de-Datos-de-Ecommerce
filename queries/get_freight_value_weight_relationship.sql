-- TODO: Esta consulta devolverá una tabla con la relación entre el peso total
-- del pedido y el valor del flete. Tendrá dos columnas: total_weight y 
-- freight_value. La primera contendrá el peso total de cada pedido y la segunda
-- el valor del flete.
-- PISTA: Todos los pedidos deben tener un estado 'delivered' y la fecha real de
-- entrega no debe ser nula.

SELECT 
    ROUND(SUM(p.product_weight_g), 2) as total_weight,
    ROUND(SUM(oi.freight_value), 2) as freight_value
FROM 
    olist_orders o
    JOIN olist_order_items oi ON o.order_id = oi.order_id
    JOIN olist_products p ON oi.product_id = p.product_id
WHERE 
    o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL
GROUP BY 
    o.order_id;
