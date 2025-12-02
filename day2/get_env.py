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
    