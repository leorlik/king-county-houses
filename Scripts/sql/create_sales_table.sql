CREATE TABLE sales_table (
	id VARCHAR(12),
	sales_date TIMESTAMP,
	price DECIMAL (16, 4),	
	PRIMARY KEY(id, sales_date)
)
