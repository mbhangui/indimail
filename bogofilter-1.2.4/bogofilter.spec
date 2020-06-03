#
#
# $Id: indimail.spec.in,v 1.42 2020-06-02 22:38:20+05:30 Cprogrammer Exp mbhangui $
%undefine _missing_build_ids_terminate_build
%global _unpackaged_files_terminate_build 1

%if %{defined _project}
# define if building on openSUSE build service
%global build_on_obs       1
%global reconfigure_mode   0
%global reconf_bogofilter  0
%global build_cflags       "-DOBS_BUILD %{build_cflags}"
%else
%define _project           local
%global build_on_obs       0
%global reconfigure_mode   0
%global reconf_bogofilter  0
%global _hardened_build    1
%endif

%global _prefix            /usr
%global servicedir         /service
%global sysconfdir         /etc/indimail
%global libexecdir         %{_prefix}/libexec/indimail
%global shareddir          %{_prefix}/share/indimail
%global mandir             %{_prefix}/share/man
%global url                https://github.com/mbhangui/indimail-virtualdomains
%if 0%{?suse_version}
%global noperms            1
%else
%global noperms            0
%endif

%if %build_on_obs == 1
%global packager Manvendra Bhangui <indimail-spamfilter@indimail.org>
%endif

Summary: Fast anti-spam filtering by Bayesian statistical analysis
Name: bogofilter
Version: 1.2.4
Release: 1.1%{?dist}

%if %build_on_obs == 1
License: GPL-3.0+
%else
License: GPLv3
%endif

%if %{undefined suse_version} && %{undefined sles_version}
Group: System Environment/Base
%else
Group: Productivity/Networking/Email/Servers
%endif
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1: http://downloads.sourceforge.net/%{name}/%{name}-rpmlintrc

URL: https://github.com/mbhangui/indimail-virtualdomains
AutoReqProv: Yes

BuildRequires: rpm gcc gcc-c++ make coreutils grep
BuildRequires: glibc glibc-devel
BuildRequires: gzip autoconf automake libtool
BuildRequires: sed findutils

BuildRequires: flex bison
%if 0%{?suse_version}
BuildRequires: db-devel
%else
%if 0%{?fedora_version} > 17 || 0%{?centos_version} > 600 || 0%{?rhel_version} > 600 || 0%{?centos_ver} > 7
BuildRequires: libdb-devel
%else
BuildRequires: db4-devel
%endif
%endif

################################# OBS ###############################
%if %build_on_obs == 1
%if 0%{?suse_version}
BuildRequires: -post-build-checks
#!BuildIgnore: post-build-checks
#!BuildIgnore: brp-check-suse
%endif
%endif
################################# OBS ###############################

Requires: procps /usr/bin/awk /usr/bin/which
Requires: sed findutils
Requires: coreutils grep /bin/sh glibc
Requires: bogofilter-wordlist indimail-mta

%if %build_on_obs == 1
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXXX)
%endif

%description
Bogofilter is a Bayesian spam filter.  In its normal mode of
operation, it takes an email message or other text on standard input,
does a statistical check against lists of "good" and "bad" words, and
returns a status code indicating whether or not the message is spam.
Bogofilter is designed with fast algorithms (including Berkeley DB system),
coded directly in C, and tuned for speed, so it can be used for production
by sites that process a lot of mail.

This version substantially improves on Paul's proposal by doing smarter
lexical analysis.  In particular, hostnames and IP addresses are retained
as recognition features rather than broken up. Various kinds of MTA
cruft such as dates and message-IDs are discarded so as not to bloat
the word lists.

%prep
%setup -q

%build
ID=$(id -u)
(
echo "---------------- INFORMATION ------------------------"
echo target         %_target
echo target_alias   %_target_alias
echo target_cpu     %_target_cpu
echo target_os      %_target_os
echo target_vendor  %_target_vendor
%if 0%{?fedora_version} > 30 || 0%{?centos_version} > 700 || 0%{?rhel_version} > 700 || 0%{?centos_ver} > 7
echo pythondir      %{python3_sitelib}
%else
echo pythondir      %{pythondir}
%endif
echo Project        %{_project}
echo Building %{name}-%{version}-%{release} Build %{_build} OS %{_os}
echo "------------------------------------------------------"
) > %{name}-rpm.info
(
echo "NAME=%{name}"
echo "Description=\"IndiMail Spamfilter Package\""
echo "SPAMFILTER_version="%{version}""
echo "ID=%{name}"
echo "HOME_URL=\"https://github.com/mbhangui/indimail-virtualdomains\""
echo "PACKAGE_BUGREPORT=\"Manvendra Bhangui indimail-spamfilter@indimail.org\""
) > %{name}-release

#### bogofilter ######################
if [ %{reconf_bogofilter} -eq 1 ] ; then
  echo "reconfiguring..."
  %{__mkdir_p} m4
  aclocal -I m4
  autoreconf -fiv
fi
(
HOME='.';export HOME
./configure --prefix=%{_prefix} --libexecdir=%{libexecdir} --sysconfdir=%{sysconfdir} \
  --mandir=%{mandir} --datarootdir=%{shareddir} \
  --enable-indimail
)

%install
ID=$(id -u)
%{__make} -s DESTDIR=%{buildroot}
%{__make} -s DESTDIR=%{buildroot} install-strip

%{__mkdir_p} %{buildroot}%{sysconfdir}
install -m 0644 %{name}-rpm.info %{buildroot}%{sysconfdir}/%{name}-rpm.info
install -m 0644 %{name}-release %{buildroot}%{sysconfdir}/%{name}-release
/bin/rm -f %{name}-rpm.info %{name}-release
if [ -x /usr/bin/chrpath ] ; then
  for i in bogofilter bogoutil bogotune
  do
    /bin/chmod 755 %{buildroot}%{_prefix}/bin/$i
    /usr/bin/chrpath -d %{buildroot}%{_prefix}/bin/$i
  done
fi

# Compress the man pages
find %{buildroot}%{mandir} -type f -exec gzip -q {} \;

if [ -x /bin/touch ] ; then
  TOUCH=/bin/touch
elif [ -x /usr/bin/touch ] ; then
  TOUCH=/usr/bin/touch
else
  TOUCH=/bin/touch
fi
%if %{undefined suse_version} && %{undefined sles_version}
$TOUCH %{buildroot}%{sysconfdir}/bogofilter.cf
%endif

%files
%defattr(-, root, root,-)
#
# Directories
#
%if "%{mandir}" != "/usr/share/man"
%dir %attr(755,root,root)              %{mandir}
%dir %attr(755,root,root)              %{mandir}/man1
%endif
%attr(444,root,root) %config(noreplace)           %{sysconfdir}/%{name}-release
%attr(444,root,root) %config(noreplace)           %{sysconfdir}/%{name}-rpm.info
%ghost %config(noreplace,missingok)               %{sysconfdir}/bogofilter.cf
%attr(644,root,root) %config(noreplace)           %{sysconfdir}/bogofilter.cf.example

# bogofilter
# setuid binary
%attr(6551,root,indimail)               %{_prefix}/bin/bogofilter
%attr(755,root,root)                    %{_prefix}/bin/bogolexer
%attr(755,root,root)                    %{_prefix}/bin/bogotune
%attr(755,root,root)                    %{_prefix}/bin/bogoutil
%attr(755,root,root)                    %{_prefix}/bin/bogoupgrade
%attr(755,root,root)                    %{_prefix}/sbin/bf_compact
%attr(755,root,root)                    %{_prefix}/sbin/bf_copy
%attr(755,root,root)                    %{_prefix}/sbin/bf_tar

%docdir %{shareddir}/doc
%docdir %{mandir}
%attr(644,root,root)                    %{mandir}/man1/*

%if %build_on_obs == 0
%license %attr(644,root,root)           %{shareddir}/doc/COPYING.bogofilter
%else
%attr(644,root,root)                    %{shareddir}/doc/COPYING.bogofilter
%endif
%attr(644,root,root)                    %{shareddir}/doc/AUTHORS.bogofilter
%attr(644,root,root)                    %{shareddir}/doc/HOWTO.bogofilter

%if %noperms == 0
%if 0%{?suse_version} >= 1120
%verify (not user group mode) %attr(6551, root, indimail)  %{_prefix}/bin/bogofilter
%endif
%endif

### SCRIPTLET ###############################################################################
%verifyscript
ID=$(id -u)
if [ $ID -ne 0 ] ; then
  echo "You are not root" 1>&2
  exit 1
fi

%if %noperms == 0
%if 0%{?suse_version} >= 1120
%verify_permissions -e %{_prefix}/bin/bogofilter
%endif
%endif

### SCRIPTLET ###############################################################################
%post
argv1=$1
ID=$(id -u)
if [ $ID -ne 0 ] ; then
  echo "You are not root" 1>&2
  exit 1
fi
if [ -x /bin/touch ] ; then
  TOUCH=/bin/touch
elif [ -x /usr/bin/touch ] ; then
  TOUCH=/usr/bin/touch
else
  TOUCH=/bin/touch
fi

if [ -z "$argv1" ] ; then
  argv1=0
fi
if [ -d /run ] ; then
  logfifo="/run/indimail/logfifo"
  %{__mkdir_p} /run/indimail
elif [ -d /var/run ] ; then
  logfifo="/var/run/indimail/logfifo"
  %{__mkdir_p} /var/run/indimail
else
  logfifo="/tmp/logfifo"
fi

%if %noperms == 0
%if 0%{?suse_version} >= 1120
%if 0%{?set_permissions:1} > 0
  if [ ! -f /tmp/no_permissions ] ; then
      %set_permissions %{name}
  fi
%else
  if [ ! -f /tmp/no_permissions ] ; then
      %run_permissions
  fi
%endif
%endif
%endif

# SMTP
# Configure SPAMFILTER, LOGFILTER
for port in 465 25
do
  if [ ! -d %{servicedir}/qmail-smtpd.$port ] ; then
    continue
  fi
  # update SPAMFILTER and also change .options, so that refreshsvc doesn't lose the settings
  echo "%{_prefix}/bin/bogofilter -p -d %{sysconfdir}" > %{servicedir}/qmail-smtpd.$port/variables/SPAMFILTER
  if [ ! -f %{servicedir}/qmail-smtpd.$port/variables/SPAMEXITCODE ] ; then
  echo 0 > %{servicedir}/qmail-smtpd.$port/variables/SPAMEXITCODE
  fi
  if [ ! -f %{servicedir}/qmail-smtpd.$port/variables/REJECTSPAM ] ; then
  echo 0 > %{servicedir}/qmail-smtpd.$port/variables/REJECTSPAM
  fi
  if [ ! -f %{servicedir}/qmail-smtpd.$port/variables/MAKESEEKABLE ] ; then
  echo 1 > %{servicedir}/qmail-smtpd.$port/variables/MAKE_SEEKABLE
  elif [ ! -s %{servicedir}/qmail-smtpd.$port/variables/MAKESEEKABLE ] ; then
  echo 1 > %{servicedir}/qmail-smtpd.$port/variables/MAKE_SEEKABLE
  fi
  if [ ! -f %{servicedir}/qmail-smtpd.$port/variables/LOGFILTER ] ; then
  echo $logfifo > %{servicedir}/qmail-smtpd.$port/variables/LOGFILTER
  fi
  grep bogofilter %{servicedir}/qmail-smtpd.$port/variables/.options > /dev/null 2>&1
  if [ $? -ne 0 ] ; then
    options="`cat %{servicedir}/qmail-smtpd.$port/variables/.options`
    --spamfilter=\"%{_prefix}/bin/bogofilter -p -d %{sysconfdir}\"
    --logfilter=\"$logfifo\" --rejectspam=\"0\" --spamexitcode=\"0\""
    if [ -f %{servicedir}/qmail-smtpd.$port/variables/.options ] ; then
      %{__mv} %{servicedir}/qmail-smtpd.$port/variables/.options \
        %{servicedir}/qmail-smtpd.$port/variables/.options.nospamfilter
    fi
    echo $options > %{servicedir}/qmail-smtpd.$port/variables/.options
  fi
done
if [ -d %{servicedir}/fetchmail ] ; then
  # update SPAMFILTER and also change .options, so that refreshsvc doesn't lose the settings
  echo "%{_prefix}/bin/bogofilter -p -d %{sysconfdir}" > %{servicedir}/fetchmail/variables/SPAMFILTER
  if [ ! -f %{servicedir}/fetchmail/variables/SPAMEXITCODE ] ; then
  echo 0 > %{servicedir}/fetchmail/variables/SPAMEXITCODE
  fi
  if [ ! -f %{servicedir}/fetchmail/variables/REJECTSPAM ] ; then
  echo 0 > %{servicedir}/fetchmail/variables/REJECTSPAM
  fi
  if [ ! -f %{servicedir}/fetchmail/variables/MAKESEEKABLE ] ; then
  echo 1 > %{servicedir}/fetchmail/variables/MAKE_SEEKABLE
  elif [ ! -s %{servicedir}/fetchmail/variables/MAKESEEKABLE ] ; then
  echo 1 > %{servicedir}/fetchmail/variables/MAKE_SEEKABLE
  fi
  if [ ! -f %{servicedir}/fetchmail/variables/LOGFILTER ] ; then
  echo $logfifo > %{servicedir}/fetchmail/variables/LOGFILTER
  fi
  grep bogofilter %{servicedir}/fetchmail/variables/.options > /dev/null 2>&1
  if [ $? -ne 0 ] ; then
    options="`cat %{servicedir}/fetchmail/variables/.options`
    --spamfilter=\"%{_prefix}/bin/bogofilter -p -d %{sysconfdir}\"
    --logfilter=\"$logfifo\" --rejectspam=\"0\" --spamexitcode=\"0\""
    if [ -f %{servicedir}/fetchmail/variables/.options ] ; then
      %{__mv} %{servicedir}/fetchmail/variables/.options \
        %{servicedir}/fetchmail/variables/.options.nospamfilter
    fi
    echo $options > %{servicedir}/fetchmail/variables/.options
  fi
fi

#
# bogofilter configuration
#
if [ -d %{sysconfdir} ] ; then
  if [ -x %{_prefix}/sbin/svctool ] ; then
    %{_prefix}/sbin/svctool --config=bogofilter
  fi
fi

### SCRIPTLET ###############################################################################
%postun
argv1=$1
ID=$(id -u)
if [ $ID -ne 0 ] ; then
  echo "You are not root" 1>&2
  exit 1
fi
if [ -z "$argv1" ] ; then
  argv1=0
fi
for dir in fetchmail qmail-smtpd.465 qmail-smtpd.25
do
  > %{servicedir}/$dir/variables/SPAMFILTER
  > %{servicedir}/$dir/variables/SPAMEXITCODE
  > %{servicedir}/$dir/variables/REJECTSPAM
  > %{servicedir}/$dir/variables/LOGFILTER
  if [ -f %{servicedir}/$dir/variables/.options.nospamfilter ] ; then
    %{__mv} %{servicedir}/$dir/variables/.options.nospamfilter \
      %{servicedir}/$dir/variables/.options
  fi
done

# fix changelog for openSUSE buildservice
%changelog
* Thu Jun 04 2020 10:46:13 +0530 indimail-spamfilter@indimail.org 1.2.4-1.1%{?dist}
BOGOFILTER NEWS
    =================
    !!!!!!!! READ THE RELEASE.NOTES !!!!!!!!
    This file is in Unicode charset, with UTF-8 encoding.
    Sections headed '[Incompat <version>]' and '[Major <version>]'
    are particularly important.  They describe changes that are
    incompatible with earlier releases or are significantly
    different.
    !!!!!!!! READ THE RELEASE.NOTES !!!!!!!!
    -------------------------------------------------------------------------------
1.2.4	2013-07-01 (released)
2013-06-28
