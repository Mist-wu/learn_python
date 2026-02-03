import time
import threading
import asyncio
import concurrent.futures

# --- 1. Synchronous (Blocking) ---
def sync_task(name, duration):
    print(f"Sync task {name} started (waiting {duration}s)")
    time.sleep(duration)
    print(f"Sync task {name} finished")

def run_sync():
    print("\n--- Running Synchronously ---")
    start = time.time()
    sync_task("A", 2)
    sync_task("B", 2)
    sync_task("C", 2)
    print(f"Sync Total Time: {time.time() - start:.2f} seconds")

# --- 2. Threading (Concurrency for I/O bound) ---
def thread_task(name, duration):
    print(f"Thread task {name} started (waiting {duration}s)")
    time.sleep(duration)
    print(f"Thread task {name} finished")

def run_threading():
    print("\n--- Running with Threads ---")
    start = time.time()
    threads = []
    # Create threads
    t1 = threading.Thread(target=thread_task, args=("A", 2))
    t2 = threading.Thread(target=thread_task, args=("B", 2))
    t3 = threading.Thread(target=thread_task, args=("C", 2))
    
    threads.extend([t1, t2, t3])
    
    # Start threads
    for t in threads:
        t.start()
        
    # Wait for all to complete
    for t in threads:
        t.join()
        
    print(f"Threading Total Time: {time.time() - start:.2f} seconds")

# --- 3. Asyncio (Cooperative Multitasking) ---
async def async_task(name, duration):
    print(f"Async task {name} started (waiting {duration}s)")
    # await asyncio.sleep is non-blocking
    await asyncio.sleep(duration)
    print(f"Async task {name} finished")

async def run_async():
    print("\n--- Running with Asyncio ---")
    start = time.time()
    # Schedule calls concurrently
    await asyncio.gather(
        async_task("A", 2),
        async_task("B", 2),
        async_task("C", 2)
    )
    print(f"Async Total Time: {time.time() - start:.2f} seconds")

if __name__ == "__main__":
    print("Starting Concepts Demo...")
    
    run_sync()
    run_threading()
    
    # Run the top-level entry point for asyncio
    asyncio.run(run_async())
