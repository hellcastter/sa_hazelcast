import hazelcast
import threading
import time


def increment_with_lock(client, map_name):
    my_map = client.get_map(map_name).blocking()
    key = "key"
    
    my_map.put_if_absent(key, 0)
    
    for _ in range(10_000):
        my_map.lock(key)

        value = my_map.get(key) 
        value += 1
        my_map.put(key, value)

        my_map.unlock(key)

def run_clients():
    # Створення трьох окремих клієнтів
    client1 = hazelcast.HazelcastClient()
    client2 = hazelcast.HazelcastClient()
    client3 = hazelcast.HazelcastClient()

    map_name = "distributed_map"
    
    start_time = time.time()

    thread1 = threading.Thread(target=increment_with_lock, args=(client1, map_name))
    thread2 = threading.Thread(target=increment_with_lock, args=(client2, map_name))
    thread3 = threading.Thread(target=increment_with_lock, args=(client3, map_name))

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

    my_map = client1.get_map(map_name).blocking()
    final_value = my_map.get("key")
    end_time = time.time()
    
    print(f"Final value for 'key': {final_value}")
    print(f"Time taken: {end_time - start_time} seconds")
    
    client1.shutdown()
    client2.shutdown()
    client3.shutdown()

run_clients()
