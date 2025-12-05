


# 1) Dimension topics → COMPACTED

```
docker exec -it kafka-tools bash
```

```
kafka-topics --bootstrap-server broker:9092 \
  --create --topic dim_customers \
  --partitions 3 --replication-factor 1 \
  --config cleanup.policy=compact \
  --config min.cleanable.dirty.ratio=0.2 \
  --config segment.ms=600000
```

```
kafka-topics --bootstrap-server broker:9092 \
  --create --topic dim_products \
  --partitions 3 --replication-factor 1 \
  --config cleanup.policy=compact \
  --config min.cleanable.dirty.ratio=0.1 \
  --config segment.ms=600000
```

# 2) Fact topics → APPEND (normal)

```
kafka-topics --bootstrap-server broker:9092 \
  --create --topic fact_orders \
  --partitions 3 --replication-factor 1
```
```
kafka-topics --bootstrap-server broker:9092 \
  --create --topic fact_order_items \
  --partitions 3 --replication-factor 1
```


# 3) Result

debzium like format

```
kafka-topics --bootstrap-server broker:9092 \
  --create --topic customer_revenue \
  --partitions 3 --replication-factor 1
```

kafka-upsert

```
kafka-topics --bootstrap-server broker:9092 \
  --create --topic customer_revenue_upsert \
  --partitions 3 --replication-factor 1 \
  --config cleanup.policy=compact \
  --config min.cleanable.dirty.ratio=0.1 \
  --config segment.ms=600000
```

Another Tab

```


```
docker exec -it kafka-tools bash
```

```
kafka-console-producer \
  --bootstrap-server broker:9092 \
  --topic dim_customers \
  --property "parse.key=true" \
  --property "key.separator=|"
```

```
1|{"customer_id":1,"full_name":"Vel","email":"vel@example.com","signup_date":"2025-01-10","country":"India","city":"Chennai","segment":"Prime"}
```

```

kafka-console-producer \
--bootstrap-server broker:9092 \
--topic dim_products \
--property "parse.key=true" \
--property "key.separator=|"

```

```
10|{"product_id":10,"product_name":"Noise Cancelling Headphones", "category":"Electronics","subcategory":"Audio",  "brand":"Sony","unit_price":249.99,"active":true}
```

```
20|{"product_id":20,"product_name":"Mechanical Keyboard", "category":"Electronics","subcategory":"Accessories", "brand":"Logitech","unit_price":129.50,"active":true}
```

```
kafka-console-producer \
  --bootstrap-server broker:9092 \
  --topic fact_orders \
  --property "parse.key=true" \
  --property "key.separator=|"
```

```
101|{"order_id":101,"customer_id":1,  "order_datetime":"2025-10-05T14:32:00", "order_status":"PAID","payment_method":"CARD", "shipping_fee":5.99,"discount_amt":10.00}
```

```
102|{"order_id":102,"customer_id":1,  "order_datetime":"2025-10-12T09:15:00",  "order_status":"PAID","payment_method":"WALLET", "shipping_fee":4.99,"discount_amt":5.00}
```

```
kafka-console-producer \
  --bootstrap-server broker:9092 \
  --topic fact_order_items \
  --property "parse.key=true" \
  --property "key.separator=|"
```

```
1001|{"order_item_id":1001,"order_id":101,"product_id":10,  "quantity":2,"item_price":249.99}
```
```
1002|{"order_item_id":1002,"order_id":102,"product_id":20,   "quantity":1,"item_price":129.50}
```
```
1003|{"order_item_id":1003,"order_id":102,"product_id":20,  "quantity":1,"item_price":129.50}
```
```
1004|{"order_item_id":1004,"order_id":102,"product_id":20,  "quantity":1,"item_price":129.50}
```

Another tab

```
kafka-console-consumer \
  --bootstrap-server broker:9092 \
  --topic customer_revenue_upsert \
  --from-beginning \
  --property print.key=true \
  --property key.separator=" | "
```

```
kafka-console-consumer \
  --bootstrap-server broker:9092 \
  --topic customer_revenue_upsert \
  --from-beginning \
  --property print.key=true \
  --property key.separator=" | "
```
