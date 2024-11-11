import concurrent.futures
import time


def ppprint():
    start_time = time.time()
    x = 0
    for _ in range(int(10e2)):
        x += 1
    execution_time = time.time() - start_time
    return x, execution_time


def babat(*args):
    start_time = time.time()
    x = 0
    for _ in range(int(10e8)):
        x += 1
    execution_time = time.time() - start_time
    return x, execution_time


def run_func(func):
    result, execution_time = func()
    print(
        f"{func.__name__} Result: {result}, Execution Time: {execution_time:.6f} seconds"
    )
    return result, execution_time


def other_code():
    # This is the other code you want to run concurrently
    for i in range(5):
        print(f"Running other code iteration {i}")
        time.sleep(1)


if __name__ == "__main__":
    a = {"p": ppprint}
    b = [babat, ppprint]

    # The freeze_support() call is needed to prevent issues with certain environments
    # concurrent.futures.freeze_support()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Submit the tasks and get the futures
        futures = [executor.submit(run_func, func) for func in b]

        # Run other code concurrently while waiting for futures to complete
        with concurrent.futures.ThreadPoolExecutor() as thread_executor:
            thread_executor.submit(other_code)

        # Collect results as they become available
        results = []
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error: {e}")

    # Wait for all functions to finish before printing the final result list
    # concurrent.futures.wait(futures)

    print("Final Results:")
    print(results)
