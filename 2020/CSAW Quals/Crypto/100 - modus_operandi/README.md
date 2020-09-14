# modus_operandi
> 100 points  
> Can't play CSAW without your favorite block cipher!  
> nc crypto.chal.csaw.io 5001  

Here, we are given a service which ask for any input of any length. Then they encrypt it using either EBC or CBC block cipher. We need to "guess" for each iteration wether the block cipher being used is EBC or CBC.

It is easy since we can send any length of input of a same letter. The idea here is that they will split our input into blocks of plain text then encrypt each individual block. In EBC mode, if two plain text block has the same content, the cipher text generated will also be the same.

Also, after several times playing around with the input, I found that the sequence of EBC / CBC used is always the same. For example, the first iteration will always use EBC mode.

So first, we check this by sending a very very long input like:
```
Hello! For each plaintext you enter, find out if the block cipher used is ECB or CBC. Enter "ECB" or "CBC" to get the flag!
Enter plaintext:
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Ciphertext is:  3328282e39dec66b166030e456c1f2583328282e39dec66b166030e456c1f2583328282e39dec66b166030e456c1f2583328282e39dec66b166030e456c1f2583328282e39dec66b166030e456c1f2583328282e39dec66b166030e456c1f2583328282e39dec66b166030e456c1f2583328282e39dec66b166030e456c1f2583328282e39dec66b166030e456c1f2583328282e39dec66b166030e456c1f2583328282e39dec66b166030e456c1f2583328282e39dec66b166030e456c1f2581be91bef6543768445f822e640f59cac
```

Since We know that this cipher is encrypted using EBC block cipher, we can find any recurring pattern. And the first occurence is at index 32 (not hex decoded), so we know that if they are using EBC, cipher text from index 0 to 31 will be the same with ciphertext from index 32 to 63.  

After a bit trial and error, I found that there are only 176 iteration. Then there's no flag >:( .  
So after the competition is over, I read some write up and it turns out that the sequence of the answer is actually a binary digit (ECB == 0 and CBC == 1).

So I write this [script](ex.py) then the flag pops out.

flag{ECB_re@lly_sUck$}