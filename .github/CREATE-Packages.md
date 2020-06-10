# Build Binary Packages

## Clone git repository

```
$ cd /usr/local/src
$ git clone https://github.com/mbhangui/libqmail.git
$ git clone https://github.com/mbhangui/indimail-virtualdomains.git
$ git clone https://github.com/mbhangui/indimail-mta.git
```

## Build indimail-mta package

```
$ cd /usr/local/src/indimail-mta/indimail-mta-x
$ ./create_rpm    # for RPM
or
$ ./create_debian # for deb
```

## Build indimail-auth package
```
$ cd /usr/local/src/indimail-virtualdomains/indimail-auth
$ ./create_rpm    # for RPM
or
$ ./create_debian # for deb
```

## Build indimail-access package
```
$ cd /usr/local/src/indimail-virtualdomains/indimail-access
$ ./create_rpm    # for RPM
or
$ ./create_debian # for deb
```

## Build indimail-utils package
```
$ cd /usr/local/src/indimail-virtualdomains/indimail-utils
$ ./create_rpm    # for RPM
or
$ ./create_debian # for deb
```

## Build indimail-spamfilter package
```
$ cd /usr/local/src/indimail-virtualdomains/bogofilter-x
$ ./create_rpm    # for RPM
or
$ ./create_debian # for deb
```

## Build indimail-virtualdomains package
```
$ cd /usr/local/src/indimail-virtualdomains/indimail-x
$ ./create_rpm    # for RPM
or
$ ./create_debian # for deb
```