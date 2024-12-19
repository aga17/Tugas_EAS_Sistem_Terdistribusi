# Redis Distributed Lock: Release Lock
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

# Function to release a lock
def release_lock(lock_name):
    try:
        result = redis_cluster.delete(lock_name)
        if result:
            print(f"Lock '{lock_name}' released successfully.")
        else:
            print(f"Failed to release lock '{lock_name}'. It may not exist.")
    except Exception as e:
        print(f"Error while releasing lock: {str(e)}")

# Main program for testing release lock
if __name__ == "__main__":
    lock_name = input("Enter the name of the lock to release: ")
    release_lock(lock_name)

