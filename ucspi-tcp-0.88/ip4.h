/*
 * $Log: ip4.h,v $
 * Revision 1.3  2005-06-10 09:18:13+05:30  Cprogrammer
 * added for ipv6 support
 *
 * Revision 1.2  2005-05-13 23:45:39+05:30  Cprogrammer
 * code indentation
 *
 * Revision 1.1  2003-12-31 19:57:33+05:30  Cprogrammer
 * Initial revision
 *
 */
#ifndef IP4_H
#define IP4_H

extern char     ip4loopback[4]; /* = {127,0,0,1}; */
unsigned int    ip4_scan(char *, char *);
unsigned int    ip4_fmt(char *, char *);

#define IP4_FMT 20

#endif
