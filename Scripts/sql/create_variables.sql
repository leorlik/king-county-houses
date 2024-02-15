CREATE TABLE house_variables AS SELECT *, CASE
		WHEN [view] < 3 then "bad"
		ELSE "good"
	  END AS better_view,
	  CASE
		WHEN yr_renovated > 0 then 1
		ELSE 0
	  END AS renewed,
	  CEIL(bathrooms) as ceil_bathrooms,
	  CEIL(floors) as ceil_floors,
	  CASE
		WHEN sqft_basement > 0 then 1
		ELSE 0
	  END AS has_basement,
	  CEIL(bathrooms)/CEIL(floors) as bathrooms_per_floor,
	  bedrooms/CEIL(floors) as bedrooms_per_floor,
	  sqft_above/floors as sqft_per_floor,
	  (CEIL(sqft_above/floors)/sqft_lot) * 100 as percentage_lot_used,
	  100 - (CEIL(sqft_above/floors)/sqft_lot) * 100 as percentage_lot_free,
	  (sqft_basement/sqft_living) * 100 as percentage_basement,
	  CASE 
		WHEN sqft_living > sqft_living15 then 1
		ELSE 0
	  END as bigger_house_than_neighborhood,
	  CASE 
		WHEN sqft_lot > sqft_lot15 then 1
		ELSE 0
	  END AS bigger_lot_than_neighborhood,
	  LOG(sqft_living) as log_living,
	  LOG(sqft_above) as log_above,
	  LOG(sqft_lot) as log_lot,
	  LOG(sqft_living15) as log_living15,
	  LOG(sqft_lot15) as log_lot15,
	  LOG(sqft_basement) as log_basement,
	  NTILE(4) OVER (ORDER BY [long]) AS long_quartile,
	  NTILE(4) OVER (ORDER BY lat) AS lat_quartile
	FROM house_table;

CREATE TABLE sales_variables AS
	SELECT *,
       		CASE
           		WHEN (CAST(strftime('%m', sales_date) AS INTEGER) < 3) OR (CAST(strftime('%m', sales_date) AS INTEGER) == 3 AND CAST(strftime('%d', sales_date) AS INTEGER) <= 19) OR (CAST(strftime('%m', sales_date) AS INTEGER) == 12 AND CAST(strftime('%d', sales_date) AS INTEGER) >= 21) THEN 'winter'
           		WHEN (CAST(strftime('%m', sales_date) AS INTEGER) < 6) OR (CAST(strftime('%m', sales_date) AS INTEGER) == 6 AND CAST(strftime('%d', sales_date) AS INTEGER) <= 21) THEN 'spring'
           		WHEN (CAST(strftime('%m', sales_date) AS INTEGER) < 9) OR (CAST(strftime('%m', sales_date) AS INTEGER) == 9 AND CAST(strftime('%d', sales_date) AS INTEGER) <= 23) THEN 'summer'
           		ELSE 'autumn'
       		END AS season,
		strftime('%d', sales_date) AS day,
           	strftime('%m', sales_date) AS month
	FROM sales_table;
