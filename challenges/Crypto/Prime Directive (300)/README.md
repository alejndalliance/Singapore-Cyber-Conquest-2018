## Prime Directive

**Category :** Crypto

**Points :** 300

**Solves :** -

**Description :**
Follow the instructions.

**Hint :** 

### Write-up

Unpacking the `zip` file, then we got two files.

**challenge.txt**
```
The most widely used public-key cryptosystem is RSA. Read about it here: https://en.wikipedia.org/wiki/RSA_(cryptosystem)

You've intercepted a ciphertext, provided as "ct.bin". You know N is 981778926678155569 and the encryption key is 3 but you don't know d.

Can you decrypt the message?
```

**ct.bin** = Random junk bytes

So, one thought came out quickly, this bin was encrypted with RSA crypto algorithm. The public-key information was revealed inside `challenge.txt` file.  

For those who learned RSA, we all know that RSA strengthness come from [Prime Factorization](https://en.wikipedia.org/wiki/Integer_factorization) problem.   

But, N, which is product of `N=p*q`, is small, so we can either 1) brute-force it, or cleverly, 2) looking at it online.  

In this case, [FactorDB](factordb.com) is our friend. So, pasting N into that website and this come out:  
  
`981778926678155569 = 3133337 · 313333333337`  

Great! We can derive `d` by having both `p`, `q`, `e` available for us.  

For deriving `d` value, I used [rsatool]() help.

```
[shahril@archuser]: rsatool>$ python rsatool.py  -p 3133337 -q 313333333337 -e 3
Using (p, q) to initialise RSA instance

n = 981778926678155569 (0xd9ffabb6c9da131)

e = 3 (0x3)

d = 654519075561125931 (0x91551a1a589b82b)

p = 3133337 (0x2fcf99)

q = 313333333337 (0x48f41f3d59)
```

Once we all have these numbers, then it is game over. 😁

Using this site [http://extranet.cryptomathic.com/rsacalc/index](http://extranet.cryptomathic.com/rsacalc/index), we can decrypt the content of `ct.bin` with above values.

Flag: `URELITE`