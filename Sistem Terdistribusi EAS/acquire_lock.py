# Redis Distributed Lock: Acquire Lock
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

# Function to acquire a lock
def acquire_lock(lock_name, timeout=10):
    try:
        lock_acquired = redis_cluster.set(lock_name, "locked", nx=True, ex=timeout)
        if lock_acquired:
            print(f"Lock '{lock_name}' acquired successfully.")
            return True
        else:
            print(f"Failed to acquire lock '{lock_name}'. It is already held.")
            return False
    except Exception as e:
        print(f"Error while acquiring lock: {str(e)}")
        return False

# Main program for testing acquire lock
if __name__ == "__main__":
    lock_name = input("Enter the name of the lock to acquire: ")
    timeout = int(input("Enter the timeout for the lock (in seconds): "))
    acquire_lock(lock_name, timeout)

