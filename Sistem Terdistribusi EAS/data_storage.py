# Full Script for Redis Cluster Implementation with Interactive Command Menu

# Import necessary modules
import redis
from rediscluster import RedisCluster

# Configuration for Redis cluster startup nodes
startup_nodes = [
    {"host": "127.0.0.1", "port": "7000"},
    {"host": "127.0.0.1", "port": "7001"},
    {"host": "127.0.0.1", "port": "7002"},
    {"host": "127.0.0.1", "port": "7003"},
    {"host": "127.0.0.1", "port": "7004"},
    {"host": "127.0.0.1", "port": "7005"}
]

# Connect to Redis cluster
try:
    redis_cluster = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
    print("Connected to Redis Cluster.")
except Exception as e:
    print(f"Error connecting to Redis Cluster: {str(e)}")
    exit(1)

# Function to store data in the cluster
def store_data(key, value):
    try:
        redis_cluster.set(key, value)
        print(f"Data stored: {key} -> {value}")
    except Exception as e:
        print(f"Error storing data: {str(e)}")

# Function to retrieve data from the cluster
def retrieve_data(key):
    try:
        value = redis_cluster.get(key)
        if value:
            print(f"Data retrieved: {key} -> {value}")
            return value
        else:
            print(f"Data not found for key: {key}")
            return None
    except Exception as e:
        print(f"Error retrieving data: {str(e)}")

# Function to delete data from the cluster
def delete_data(key):
    try:
        result = redis_cluster.delete(key)
        if result:
            print(f"Data deleted: {key}")
        else:
            print(f"No data found to delete for key: {key}")
    except Exception as e:
        print(f"Error deleting data: {str(e)}")

# Function to update data in the cluster
def update_data(key, new_value):
    try:
        if redis_cluster.exists(key):
            redis_cluster.set(key, new_value)
            print(f"Data updated: {key} -> {new_value}")
        else:
            print(f"Cannot update non-existent key: {key}")
    except Exception as e:
        print(f"Error updating data: {str(e)}")

# Interactive menu to perform operations
def command_menu():
    while True:
        print("\nRedis Cluster Operations Menu")
        print("1. Store Data")
        print("2. Retrieve Data")
        print("3. Update Data")
        print("4. Delete Data")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            key = input("Enter key: ")
            value = input("Enter value: ")
            store_data(key, value)
        elif choice == '2':
            key = input("Enter key: ")
            retrieve_data(key)
        elif choice == '3':
            key = input("Enter key: ")
            new_value = input("Enter new value: ")
            update_data(key, new_value)
        elif choice == '4':
            key = input("Enter key: ")
            delete_data(key)
        elif choice == '5':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Main function to start the program
def main():
    print("Starting Redis Cluster Interactive Menu...")
    command_menu()

if __name__ == "__main__":
    main()

