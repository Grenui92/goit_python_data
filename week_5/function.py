from multiprocessing import Pool
from os import cpu_count
def factorize(x):
    result = []
    for num in range(1, x+1):
        if x%num == 0:
            result.append(num)
    return result


if __name__ == "__main__":
    factor = [128, 255, 99999, 10651060]
    with Pool(processes=cpu_count()) as pool:
        a, b, c, d = pool.map(factorize, factor)
    print(a, b, c, d)
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
