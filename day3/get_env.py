from pyflink.java_gateway import get_gateway
from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode

"""

import get_env
env = get_env.get_env("remote")

env = get_env.get_remote_env()

"""

def get_remote_env(jobmanager_host = "jobmanager"):
    # Get the Java gateway
    gateway = get_gateway()
    
    # Define the remote Flink JobManager host and port
    jobmanager_host = "jobmanager"  # Replace with your JobManager host
    jobmanager_port = 8081        # Replace with your JobManager port
    
    # Create a Java String array for the JAR files (empty if no UDFs or dependencies)
    # If you have custom UDFs or dependencies, you would add their JAR paths here.
    # Example: gateway.new_array(string_class, 1, "/path/to/your/udf.jar")
    string_class = gateway.jvm.String
    jar_files_array = gateway.new_array(string_class, 0)
    
    # Create the Java RemoteStreamExecutionEnvironment
    j_stream_execution_environment = gateway.jvm.org.apache.flink.streaming.api.environment.StreamExecutionEnvironment.createRemoteEnvironment(
        jobmanager_host,
        jobmanager_port,
        jar_files_array
    )
    
    # Wrap the Java environment with PyFlink's StreamExecutionEnvironment
    env = StreamExecutionEnvironment(j_stream_execution_environment)
    return env
 

def get_env(name=""):
    #if 'get_ipython' in locals(): # runs in notebook, we want to connect to task manager
    if name == "remote":
        print ("returning remote env")
        return get_remote_env()

    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_runtime_mode(RuntimeExecutionMode.STREAMING)
    env.set_parallelism(1)
    return env

from pyflink.table import EnvironmentSettings, TableEnvironment
import os

def get_remote_batch_env():
        
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/etc/gcp/key.json"
    os.environ["HADOOP_CONF_DIR"] = "/opt/flink/conf"
    os.environ["AWS_ACCESS_KEY_ID"] = "minio"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "minio12345"
    os.environ["AWS_REGION"] = "us-east-1"
    os.environ["HADOOP_USER_NAME"] = "minio"
    
    
    env = EnvironmentSettings.new_instance().in_batch_mode().build()
    # Create the TableEnvironment
    t_env = TableEnvironment.create(environment_settings=env)

    conf = t_env.get_config().get_configuration()
    
    # # === Remote JobManager ===
    conf.set_string("execution.target", "remote")
    conf.set_string("jobmanager.rpc.address", "jobmanager")
    conf.set_string("rest.address", "jobmanager")
    conf.set_string("rest.port", "8081")
    
    # === Python Exec Location ===
    conf.set_string("python.executable", "/usr/bin/python3")
    conf.set_string("pipeline.jars", "file:///opt/flink/plugins/gs-fs-hadoop/flink-gs-fs-hadoop-1.20.2.jar")  # client-side path
    
    # === Allow fallback to Hadoop FS for gs:// and s3:// ===
    conf.set_string("fs.allowed-fallback-filesystems", "hadoop")
    
    # GCS (Hadoop connector) - optional if already present in flink-conf.yaml
    # conf.set_string("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
    # conf.set_string("fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
    
    # conf.set_string("google.cloud.auth.service.account.enable", "true")
    # conf.set_string("google.cloud.auth.service.account.json.keyfile", "/etc/gcp/key.json")
    
    
    t_env.get_config().set("parallelism.default", "1")

    return (env, t_env)
        
        