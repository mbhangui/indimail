/*
 * $Id: user.h,v 1.2 2019-07-15 12:57:00+05:30 Cprogrammer Exp mbhangui $
 */

void            adduser();
void            addusernow();
void            bounceall();
int             call_hooks(char *hook_type, char *p1, char *p2, char *p3, char *p4);
void            count_users();
void            deleteall();
void            ideluser();
void            delusergo();
void            delusernow();
int             get_catchall();
void            moduser();
void            modusergo();
void            modusernow();
void            parse_users_dotqmail(char newchar);
void            setremotecatchall();
void            setremotecatchallnow();
void            show_users();
int             show_user_lines(char *user, char *dom, time_t mytime, char *dir);
