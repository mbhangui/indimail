# indimail
Messaging Platform based on qmail for MTA Virtual Domains, Courier-IMAP for IMAP/POP3

Look at indimail-3.x/doc/README for details. indimail needs indimail-mta to be installed. Look at
https://github.com/mbhangui/indimail-mta
for details on installing indimail-mta

Look at indimail-3.x/doc/INSTALL for Source Installation instructions

# Compile libqmail-0.1
```
$ cd /usr/local/src
$ git clone https://github.com/mbhangui/libqmail-0.1.git
$ cd /usr/local/src/libqmail-0.1
$ ./default.configure
$ make
$ sudo make install-strip
```

# Download indimail, indimail-mta and components
```
$ cd /usr/local/src
$ git clone https://github.com/mbhangui/indimail-virtualdomains.git
$ git clone https://github.com/mbhangui/indimail-mta.git
```

# Compile libdkim-1.4 (with dynamic libaries)
```
$ cd /usr/local/src/indimail-mta/libdkim-1.4
$ ./default.configure
$ make
$ sudo make -s install-strip
```

# Compile libsrs2-1.0.18 (with dynamic libaries)
```
$ cd /usr/local/src/indimail-mta/libsrs2-1.0.18
$ ./defaualt.configure
$ make
$ sudo make install-strip
```

# Build ucspi-tcp-0.88 (with all patches applied)
```
$ cd /usr/local/src/indimail-mta/ucspi-tcp-0.88
$ make
$ sudo make install-strip
```

# Build bogofilter
```
$ cd /usr/local/src/indimail-virtualdomains/bogofilter-1.2.4
$ ./defaualt.configure
$ make
$ sudo make install-strip
```

# Build bogofilter-wordlist
```
$ cd /usr/local/src/indimail-virtualdomains/bogofilter-wordlist-1.0
$ ./defaualt.configure
$ make
$ sudo make install-strip
```

# Build indimail-mta-2.x
(here x is the release)
```
$ cd /usr/local/src/indimail-mta/indimail-mta-2.x
$ make
$ sudo make install-strip
$ sudo sh ./svctool --config=users --nolog
```

# Build indimail-3.x
```
$ cd /usr/local/src/indimail-virtualdomains/indimail-3.0
$ ./default.configure
$ make
$ sudo make install-strip
```

# Build courier-imap
```
$ cd /usr/local/src/indimail-virtualdomains/courier-imap-5.0.7
$ ./default.configure
$ sudo make install-strip
```

# Build nssd
```
$ cd /usr/local/src/indimail-virtualdomains/nssd-1.1
$ ./default.configure
$ make
$ sudo make install-strip
```

# Setup & Configuration

Setup (this uses svctool a general purpose utility to configure indimail-mta
services. The create_services is a shell script which uses svctool to setup
indimail-mta. It will also put a systemd unit file indimail.service in
/lib/systemd/system

```
$ cd /usr/local/src/indimail-mta/indimail-mta-2.7
$ sudo sh ./create_services --servicedir=/services --mysqlPrefix=/usr
$ sudo service indimail start
```

or

```
$ /etc/init.d/indimail start
```

or

```
$ /usr/bin/qmailctl start
```

# Binary Builds
You can get binary RPM / Debian packages at

Stable Releases       - http://download.opensuse.org/repositories/home:/indimail/

Experimental Releases - http://download.opensuse.org/repositories/home:/mbhangui/

If you want to use DNF / YUM / apt-get, the corresponding install instructions for the two repositories are at

https://software.opensuse.org/download.html?project=home%3Aindimail&package=indimail

&

https://software.opensuse.org/download.html?project=home%3Ambhangui&package=indimail

```
Currently, the list of supported distributions for IndiMail is

    * SUSE
          o openSUSE_Leap_15.0
          o openSUSE_Leap_15.1
          o openSUSE_Leap_15.2
		  o openSUSE_Tumbleweed
          o SUSE Linux Enterprise 15
          o SUSE Linux Enterprise 15 SP1

    * Red Hat
          o Fedora 30
          o Fedora 31
          o Red Hat Enterprise Linux 6
          o Red Hat Enterprise Linux 7
          o CentOS 6
          o CentOS 7

    * Debian
          o Debian 7.0
          o Debian 8.0
          o Debian 9.0
          o Ubuntu 16.04
          o Ubuntu 17.04
          o Ubuntu 18.04
          o Ubuntu 19.04
          o Ubuntu 19.10
```

# Docker / Podman Repository
The docker repository for indimail is at

https://hub.docker.com/r/cprogrammer/indimail

for Docker
```
docker pull cprogrammer/indimail:tag
```
or

for Podman
```
podman pull cprogrammer/indimail:tag
```

where tag is one of

xenial   for ubuntu 16.04

bionic   for ubuntu 18.04

disco    for ubuntu 19.04

centos7  for centos7

debian8  for debian8

debian9  for debian9

debian10 for debian10

fc31     for fc31

fc30     for fc30
