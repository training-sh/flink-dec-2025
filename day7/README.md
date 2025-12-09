# DAY 7


https://confluent.cloud/login/sso/flink-demo


PLS add volumnes to kafka-tools in docker-compose.yml

ensure proper intentation

```
    volumes:
      - ./secret:/secret:ro
```

It will look like

```
  kafka-tools:
    image: confluentinc/cp-kafka:${CP_TAG:-6.2.0}
    container_name: kafka-tools
    networks: [flink-net]
    depends_on: [broker]
    entrypoint: ["bash","-lc","sleep infinity"]
    volumes:
      - ./secret:/secret:ro
```

# Day 1 

Open terminal

```
cd ~
```

```
cd lab
```

```
cd flink-cluster-1
```

ONLY IF YOU WANT TO BUILD IMAGE, NOT NEEDED FOR DAY 2, DAY 3

```
docker compose build --no-cache
```

```
docker compose up --build 
```


      
