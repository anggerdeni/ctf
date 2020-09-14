from pwn import *
def detect(c):
    if(c[:32] == c[32:64]):
        return 'ECB'
    return 'CBC'

l = []
r = remote('crypto.chal.csaw.io',5001)
r.recvline()
for i in range(176):
    cek = r.recvline()
    print i
    if('Enter plaintext:' not in cek):
        r.interactive()
    r.sendline('A'*64)
    r.recvuntil('Ciphertext is:  ')
    c = r.recvuntil('\n')[:-1]
    res = detect(c)
    l.append((res,c))
    r.recvline()
    r.sendline(res)

x = ''
for i in l:
    if(i[0] == 'ECB'):
        x += '0'
    else:
        x += '1'

print x
print hex(int(x,2))
print hex(int(x,2))[2:].decode('hex')