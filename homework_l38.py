"""
Задание 1. При старте приложения запускаются три потока. Первый поток заполняет
список случайными числами. Второй поток находит сумму элементов списка,
а третий поток среднеарифметическое значение в списке. Полученный список, сумма и
среднеарифметическое выводятся на экран.

Задание 2. Пользователь с клавиатуры вводит путь к файлу. После чего запускаются
три потока. Первый поток заполняет файл случайными числами. Второй поток находит
все простые числа, а третий поток факториал каждого числа в файле. Результаты поиска
каждый поток должен записать в новый файл.

Подсказка: можно воспользоваться высокоуровневой библиотекой concurrent.futures для
создания пула потоков.

Нюансы реализации разрешаются программистом.
"""


"""
МОИ КОММЕНТАРИИ
- Я не стал делать запрос ввода пользвоателя в Задании 2 из соображений удобства. В папке с ДЗ создатутся
    файлы test.txt, test_prime.txt, test_factorial.txt, где будет отображаться результат. 
- В первом задании я вывожу первые 10 элементов списка (чтобы показать, что все работает и не загромождать экран)
- В итоговом print'e я вывел результаты без использования concurrent.futures и с ним - для сравнения. Почему-то с 
    использованием оно работает на доли секунды дольше или почти так же. Может, я что-то делаю не так.
- В main() к каждому TASK'у в комментариях пометил, какие параметры нужно менять для тестирования более долгих 
    вычислений
"""


import random
import threading
import time
import math
import concurrent.futures

# TASK 1

def create_random_list(start, stop, how_many):
    result = random.choices(range(start, stop+1), k=how_many)
    print(f'\nFirst 10 elems: {result[:10]}')
    return result

def sum_of_elements(start, stop, how_many):
    randomlist = random.choices(range(start, stop + 1), k=how_many)
    result = sum(randomlist)
    return (f'Sum: {result}')


def avg_of_elements(start, stop, how_many):
    randomlist = random.choices(range(start, stop + 1), k=how_many)
    result = sum(randomlist) / len(randomlist)
    return (f'Avg: {result}')


# TASK 2

lock = threading.Lock()

def random_list_to_file(start, stop, how_many, lock):
    result = random.choices(range(start, stop+1), k=how_many)
    with open('test.txt', 'w') as f:
        f.writelines(str(result))
# Полагаю нужно сделать lock, пока файл не запишется, чтобы другие процессы не входили в файл во время его записи
    with lock:
        return result


def prime_numbers_finder():
    with open('test.txt', 'r') as f:
        result = []
        my_list = f.read()
        my_list = my_list[1:-1] # убираем квадратные скобки в начале и в конце строки
        my_list = [int(i) for i in my_list.split(',')]
        # print(f'\nOriginal list: {my_list}')
        for number in my_list:
            if number > 1:
                for i in range(2, int(number)):
                    if number % i == 0:
                        break
                else:
                    result.append(number)
                    with open('test_prime.txt', 'w') as t:
                        t.write(f'Primes: {str(result)}')
        return f'Primes: {result}'


def factorial_finder():
    with open('test.txt', 'r') as f:
        factorials = []
        my_list = f.read()
        my_list = my_list[1:-1]
        my_list = [int(i) for i in my_list.split(',')]
        for number in my_list:
            factorials.append(f'Factorial of {number} is {math.factorial(number)}')
            result = '\n'.join(factorials)
        with open('test_factorial.txt', 'w') as fact:
            fact.write(f'{str(result)}')
    return result






def main():
    print('TASK 1\n')

    # Изменить значение "how_many" (например на 10_000_000) для более долгих калькуляций
    start = 0
    stop = 100_000
    how_many = 1_000_000

    start_time = time.time()
    print('Calculating...')

    create_random_list(start, stop, how_many)
    print(sum_of_elements(start, stop, how_many))
    print(f'{avg_of_elements(start, stop, how_many)}\nWITHOUT concurrent.futures: ', end='')

    end_time1 = time.time()
    print(f'{end_time1 - start_time:.3f}s')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future1 = executor.submit(create_random_list, start, stop, how_many)
        future2 = executor.submit(sum_of_elements, start, stop, how_many)
        future3 = executor.submit(avg_of_elements, start, stop, how_many)
        print(f'{future2.result()}'
              f'\n{future3.result()}'
              f'\nWITH concurrent.futures: ', end='')

    end_time2 = time.time()
    print(f'{end_time2 - end_time1:.3f}s')
    


    print('\nTASK 2\n')

    # Изменить значения "stop" и/или "how_many" для более долгих калькуляций
    start = 0
    stop = 1000
    how_many = 1000

    print('Calculating...')
    start_time = time.time()

    random_list_to_file(start, stop, how_many, lock)
    prime_numbers_finder()
    factorial_finder()

    end_time1 = time.time()
    print(f'WITHOUT concurrent.futures: {end_time1 - start_time:.3f}')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future4 = executor.submit(random_list_to_file, start, stop, how_many, lock)
        future5 = executor.submit(prime_numbers_finder)
        future6 = executor.submit(factorial_finder)


    end_time2 = time.time()
    print(f'WITH concurrent.futures: {end_time2 - end_time1:.3f}s')



if __name__ == '__main__':
    main()