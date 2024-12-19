import redis
from rediscluster import RedisCluster
import time

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

# Distributed commit function using WATCH with retry mechanism
def distributed_commit(transaction_key, transaction_value, retries=3, delay=2):
    attempt = 0
    while attempt < retries:
        try:
            # WATCH the key for concurrent modifications
            redis_cluster.watch(transaction_key)
            print(f"Watching key: {transaction_key}")

            # Get the current value before starting the transaction
            current_value = redis_cluster.get(transaction_key)
            print(f"Current value of {transaction_key}: {current_value}")

            # Simulate a delay (optional, to test concurrency handling)
            time.sleep(2)  # Simulates concurrent modification scenario

            # Check if the key was modified during the delay
            if redis_cluster.get(transaction_key) != current_value:
                print(f"Key '{transaction_key}' was modified by another process.")
                redis_cluster.unwatch()  # Release the watch on the key
                return False  # Abort transaction if key was modified

            # Set the new value only if the key hasn't changed
            redis_cluster.set(transaction_key, transaction_value)
            print(f"Transaction committed: {transaction_key} -> {transaction_value}")
            redis_cluster.unwatch()  # Release the watch after the transaction

            return True

        except redis.exceptions.WatchError:
            # Transaction aborted due to another modification
            print(f"Transaction aborted: Key '{transaction_key}' was modified by another process.")
            redis_cluster.unwatch()  # Unwatch the key in case of error
            return False

        except Exception as e:
            print(f"Error during distributed commit: {str(e)}")
            redis_cluster.unwatch()  # Ensure the key is unwatched on error
            return False

        finally:
            attempt += 1
            if attempt < retries:
                print(f"Retrying transaction... Attempt {attempt}/{retries}")
                time.sleep(delay)
            else:
                print("Max retry attempts reached. Transaction failed.")

    return False

# Main program for testing
if __name__ == "__main__":
    transaction_key = input("Enter the transaction key: ")
    transaction_value = input("Enter the transaction value: ")
    success = distributed_commit(transaction_key, transaction_value)

    if success:
        print("Transaction successfully committed.")
    else:
        print("Transaction failed.")

