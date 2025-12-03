# Flink 1.20.2, Scala 2.12, Java 11
FROM flink:1.20.2-scala_2.12-java11

# --- System deps & Python ---
USER root
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
     unzip python3 python3-pip python3-venv curl ca-certificates && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    rm -rf /var/lib/apt/lists/*

# --- PyFlink & common libs (match the Flink version) ---
# apache-flink==1.20.* = PyFlink for Flink 1.20.x
RUN pip3 install --no-cache-dir \
      "apache-flink==1.20.*" \
      jupyterlab pyarrow pandas pymysql \
      google-cloud-bigquery google-cloud-bigquery-storage google-cloud-storage google-auth google-auth-oauthlib

# --- Ensure the Python operator JAR is on the CLASSPATH ---
# In official images it’s in /opt/flink/opt; copy it into /opt/flink/lib.
# If not found (custom base), fetch from Maven Central.
ARG FLINK_VERSION=1.20.2
RUN set -eux; \
    if ls /opt/flink/opt/flink-python-${FLINK_VERSION}.jar >/dev/null 2>&1; then \
        cp -n /opt/flink/opt/flink-python-${FLINK_VERSION}.jar /opt/flink/lib/; \
    else \
        curl -fSL "https://repo1.maven.org/maven2/org/apache/flink/flink-python/${FLINK_VERSION}/flink-python-${FLINK_VERSION}.jar" \
          -o "/opt/flink/lib/flink-python-${FLINK_VERSION}.jar"; \
    fi


# --- Iceberg for Flink 1.20 ---
ARG ICEBERG_VERSION=1.9.2
RUN curl -fSL "https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-flink-runtime-1.20/${ICEBERG_VERSION}/iceberg-flink-runtime-1.20-${ICEBERG_VERSION}.jar" \
      -o "/opt/flink/lib/iceberg-flink-runtime-1.20-${ICEBERG_VERSION}.jar"


# --- Hadoop client (needed by Iceberg Hadoop/Hive catalogs) ---
ARG HADOOP_VERSION=3.3.6
RUN curl -fSL "https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-client-api/${HADOOP_VERSION}/hadoop-client-api-${HADOOP_VERSION}.jar" \
      -o "/opt/flink/lib/hadoop-client-api-${HADOOP_VERSION}.jar" \
 && curl -fSL "https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-client-runtime/${HADOOP_VERSION}/hadoop-client-runtime-${HADOOP_VERSION}.jar" \
      -o "/opt/flink/lib/hadoop-client-runtime-${HADOOP_VERSION}.jar"

# --- Logging needed by Hadoop (LogFactory) ---
ARG COMMONS_LOGGING_VERSION=1.2
RUN curl -fSL "https://repo1.maven.org/maven2/commons-logging/commons-logging/${COMMONS_LOGGING_VERSION}/commons-logging-${COMMONS_LOGGING_VERSION}.jar" \
      -o "/opt/flink/lib/commons-logging-${COMMONS_LOGGING_VERSION}.jar"



# =======================
#     KAFKA SUPPORT
# =======================
# Add the Kafka connector fat-jar matching your Flink version.
# This jar bundles the runtime connector + kafka-clients, so no extra deps needed.
ARG KAFKA_SQL_VERSION_PRIMARY=3.4.0-1.20
ARG KAFKA_SQL_VERSION_FALLBACK=3.3.0-1.20
RUN set -eux; \
    mkdir -p /opt/flink/lib; \
    url_primary="https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/${KAFKA_SQL_VERSION_PRIMARY}/flink-sql-connector-kafka-${KAFKA_SQL_VERSION_PRIMARY}.jar"; \
    url_fallback="https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/${KAFKA_SQL_VERSION_FALLBACK}/flink-sql-connector-kafka-${KAFKA_SQL_VERSION_FALLBACK}.jar"; \
    curl -fSL "$url_primary" -o "/opt/flink/lib/flink-sql-connector-kafka-${KAFKA_SQL_VERSION_PRIMARY}.jar" \
    || curl -fSL "$url_fallback" -o "/opt/flink/lib/flink-sql-connector-kafka-${KAFKA_SQL_VERSION_FALLBACK}.jar"

# (Optional) Avro + Confluent Schema Registry format for SQL/Table API
ARG AVRO_SR_VERSION=1.20.2
RUN curl -fSL "https://repo1.maven.org/maven2/org/apache/flink/flink-sql-avro-confluent-registry/${AVRO_SR_VERSION}/flink-sql-avro-confluent-registry-${AVRO_SR_VERSION}.jar" \
      -o "/opt/flink/lib/flink-sql-avro-confluent-registry-${AVRO_SR_VERSION}.jar"


# --- Add Table formats needed by Kafka sink (JSON & CSV) ---
ARG FLINK_VERSION=1.20.2
RUN set -eux; \
    for m in json csv; do \
      if [ -f "/opt/flink/opt/flink-${m}-${FLINK_VERSION}.jar" ]; then \
        cp -n "/opt/flink/opt/flink-${m}-${FLINK_VERSION}.jar" "/opt/flink/lib/"; \
      else \
        curl -fSL "https://repo1.maven.org/maven2/org/apache/flink/flink-${m}/${FLINK_VERSION}/flink-${m}-${FLINK_VERSION}.jar" \
          -o "/opt/flink/lib/flink-${m}-${FLINK_VERSION}.jar"; \
      fi; \
    done

# =======================
#     JDBC CONNECTOR
# =======================
# Flink 1.20 requires the decoupled JDBC connector artifact.
ARG FLINK_JDBC_VERSION=3.3.0-1.20
RUN curl -fSL "https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/${FLINK_JDBC_VERSION}/flink-connector-jdbc-${FLINK_JDBC_VERSION}.jar" \
      -o "/opt/flink/lib/flink-connector-jdbc-${FLINK_JDBC_VERSION}.jar"

# =======================
#   DATABASE DRIVERS
# =======================
# --- MySQL driver (recommended current GA) ---
ARG MYSQL_J_VERSION=9.4.0
RUN curl -fSL "https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/${MYSQL_J_VERSION}/mysql-connector-j-${MYSQL_J_VERSION}.jar" \
      -o "/opt/flink/lib/mysql-connector-j-${MYSQL_J_VERSION}.jar"

# --- (Optional) PostgreSQL driver ---
ARG PG_JDBC_VERSION=42.7.7
RUN curl -fSL "https://repo1.maven.org/maven2/org/postgresql/postgresql/${PG_JDBC_VERSION}/postgresql-${PG_JDBC_VERSION}.jar" \
      -o "/opt/flink/lib/postgresql-${PG_JDBC_VERSION}.jar"

# --- Flink S3 filesystem (Hadoop flavor) plugin ---
# Put it under /opt/flink/plugins/s3-fs-hadoop (NOT /opt/flink/lib)
ARG FLINK_VERSION=1.20.2
RUN set -eux; \
    mkdir -p /opt/flink/plugins/s3-fs-hadoop; \
    curl -fSL "https://repo1.maven.org/maven2/org/apache/flink/flink-s3-fs-hadoop/${FLINK_VERSION}/flink-s3-fs-hadoop-${FLINK_VERSION}.jar" \
      -o "/opt/flink/plugins/s3-fs-hadoop/flink-s3-fs-hadoop-${FLINK_VERSION}.jar"

# mixing  s3-fs-hadoop and s3-fs-presto will cause issue, s3-fs-hadoop is good enough for iceberg

# Hadoop S3 support for Iceberg HadoopCatalog
# this helps to use s3a for iceberg, data access
ARG HADOOP_VERSION=3.3.6
RUN curl -fSL "https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_VERSION}/hadoop-aws-${HADOOP_VERSION}.jar" \
      -o "/opt/flink/lib/hadoop-aws-${HADOOP_VERSION}.jar" \
 && curl -fSL "https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.767/aws-java-sdk-bundle-1.12.767.jar" \
      -o "/opt/flink/lib/aws-java-sdk-bundle-1.12.767.jar"



# # --- Google Cloud Storage (GCS) Hadoop connector (shaded, Hadoop3) ---
ARG GCS_CONNECTOR_VERSION=hadoop3-2.2.16
RUN curl -fSL "https://repo1.maven.org/maven2/com/google/cloud/bigdataoss/gcs-connector/${GCS_CONNECTOR_VERSION}/gcs-connector-${GCS_CONNECTOR_VERSION}-shaded.jar" \
      -o "/opt/flink/lib/gcs-connector-${GCS_CONNECTOR_VERSION}-shaded.jar"


# ARG FLINK_VERSION=1.20.2
# RUN set -eux; \
#   mkdir -p /opt/flink/plugins/flink-gs-fs-hadoop; \
#   curl -fSL "https://repo1.maven.org/maven2/org/apache/flink/flink-gs-fs-hadoop/${FLINK_VERSION}/flink-gs-fs-hadoop-${FLINK_VERSION}.jar" \
#     -o "/opt/flink/plugins/flink-gs-fs-hadoop/flink-gs-fs-hadoop-${FLINK_VERSION}.jar"

    # --- Add Flink GS plugin (one jar in one plugin subfolder) ---
ARG FLINK_VERSION=1.20.2
RUN set -eux; \
  mkdir -p /opt/flink/plugins/gs-fs-hadoop; \
  curl -fSL "https://repo1.maven.org/maven2/org/apache/flink/flink-gs-fs-hadoop/${FLINK_VERSION}/flink-gs-fs-hadoop-${FLINK_VERSION}.jar" \
    -o "/opt/flink/plugins/gs-fs-hadoop/flink-gs-fs-hadoop-${FLINK_VERSION}.jar"; \
  ls -la /opt/flink/plugins/gs-fs-hadoop


    
# Change these versions/URLs if you want to pin different versions
ENV BQ_CONNECTOR_VERSION=1.0.0
ENV GOOGLE_CLOUD_BIGQUERY_VERSION=2.50.1
ENV GOOGLE_CLOUD_BIGQUERYSTORAGE_VERSION=3.17.3

# Ensure plugin directory exists and download with create-dirs; run as root during build
# RUN mkdir -p /opt/flink/plugins/flink-bigquery-connector && \
#     curl --create-dirs -fSL \
#       -o /opt/flink/plugins/flink-bigquery-connector/flink-1.17-connector-bigquery-${BQ_CONNECTOR_VERSION}.jar \
#       "https://repo1.maven.org/maven2/com/google/cloud/flink/flink-1.17-connector-bigquery/${BQ_CONNECTOR_VERSION}/flink-1.17-connector-bigquery-${BQ_CONNECTOR_VERSION}.jar" && \
#     ls -l /opt/flink/plugins/flink-bigquery-connector/


# Add shaded Flink BigQuery connector plugin
RUN mkdir -p /opt/flink/plugins/flink-bigquery-connector && \
    curl -fSL --create-dirs -o /opt/flink/plugins/flink-bigquery-connector/flink-1.17-connector-bigquery-1.0.0-shaded.jar \
      "https://repo1.maven.org/maven2/com/google/cloud/flink/flink-1.17-connector-bigquery/1.0.0/flink-1.17-connector-bigquery-1.0.0-shaded.jar" && \
    ls -l /opt/flink/plugins/flink-bigquery-connector/

ARG FLINK_VERSION=1.20.2
# 1) flink-parquet format module (adds the 'parquet' format factory)
RUN set -eux; \
  if [ -f "/opt/flink/opt/flink-parquet-${FLINK_VERSION}.jar" ]; then \
    cp -n "/opt/flink/opt/flink-parquet-${FLINK_VERSION}.jar" "/opt/flink/lib/"; \
  else \
    curl -fSL "https://repo1.maven.org/maven2/org/apache/flink/flink-parquet/${FLINK_VERSION}/flink-parquet-${FLINK_VERSION}.jar" \
      -o "/opt/flink/lib/flink-parquet-${FLINK_VERSION}.jar"; \
  fi

# 2) parquet-hadoop bundle (runtime parquet libs used by many formats)
ARG PARQUET_BUNDLE_VERSION=1.12.3
RUN curl -fSL "https://repo1.maven.org/maven2/org/apache/parquet/parquet-hadoop-bundle/${PARQUET_BUNDLE_VERSION}/parquet-hadoop-bundle-${PARQUET_BUNDLE_VERSION}.jar" \
  -o "/opt/flink/lib/parquet-hadoop-bundle-${PARQUET_BUNDLE_VERSION}.jar"


# --- Convenience envs for PyFlink ---
ENV FLINK_HOME=/opt/flink \
    FLINK_CONF_DIR=/opt/flink/conf \
    PYFLINK_CLIENT_EXECUTABLE=/usr/bin/python3 \
    PATH=/opt/flink/bin:$PATH


# put presto plugin into plugins directory
RUN mkdir -p /opt/flink/plugins/s3-fs-presto && \
    curl -fSL "https://repo1.maven.org/maven2/org/apache/flink/flink-s3-fs-presto/1.20.2/flink-s3-fs-presto-1.20.2.jar" \
      -o "/opt/flink/plugins/s3-fs-presto/flink-s3-fs-presto-1.20.2.jar"



# --- Notebooks directory for the Jupyter service ---
RUN mkdir -p /notebooks && chown -R 9999:9999 /notebooks || true
VOLUME ["/notebooks"]

RUN mkdir -p /warehouse/iceberg

# (No CMD here; docker-compose will set commands for JM/TM/Jupyter)
# Keep running as root unless you prefer the 'flink' user in your setup
USER root