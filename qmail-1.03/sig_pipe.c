/*
 * $Log: sig_pipe.c,v $
 * Revision 1.3  2004-10-22 20:30:26+05:30  Cprogrammer
 * added RCS id
 *
 * Revision 1.2  2004-07-17 21:23:15+05:30  Cprogrammer
 * added RCS log
 *
 */
#include <signal.h>
#include "sig.h"

void
sig_pipeignore()
{
	sig_catch(SIGPIPE, SIG_IGN);
}

void
sig_pipedefault()
{
	sig_catch(SIGPIPE, SIG_DFL);
}

void
getversion_sig_pipe_c()
{
	static char    *x = "$Id: sig_pipe.c,v 1.3 2004-10-22 20:30:26+05:30 Cprogrammer Stab mbhangui $";

	x++;
}
