# legrand-lc7001
Proof of Concept to authenticate to Legrand Hub LC7001

Latest LC7001 firmware update added authentication and broke a few integrations with the Hub. After talking to Legrand Technical team and explaining the situation they agreed and sent me some documents explaining how the authentication is handled.

I implemented this POC in Python 3 to test it out and so far as today it works perfectly.

```bash
$ ./legrand.py
Socket Created
Socket Connected to LCM1.local on ip 192.168.1.112
Challenge: 51C8D6C53A0DF927FF01F03E46575E26
Encrypted Response C4CF376EE064BDF2529FDAAD361B7DB6
[OK]

{"ID":0,"Service":"ping","CurrentTime":1605076627,"PingSeq":1,"Status":"Success"}
```
