


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

