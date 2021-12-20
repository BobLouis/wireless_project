import time

duration = 0.0
start_t = time.time()
counter = 0


while True:
    if duration > 1:
        print(counter)
        counter += 1
        duration = 0.0
        start_t = time.time()
    duration = time.time()-start_t
