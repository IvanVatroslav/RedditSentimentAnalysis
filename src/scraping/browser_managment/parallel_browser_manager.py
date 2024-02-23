from concurrent.futures import ThreadPoolExecutor, as_completed


class ParallelBrowserManager:
    def __init__(self, workers=5):
        self.workers = workers

    def perform_parallel_action(self, action, args_list):
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = [executor.submit(action, *args) for args in args_list]
            results = []
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                    print(f"Task completed with result: {result}")
                except Exception as exc:
                    print(f"Task generated an exception: {exc}")
                    results.append(None)
        return results
