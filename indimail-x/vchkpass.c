/*
 * $Log: vchkpass.c,v $
 * Revision 1.8  2021-01-27 13:23:25+05:30  Cprogrammer
 * use use_dovecot variable instead of env_get() twice
 *
 * Revision 1.7  2021-01-26 14:17:22+05:30  Cprogrammer
 * set HOME, userdb_uid, userdb_gid, EXTRA env variables for dovecot
 *
 * Revision 1.6  2021-01-26 13:45:03+05:30  Cprogrammer
 * modified to support dovecot checkpassword authentication
 *
 * Revision 1.5  2020-09-28 13:28:28+05:30  Cprogrammer
 * added pid in debug statements
 *
 * Revision 1.4  2020-09-28 12:49:53+05:30  Cprogrammer
 * print authmodule name in error logs/debug statements
 *
 * Revision 1.3  2020-04-01 18:58:32+05:30  Cprogrammer
 * moved authentication functions to libqmail
 *
 * Revision 1.2  2019-07-10 12:58:04+05:30  Cprogrammer
 * print more error information in print_error
 *
 * Revision 1.1  2019-04-18 08:14:23+05:30  Cprogrammer
 * Initial revision
 *
 */
#ifdef HAVE_CONFIG_H
#include "config.h"
#endif
#ifdef HAVE_CTYPE_H
#include <ctype.h>
#endif
#ifdef ENABLE_DOMAIN_LIMITS
#include <time.h>
#endif
#ifdef HAVE_UNISTD_H
#define _XOPEN_SOURCE
#include <unistd.h>
#endif
#ifdef HAVE_QMAIL
#include <alloc.h>
#include <stralloc.h>
#include <strerr.h>
#include <fmt.h>
#include <str.h>
#include <env.h>
#include <error.h>
#include <pw_comp.h>
#include <getEnvConfig.h>
#endif
#include "parse_email.h"
#include "sqlOpen_user.h"
#include "sql_getpw.h"
#include "vlimits.h"
#include "common.h"
#include "iopen.h"
#include "iclose.h"
#include "inquery.h"
#include "pipe_exec.h"
#include "indimail.h"
#include "variables.h"
#include "runcmmd.h"

#ifndef lint
static char     sccsid[] = "$Id: vchkpass.c,v 1.8 2021-01-27 13:23:25+05:30 Cprogrammer Exp mbhangui $";
#endif

#ifdef AUTH_SIZE
#undef AUTH_SIZE
#define AUTH_SIZE 512
#else
#define AUTH_SIZE 512
#endif

int             authlen = AUTH_SIZE;

void
print_error(char *str)
{
	out("vchkpass", "454-");
	out("vchkpass", str);
	out("vchkpass", ": ");
	out("vchkpass", error_str(errno));
	out("vchkpass", " (#4.3.0)\r\n");
	flush("vchkpass");
}

static void
die_nomem()
{
	strerr_warn1("vchkpass: out of memory", 0);
	_exit(111);
}

int
main(int argc, char **argv)
{
	char           *authstr, *login, *ologin, *response, *challenge, *crypt_pass, *ptr, *cptr;
	char            strnum[FMT_ULONG], module_pid[FMT_ULONG];
	static stralloc user = {0}, fquser = {0}, domain = {0}, buf = {0};
	int             i, count, offset, norelay = 0, status, auth_method, use_dovecot;
	struct passwd  *pw;
#ifdef ENABLE_DOMAIN_LIMITS
	time_t          curtime;
	struct vlimits  limits;
#endif

	if (argc < 2)
		_exit(2);
	if (!(authstr = alloc((authlen + 1) * sizeof(char)))) {
		print_error("out of memory");
		strnum[fmt_uint(strnum, (unsigned int) authlen + 1)] = 0;
		strerr_warn3("alloc-", strnum, ": ", &strerr_sys);
		_exit(111);
	}
	for (offset = 0;;) {
		do {
			count = read(3, authstr + offset, authlen + 1 - offset);
#ifdef ERESTART
		} while (count == -1 && (errno == EINTR || errno == ERESTART));
#else
		} while (count == -1 && errno == EINTR);
#endif
		if (count == -1) {
			print_error("read error");
			strerr_warn1("syspass: read: ", &strerr_sys);
			_exit(111);
		} else
		if (!count)
			break;
		offset += count;
		if (offset >= (authlen + 1))
			_exit(2);
	}
	count = 0;
	login = authstr + count; /*- username */
	for (;authstr[count] && count < offset;count++);
	if (count == offset || (count + 1) == offset)
		_exit(2);

	count++;
	challenge = authstr + count; /*- challenge (or plain text) */
	for (;authstr[count] && count < offset;count++);
	if (count == offset || (count + 1) == offset)
		_exit(2);

	count++;
	response = authstr + count; /*- response (cram-md5, cram-sha1, etc) */
	for (; authstr[count] && count < offset; count++);
	if (count == offset || (count + 1) == offset)
		auth_method = 0;
	else
		auth_method = authstr[count + 1];

	ologin = login;
	for (ptr = login; *ptr && *ptr != '@'; ptr++);
	if (!*ptr) { /*- no @ in the login */
		if (auth_method == AUTH_DIGEST_MD5) { /*- for handling dumb programs like
												outlook written by dumb programmers */
			if ((ptr = str_str(login, "realm="))) {
				ptr += 6;
				for (i = 0, cptr = ptr; *ptr && *ptr != ','; ptr++) {
					if (isspace(*ptr) || *ptr == '\"')
						continue;
					i++;
				}
				if (!stralloc_ready(&domain, i + 1))
					die_nomem();
				for (i = 0, ptr = cptr; *ptr && *ptr != ','; ptr++) {
					if (isspace(*ptr) || *ptr == '\"')
						continue;
					domain.s[i++] = *ptr;
				}
				domain.len = i;
				if (!stralloc_0(&domain))
					die_nomem();
				domain.len--;
				for (i = 0, ptr = login; *ptr && *ptr != '@'; i++, ptr++);
				if (!stralloc_copyb(&fquser, login, i) ||
						!stralloc_append(&fquser, "@") ||
						!stralloc_cat(&fquser, &domain) ||
						!stralloc_0(&fquser))
					die_nomem();
				login = fquser.s;
			}
		}
	}
	if (!env_unset("HOME"))
		die_nomem();
	use_dovecot = env_get("DOVECOT_VERSION") ? 1 : 0;
	if (use_dovecot) {
		if (!env_unset("userdb_uid") || !env_unset("userdb_gid") ||
				!env_unset("EXTRA"))
			die_nomem();
	}
	parse_email(login, &user, &domain);
#ifdef QUERY_CACHE
	if (!env_get("QUERY_CACHE")) {
#ifdef CLUSTERED_SITE
		if (sqlOpen_user(login, 0))
#else
		if (iopen((char *) 0))
#endif
		{
			if (userNotFound)
				use_dovecot ? _exit (1) : pipe_exec(argv, authstr, offset);
			else
#ifdef CLUSTERED_SITE
				strerr_warn1("sqlOpen_user: failed to connect to db: ", &strerr_sys);
#else
				strerr_warn1("iopen: failed to connect to db: ", &strerr_sys);
#endif
			out("vchkpass", "454-failed to connect to database (");
			out("vchkpass", error_str(errno));
			out("vchkpass", ") (#4.3.0)\r\n");
			flush("vchkpass");
			_exit (111);
		}
		pw = sql_getpw(user.s, domain.s);
		iclose();
		ptr = "sql_getpw";
	} else {
		pw = inquery(PWD_QUERY, login, 0);
		ptr = "inquery";
	}
#else
#ifdef CLUSTERED_SITE
	if (sqlOpen_user(login, 0))
#else
	if (iopen((char *) 0))
#endif
	{
		if (userNotFound)
			use_dovecot ? _exit (1) : pipe_exec(argv, authstr, offset);
		else
#ifdef CLUSTERED_SITE
			strerr_warn1("sqlOpen_user: failed to connect to db: ", &strerr_sys);
#else
			strerr_warn1("iopen: failed to connect to db: ", &strerr_sys);
#endif
		out("vchkpass", "454-failed to connect to database (");
		out("vchkpass", error_str(errno));
		out("vchkpass", ") (#4.3.0)\r\n");
		flush("vchkpass");
		_exit (111);
	}
	pw = sql_getpw(user.s, domain.s);
	ptr = "sql_getpw";
	iclose();
#endif
	if (!pw) {
		if (userNotFound)
			use_dovecot ? _exit (1) : pipe_exec(argv, authstr, offset);
		else
			strerr_warn3("vchkpass: ", ptr, ": ", &strerr_sys);
		print_error(ptr);
		_exit (111);
	} else
	if (pw->pw_gid & NO_SMTP) {
		out("vchkpass", "553-Sorry, this account cannot use SMTP (#5.7.1)\r\n");
		flush("vchkpass");
		_exit (1);
	} else
	if (is_inactive && !env_get("ALLOW_INACTIVE")) {
		out("vchkpass", "553-Sorry, this account is inactive (#5.7.1)\r\n");
		flush("vchkpass");
		_exit (1);
	} else
	if (pw->pw_gid & NO_RELAY)
		norelay = 1;
	crypt_pass = pw->pw_passwd;
	strnum[fmt_uint(strnum, (unsigned int) auth_method)] = 0;
	module_pid[fmt_ulong(module_pid, getpid())] = 0;
	if (env_get("DEBUG_LOGIN"))
		strerr_warn14("vchkpass", "pid [", module_pid, ": login [", login, "] challenge [", challenge,
			"] response [", response, "] pw_passwd [", crypt_pass, "] method [", strnum, "]", 0);
	else
	if (env_get("DEBUG"))
		strerr_warn8("vchkpass", "pid [", module_pid, ": login [", login, "] method [", strnum, "]", 0);
	if (pw_comp((unsigned char *) ologin, (unsigned char *) crypt_pass,
		(unsigned char *) (*response ? challenge : 0),
		(unsigned char *) (*response ? response : challenge), auth_method)) {
		use_dovecot ? _exit (1) : pipe_exec(argv, authstr, offset);
		print_error("exec");
		_exit (111);
	}
#ifdef ENABLE_DOMAIN_LIMITS
	if (env_get("DOMAIN_LIMITS")) {
		struct vlimits *lmt;
#ifdef QUERY_CACHE
		if (!env_get("QUERY_CACHE")) {
			if (vget_limits(domain.s, &limits)) {
				strerr_warn2("vchkpass: unable to get domain limits for for ", domain.s, 0);
				out("vchkpass", "454-unable to get domain limits for ");
				out("vchkpass", domain.s);
				out("vchkpass", "\r\n");
				flush("vchkpass");
				_exit (111);
			}
			lmt = &limits;
		} else
			lmt = inquery(LIMIT_QUERY, login, 0);
#else
		if (vget_limits(domain.s, &limits)) {
			strerr_warn2("vchkpass: unable to get domain limits for for ", domain.s, 0);
			out("vchkpass", "454-unable to get domain limits for ");
			out("vchkpass", domain.s);
			out("vchkpass", "\r\n");
			flush("vchkpass");
			_exit (111);
		}
		lmt = &limits;
#endif
		curtime = time(0);
		if (lmt->domain_expiry > -1 && curtime > lmt->domain_expiry) {
			out("vchkpass", "553-Sorry, your domain has expired (#5.7.1)\r\n");
			flush("vchkpass");
			_exit (1);
		} else
		if (lmt->passwd_expiry > -1 && curtime > lmt->passwd_expiry) {
			out("vchkpass", "553-Sorry, your password has expired (#5.7.1)\r\n");
			flush("vchkpass");
			_exit (1);
		} 
	}
#endif
	status = 0;
	if (!env_put2("HOME", pw->pw_dir))
		die_nomem();
	if ((ptr = (char *) env_get("POSTAUTH")) && !access(ptr, X_OK)) {
		if (!stralloc_copys(&buf, ptr) ||
				!stralloc_append(&buf, " ") ||
				!stralloc_cats(&buf, login) ||
				!stralloc_0(&buf))
			die_nomem();
		status = runcmmd(buf.s, 0);
	}
	if (use_dovecot) { /*- support dovecot checkpassword */
		if (!env_put2("userdb_uid", "indimail") ||
				!env_put2("userdb_gid", "indimail"))
			die_nomem();
		if ((ptr = env_get("EXTRA"))) {
			if (!stralloc_copyb(&buf, "userdb_uid userdb_gid ", 22) ||
					!stralloc_cats(&buf, ptr) || !stralloc_0(&buf))
				die_nomem();
		} else
		if (!stralloc_copyb(&buf, "userdb_uid userdb_gid", 21) ||
				!stralloc_0(&buf))
			die_nomem();
		if (!env_put2("EXTRA", buf.s))
			die_nomem();
		execv(argv[1], argv + 1);
		print_error("exec");
		_exit (111);
	}
	_exit(norelay ? 3 : status);
	/*- Not reached */
	return(0);
}
