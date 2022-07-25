select product_name, product_cat ,sales_amount from product_table
join
sales_table on product_id=product_id
join location_table on sales.location_id=location.location_id
join date_table on sls.date=date_table.date
where date> jan1 2022