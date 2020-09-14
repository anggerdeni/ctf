# ezbreezy
> 100 points  
> This [binary](app) has nothing to hide!

I tried opening the binary in ghidra. And the first thing that caught my eyes is this strange section named `.aj1ishudgqis` which contains a bunch of code that does nothing but setting registers and stack.

Collecting the value which is stored in register result in this:
'\x8e\x94\x89\x8f\xa3\x9d\x87\x90\x5c\x9e\x5b\x87\x9a\x5b\x8b\x58\x9e\x5b\x9a\x5b\x8c\x87\x95\x5b\xa5'

I tried xor ing it, play around with it, but doesn't come up with any idea. Then I read a write up that says we only need to substract each value by 0x28.

```
>>> f = bytearray('\x8e\x94\x89\x8f\xa3\x9d\x87\x90\x5c\x9e\x5b\x87\x9a\x5b\x8b\x58\x9e\x5b\x9a\x5b\x8c\x87\x95\x5b\xa5')
>>> for i in range(len(f)):
...  f[i] = f[i] - 0x28
...
>>> f
bytearray(b'flag{u_h4v3_r3c0v3r3d_m3}')
```

flag{u_h4v3_r3c0v3r3d_m3}