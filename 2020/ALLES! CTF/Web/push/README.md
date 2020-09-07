# push
> Difficulty: Easy  
> Author: Flo

[https://push.ctf.allesctf.net](https://push.ctf.allesctf.net)

There is no hint and nothing at all. Visiting the website gives us nothing but a marquee text.

Then I tried to do a request using curl:
```
root@c96f122d9031:/# curl -I https://push.ctf.allesctf.net
HTTP/2 200 
server: nginx/1.14.1
date: Mon, 07 Sep 2020 16:46:51 GMT
content-type: text/html
content-length: 26
last-modified: Thu, 03 Sep 2020 21:02:18 GMT
etag: "5f5159da-1a"
accept-ranges: bytes
```

The website is running on nginx and is using HTTP/2. Then I do a little research on this using the keyword `nginx push` and come across this website: [https://www.nginx.com/blog/nginx-1-13-9-http2-server-push/](https://www.nginx.com/blog/nginx-1-13-9-http2-server-push/)

> Server push, which is defined in the HTTP/2 specification, allows a server to pre‑emptively push resources to a remote client, anticipating that the client may soon request those resources. By doing so, you can potentially reduce the number of RTTs (round trip time – the time needed for a request and response) in a page‑load operation by one RTT or more, providing faster response to the user. 

Then I assume the server is serving flag file pre-emptively without us noticing. As mentioned [here](https://github.com/0x13A0F/CTF_Writeups/tree/master/alles_ctf), most nowadays tools and proxies like Burp doesn't support HTTP/2, that's why no matter what proxy you use, you can't see the hidden requests.

I followed the tutorial [here](https://www.nginx.com/blog/nginx-1-13-9-http2-server-push/) on how to verify HTTP/2 Server Push, by using `nghttp2` ([installation](https://zoomadmin.com/HowToInstall/UbuntuPackage/nghttp2))

And here is the output of the command: `nghttp -ans https://push.ctf.allesctf.net`.
```
root@c96f122d9031:/# nghttp -ans https://push.ctf.allesctf.net
***** Statistics *****

Request timing:
  responseEnd: the  time  when  last  byte of  response  was  received
               relative to connectEnd
 requestStart: the time  just before  first byte  of request  was sent
               relative  to connectEnd.   If  '*' is  shown, this  was
               pushed by server.
      process: responseEnd - requestStart
         code: HTTP status code
         size: number  of  bytes  received as  response  body  without
               inflation.
          URI: request URI

see http://www.w3.org/TR/resource-timing/#processing-model

sorted by 'complete'

id  responseEnd requestStart  process code size request path
 13   +223.39ms        +85us 223.31ms  200   26 /
  2   +224.56ms *  +194.93ms  29.63ms  200   32 /flag_3a51b14e2e408ad9ae23d5f1e59f22147c5fc336d7874a7b06905c60cc629bab.txt
```

As we can see, the server does serve a txt file named `flag_3a51b14e2e408ad9ae23d5f1e59f22147c5fc336d7874a7b06905c60cc629bab.txt`, the next step is to simply grab the file by visiting [https://push.ctf.allesctf.net/flag_3a51b14e2e408ad9ae23d5f1e59f22147c5fc336d7874a7b06905c60cc629bab.txt](https://push.ctf.allesctf.net/flag_3a51b14e2e408ad9ae23d5f1e59f22147c5fc336d7874a7b06905c60cc629bab.txt)


Flag: ALLES{http2_push_dashdash_force}