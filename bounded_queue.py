from hazelcast import HazelcastClient
import threading
import time

def writer(client: HazelcastClient, queue_name):
    my_queue = client.get_queue(queue_name).blocking()
    
    for i in range(1, 101):
        my_queue.put(i)
        print(f"Writing {i}")
        
    my_queue.put(-1) # poison pill

def reader(client: HazelcastClient, queue_name):
    my_queue = client.get_queue(queue_name).blocking()
    
    while True:
        value = my_queue.take()

        if value == -1:
            my_queue.put(-1) # poison pill
            break
        
        print(f"Read value: {value}")

def run_clients():
    client1 = HazelcastClient()
    client2 = HazelcastClient()
    client3 = HazelcastClient()

    queue_name = "bounded_queue"

    writer_thread = threading.Thread(target=writer, args=(client1, queue_name))
    
    reader_thread1 = threading.Thread(target=reader, args=(client2, queue_name))
    reader_thread2 = threading.Thread(target=reader, args=(client3, queue_name))

    writer_thread.start()
    reader_thread1.start()
    reader_thread2.start()

    writer_thread.join()
    reader_thread1.join()
    reader_thread2.join()
    
    queue = client1.get_queue(queue_name).blocking()
    queue.destroy()

    client1.shutdown()
    client2.shutdown()
    client3.shutdown()

run_clients()
