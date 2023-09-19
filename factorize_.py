import time
import logging
from multiprocessing import Pool, current_process
from rich import print


# def timing_decorator(func):
#     def wrapper(*args, **kwargs):
#         start_time = time.time()
#         result = func(*args, **kwargs)
#         end_time = time.time()
#         completed_time = end_time - start_time
#         print(f"{func.__name__} completed in - {completed_time:.4f} seconds")
#         return result

#     return wrapper


# @timing_decorator
def factorize(*numbers):
    result_list = []

    for num in numbers:
        result_each_number = [i for i in range(1, num + 1) if num % i == 0]
        result_list.append(result_each_number)

    return result_list


# # @timing_decorator
# def factorize_pool(list_numbers: list):
#     with Pool(processes=4) as pool:
#         result = pool.map(factorize, list_numbers)
#         return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")

    # Sync implementation

    start_time_sync = time.time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    end_time_sync = time.time()
    completed_time_sync = end_time_sync - start_time_sync
    print(
        a,
        b,
        c,
        d,
        sep="\n",
    )

    #  Multiprossecing implementation

    list_for_pool = [128, 255, 99999, 10651060]

    start_time_multi = time.time()

    with Pool(processes=8) as pool:
        result = pool.map(factorize, list_for_pool)

    end_time_multi = time.time()
    completed_time_multi = end_time_multi - start_time_multi

    logging.info(result)
    logging.info(
        f"Time sync implementation - {completed_time_sync} \\n Time multiprossecing implementation - {completed_time_multi} "
    )
