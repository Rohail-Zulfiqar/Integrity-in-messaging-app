It consists of client and server files. Server is running on port 5555 on localhost. clients get connected to the server through this port and get assigned the names in increasing
order of client1, client2 and so on. also, server will assign random ports to the clients and maintain a dictionary of client names and its dictionaries.
First use the files only 'c.py' and 's.py'. First run the server file and then run multiple clients in different terminals. in this case we have two clients client1 and client2. 
Then type recipient and it will send message to that recipient message and it will send that message. 

now you can check the attack procedure by running the mitmserver.py file along with c1.py and s1.py. It shows that client is actually connected to mintm server and it will forward the 
message to recipient client. It has 4 option to change the message in different ways, every time it changes the message client will get notified by showing that message may be tempered 
compromising the integrity.


Terminology used in this project are thread computing, socket programming, hashing and client & server protocol mechanism.
