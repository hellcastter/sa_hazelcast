import hazelcast
import threading

master_client = hazelcast.HazelcastClient()
master_map = master_client.get_map("test_map").blocking()
master_map.put_if_absent("key", 0)

def increment(client):
    map = client.get_map("test_map").blocking()
    
    for _ in range(10_000):
        value = map.get("key")
        value += 1
        map.put("key", value)

threads = []
for _ in range(3):
    client = hazelcast.HazelcastClient()
    thread = threading.Thread(target=increment, args=(client,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

final_value = master_map.get("key")
print(f"Final value of 'key': {final_value}")

client.shutdown()
