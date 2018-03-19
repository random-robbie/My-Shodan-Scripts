ETCD..... Dumper
-----------


Inspired by https://elweb.co/the-security-footgun-in-etcd/

I wrote this script to dump the results so that you can grep through them later to find all the little secrets you want.

it basically does 

```
GET http://<ip address>:2379/v2/keys/?recursive=true
```