#!/usr/bin/env python3

def transform(subj_num, secret_loop_size):
    v = 1
    for i in range(secret_loop_size):
        v = (v * subj_num) % 20201227
    return v

def find_secret(subj_num, pk):
    v = 1
    iterations = 0
    while True:
        if v == pk: return iterations
        v = (v * subj_num) % 20201227
        iterations += 1

def part1():
    subj_num = 7
    pk_a = 15113849
    pk_b = 4206373
    secret_a = find_secret(subj_num, pk_a)
    secret_b = find_secret(subj_num, pk_b)
    enc_key_a = transform(pk_b, secret_a)
    enc_key_b = transform(pk_a, secret_b)
    if enc_key_a != enc_key_b:
        print("Something is wrong.")
        return None
    return enc_key_a

print("Part 1: {}".format(part1()))
