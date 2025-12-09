Thumble window

```
CREATE  TABLE gks_orders (
  order_id        STRING,
  user_id         STRING,
  product_id      STRING,
  amount          DOUBLE,
  order_time      TIMESTAMP(3),
  WATERMARK FOR order_time AS order_time - INTERVAL '15' SECOND
) WITH (
 'connector' = 'confluent',
  'scan.startup.mode' = 'earliest-offset',
  'value.format' = 'json-registry'
);
```


```
CREATE VIEW gks_orders_tumble_5m AS
SELECT
  window_start,
  window_end,
  COUNT(*) AS orders_count,
  SUM(amount) AS total_amount
FROM TABLE(
  TUMBLE(
    TABLE gks_orders,
    DESCRIPTOR(order_time),
    INTERVAL '5' MINUTE
  )
)
GROUP BY window_start, window_end;
```


```
SELECT * FROM gks_orders_tumble_5m;
```

```
INSERT INTO gks_orders VALUES
  ('o1', 'u1', 'p100', 100.0, TIMESTAMP '2025-11-05 10:01:00.000'),
  ('o2', 'u2', 'p101', 150.0, TIMESTAMP '2025-11-05 10:03:30.000');
```

Trigger record.. work around..

```
INSERT INTO gks_orders VALUES
  ('trigger', 'uX', 'pX', 10.0, TIMESTAMP '2025-11-08 10:06:00.000');
```

```
INSERT INTO gks_orders VALUES
  ('o2', 'u2', 'p101', 150.0, TIMESTAMP '2025-11-05 10:04:30.000');
```
