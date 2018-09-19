#!/usr/bin/env python

from telnetlib import Telnet
import sys
import re

HOST = 'localhost'
PORT = 31013
PASSWORD = "terminal"

if len(sys.argv) > 1:
    HOST = sys.argv[1]
if len(sys.argv) > 2:
    PORT = int(sys.argv[2])

BUFSIZE = 4096

def is_prime(n):
    """ Determines whether a number is prime"""
    f = n * 1.0
    for divisor in range(2, int(n ** 0.5) + 1):
        if f / divisor == n / divisor:
            return False
    return True


def get_primes(n):
    """Get a list of primes < n"""
    return [x for x in xrange(3, n) if is_prime(x) ]

def send_answer(tn):
    """ Attempts to read the question and send the answer.
    Returns True if the question is answered
    """

    answered = False
    try:
        question = tn.read_until("\n")
        m = re.search(": (\d*)", question)
        if m is None:
            print question
        else:
            num = int(m.groups()[0])
            print "Finding prime below: %d" % num
            prime = get_primes(num)[-1]
            print "Sending: %d" % prime
            tn.write("%s\n" % prime)
            print tn.read_until("\n")
            answered = True
    except EOFError:
        print "Connection closed"
    return answered

tn = Telnet(HOST, PORT)
# Password challenge/response
data = tn.read_until(": ")
print data
tn.write(PASSWORD + "\n")
# Welcome message
print tn.read_until("\n")
print tn.read_until("\n")

# Now solve the challenge
while send_answer(tn):
    pass

tn.close()


