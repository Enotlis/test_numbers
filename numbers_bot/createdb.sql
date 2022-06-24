create table orders(
	number_order bigint primary key,
	price_usd integer NOT NULL,
	price_rub decimal NOT NULL,
	delivery_time date NOT NULL
);