FSSOS stands for Flexible Single Sign-On Solution and
has been written by Ben Goodwin.

[Official website](http://fssos.sourceforge.net/)

This source has been hacked and adapted to indimail as nssd from the FSSOS site. The hacked source will also work with vpopmail by just changing the configuration file nssd.conf

nssd is experimental and without warranty.

The hacked source can be downloaded from [here](https://github.com/mbhangui/indimail-virtualdomains/tree/master/nssd-x)

nssd has been modified to have user and domain in the query e.g.

mbhangui@indimail.org gets split into mbhangui as the user and indimail.org as the domain.

This split allows authentication against IndiMail's MySQL database. By just changing the configuration, authentication should also work for vpopmail. The other change made to nssd, is to make the Name Service Switch daemon supervise friendly.

You may also want to look at the wonderful original code written by Ben.

You may find this of use if you want to run a IMAP/POP3 server which does not yet have support for IndiMail or vpopmail

nssd allows many IMAP/POP3 servers, which use getpwnam(), getspnam(), PAM, etc to authenticate against IndiMail's database without making a single change to the IMAP/POP3 server code.  This gives a Yet Another Way to have courier-imap, dovecot, etc to authenticate against your own custom MySQL database.

## NSSD - Name Service Switch Daemon

Supported Operating Systems:

    * Linux (glibc >= 2.2.5)
    * Solaris (Sparc or Intel >= 8) (SEE NOTE BELOW)
    * FreeBSD (5.1+, prefer 5.2+)   (SEE NOTE BELOW)

Supported MySQL Versions:

    * MySQL 3.23.9 - 6.0.3-alpha

Supported Compilers:

    * GCC (2.95.2, 3.x)

## Prerequisites

* Installing from source:

  * A functional compile environment (system headers, gcc, ...)
  * MySQL client library & header files (local)
  * MySQL server (local or remote)

## INSTALLATION DETAILS

If installing from source:

```
$ cd /usr/local/src
$ git clone https://github.com/mbhangui/indimail-virtualdomains.git
$ cd /usr/local/src/indimail-virtualdomains/nssd-x
$ ./default.configure
$ make
$ sudo make install-strip
```

On some systems, libtool insists on adding "-lc" to the link stage (due to the way gcc was built for that system), which breaks nssd threading in daemon mode.  If you see a "-lc" before a "-pthread" or "-lpthread", then you're in trouble.  You'll notice the broken behavior in the form of fewer-than-expected threads running (3) and the inability to kill the parent process off without a "-9" signal. To fix this, do the following:

`PTRHEAD_LIBS="-lpthread -lc" ./configure`

and then run make/make install.

If your MySQL installation is based in a strange directory, use
the --with-mysql=DIR option of ./configure to specify.  For example,

`./configure --with-mysqlprefix=/usr/local`

* Edit /etc/indimail/nssd.conf (or /var/vpopmail/etc/nssd.conf) You will find nssd.conf in samples directory of the source

* Edit (or create) /etc/nsswitch.conf such that it contains at least the following:

  ```
  passwd: files nssd
  shadow: files nssd
  ```

  If you don't want groups from MySQL, simply don't include 'nssd' in in the 'group' line.

* Start 'nssd' (e.g. "/usr/sbin/nssd" )

  For vpopmail, you need to have nssd run either by supervise or by your favourite method (rc, etc)
  For IndiMail, to install a supervise service, run the svctool command

  ```
  # /usr/sbin/svctool --pwdlookup="/run/indimail/nssd.sock"
      --threads="5" --timeout="-1" --mysqlhost="localhost"
      --mysqluser="indimail" --mysqlpass="ssh-1.5-"
      --mysqlsocket="/var/run/mysqld/mysqld.sock"
      --servicedir="/service"
  ```

  The above command will create /service/pwlookup/run as below

  ```
  #!/bin/sh
  # $Id: svctool.in,v 2.478 2020-05-24 23:55:49+05:30 Cprogrammer Exp mbhangui $
  # generated on x86_64-pc-linux-gnu on Monday 25 May 2020 06:35:11 PM IST
  # /usr/sbin/svctool --pwdlookup="/run/indimail/nssd.sock" --threads="5" --timeout="-1" --mysqlhost="localhost" --mysqluser="indimail" --mysqlpass="ssh-1.5-" --mysqlsocket="/var/run/mysqld/mysqld.sock" --servicedir="/service"

  if [ -d /run ] ; then
    mkdir -p /run/indimail
    chown indimail:indimail /run/indimail
    chmod 775 /run/indimail
  elif [ -d /var/run ] ; then
    mkdir -p /var/run/indimail
    chown indimail:indimail /var/run/indimail
    chmod 775 /var/run/indimail
  fi
  exec 2>&1
  exec /usr/bin/envdir /service/pwdlookup/variables \
      /usr/bin/setuidgid indimail /usr/sbin/nssd -d notice
  ```

* Test pwlookup using a virtual user configured in indimail/vpopmail
  `# /usr/libexec/indimail/check_getpw user@domain`

## NOTE

This version has been packaged as part of [indimail-auth package](https://github.com/mbhangui/indimail-virtualdomains)

Send all bug reports to indimail-auth@indimail.org 