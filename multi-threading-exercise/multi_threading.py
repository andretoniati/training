import logging
import threading
import time
import concurrent.futures
from itertools import chain

def run():
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        executor.submit(fun01)
        executor.submit(fun02)
        executor.submit(fun03)
        executor.submit(fun04)
        executor.submit(fun05)
        

def list_converter_str_int(list_to_be_converted):
    list_converted = list(map(int, list_to_be_converted))
    return list_converted

def fun01():
    fp = ['10 12', '10 14', '100 150']
    difference = []

    for line in fp:
        numbers = line.split(' ')
        numbers = list_converter_str_int(numbers)
        difference.append(numbers[1] - numbers[0])

    print('Outuput Function 01:')
    print(difference)

def encrypt_step_one(list_words):

    letters_in_ASCII = [i for i in chain(range(65, 90), range(97, 122))]
    crypt_words = []

    for word in list_words:
        crypt = []
        char_list = list(word)
        for char in char_list:
            if ord(char) in letters_in_ASCII:
                temp = ord(char) + 3
                crypt.append(chr(temp))
            else:
                crypt.append(char)
            crypt_word = ''.join(crypt)
        crypt_words.append(crypt_word.rstrip())
    return crypt_words

def encrypt_step_two(list_words):
    crypt_words = []

    for word in list_words:
        word = word[::-1]
        crypt_words.append(word)

    return crypt_words

def encrypt_step_three(list_words):
    crypt_words = []

    for word in list_words:
        pos = int(len(word)/2)
        for index in range(pos, len(word)):
            word = word[:index] + chr(ord(word[index]) -1) + word[index + 1:]
        crypt_words.append(word)

    return crypt_words

def fun02():
    list_words = ['Texto #3', 'abcABC1', 'vxpdylY .ph', 'vv.xwfxo.fd']

    list_words = encrypt_step_one(list_words)
    list_words = encrypt_step_two(list_words)
    list_words = encrypt_step_three(list_words)

    print('Outuput Function 02:')
    print(list_words)

def is_prime(n):
    cnt = 0
    if n < 2:
        return False
    for i in range(2, n + 1):
        if n % i == 0:
            cnt += 1
    if cnt > 1:
        return False  
    return True

def fun03():
    
    info = [4, 6, 8, 10, 13, 20, 21, 33, 37, 43, 55]
    output_list = []
    for element in info:
        if(is_prime(element)):
            output_list.append(str(element))
        if len(output_list) != 0:
            output_string = ' '.join(output_list)
        else:
            output_string = '*'

    print('Outuput Function 03:')
    print(output_string)

def fun04():
    marbles = [1, 3, 3, 3, 1]
    consulting = [2, 3]
    ans = []
    for try_consult in consulting:
        cnt = 0
        is_founded = False
        for marble in marbles:
            cnt += 1
            if try_consult == marble:
                ans.append(str(try_consult) + ' found at ' + str(cnt))
                is_founded = True
        if (is_founded == False):
            ans.append(str(try_consult) + ' not found')
    
    print('Outuput Function 04:')
    print(ans)

def fun05():
    N = 100000000
    prime = [True for i in range(N + 1)] 
    p = 2
    while (p * p <= N): 
        if (prime[p] == True): 
            for i in range(p * p, N + 1, p): 
                prime[i] = False
        p += 1
    prime_numbers = []
    for p in range(2, N): 
        if prime[p]: 
            prime_numbers.append(str(p) +  '\n')
    
    file = open('prime_number.txt', 'w')
    file.writelines(prime_numbers)
    print('Outuput Function 05:')
    print('File created!')

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    print('multi-threading:')
    start = time.time()
    run()
    end = time.time()
    print("Tempo decorrido = %.2f minutos " %((end - start)/60))

    print('single thread - functions in series')
    start = time.time()
    fun01()
    fun02()
    fun03()
    fun04()
    fun05()
    end = time.time()
    print("Tempo decorrido = %.2f minutos " %((end - start)/60))

