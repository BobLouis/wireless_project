import time


def main():
    time.sleep(1)


start_time = time.time()
main()
print(time.time() - start_time, "seconds")
