# Session Window

```sql
CREATE TABLE gks_orders_session_ex (
  order_id STRING,
  user_id STRING,
  product_id STRING,
  amount DOUBLE,
  order_time TIMESTAMP(3),
  WATERMARK FOR order_time AS order_time - INTERVAL '15' SECOND
) WITH (
  'connector' = 'confluent',
  'scan.startup.mode' = 'earliest-offset',
  'value.format' = 'json-registry'
);
```


```sql
INSERT INTO gks_orders_session_ex VALUES
  ('o1', 'u1', 'p100', 100.0, TIMESTAMP '2025-11-05 10:01:00.000'),
  ('o2', 'u2', 'p101', 150.0, TIMESTAMP '2025-11-05 10:03:30.000');
```

-- Session 1 (morning) : 4 orders, totals in tens (40)
-- events close together -> single session

```sql
INSERT INTO gks_orders_session_ex VALUES
  ('s1_o1','u1','p200', 10.0, TIMESTAMP '2025-11-05 09:00:00.000'),
  ('s1_o2','u1','p201', 10.0, TIMESTAMP '2025-11-05 09:05:00.000'),
  ('s1_o3','u1','p202', 10.0, TIMESTAMP '2025-11-05 09:10:00.000'),
  ('s1_o4','u1','p203', 10.0, TIMESTAMP '2025-11-05 09:20:00.000');
```

-- Session 2 (afternoon) : starts 13:00, event at 13:25 extends session,
-- another event at 13:40 still within 30 min of previous -> same session
-- totals in hundreds (300)

```sql
INSERT INTO gks_orders_session_ex VALUES
  ('s2_o1','u1','p300', 100.0, TIMESTAMP '2025-11-05 13:00:00.000'),
  ('s2_o2','u1','p301', 150.0, TIMESTAMP '2025-11-05 13:25:00.000'),
  ('s2_o3','u1','p302',  50.0, TIMESTAMP '2025-11-05 13:40:00.000');
```




-- Session 3 (evening) : two big orders -> thousands (2000)

```sql
INSERT INTO gks_orders_session_ex VALUES
  ('s3_o1','u1','p400',1000.0, TIMESTAMP '2025-11-05 18:00:00.000'),
  ('s3_o2','u1','p401',1000.0, TIMESTAMP '2025-11-05 18:05:00.000');
```

```sql
CREATE or REPLACE VIEW gks_orders_session_view AS
SELECT
  user_id,
  window_start AS session_start,
  window_end   AS session_end,
  COUNT(*)     AS order_count,
  SUM(amount)  AS total_amount
FROM TABLE(
  SESSION(
    TABLE gks_orders_session_ex,          -- input table
    DESCRIPTOR(order_time),               -- event-time descriptor
    INTERVAL '30' MINUTE                  -- session gap
  )
) AS T (
  order_id,      -- original columns (keep same order as source)
  user_id,
  product_id,
  amount,
  order_time,
  window_start,  -- TVF-provided columns
  window_end,
  window_time
)
GROUP BY
  user_id,
  window_start,
  window_end;
```

```sql
SELECT *
FROM gks_orders_session_view;
```

```sql
INSERT INTO gks_orders_session_ex VALUES
  ('tri','tri','p400',0.0, TIMESTAMP '2025-11-06 18:00:00.000')
```

