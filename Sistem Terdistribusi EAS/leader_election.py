# Redis Leader Election Example
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

leader_key = "cluster_leader"

# Function to perform leader election
def leader_election(candidate_id, ttl=5):
    try:
        is_leader = redis_cluster.set(leader_key, candidate_id, nx=True, ex=ttl)
        if is_leader:
            print(f"Node {candidate_id} is elected as the leader.")
            return True
        else:
            current_leader = redis_cluster.get(leader_key)
            print(f"Node {candidate_id} is not the leader. Current leader: {current_leader}")
            return False
    except Exception as e:
        print(f"Error during leader election: {str(e)}")

# Function to get the current leader
def get_current_leader():
    try:
        current_leader = redis_cluster.get(leader_key)
        if current_leader:
            print(f"Current leader is: {current_leader}")
        else:
            print("No leader is currently elected.")
    except Exception as e:
        print(f"Error fetching current leader: {str(e)}")

# Main program for testing
if __name__ == "__main__":
    print("Choose an action:")
    print("1. Elect a leader")
    print("2. View current leader")
    choice = input("Enter your choice (1/2): ")

    if choice == "1":
        candidate_id = input("Enter candidate ID: ")
        leader_election(candidate_id)
    elif choice == "2":
        get_current_leader()
    else:
        print("Invalid choice.")

