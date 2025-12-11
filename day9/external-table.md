```
CREATE TABLE mysql_products_ext3 (
  id INT,
  name STRING,
  price INT,
  create_ts TIMESTAMP(3),
  update_ts TIMESTAMP(3)
) WITH (
  'connector' = 'confluent-jdbc',
  'confluent-jdbc.connection' = 'confluent-jdbc-connection-dc83ab9b-5d55-4e99-8bcb-10c6a8581c06',
  'confluent-jdbc.table-name' = 'gks_products' 
);
```

```
SELECT search_results
FROM TABLE(
  KEY_SEARCH_AGG(
    mysql_products_ext3,
    DESCRIPTOR(id),
    1    -- some id that exists in your MySQL table
  )
);

```
-- 1) Unnest the returned array/rows and select fields
SELECT
  x.id,
  x.name,
  x.price,
  x.create_ts,
  x.update_ts
FROM TABLE(
  KEY_SEARCH_AGG(
    mysql_products_ext3,
    DESCRIPTOR(id),
    1
  )
) AS T(search_results)
CROSS JOIN UNNEST(T.search_results) AS x(id, name, price, create_ts, update_ts);
```

```
SELECT
  x.id,
  x.name,
  x.price,
  x.create_ts,
  x.update_ts
FROM
  (VALUES (1)) AS key_input(key_id)
CROSS JOIN LATERAL
  TABLE(
    KEY_SEARCH_AGG(
      mysql_products_ext3,
      DESCRIPTOR(id),
      key_input.key_id
    )
  ) AS T(search_results)
CROSS JOIN UNNEST(T.search_results)
    AS x(id, name, price, create_ts, update_ts);
```
