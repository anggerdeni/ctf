# baby_mult
> 50 points  
> Welcome to reversing! Prove your worth and get the flag from this neat little program!  

We are given a text file [program.txt](program.txt) which contains a sequence of numbers.

The fist step I tried was interpretting this number as ascii representation of character. So I turn it back into sequence of chars.

```py
with open('program.txt','rb') as f:
    t = f.read().strip()
    t = t.split(', ')
    f.close()

print repr(''.join(map(lambda c: chr(int(c)), t)))
```

Result:
```
'UH\x89\xe5H\x83\xec\x18H\xc7E\xf8O\x00\x00\x00H\xb8\x15O\xe7K\x01\x00\x00\x00H\x89E\xf0H\xc7E\xe8\x04\x00\x00\x00H\xc7E\xe0\x03\x00\x00\x00H\xc7E\xd8\x13\x00\x00\x00H\xc7E\xd0\x15\x01\x00\x00H\xb8a[dK\xcfw\x00\x00H\x89E\xc8H\xc7E\xc0\x02\x00\x00\x00H\xc7E\xb8\x11\x00\x00\x00H\xc7E\xb0\xc1!\x00\x00H\xc7E\xa8\xe9e"\x18H\xc7E\xa03\x08\x00\x00H\xc7E\x98\xab\n\x00\x00H\xc7E\x90\xad\xaa\x8d\x00H\x8bE\xf8H\x0f\xafE\xf0H\x89E\x88H\x8bE\xe8H\x0f\xafE\xe0H\x0f\xafE\xd8H\x0f\xafE\xd0H\x0f\xafE\xc8H\x89E\x80H\x8bE\xc0H\x0f\xafE\xb8H\x0f\xafE\xb0H\x0f\xafE\xa8H\x89\x85x\xff\xff\xffH\x8bE\xa0H\x0f\xafE\x98H\x0f\xafE\x90H\x89\x85p\xff\xff\xff\xb8\x00\x00\x00\x00\xc9'
```
As expected, the text is not readable (expected because this is reverse chal, not some misc or forensics). But hey, there's the pattern 'UH\x89\xe5' which stands for
```
push rbp
mov  rbp, rsp
```

So I tried disassembling this string using pwntools.
```py
from pwn import *
context.arch = 'amd64'
print disasm('UH\x89\xe5H\x83\xec\x18H\xc7E\xf8O\x00\x00\x00H\xb8\x15O\xe7K\x01\x00\x00\x00H\x89E\xf0H\xc7E\xe8\x04\x00\x00\x00H\xc7E\xe0\x03\x00\x00\x00H\xc7E\xd8\x13\x00\x00\x00H\xc7E\xd0\x15\x01\x00\x00H\xb8a[dK\xcfw\x00\x00H\x89E\xc8H\xc7E\xc0\x02\x00\x00\x00H\xc7E\xb8\x11\x00\x00\x00H\xc7E\xb0\xc1!\x00\x00H\xc7E\xa8\xe9e"\x18H\xc7E\xa03\x08\x00\x00H\xc7E\x98\xab\n\x00\x00H\xc7E\x90\xad\xaa\x8d\x00H\x8bE\xf8H\x0f\xafE\xf0H\x89E\x88H\x8bE\xe8H\x0f\xafE\xe0H\x0f\xafE\xd8H\x0f\xafE\xd0H\x0f\xafE\xc8H\x89E\x80H\x8bE\xc0H\x0f\xafE\xb8H\x0f\xafE\xb0H\x0f\xafE\xa8H\x89\x85x\xff\xff\xffH\x8bE\xa0H\x0f\xafE\x98H\x0f\xafE\x90H\x89\x85p\xff\xff\xff\xb8\x00\x00\x00\x00\xc9')
```

Result
```
   0:   55                      push   rbp
   1:   48 89 e5                mov    rbp, rsp
   4:   48 83 ec 18             sub    rsp, 0x18
   8:   48 c7 45 f8 4f 00 00    mov    QWORD PTR [rbp-0x8], 0x4f
   f:   00
  10:   48 b8 15 4f e7 4b 01    movabs rax, 0x14be74f15
  17:   00 00 00
  1a:   48 89 45 f0             mov    QWORD PTR [rbp-0x10], rax
  1e:   48 c7 45 e8 04 00 00    mov    QWORD PTR [rbp-0x18], 0x4
  25:   00
  26:   48 c7 45 e0 03 00 00    mov    QWORD PTR [rbp-0x20], 0x3
  2d:   00
  2e:   48 c7 45 d8 13 00 00    mov    QWORD PTR [rbp-0x28], 0x13
  35:   00
  36:   48 c7 45 d0 15 01 00    mov    QWORD PTR [rbp-0x30], 0x115
  3d:   00
  3e:   48 b8 61 5b 64 4b cf    movabs rax, 0x77cf4b645b61
  45:   77 00 00
  48:   48 89 45 c8             mov    QWORD PTR [rbp-0x38], rax
  4c:   48 c7 45 c0 02 00 00    mov    QWORD PTR [rbp-0x40], 0x2
  53:   00
  54:   48 c7 45 b8 11 00 00    mov    QWORD PTR [rbp-0x48], 0x11
  5b:   00
  5c:   48 c7 45 b0 c1 21 00    mov    QWORD PTR [rbp-0x50], 0x21c1
  63:   00
  64:   48 c7 45 a8 e9 65 22    mov    QWORD PTR [rbp-0x58], 0x182265e9
  6b:   18
  6c:   48 c7 45 a0 33 08 00    mov    QWORD PTR [rbp-0x60], 0x833
  73:   00
  74:   48 c7 45 98 ab 0a 00    mov    QWORD PTR [rbp-0x68], 0xaab
  7b:   00
  7c:   48 c7 45 90 ad aa 8d    mov    QWORD PTR [rbp-0x70], 0x8daaad
  83:   00
  84:   48 8b 45 f8             mov    rax, QWORD PTR [rbp-0x8]
  88:   48 0f af 45 f0          imul   rax, QWORD PTR [rbp-0x10]
  8d:   48 89 45 88             mov    QWORD PTR [rbp-0x78], rax
  91:   48 8b 45 e8             mov    rax, QWORD PTR [rbp-0x18]
  95:   48 0f af 45 e0          imul   rax, QWORD PTR [rbp-0x20]
  9a:   48 0f af 45 d8          imul   rax, QWORD PTR [rbp-0x28]
  9f:   48 0f af 45 d0          imul   rax, QWORD PTR [rbp-0x30]
  a4:   48 0f af 45 c8          imul   rax, QWORD PTR [rbp-0x38]
  a9:   48 89 45 80             mov    QWORD PTR [rbp-0x80], rax
  ad:   48 8b 45 c0             mov    rax, QWORD PTR [rbp-0x40]
  b1:   48 0f af 45 b8          imul   rax, QWORD PTR [rbp-0x48]
  b6:   48 0f af 45 b0          imul   rax, QWORD PTR [rbp-0x50]
  bb:   48 0f af 45 a8          imul   rax, QWORD PTR [rbp-0x58]
  c0:   48 89 85 78 ff ff ff    mov    QWORD PTR [rbp-0x88], rax
  c7:   48 8b 45 a0             mov    rax, QWORD PTR [rbp-0x60]
  cb:   48 0f af 45 98          imul   rax, QWORD PTR [rbp-0x68]
  d0:   48 0f af 45 90          imul   rax, QWORD PTR [rbp-0x70]
  d5:   48 89 85 70 ff ff ff    mov    QWORD PTR [rbp-0x90], rax
  dc:   b8 00 00 00 00          mov    eax, 0x0
  e1:   c9                      leave
```

Not too much assembly, lets decompile it by hand.
```
   0:   55                      push   rbp
   1:   48 89 e5                mov    rbp, rsp
   4:   48 83 ec 18             sub    rsp, 0x18

Below is data initialization. It just set some value at stack
   8:   48 c7 45 f8 4f 00 00    mov    QWORD PTR [rbp-0x8], 0x4f
   f:   00
  10:   48 b8 15 4f e7 4b 01    movabs rax, 0x14be74f15
  17:   00 00 00
  1a:   48 89 45 f0             mov    QWORD PTR [rbp-0x10], rax
  1e:   48 c7 45 e8 04 00 00    mov    QWORD PTR [rbp-0x18], 0x4
  25:   00
  26:   48 c7 45 e0 03 00 00    mov    QWORD PTR [rbp-0x20], 0x3
  2d:   00
  2e:   48 c7 45 d8 13 00 00    mov    QWORD PTR [rbp-0x28], 0x13
  35:   00
  36:   48 c7 45 d0 15 01 00    mov    QWORD PTR [rbp-0x30], 0x115
  3d:   00
  3e:   48 b8 61 5b 64 4b cf    movabs rax, 0x77cf4b645b61
  45:   77 00 00
  48:   48 89 45 c8             mov    QWORD PTR [rbp-0x38], rax
  4c:   48 c7 45 c0 02 00 00    mov    QWORD PTR [rbp-0x40], 0x2
  53:   00
  54:   48 c7 45 b8 11 00 00    mov    QWORD PTR [rbp-0x48], 0x11
  5b:   00
  5c:   48 c7 45 b0 c1 21 00    mov    QWORD PTR [rbp-0x50], 0x21c1
  63:   00
  64:   48 c7 45 a8 e9 65 22    mov    QWORD PTR [rbp-0x58], 0x182265e9
  6b:   18
  6c:   48 c7 45 a0 33 08 00    mov    QWORD PTR [rbp-0x60], 0x833
  73:   00
  74:   48 c7 45 98 ab 0a 00    mov    QWORD PTR [rbp-0x68], 0xaab
  7b:   00
  7c:   48 c7 45 90 ad aa 8d    mov    QWORD PTR [rbp-0x70], 0x8daaad
  83:   00

Here comes the calculation
  84:   48 8b 45 f8             mov    rax, QWORD PTR [rbp-0x8]     ; rax = 0x4f
  88:   48 0f af 45 f0          imul   rax, QWORD PTR [rbp-0x10]    ; rax *= 0x14be74f15
  8d:   48 89 45 88             mov    QWORD PTR [rbp-0x78], rax    ; store the value of rax
  91:   48 8b 45 e8             mov    rax, QWORD PTR [rbp-0x18]    ; rax = 0x4
  95:   48 0f af 45 e0          imul   rax, QWORD PTR [rbp-0x20]    ; rax *= 0x3
  9a:   48 0f af 45 d8          imul   rax, QWORD PTR [rbp-0x28]    ; rax *= 0x13
  9f:   48 0f af 45 d0          imul   rax, QWORD PTR [rbp-0x30]    ; rax *= 0x115
  a4:   48 0f af 45 c8          imul   rax, QWORD PTR [rbp-0x38]    ; rax *= 0x77cf4b645b61
  a9:   48 89 45 80             mov    QWORD PTR [rbp-0x80], rax    ; store the value of rax
  ad:   48 8b 45 c0             mov    rax, QWORD PTR [rbp-0x40]    ; rax = 0x2
  b1:   48 0f af 45 b8          imul   rax, QWORD PTR [rbp-0x48]    ; rax *= 0x11
  b6:   48 0f af 45 b0          imul   rax, QWORD PTR [rbp-0x50]    ; rax *= 0x21c1
  bb:   48 0f af 45 a8          imul   rax, QWORD PTR [rbp-0x58]    ; rax *= 0x182265e9
  c0:   48 89 85 78 ff ff ff    mov    QWORD PTR [rbp-0x88], rax    ; store the value of rax
  c7:   48 8b 45 a0             mov    rax, QWORD PTR [rbp-0x60]    ; rax = 0x833
  cb:   48 0f af 45 98          imul   rax, QWORD PTR [rbp-0x68]    ; rax *= 0xaab
  d0:   48 0f af 45 90          imul   rax, QWORD PTR [rbp-0x70]    ; rax *= 0x8daaad
  d5:   48 89 85 70 ff ff ff    mov    QWORD PTR [rbp-0x90], rax    ; store the value of rax


  dc:   b8 00 00 00 00          mov    eax, 0x0
  e1:   c9                      leave
```

Basically it just do some multiplication then store the result on the stack in a consecutive addresses. So I tried replicate this process on python, then interpret all of the results as string.  
```py
rax = 0x4f
rax *= 0x14be74f15
var1 = rax

rax = 0x4
rax *= 0x3
rax *= 0x13
rax *= 0x115
rax *= 0x77cf4b645b61
var2 = rax

rax = 0x2
rax *= 0x11
rax *= 0x21c1
rax *= 0x182265e9
var3 = rax

rax = 0x833
rax *= 0xaab
rax *= 0x8daaad
var4 = rax

flag = hex(var1)[2:].decode('hex') + hex(var2)[2:].decode('hex') + hex(var3)[2:].decode('hex') + hex(var4)[2:].decode('hex')
print flag
```

flag{sup3r_v4l1d_pr0gr4m}