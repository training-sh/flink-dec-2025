# Day 4
```
docker exec -it kafka-tools bash
```

```
kafka-topics --bootstrap-server broker:9092 --create --topic test --partitions 1 --replication-factor 1
```

```
kafka-topics \
  --list \
  --bootstrap-server broker:9092  
```

```
kafka-topics \
  --describe \
  --topic demo-topic \
  --bootstrap-server   broker:9092 
``

```
kafka-topics --bootstrap-server broker:9092 --create --topic sentence --partitions 1 --replication-factor 1
```

```
kafka-console-producer --bootstrap-server broker:9092 --topic test
```


open new tab


```
kafka-console-consumer --bootstrap-server broker:9092 --topic test --from-beginning
```
