# Perfect Secrecy
> 50 points  
> Alice sent over a couple of images with sensitive information to Bob, encrypted with a pre-shared key. It is the most secure encryption scheme, theoretically...  

We are given two images: [image1.png](image1.png) and [image2.png](image2.png).  

```
image1.png: PNG image data, 256 x 256, 1-bit grayscale, non-interlaced
image2.png: PNG image data, 256 x 256, 1-bit grayscale, non-interlaced
```

Inspecting the file, there are not so many different pixels in those images, so I come up with an idea to try using stegsolve to combine / xor those image. And the result shows an image with flag.  

Or, we can implement our own method to do this using python: 
```py
# pip install pillow
from PIL import Image
from pwn import xor
img1 = Image.open('image1.png')
img2 = Image.open('image2.png')
dat1 = list(img1.getdata())
dat2 = list(img2.getdata())

new_dat = xor(dat1,dat2)
new_img = Image.new(mode = '1', size = (256,256))
new_img.putdata(new_dat)
new_img.save('result.png')
```

flag{0n3_t1m3_P@d!}