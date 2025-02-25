import hazelcast
import threading
import time

class Value:
    def __init__(self, amount=0):
        self.amount = amount

    def __eq__(self, other):
        if isinstance(other, Value):
            return self.amount == other.amount
        return False

def increment_with_optimistic_lock(client: hazelcast.HazelcastClient, map_name):
    my_map = client.get_map(map_name).blocking()
    key = "key"
    
    # Initialize the value if it's absent
    my_map.put_if_absent(key, 0)
    
    for _ in range(10_000):
        while True:
            old_value = my_map.get(key)
            new_value = old_value + 1

            if my_map.replace_if_same(key, old_value, new_value):
                break

def run_clients():
    # Create three separate Hazelcast clients
    client1 = hazelcast.HazelcastClient()
    client2 = hazelcast.HazelcastClient()
    client3 = hazelcast.HazelcastClient()

    map_name = "distributed_map"
    
    start_time = time.time()

    # Start threads for the clients
    thread1 = threading.Thread(target=increment_with_optimistic_lock, args=(client1, map_name))
    thread2 = threading.Thread(target=increment_with_optimistic_lock, args=(client2, map_name))
    thread3 = threading.Thread(target=increment_with_optimistic_lock, args=(client3, map_name))

    thread1.start()
    thread2.start()
    thread3.start()

    # Wait for all threads to finish
    thread1.join()
    thread2.join()
    thread3.join()

    # Retrieve the final value from the map
    my_map = client1.get_map(map_name).blocking()
    final_value = my_map.get("key")
    print(f"Final value for 'key': {final_value}")

    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    
    # Shutdown clients
    client1.shutdown()
    client2.shutdown()
    client3.shutdown()

run_clients()
