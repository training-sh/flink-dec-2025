# Basic stream operation

change gks with your initial, as we share cluster

```
CREATE  TABLE gks_dim_customers_kafka (
  customer_id INT  PRIMARY KEY NOT ENFORCED,
  full_name   STRING,
  email       STRING,
  signup_date STRING,
  country     STRING,
  city        STRING,
  segment     STRING
) WITH (
 
  'connector' = 'confluent',
  'scan.startup.mode' = 'earliest-offset',
  'value.format' = 'json-registry'
);
```

check topics and schema registry

```
CREATE  TABLE gks_dim_products_kafka (
  product_id   INT  PRIMARY KEY NOT ENFORCED,
  product_name STRING,
  category     STRING,
  subcategory  STRING,
  brand        STRING,
  unit_price   DECIMAL(10,2),
  active       BOOLEAN
) WITH (
 
  'connector' = 'confluent',
  'scan.startup.mode' = 'earliest-offset',
  'value.format' = 'json-registry'
)
```

```
CREATE  TABLE gks_fact_orders_kafka (
  order_id       INT,
  customer_id    INT,
  order_datetime TIMESTAMP(3),
  order_status   STRING,
  payment_method STRING,
  shipping_fee   DECIMAL(10,2),
  discount_amt   DECIMAL(10,2)
) WITH (
  'connector' = 'confluent',
  'scan.startup.mode' = 'earliest-offset',
  'value.format' = 'json-registry'
)
```

```
CREATE  TABLE gks_fact_order_items_kafka (
  order_item_id INT,
  order_id      INT,
  product_id    INT,
  quantity      INT,
  item_price    DECIMAL(10,2)
) WITH (
  'connector' = 'confluent',
  'scan.startup.mode' = 'earliest-offset',
  'value.format' = 'json-registry'
)
```

Query, without window, will cause state related issue if it is run longer period.

```
CREATE  VIEW gks_v_customer_revenue_kafka AS
SELECT
  c.customer_id,
  c.full_name,
  SUM(i.quantity * i.item_price) AS total_revenue,
  COUNT(DISTINCT o.order_id)     AS total_orders,
  MAX(o.order_datetime)          AS last_order_ts
FROM gks_dim_customers_kafka AS c
JOIN gks_fact_orders_kafka AS o
  ON c.customer_id = o.customer_id
JOIN gks_fact_order_items_kafka AS i
  ON o.order_id = i.order_id
WHERE o.order_status = 'PAID'
GROUP BY c.customer_id, c.full_name
```

Output

```
CREATE   TABLE gks_customer_revenue_kafka_out (
  customer_id   INT  PRIMARY KEY NOT ENFORCED,
  full_name     STRING,
  total_revenue DECIMAL(18, 2),
  total_orders  BIGINT,
  last_order_ts TIMESTAMP(3) 
) WITH (
  'connector' = 'confluent',
  'value.format' = 'json-registry',
  'changelog.mode' = 'upsert'
)
```

```
INSERT INTO gks_customer_revenue_kafka_out
SELECT
  c.customer_id,
  c.full_name,
  CAST(total_revenue AS DECIMAL(18, 2)) AS total_revenue,
  total_orders,
  last_order_ts
FROM gks_v_customer_revenue_kafka AS c
```

```
SELECT * FROM gks_customer_revenue_kafka_out LIMIT 2;
```

