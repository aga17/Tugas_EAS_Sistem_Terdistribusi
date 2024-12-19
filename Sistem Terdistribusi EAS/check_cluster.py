# Redis Cluster Communication Example
import redis
from rediscluster import RedisCluster

# Configuration for Redis cluster startup nodes
startup_nodes = [
    {"host": "127.0.0.1", "port": "7000"},
    {"host": "127.0.0.1", "port": "7001"},
    {"host": "127.0.0.1", "port": "7002"}
]

# Connect to Redis cluster
try:
    redis_cluster = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
    print("Connected to Redis Cluster.")
except Exception as e:
    print(f"Error connecting to Redis Cluster: {str(e)}")
    exit(1)

# Function to check cluster status
def check_cluster_status():
    try:
        cluster_info = redis_cluster.info('cluster')
        print("Cluster Info:")
        for key, value in cluster_info.items():
            print(f"Node: {key}, Info: {value}")
    except Exception as e:
        print(f"Error checking cluster status: {str(e)}")

# Test Cluster Communication
if __name__ == "__main__":
    check_cluster_status()

