import hazelcast

client = hazelcast.HazelcastClient(cluster_members=["127.0.0.1:5701", "127.0.0.1:5703"])

my_map = client.get_map("my-distributed-map").blocking()

missing_keys = [i for i in range(1000) if my_map.get(i) is None]

print(f"Lost keys: {missing_keys}")
print(f"Number of lost keys: {len(missing_keys)}")
client.shutdown()
