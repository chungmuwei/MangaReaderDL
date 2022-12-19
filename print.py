import time, random
x = range(101)
for n in x:
    timefluc = random.uniform(0, 1.2)
    time.sleep(0.1)
    print("\r{0}%".format(n), end='')