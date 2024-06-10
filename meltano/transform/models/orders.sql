SELECT
	ord.order_id,
	ord.customer_id,
	ord.employee_id,
	ord.order_date,
	ord.required_date,
	ord.shipped_date,
	ord.ship_via,
	ord.ship_name,
	ord.ship_address,
	ord.ship_city,
	ord.ship_region,
	ord.ship_postal_code,
	ord.ship_country,
	details.product_id,
	details.unit_price,
	details.quantity,
	details.discount
FROM
	raw.orders ord
LEFT JOIN
	raw.order_details details
ON
	ord.order_id = details.order_id