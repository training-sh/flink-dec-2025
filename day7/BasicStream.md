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


```
kafka-console-producer \
  --bootstrap-server <<replace>>.europe-west3.gcp.confluent.cloud:9092 \
  --topic gks_dim_customers_kafka \
  --property "parse.key=true" \
  --property "key.separator=|" \
  --producer.config /secret/ccloud.properties
```

```
1|{"customer_id":1,"full_name":"Vel","email":"vel@example.com","signup_date":"2025-01-10","country":"India","city":"Chennai","segment":"Prime"}
```

```
2|{"customer_id":2,"full_name":"Shiv","email":"shiv@example.com","signup_date":"2025-02-20","country":"India","city":"Bangalore","segment":"Standard"}
```

```
kafka-console-producer \
  --bootstrap-server <<replace>>.europe-west3.gcp.confluent.cloud:9092 \
  --topic gks_dim_products_kafka \
  --property "parse.key=true" \
  --property "key.separator=|" \
  --producer.config /secret/ccloud.properties
```

```
10|{"product_id":10,"product_name":"Noise Cancelling Headphones","category":"Electronics","subcategory":"Audio","brand":"Sony","unit_price":249.99,"active":true}
```

```
20|{"product_id":20,"product_name":"Mechanical Keyboard","category":"Electronics","subcategory":"Accessories","brand":"Logitech","unit_price":129.50,"active":true}
```

```
kafka-console-producer \
  --bootstrap-server <<replace>>.europe-west3.gcp.confluent.cloud:9092 \
  --topic gks_fact_orders_kafka \
  --property "parse.key=true" \
  --property "key.separator=|" \
  --producer.config /secret/ccloud.properties
```

```
101|{"order_id":101,"customer_id":1,"order_datetime":"2025-10-05T14:32:00","order_status":"PAID","payment_method":"CARD","shipping_fee":5.99,"discount_amt":10.00}
```
```
102|{"order_id":102,"customer_id":1,"order_datetime":"2025-10-12T09:15:00","order_status":"PAID","payment_method":"WALLET","shipping_fee":4.99,"discount_amt":5.00}
```
```
103|{"order_id":103,"customer_id":1,"order_datetime":"2025-11-01T18:45:00","order_status":"PAID","payment_method":"CARD","shipping_fee":6.99,"discount_amt":0.00}
```
```
104|{"order_id":104,"customer_id":2,"order_datetime":"2025-10-20T11:22:00","order_status":"PAID","payment_method":"UPI","shipping_fee":4.50,"discount_amt":5.00}
```

```
kafka-console-producer \
  --bootstrap-server <<replace>>.europe-west3.gcp.confluent.cloud:9092 \
  --topic gks_fact_order_items_kafka \
  --property "parse.key=true" \
  --property "key.separator=|" \
  --producer.config /secret/ccloud.properties
```

```
1001|{"order_item_id":1001,"order_id":101,"product_id":10,"quantity":2,"item_price":249.99}
```

```
1002|{"order_item_id":1002,"order_id":102,"product_id":20,"quantity":1,"item_price":129.50}
```

```
1003|{"order_item_id":1003,"order_id":102,"product_id":20,"quantity":1,"item_price":129.50}
```

```
1004|{"order_item_id":1004,"order_id":102,"product_id":20,"quantity":1,"item_price":129.50}
```
```
1005|{"order_item_id":1005,"order_id":103,"product_id":10,"quantity":1,"item_price":249.99}
```

```
1006|{"order_item_id":1006,"order_id":104,"product_id":10,"quantity":1,"item_price":249.99}
```

```
1007|{"order_item_id":1007,"order_id":104,"product_id":20,"quantity":1,"item_price":129.50}
```
```
1008|{"order_item_id":1008,"order_id":104,"product_id":20,"quantity":1,"item_price":100.00}
```
