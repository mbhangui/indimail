# Introduction

[pam-multi](https://github.com/mbhangui/indimail-virtualdomains/tree/master/pam-multi-x) helps you to extend authentication of an existing pam-module (e.g. courier-imap, dovecout, cyrus, etc) to transparently authenticate against [IndiMail's](https://github.com/mbhangui/indimail-virtualdomains) own MySQL database. The primary goal of pam-multi was to allow authentication of IMAP/POP3 servers like courier-imap, dovecot against IndiMail MySQL database. In short, pam-multi provides a pam service, which is configurable to look at any datasource. IndiMail uses pam-multi to make possible usage of any IMAP/POP3 server with IndiMail's database, without modifying a single line of code in the IMAP/POP3 server.  see the man page pam-multi

pam-multi supports four methods for password hashing schemes.

`crypt (DES), MD5, SHA256, SHA512.`

To use pam-multi for your application (which currently uses PAM), you need to modify the PAM configuration file for that application. The following options are supported in configuration file in /etc/pam.d.  See man pam-multi(8) for more details.

All that is needed is for you is to configure the appropriate command which returns an encrypted password for the user. pam-multi will encrypt the plain text password given by the user and compare it with the result fetched by one of the three configured method. If the encrypted password matches, access will be granted. The comparision will utilize one of the four hashing schemes.

* $1$ .. MD5
* $5$ .. SHA256
* $6$ .. SHA512

anything else than above, the hashing scheme will be DES

Three methods are supported for fetching the encrypted password from your database

```
-m sql_statement
   MySQL mode. You will need to specify -u, -p, -d, -H and -P options.
   It is expected that the sql_statement will return a row containing
   the encrypted password for the user.

-c command
   Command mode. pam-multi will do sh -c "command". It is expected that
   the output of the command will be an encrypted password.

-s shared_library
   Library Mode. pam-multi will dynamically load the shared library. It is
   expected for the library to provide the function

   `char *iauth(char *email, char *service)`

   The function iauth() will be passed arguments username, service
   argument denoting the name of service. The service argument will be
   used only for identification purpose. It is expected for the function
   to return a string containing the encrypted password. An example shared
   library iauth.so has been provided in the package. authenticate.so has
   a iauth() function to authenticate against IndiMail's database.
```

The following tokens if present in command string or the sql string (-m or -c options),
will be replaced as follows

* %u - Username
* %d - Domain

A checkpassword compatible program **pam-checkpwd** has been provided in the package. pam-checkpwd can use pam-multi as well as any existing pam service on your system. See man pam-checkpwd(8) for more details.

## Examples

### System PAM Configuration

If you want an existing application on your system which uses PAM to use pam-multi, you will neeed to modify the configuration file which your application uses to have any one of the three options below.

```
1. auth optional pam-multi.so args -m [select pw\_passwd from indimail where pw\_name=’%u’ and pw\_domain=’%d’] -u indimail -p ssh-1.5- -d indimail -H localhost -P 3306
2. auth optional pam-multi.so args -c [grep "^%u:" /etc/passwd | awk -F: ’{print $2}’]
3. auth optional pam-multi.so args -s /var/indimail/modules/iauth.so
```
NOTE: Read the **pam**(8) man page to cconfigure your PAM

### Config /etc/pam.d/pam-multi

```
#
# auth     required  pam-multi.so args -m [select pw_passwd from indimail where pw_name='%u' and pw_domain='%d'] -u indimail -p ssh-1.5- -D indimail -H localhost -P 3306 -d
# auth     required  pam-multi.so args -s /var/indimail/modules/iauth.so -d
# account  required  pam-multi.so args -d
# account  required  pam-multi.so args -s /var/indimail/modules/iauth.so -d
#
auth     required  pam-multi.so args -s /var/indimail/modules/iauth.so
account  required  pam-multi.so args -s /var/indimail/modules/iauth.so
#pam_selinux.so close should be the first session rule
session  required  pam_selinux.so close
#pam_selinux.so  open should only be followed by sessions to be executed in the user context
session  required  pam_selinux.so open env_params
session  optional  pam_keyinit.so force revoke
```

NOTE: Any line starting with `#` is a comment

## TESTING

```
printf "user01@example.com\0pass\0\0" | pam-checkpwd -s pam-multi -e -- /usr/bin/id 3<&0
```

pam-multi is experimental at this stage. It is covered under GNU GPL V3 license and no warranty is implied. Suggestions to improve it are welcome.