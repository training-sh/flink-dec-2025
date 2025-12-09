# Hopping Window/Sliding Window/Overlapping Window

-- easy to understand example for hopping window.


```sql
CREATE TABLE gks_orders_hopping_ex (
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

```sql
INSERT INTO gks_orders_hopping_ex VALUES
  ('o1', 'u1', 'p100', 100.0, TIMESTAMP '2025-11-05 10:01:00.000'),  -- 1-5 min (1)
  ('o2', 'u2', 'p101', 150.0, TIMESTAMP '2025-11-05 10:03:30.000'),  -- 1-5 min (2)
  ('o3', 'u3', 'p102', 200.0, TIMESTAMP '2025-11-05 10:04:45.000'),  -- 1-5 min (3)
  ('o4', 'u4', 'p103', 120.0, TIMESTAMP '2025-11-05 10:06:10.000'),  -- 6-10 min (1)
  ('o5', 'u5', 'p104',  80.0, TIMESTAMP '2025-11-05 10:09:55.000'),  -- 6-10 min (2)
  ('o6', 'u6', 'p105',  60.0, TIMESTAMP '2025-11-05 10:11:20.000'),  -- 11-15 min (1)
  ('o7', 'u7', 'p106',  90.0, TIMESTAMP '2025-11-05 10:14:05.000'),  -- 11-15 min (2)
  ('o8', 'u8', 'p107', 110.0, TIMESTAMP '2025-11-05 10:18:30.000');  -- 16-20 min (extra)
```

```sql
CREATE VIEW gks_orders_hopping_ex_hop_10m_5m AS
SELECT
  T.window_start,
  T.window_end,
  COUNT(*)      AS orders,
  SUM(T.amount) AS total_amount
FROM TABLE(
  HOP(
    TABLE gks_orders_hopping_ex,
    DESCRIPTOR(order_time),
    INTERVAL '5' MINUTE,
    INTERVAL '10' MINUTE
  )
) AS T(
  order_id,      -- original columns from source table
  user_id,
  product_id,
  amount,
  order_time,
  window_start,  -- window metadata appended by TVF
  window_end,
  window_time
)
GROUP BY
  T.window_start,
  T.window_end;
```

```sql
SELECT * FROM gks_orders_hopping_ex_hop_10m_5m;
```

```sql
-- heart beat or trigger for last window, you may notice 10-10 to 10-20 records not yet published
-- just a second after past 20 would trigger window close for 10:10 to 10:20 window.
INSERT INTO gks_orders_hopping_ex VALUES
  ('hb1', 'hb', 'p_hb', 0.0, TIMESTAMP '2025-11-05 10:21:00.000');
```

```
-- try to insert few records based on your mental model, try to tally the results, insert trigger /heart beat.
-- stop running queries if you are done, play
```
