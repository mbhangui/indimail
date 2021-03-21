#
#
# $Id: indimail.spec.in,v 1.85 2021-03-02 16:47:25+05:30 Cprogrammer Exp mbhangui $
%undefine _missing_build_ids_terminate_build
%global _unpackaged_files_terminate_build 1

%if %{defined _project}
# define if building on openSUSE build service
%global build_on_obs       1
%global reconfigure_mode   0
%else
%define _project           local
%global build_on_obs       0
%global reconfigure_mode   0
%global _hardened_build    1
%endif

%if %{defined nodebug}
%global debug_package      %{nil}
%endif

%if 0%{?fedora_version} > 30 || 0%{?centos_version} > 700 || 0%{?rhel_version} > 700 || 0%{?centos_ver} > 7
%global pythondir %{python3_sitelib}
%else
%global pythondir %(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif
%global _prefix            /usr
%global indimaildir        /var/indimail
%global domaindir          /var/indimail
%global sysconfdir         /etc/indimail
%global libexecdir         /usr/libexec/indimail
%global shareddir          /usr/share/indimail
%global mandir             /usr/share/man
%global defaultDomain      argos.indimail.org
%global url                https://github.com/mbhangui/indimail-virtualdomains
%global noproxy            0

%global qcount             5
%global qbase              %{indimaildir}/queue
%global mbase              /home/mail
%global logdir             /var/log/svc
%global imoduledir         %{_prefix}/lib/indimail/modules
%global servicedir         /service
%global _pkg_config_path   /usr/%{_lib}/pkgconfig
%global mysqlSocket        /var/run/mysqld/mysqld.sock
%global mysqlPrefix        /usr

%if %build_on_obs == 1
%global packager Manvendra Bhangui <manvendra@indimail.org>
%endif

Summary: A Flexible Messaging Platform with Multi-Host/Multi-Protocol support
Name: indimail
Version: 3.4
Release: 1.1%{?dist}

## user/group management
# Note: it is not necessary to assign 555 for uid, gid. The package will use any id assigned to username, groupname
# at runtime
%global uid                555
%global gid                555
%global username           indimail
%global groupname          indimail
# Note: 999 indimail-mta does not require any specific values for uids/gids. 999 is just
# for rpmlint to shut up and stop complaining
Requires: user(alias)
Requires: user(qmaill)
Requires: user(indimail)
Requires: user(qscand)
Requires: group(qmail)
Requires: group(nofiles)
Requires: group(qscand)
Requires: group(indimail)
%if %build_on_obs == 0
Requires(pre): shadow-utils
Requires(postun): shadow-utils
%endif

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
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1: http://downloads.sourceforge.net/%{name}/%{name}-rpmlintrc
%if 0%{?suse_version} >= 1120
Source2: http://downloads.sourceforge.net/%{name}/%{name}-permissions.easy
Source3: http://downloads.sourceforge.net/%{name}/%{name}-permissions.secure
Source4: http://downloads.sourceforge.net/%{name}/%{name}-permissions.paranoid
%endif

URL: https://github.com/mbhangui/indimail-virtualdomains
AutoReq: Yes
# few binaries were moved to sbin and indimail >= 2.5 depends on that
Requires: indimail-mta > 2.6
Conflicts: %{name} < 2.0
Obsoletes: %{name} < 2.0

BuildRequires: openssl-devel rpm gcc gcc-c++ make coreutils grep
BuildRequires: glibc glibc-devel openssl procps ncurses-devel
BuildRequires: gzip autoconf automake libtool pkgconfig
BuildRequires: sed findutils binutils
BuildRequires: mysql-devel libqmail-devel libqmail

%if %{defined fedora_version} || 0%{?centos_version} > 700 || 0%{?rhel_version} > 700 || 0%{?centos_ver} > 7
BuildRequires: redhat-lsb-core
%endif
%if %{defined rhel_version}
BuildRequires: redhat-lsb
%endif
%if %{defined centos_version}
%if 0%{?centos_version} <= 700
BuildRequires: redhat-lsb
%endif
%endif

# suse_version gets defined for sles too
%if %{defined suse_version}
BuildRequires: lsb-release
%if %{undefined sles_version}
BuildRequires: openSUSE-release
%endif
%if !0%{?is_opensuse}
BuildRequires: sles-release
%else
BuildRequires: openSUSE-release
%endif
%endif
%if %{undefined centos_version} && %{undefined rhel_version} && %{undefined centos_vers}
BuildRequires: chrpath
%endif

%if 0%{?suse_version} == 1220 || 0%{?suse_version} == 1210 || 0%{?suse_version} == 1140 || 0%{?suse_version} == 1100 || 0%{?suse_version} == 1030 || 0%{?suse_version} == 1020
BuildRequires: chrpath
%endif

%if 0%{?suse_version}
BuildRequires: openldap2-devel
%else
BuildRequires: openldap-devel
%endif

%if 0%{?suse_version}
PreReq: permissions
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

# rpm -qf /bin/ls
# rpm -qp --queryformat %%{arch} some-file.rpm
# rpm --showrc for all macros
# rpm -qlp some-file.rpm
Requires: /usr/sbin/useradd /usr/sbin/groupadd /usr/sbin/groupdel
Requires: /sbin/chkconfig procps /usr/bin/awk /usr/bin/which
Requires: sed findutils pkgconfig
Requires: coreutils grep /bin/sh glibc openssl
Requires: /usr/bin/hostname mrtg

%if 0%{?sles_version}
Requires: mysql-community-server
%else
Requires: mysql-server
%endif

%if 0%{?fedora_version} > 30 || 0%{?centos_version} > 700 || 0%{?rhel_version} > 700 || 0%{?centos_ver} > 7
Requires: python3-policycoreutils
%else
%if %{defined centos_version} || %{defined rhel_version} || %{defined centos_ver}
Requires: policycoreutils-python
%endif
%endif
Requires: indimail-access indimail-libs

%if %build_on_obs == 1
BuildRoot: %{_tmppath}/%{name}-%{version}-build
%endif
#
# IndiMail is choosy and runs on reliable OS only
#
Excludeos: windows

%description
IndiMail is a messaging platform providing multi-cluster domain support.

IndiMail provides ability for a single domain to have users across multiple
hosts (even across different geographical locations) and tools to manage
virtual domains.

For more details visit %{url}

%package devel
Summary: IndiMail - Development header files and libraries
Group: Development/Libraries/Other
Requires: libindimail >= %{version}
Conflicts: %{name}-devel < 2.0

%description devel
This package contains the development header files and libraries
necessary to develop IndiMail client applications.

For more details visit %{url}

%package -n libindimail
Summary: IndiMail - Shared libraries
Group: Development/Libraries/Other
Conflicts: libindimail < 2.0
Provides: indimail-libs = %{version}
Provides: indimail-libs%{?_isa} = %{version}

%description -n libindimail
This package contains the shared libraries (*.so*) which certain
languages and applications need to dynamically load and use IndiMail.

For more details visit %{url}

%prep
%if %build_on_obs == 1
sh ../SOURCES/obs_script indimail-x indimail
%setup -TDqn %{name}-%{version}
%else
%setup -q
%endif

%build
ID=$(id -u)
(
echo "---------------- INFORMATION ------------------------"
echo target         %_target
echo target_alias   %_target_alias
echo target_cpu     %_target_cpu
echo target_os      %_target_os
echo target_vendor  %_target_vendor
echo Project        %{_project}
echo Building %{name}-%{version}-%{release} Build %{_build} OS %{_os} lib=%{_lib} libdir=%{_libdir}
echo "------------------------------------------------------"
) > %{name}-rpm.info

#### IndiMail ######################
if [ %{reconfigure_mode} -eq 1 ] ; then
  echo "reconfiguring..."
  %{__mkdir_p} m4
  aclocal -I m4
  autoreconf -fiv
fi

%if %build_on_obs == 0
  if [ -x /usr/bin/uname -o -x /bin/uname ] ; then
    default_domain=$([ -n "$HOSTNAME" ] && echo "$HOSTNAME" || `uname -n`)
  else
    default_domain=$([ -n "$HOSTNAME" ] && echo "$HOSTNAME" || echo %{defaultDomain})
  fi
%else
  default_domain=%{defaultDomain}
%endif
%configure --prefix=%{_prefix} --sysconfdir=%{sysconfdir} \
  --mandir=%{_prefix}/share/man --datarootdir=%{_prefix}/share/indimail \
  --with-pkgconfigdir=%{_pkg_config_path} --libdir=%{_libdir} --enable-domaindir=%{domaindir} \
  --enable-mysqlprefix=%{mysqlPrefix} \
  --libexecdir=%{libexecdir} --mandir=%{mandir} --enable-qmaildir=%{indimaildir} \
  --enable-basepath=/home/mail --enable-logdir=%{logdir} \
  --enable-tcprules-prog=%{_prefix}/bin/tcprules --enable-tcpserver-file=%{sysconfdir}/tcp/tcp.smtp \
  --enable-default-domain=${default_domain} `%{__cat} config/indimail.opts`

if [ $ID -eq 0 ] ; then
  if [ $nscd_up -ge 1 ] ; then
    if [ -x %{_sysconfdir}/init.d/nscd ] ; then
      %{_sysconfdir}/init.d/nscd start
    elif [ -f %{_sysconfdir}/lib/systemd/system/multi-user.target/nscd.service ] ; then
      /bin/systemctl start nscd.service
    fi
  fi
fi

%install
ID=$(id -u)
%if 0%{?suse_version} >= 1120
%if 0%{?build_cflags:1}
  CFLAGS="%{build_cflags} -fPIC -fno-lto"
%else
  CFLAGS="%{optflags} -fPIC -fno-lto"
%endif
%if 0%{?build_ldflags:1}
  LDFLAGS="%{build_ldflags} -fno-lto -pie $LDFLAGS"
%else
  LDFLAGS="-fno-lto -pie $LDFLAGS"
%endif
  %{__make} SYSTEM=LINUX %{?_smp_mflags} CC="%{__cc}" CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS"
%else
  %{__make} -s %{?_smp_mflags}
%endif
%if %{defined nodebug}
%{__make} -s %{?_smp_mflags} DESTDIR=%{buildroot} install-strip
%else
%{__make} -s %{?_smp_mflags} DESTDIR=%{buildroot} install
%endif
%{__mkdir_p} %{buildroot}%{sysconfdir}
install -m 0644 %{name}-rpm.info %{buildroot}%{sysconfdir}/%{name}-rpm.info
/bin/rm -f %{name}-rpm.info
for i in eps cdb indimail
do
  %{__rm} -f %{buildroot}%{_libdir}/lib"$i".la
done
%{__rm} -f %{buildroot}%{imoduledir}/iauth.la

%{__mkdir_p} %{buildroot}%{domaindir}/domains
%{__mkdir_p} %{buildroot}%{_prefix}/include/indimail

%if 0%{?suse_version} >= 1120
%{__mkdir_p} %{buildroot}%{_sysconfdir}/permissions.d/
install -m 644 %{S:2} %{buildroot}%{_sysconfdir}/permissions.d/%{name}-permissions
install -m 644 %{S:3} %{buildroot}%{_sysconfdir}/permissions.d/%{name}-permissions.secure
%endif

if [ -x /usr/bin/chrpath ] ; then
  /usr/bin/chrpath -d %{buildroot}%{_libdir}/*.so
  for i in dbinfo hostcntrl printdir sigtool vacation vaddaliasdomain \
  vadddomain vadduser valias vatrn vbulletin vcalias vcfilter \
  vdeldomain vdelusevdominfo vgroup vhostid vipmap vlimit vmoduser \
  vmoveuser vpasswd vpriv vproxy vrenamedomain vrenameuser \
  vsetuserquota vsmtp vuserinfo tcpserver ismaildup
  do
    if [ -f %{buildroot}%{_prefix}/bin/$i ] ; then
      /usr/bin/chrpath -d %{buildroot}%{_prefix}/bin/$i
    fi
  done

  /usr/bin/chrpath -d %{buildroot}%{libexecdir}/imapmodules/authindi
  /usr/bin/chrpath -d %{buildroot}%{libexecdir}/sq_vacation
  /usr/bin/chrpath -d %{buildroot}%{libexecdir}/qmailmrtg7
  /usr/bin/chrpath -d %{buildroot}%{imoduledir}/iauth.so
  /usr/bin/chrpath -d %{buildroot}%{imoduledir}/tcplookup.so

  for i in adminclient chowkidar clearopensmtp tcplookup \
  hostsync indisrvr inlookup inquerytest install_tables ipchange \
  mgmtpass updatefile updaterules vchkpass vdelivermail \
  vdeloldusers vfilter vfstab vmoddomain vreorg vsetpass \
  vserverinfo vpurge vtable resetquota
  do
    if [ -f %{buildroot}%{_prefix}/sbin/$i ] ; then
      /usr/bin/chrpath -d %{buildroot}%{_prefix}/sbin/$i
    fi
    if [ -f %{buildroot}%{libexecdir}/$i ] ; then
      /usr/bin/chrpath -d %{buildroot}%{libexecdir}/$i
    fi
  done
fi
# Compress the man pages
find %{buildroot}%{mandir} -type f -exec gzip -q {} \;
if [ -f %{buildroot}%{mandir}/man7/authlib.7.gz ] ; then
  for i in authshadow.7 authpwd.7 authpam.7 authcustom.7
  do
    %{__rm} -f %{buildroot}%{mandir}/man7/$i
    echo ".so man7/authlib.7" |gzip -c > %{buildroot}%{mandir}/man7/$i.gz
  done
fi

%{__mkdir_p} %{buildroot}%{indimaildir}/inquery
%{__mkdir_p} %{buildroot}%{sysconfdir}/users
%{__mkdir_p} %{buildroot}%{sysconfdir}/control
%{__mkdir_p} %{buildroot}%{sysconfdir}/tcp
# Create these files so that %%ghost does not complain
for i in tcp.poppass tcp.poppass.cdb
do
  if [ ! -f %{buildroot}%{sysconfdir}/tcp/$i ] ; then
    touch %{buildroot}%{sysconfdir}/tcp/$i
  fi
done

for i in indimail.cnf procmailrc indimail.pp indimail.mod \
users/cdb users/assign
do
  if [ ! -f %{buildroot}%{sysconfdir}/$i ] ; then
    touch %{buildroot}%{sysconfdir}/$i
  fi
done
(
# host.mysql, host.cntrl, host.master, host.ldap
for i in `%{__cat} %{buildroot}%{sysconfdir}/controlfiles.i`
do
  echo "%ghost %attr(0640,indimail,qmail) %config(noreplace,missingok) %{sysconfdir}/control/$i"
  touch %{buildroot}%{sysconfdir}/control/$i
done
) > config_files.list

%if %{undefined suse_version} && %{undefined sles_version}
  %{__mkdir_p} %{buildroot}%{logdir}
  for i in indisrvr.4000 inlookup.infifo logfifo \
  mrtg mysql.3306 poppass.106 
  do
    %{__mkdir_p} %{buildroot}%{logdir}/$i
    touch %{buildroot}%{logdir}/$i/current
  done

%if %{noproxy} == 0
  for i in proxyIMAP.4143 proxyIMAP.9143 \
    proxyPOP3.4110 proxyPOP3.9110
  do
    %{__mkdir_p} %{buildroot}%{logdir}/$i
    touch %{buildroot}%{logdir}/$i/current
  done
%endif
%endif
%if %{undefined nodebug}
  /bin/chmod 755 %{buildroot}%{imoduledir}/iauth.so
  /bin/chmod 755 %{buildroot}%{imoduledir}/tcplookup.so
%endif

%files -f config_files.list
%defattr(-, root, root,-)
#
# Directories
#
# opensuse requres ghost files to be present
%if %{undefined suse_version} && %{undefined sles_version}
%ghost %dir %attr(0755,qmaill,nofiles) %{logdir}
%ghost %dir %attr(0755,qmaill,nofiles) %{logdir}/*
%ghost      %attr(-,qmaill,nofiles)    %{logdir}/*/*
%endif

%dir %attr(775,root,indimail)          %{domaindir}/domains
%dir %attr(770,indimail,qmail)         %{indimaildir}/inquery
%dir %attr(555,root,root)              %{libexecdir}/imapmodules
%dir %attr(755,root,root)              %{_prefix}/lib/indimail/modules
%if "%{mandir}" != "/usr/share/man"
%dir %attr(755,root,root)              %{mandir}
%dir %attr(755,root,root)              %{mandir}/man1
%dir %attr(755,root,root)              %{mandir}/man5
%dir %attr(755,root,root)              %{mandir}/man7
%dir %attr(755,root,root)              %{mandir}/man8
%endif
%if "%{_prefix}" != "/usr"
%dir %attr(555,root,root)              %{_libdir}
%endif

#
# If the configuration file should not be replaced when the RPM is
# upgraded, mark it as follows:
# %%config(noreplace) filename
#
# Configuration files must be marked as such in packages.
# As a rule of thumb, use %%config(noreplace) instead of plain %%config unless your best,
# educated guess is that doing so will break things. In other words, think hard before
# overwriting local changes in configuration files on package upgrades.
# An example case when /not/ to use noreplace is when a package's configuration file
# changes so that the new package revision wouldn't work with the config file
# from the previous package revision. Whenever plain %%config is used,
# add a brief comment to the specfile explaining why.

%attr(444,root,root) %config(noreplace)           %{sysconfdir}/osh.table
# Allow new control files to get added with new packages
# unlikely for this file to have local changes
%attr(444,root,root) %config(noreplace)           %{sysconfdir}/controlfiles.i
# For configuration files that may be found missing during uninstall have
# $config(missingok)
#
# For files that should be included in the list of files so that they
# are uninstalled when the package is removed but may not exist until
# they are created during post-install should be marked as follows:
# %%ghost filename
%ghost %attr(0644,root,root) %config(noreplace,missingok) %{sysconfdir}/users/assign
%ghost %attr(0644,root,root) %config(noreplace,missingok) %{sysconfdir}/users/cdb
%ghost %config(noreplace,missingok)               %{sysconfdir}/procmailrc
%ghost %config(noreplace,missingok)               %{sysconfdir}/indimail.cnf
%ghost %config(noreplace,missingok)               %{sysconfdir}/tcp/tcp.poppass
#
# These files will get removed during uninstallation
#
%ghost %attr(0644,indimail,indimail)              %{sysconfdir}/tcp/tcp.poppass.cdb
#
#
%ghost %attr(0644,root,root)                      %{sysconfdir}/indimail.pp
%ghost %attr(0644,root,root)                      %{sysconfdir}/indimail.mod

%attr(444,root,root) %config(noreplace)           %{sysconfdir}/cronlist.i
%attr(444,root,root) %config(noreplace)           %{sysconfdir}/indimail.mrtg.cfg
%attr(444,root,root) %config(noreplace)           %{sysconfdir}/headerlist
%attr(444,root,root) %config(noreplace)           %{sysconfdir}/indimail.settings
%attr(444,root,root) %config(noreplace)           %{sysconfdir}/%{name}-release
%attr(444,root,root) %config(noreplace)           %{sysconfdir}/%{name}-rpm.info
%attr(444,root,root) %config(noreplace)           %{sysconfdir}/perm_list.indimail

%attr(644,root,root)  %config(noreplace)          %{sysconfdir}/indimail.te
%attr(644,root,root)  %config(noreplace)          %{sysconfdir}/indimail.fc

%if 0%{?suse_version} >= 1120
%attr(644,root,root)  %config(noreplace)          %{_sysconfdir}/permissions.d/%{name}-permissions
%attr(644,root,root)  %config(noreplace)          %{_sysconfdir}/permissions.d/%{name}-permissions.secure
%endif
#
# setuid binaries
#
%if 0%{?suse_version} >= 1120
%verify (not user group mode caps) %attr(4555,root,root) %{_prefix}/bin/vrenameuser
%verify (not user group mode caps) %attr(4555,root,root) %{_prefix}/bin/vmoveuser
%verify (not user group mode caps) %attr(4555,root,root) %{_prefix}/bin/vrenamedomain
%verify (not user group mode caps) %attr(4555,root,root) %{_prefix}/bin/vmoduser
%verify (not user group mode caps) %attr(4555,root,root) %{_prefix}/bin/vcfilter
%verify (not user group mode caps) %attr(4555,root,root) %{_prefix}/bin/vsetuserquota
%verify (not user group mode caps) %attr(4555,root,root) %{_prefix}/bin/vaddaliasdomain
%verify (not user group mode caps) %attr(4555,root,root) %{_prefix}/bin/vadduser
%verify (not user group mode caps) %attr(4555,root,root) %{_prefix}/bin/printdir
%verify (not user group mode caps) %attr(4555,root,root) %{_prefix}/bin/vdeluser
%verify (not user group mode caps) %attr(4555,root,root) %{_prefix}/bin/vbulletin
%verify (not user group mode caps) %attr(4555,root,root) %{_prefix}/bin/vdominfo
%verify (not user group mode caps) %attr(4555,root,root) %{_prefix}/bin/vadddomain
%verify (not user group mode caps) %attr(4555,root,root) %{_prefix}/bin/vdeldomain
%verify (not user group mode caps) %attr(4555,root,root) %{libexecdir}/sq_vacation
%else
%attr(4555,root,root)                   %{_prefix}/bin/vrenameuser
%attr(4555,root,root)                   %{_prefix}/bin/vmoveuser
%attr(4555,root,root)                   %{_prefix}/bin/vrenamedomain
%attr(4555,root,root)                   %{_prefix}/bin/vmoduser
%attr(4555,root,root)                   %{_prefix}/bin/vcfilter
%attr(4555,root,root)                   %{_prefix}/bin/vsetuserquota
%attr(4555,root,root)                   %{_prefix}/bin/vaddaliasdomain
%attr(4555,root,root)                   %{_prefix}/bin/vadduser
%attr(4555,root,root)                   %{_prefix}/bin/printdir
%attr(4555,root,root)                   %{_prefix}/bin/vdeluser
%attr(4555,root,root)                   %{_prefix}/bin/vbulletin
%attr(4555,root,root)                   %{_prefix}/bin/vdominfo
%attr(4555,root,root)                   %{_prefix}/bin/vadddomain
%attr(4555,root,root)                   %{_prefix}/bin/vdeldomain
%attr(4555,root,root)                   %{libexecdir}/sq_vacation
%endif

# indimail binaries
%attr(755,root,root)                    %{_prefix}/bin/vuserinfo
%attr(755,root,root)                    %{_prefix}/bin/hostcntrl
%attr(755,root,root)                    %{_prefix}/bin/vpasswd
%attr(755,root,root)                    %{_prefix}/bin/vcalias
%attr(755,root,root)                    %{_prefix}/bin/vhostid
%attr(755,root,root)                    %{_prefix}/bin/vatrn
%attr(755,root,root)                    %{_prefix}/bin/vlimit
%attr(755,root,root)                    %{_prefix}/bin/incrypt
%attr(755,root,root)                    %{_prefix}/bin/vpriv
%attr(755,root,root)                    %{_prefix}/bin/vipmap
%attr(755,root,root)                    %{_prefix}/bin/vsmtp
%attr(755,root,root)                    %{_prefix}/bin/vgroup
%attr(755,root,root)                    %{_prefix}/bin/vcaliasrev
%attr(755,root,root)                    %{_prefix}/bin/vacation
%attr(755,root,root)                    %{_prefix}/bin/proxyimap
%attr(755,root,root)                    %{_prefix}/bin/proxypop3
%attr(755,root,root)                    %{_prefix}/bin/crc

%attr(755,root,root)                    %{_prefix}/bin/crcdiff
%attr(755,root,root)                    %{_prefix}/bin/dbinfo

%attr(755,root,root)                    %{_prefix}/sbin/resetquota
%attr(755,root,root)                    %{_prefix}/sbin/vserverinfo
%attr(755,root,root)                    %{_prefix}/sbin/adminclient
%attr(755,root,root)                    %{_prefix}/sbin/chowkidar
%attr(755,root,root)                    %{_prefix}/sbin/clearopensmtp
%attr(755,root,root)                    %{_prefix}/sbin/hostsync
%attr(755,root,root)                    %{_prefix}/sbin/indisrvr
%attr(755,root,root)                    %{_prefix}/sbin/initsvc
%attr(755,root,root)                    %{_prefix}/sbin/inlookup
%attr(755,root,root)                    %{_prefix}/sbin/tcplookup
%attr(755,root,root)                    %{_prefix}/sbin/inquerytest
%attr(755,root,root)                    %{_prefix}/sbin/install_tables
%attr(755,root,root)                    %{_prefix}/sbin/vtable
%attr(755,root,root)                    %{_prefix}/sbin/ipchange
%attr(755,root,root)                    %{_prefix}/sbin/mgmtpass
%attr(755,root,root)                    %{_prefix}/sbin/updaterules
%attr(755,root,root)                    %{_prefix}/sbin/vchkpass
%attr(755,root,root)                    %{_prefix}/sbin/vsetpass
%attr(755,root,root)                    %{_prefix}/sbin/vdelivermail
%attr(755,root,root)                    %{_prefix}/sbin/vdeloldusers
%attr(755,root,root)                    %{_prefix}/sbin/vpurge
%attr(755,root,root)                    %{_prefix}/sbin/vfilter
%attr(755,root,root)                    %{_prefix}/sbin/vfstab
%attr(755,root,root)                    %{_prefix}/sbin/vmoddomain
%attr(755,root,root)                    %{_prefix}/sbin/vreorg
%attr(755,root,root)                    %{_prefix}/bin/valias
%attr(755,root,root)                    %{_prefix}/bin/vproxy
%attr(755,root,root)                    %{_prefix}/sbin/osh
%attr(755,root,root)                    %{_prefix}/bin/ismaildup

%attr(755,root,root)                    %{libexecdir}/controlsync
%attr(755,root,root)                    %{libexecdir}/mailzipper
%attr(755,root,root)                    %{libexecdir}/updatefile
%attr(755,root,root)                    %{libexecdir}/cputime
%attr(755,root,root)                    %{libexecdir}/myslave
%attr(755,root,root)                    %{libexecdir}/bogofilter-qfe
%attr(755,root,root)                    %{libexecdir}/iupgrade.sh
%verify (not md5 size mtime mode)       %{libexecdir}/ilocal_upgrade.sh

%attr(755,root,root)                    %{libexecdir}/vadddomain
%attr(755,root,root)                    %{libexecdir}/vaddaliasdomain
%attr(755,root,root)                    %{libexecdir}/vpasswd
%attr(755,root,root)                    %{libexecdir}/vrenamedomain
%attr(755,root,root)                    %{libexecdir}/vdeldomain
%attr(755,root,root)                    %{libexecdir}/vadduser
%attr(755,root,root)                    %{libexecdir}/vmoduser
%attr(755,root,root)                    %{libexecdir}/vdeluser
%attr(755,root,root)                    %{libexecdir}/vrenameuser
%attr(755,root,root)                    %{libexecdir}/overquota.sh
%attr(755,root,root)                    %{libexecdir}/qmailmrtg7

%attr(755,root,root)                    %{libexecdir}/imapmodules/authindi
%attr(755,root,root)                    %{libexecdir}/imapmodules/authgeneric
%attr(755,root,root)                    %{imoduledir}/iauth.so
%attr(755,root,root)                    %{imoduledir}/tcplookup.so

%docdir %{shareddir}/doc
%docdir %{mandir}
%attr(644,root,root)                    %{mandir}/man[1,5,7,8]/*

%if %build_on_obs == 0
%license %attr(644,root,root)           %{shareddir}/doc/COPYING-indimail
%else
%attr(644,root,root)                    %{shareddir}/doc/COPYING-indimail
%endif

%attr(644,root,root)                    %{shareddir}/doc/ChangeLog-indimail
%attr(644,root,root)                    %{shareddir}/doc/FAQ.pdf
%attr(644,root,root)                    %{shareddir}/doc/README-indimail.md
%attr(644,root,root)                    %{shareddir}/doc/README-ldap.md
%attr(644,root,root)                    %{shareddir}/doc/README-vlimits.md


# Shared libraries (omit for architectures that don't support them)

%files devel
%defattr(-, root, root, 0755)
%dir %attr(755,root,root)              %{_prefix}/include/indimail
%if "%{_prefix}" != "/usr"
%dir %attr(555,root,root)              %{_libdir}
%dir %attr(555,root,root)              %{mandir}/man3
%endif
%doc %attr(644,root,root)              %{mandir}/man3/*

%attr(644,root,root)                    %{_prefix}/include/indimail/eps_unroll.h
%attr(644,root,root)                    %{_prefix}/include/indimail/eps_buffer.h
%attr(644,root,root)                    %{_prefix}/include/indimail/eps_email.h
%attr(644,root,root)                    %{_prefix}/include/indimail/rfc2822.h
%attr(644,root,root)                    %{_prefix}/include/indimail/eps_mime.h
%attr(644,root,root)                    %{_prefix}/include/indimail/eps_boundary.h
%attr(644,root,root)                    %{_prefix}/include/indimail/eps_roll.h
%attr(644,root,root)                    %{_prefix}/include/indimail/eps_line.h
%attr(644,root,root)                    %{_prefix}/include/indimail/eps_int_buffer.h
%attr(644,root,root)                    %{_prefix}/include/indimail/eps_base64.h
%attr(644,root,root)                    %{_prefix}/include/indimail/eps_misc.h
%attr(644,root,root)                    %{_prefix}/include/indimail/eps_address.h
%attr(644,root,root)                    %{_prefix}/include/indimail/eps.h
%attr(644,root,root)                    %{_prefix}/include/indimail/eps_interface.h
%attr(644,root,root)                    %{_prefix}/include/indimail/eps_int_stream.h
%attr(644,root,root)                    %{_prefix}/include/indimail/eps_header.h
%attr(644,root,root)                    %{_prefix}/include/indimail/eps_content.h
%attr(644,root,root)                    %{_prefix}/include/indimail/addaliasdomain.h
%attr(644,root,root)                    %{_prefix}/include/indimail/add_control.h
%attr(644,root,root)                    %{_prefix}/include/indimail/add_domain_assign.h
%attr(644,root,root)                    %{_prefix}/include/indimail/addressToken.h
%attr(644,root,root)                    %{_prefix}/include/indimail/add_user_assign.h
%attr(644,root,root)                    %{_prefix}/include/indimail/addusercntrl.h
%attr(644,root,root)                    %{_prefix}/include/indimail/add_vacation.h
%attr(644,root,root)                    %{_prefix}/include/indimail/adminCmmd.h
%attr(644,root,root)                    %{_prefix}/include/indimail/AliasInLookup.h
%attr(644,root,root)                    %{_prefix}/include/indimail/atrn_map.h
%attr(644,root,root)                    %{_prefix}/include/indimail/auth_admin.h
%attr(644,root,root)                    %{_prefix}/include/indimail/autoturn_dir.h
%attr(644,root,root)                    %{_prefix}/include/indimail/backfill.h
%attr(644,root,root)                    %{_prefix}/include/indimail/bulk_mail.h
%attr(644,root,root)                    %{_prefix}/include/indimail/bulletin.h
%attr(644,root,root)                    %{_prefix}/include/indimail/check_group.h
%attr(644,root,root)                    %{_prefix}/include/indimail/Check_Login.h
%attr(644,root,root)                    %{_prefix}/include/indimail/checkPerm.h
%attr(644,root,root)                    %{_prefix}/include/indimail/check_quota.h
%attr(644,root,root)                    %{_prefix}/include/indimail/clear_open_smtp.h
%attr(644,root,root)                    %{_prefix}/include/indimail/close_big_dir.h
%attr(644,root,root)                    %{_prefix}/include/indimail/cntrl_clearaddflag.h
%attr(644,root,root)                    %{_prefix}/include/indimail/cntrl_cleardelflag.h
%attr(644,root,root)                    %{_prefix}/include/indimail/common.h
%attr(644,root,root)                    %{_prefix}/include/indimail/compile_morercpthosts.h
%attr(644,root,root)                    %{_prefix}/include/indimail/CopyEmailFile.h
%attr(644,root,root)                    %{_prefix}/include/indimail/copyPwdStruct.h
%attr(644,root,root)                    %{_prefix}/include/indimail/count_dir.h
%attr(644,root,root)                    %{_prefix}/include/indimail/count_rcpthosts.h
%attr(644,root,root)                    %{_prefix}/include/indimail/count_table.h
%attr(644,root,root)                    %{_prefix}/include/indimail/crc.h
%attr(644,root,root)                    %{_prefix}/include/indimail/CreateDomainDirs.h
%attr(644,root,root)                    %{_prefix}/include/indimail/create_table.h
%attr(644,root,root)                    %{_prefix}/include/indimail/dbinfoAdd.h
%attr(644,root,root)                    %{_prefix}/include/indimail/dbinfoDel.h
%attr(644,root,root)                    %{_prefix}/include/indimail/dbinfoSelect.h
%attr(644,root,root)                    %{_prefix}/include/indimail/dbinfoUpdate.h
%attr(644,root,root)                    %{_prefix}/include/indimail/dbload.h
%attr(644,root,root)                    %{_prefix}/include/indimail/dblock.h
%attr(644,root,root)                    %{_prefix}/include/indimail/del_control.h
%attr(644,root,root)                    %{_prefix}/include/indimail/del_domain_assign.h
%attr(644,root,root)                    %{_prefix}/include/indimail/deldomain.h
%attr(644,root,root)                    %{_prefix}/include/indimail/deliver_mail.h
%attr(644,root,root)                    %{_prefix}/include/indimail/delunreadmails.h
%attr(644,root,root)                    %{_prefix}/include/indimail/del_user_assign.h
%attr(644,root,root)                    %{_prefix}/include/indimail/delusercntrl.h
%attr(644,root,root)                    %{_prefix}/include/indimail/deluser.h
%attr(644,root,root)                    %{_prefix}/include/indimail/dir_control.h
%attr(644,root,root)                    %{_prefix}/include/indimail/Dirname.h
%attr(644,root,root)                    %{_prefix}/include/indimail/disable_mysql_escape.h
%attr(644,root,root)                    %{_prefix}/include/indimail/evaluate.h
%attr(644,root,root)                    %{_prefix}/include/indimail/fappend.h
%attr(644,root,root)                    %{_prefix}/include/indimail/FifoCreate.h
%attr(644,root,root)                    %{_prefix}/include/indimail/filewrt.h
%attr(644,root,root)                    %{_prefix}/include/indimail/findhost.h
%attr(644,root,root)                    %{_prefix}/include/indimail/findmdahost.h
%attr(644,root,root)                    %{_prefix}/include/indimail/fstabChangeCounters.h
%attr(644,root,root)                    %{_prefix}/include/indimail/getactualpath.h
%attr(644,root,root)                    %{_prefix}/include/indimail/getAddressBook.h
%attr(644,root,root)                    %{_prefix}/include/indimail/get_assign.h
%attr(644,root,root)                    %{_prefix}/include/indimail/getFreeFS.h
%attr(644,root,root)                    %{_prefix}/include/indimail/getindimail.h
%attr(644,root,root)                    %{_prefix}/include/indimail/get_indimailuidgid.h
%attr(644,root,root)                    %{_prefix}/include/indimail/getlastauth.h
%attr(644,root,root)                    %{_prefix}/include/indimail/get_local_hostid.h
%attr(644,root,root)                    %{_prefix}/include/indimail/get_local_ip.h
%attr(644,root,root)                    %{_prefix}/include/indimail/get_localtime.h
%attr(644,root,root)                    %{_prefix}/include/indimail/get_message_size.h
%attr(644,root,root)                    %{_prefix}/include/indimail/get_Mplexdir.h
%attr(644,root,root)                    %{_prefix}/include/indimail/getpeer.h
%attr(644,root,root)                    %{_prefix}/include/indimail/GetPrefix.h
%attr(644,root,root)                    %{_prefix}/include/indimail/get_real_domain.h
%attr(644,root,root)                    %{_prefix}/include/indimail/GetSMTProute.h
%attr(644,root,root)                    %{_prefix}/include/indimail/smtp_port.h
%attr(644,root,root)                    %{_prefix}/include/indimail/getuidgid.h
%attr(644,root,root)                    %{_prefix}/include/indimail/hostcntrl_select.h
%attr(644,root,root)                    %{_prefix}/include/indimail/host_in_locals.h
%attr(644,root,root)                    %{_prefix}/include/indimail/iadddomain.h
%attr(644,root,root)                    %{_prefix}/include/indimail/iadduser.h
%attr(644,root,root)                    %{_prefix}/include/indimail/iclose.h
%attr(644,root,root)                    %{_prefix}/include/indimail/in_bsearch.h
%attr(644,root,root)                    %{_prefix}/include/indimail/indimail_compat.h
%attr(644,root,root)                    %{_prefix}/include/indimail/indimail_config.h
%attr(644,root,root)                    %{_prefix}/include/indimail/indimail.h
%attr(644,root,root)                    %{_prefix}/include/indimail/inquery.h
%attr(644,root,root)                    %{_prefix}/include/indimail/iopen.h
%attr(644,root,root)                    %{_prefix}/include/indimail/ipasswd.h
%attr(644,root,root)                    %{_prefix}/include/indimail/ip_map.h
%attr(644,root,root)                    %{_prefix}/include/indimail/is_alias_domain.h
%attr(644,root,root)                    %{_prefix}/include/indimail/is_already_running.h
%attr(644,root,root)                    %{_prefix}/include/indimail/is_distributed_domain.h
%attr(644,root,root)                    %{_prefix}/include/indimail/islocalif.h
%attr(644,root,root)                    %{_prefix}/include/indimail/ismaildup.h
%attr(644,root,root)                    %{_prefix}/include/indimail/isnum.h
%attr(644,root,root)                    %{_prefix}/include/indimail/is_user_present.h
%attr(644,root,root)                    %{_prefix}/include/indimail/isvalid_domain.h
%attr(644,root,root)                    %{_prefix}/include/indimail/isvirtualdomain.h
%attr(644,root,root)                    %{_prefix}/include/indimail/layout.h
%attr(644,root,root)                    %{_prefix}/include/indimail/LoadBMF.h
%attr(644,root,root)                    %{_prefix}/include/indimail/LoadDbInfo.h
%attr(644,root,root)                    %{_prefix}/include/indimail/lockfile.h
%attr(644,root,root)                    %{_prefix}/include/indimail/Login_Tasks.h
%attr(644,root,root)                    %{_prefix}/include/indimail/lowerit.h
%attr(644,root,root)                    %{_prefix}/include/indimail/maildir_to_domain.h
%attr(644,root,root)                    %{_prefix}/include/indimail/maildir_to_email.h
%attr(644,root,root)                    %{_prefix}/include/indimail/MailQuotaWarn.h
%attr(644,root,root)                    %{_prefix}/include/indimail/MakeArgs.h
%attr(644,root,root)                    %{_prefix}/include/indimail/makeseekable.h
%attr(644,root,root)                    %{_prefix}/include/indimail/make_user_dir.h
%attr(644,root,root)                    %{_prefix}/include/indimail/mdaMySQLConnect.h
%attr(644,root,root)                    %{_prefix}/include/indimail/mgmtpassfuncs.h
%attr(644,root,root)                    %{_prefix}/include/indimail/monkey.h
%attr(644,root,root)                    %{_prefix}/include/indimail/MoveFile.h
%attr(644,root,root)                    %{_prefix}/include/indimail/munch_domain.h
%attr(644,root,root)                    %{_prefix}/include/indimail/mysql_stack.h
%attr(644,root,root)                    %{_prefix}/include/indimail/next_big_dir.h
%attr(644,root,root)                    %{_prefix}/include/indimail/no_of_days.h
%attr(644,root,root)                    %{_prefix}/include/indimail/open_big_dir.h
%attr(644,root,root)                    %{_prefix}/include/indimail/open_master.h
%attr(644,root,root)                    %{_prefix}/include/indimail/open_smtp_relay.h
%attr(644,root,root)                    %{_prefix}/include/indimail/parseAddress.h
%attr(644,root,root)                    %{_prefix}/include/indimail/parse_email.h
%attr(644,root,root)                    %{_prefix}/include/indimail/parse_quota.h
%attr(644,root,root)                    %{_prefix}/include/indimail/passwd_policy.h
%attr(644,root,root)                    %{_prefix}/include/indimail/pathToFilesystem.h
%attr(644,root,root)                    %{_prefix}/include/indimail/pipe_exec.h
%attr(644,root,root)                    %{_prefix}/include/indimail/post_handle.h
%attr(644,root,root)                    %{_prefix}/include/indimail/print_control.h
%attr(644,root,root)                    %{_prefix}/include/indimail/ProcessInFifo.h
%attr(644,root,root)                    %{_prefix}/include/indimail/proxylogin.h
%attr(644,root,root)                    %{_prefix}/include/indimail/purge_files.h
%attr(644,root,root)                    %{_prefix}/include/indimail/pwcomp.h
%attr(644,root,root)                    %{_prefix}/include/indimail/PwdInLookup.h
%attr(644,root,root)                    %{_prefix}/include/indimail/qmail_remote.h
%attr(644,root,root)                    %{_prefix}/include/indimail/recalc_quota.h
%attr(644,root,root)                    %{_prefix}/include/indimail/RelayInLookup.h
%attr(644,root,root)                    %{_prefix}/include/indimail/relay_select.h
%attr(644,root,root)                    %{_prefix}/include/indimail/RemoteBulkMail.h
%attr(644,root,root)                    %{_prefix}/include/indimail/remove_line.h
%attr(644,root,root)                    %{_prefix}/include/indimail/remove_quotes.h
%attr(644,root,root)                    %{_prefix}/include/indimail/renameuser.h
%attr(644,root,root)                    %{_prefix}/include/indimail/replacestr.h
%attr(644,root,root)                    %{_prefix}/include/indimail/r_mkdir.h
%attr(644,root,root)                    %{_prefix}/include/indimail/runcmmd.h
%attr(644,root,root)                    %{_prefix}/include/indimail/SendWelcomeMail.h
%attr(644,root,root)                    %{_prefix}/include/indimail/set_mysql_options.h
%attr(644,root,root)                    %{_prefix}/include/indimail/setuserquota.h
%attr(644,root,root)                    %{_prefix}/include/indimail/skip_relay.h
%attr(644,root,root)                    %{_prefix}/include/indimail/skip_system_files.h
%attr(644,root,root)                    %{_prefix}/include/indimail/sockwrite.h
%attr(644,root,root)                    %{_prefix}/include/indimail/spam.h
%attr(644,root,root)                    %{_prefix}/include/indimail/sql_active.h
%attr(644,root,root)                    %{_prefix}/include/indimail/sql_adddomain.h
%attr(644,root,root)                    %{_prefix}/include/indimail/sql_adduser.h
%attr(644,root,root)                    %{_prefix}/include/indimail/sql_delaliasdomain.h
%attr(644,root,root)                    %{_prefix}/include/indimail/sql_deldomain.h
%attr(644,root,root)                    %{_prefix}/include/indimail/sql_deluser.h
%attr(644,root,root)                    %{_prefix}/include/indimail/sql_getall.h
%attr(644,root,root)                    %{_prefix}/include/indimail/sql_getflags.h
%attr(644,root,root)                    %{_prefix}/include/indimail/sql_gethostid.h
%attr(644,root,root)                    %{_prefix}/include/indimail/sql_getip.h
%attr(644,root,root)                    %{_prefix}/include/indimail/sql_getpw.h
%attr(644,root,root)                    %{_prefix}/include/indimail/sql_get_realdomain.h
%attr(644,root,root)                    %{_prefix}/include/indimail/sql_init.h
%attr(644,root,root)                    %{_prefix}/include/indimail/sql_insertaliasdomain.h
%attr(644,root,root)                    %{_prefix}/include/indimail/sqlOpen_user.h
%attr(644,root,root)                    %{_prefix}/include/indimail/sql_passwd.h
%attr(644,root,root)                    %{_prefix}/include/indimail/sql_renamedomain.h
%attr(644,root,root)                    %{_prefix}/include/indimail/SqlServer.h
%attr(644,root,root)                    %{_prefix}/include/indimail/sql_setpw.h
%attr(644,root,root)                    %{_prefix}/include/indimail/sql_setquota.h
%attr(644,root,root)                    %{_prefix}/include/indimail/sql_updateflag.h
%attr(644,root,root)                    %{_prefix}/include/indimail/storeHeader.h
%attr(644,root,root)                    %{_prefix}/include/indimail/strToPw.h
%attr(644,root,root)                    %{_prefix}/include/indimail/tcpbind.h
%attr(644,root,root)                    %{_prefix}/include/indimail/tcpopen.h
%attr(644,root,root)                    %{_prefix}/include/indimail/tls.h
%attr(644,root,root)                    %{_prefix}/include/indimail/trashpurge.h
%attr(644,root,root)                    %{_prefix}/include/indimail/udpopen.h
%attr(644,root,root)                    %{_prefix}/include/indimail/update_file.h
%attr(644,root,root)                    %{_prefix}/include/indimail/update_local_hostid.h
%attr(644,root,root)                    %{_prefix}/include/indimail/update_newu.h
%attr(644,root,root)                    %{_prefix}/include/indimail/update_quota.h
%attr(644,root,root)                    %{_prefix}/include/indimail/update_rules.h
%attr(644,root,root)                    %{_prefix}/include/indimail/updusercntrl.h
%attr(644,root,root)                    %{_prefix}/include/indimail/userinfo.h
%attr(644,root,root)                    %{_prefix}/include/indimail/UserInLookup.h
%attr(644,root,root)                    %{_prefix}/include/indimail/user_over_quota.h
%attr(644,root,root)                    %{_prefix}/include/indimail/valiasCount.h
%attr(644,root,root)                    %{_prefix}/include/indimail/valias_delete_domain.h
%attr(644,root,root)                    %{_prefix}/include/indimail/valias_delete.h
%attr(644,root,root)                    %{_prefix}/include/indimail/valiasinfo.h
%attr(644,root,root)                    %{_prefix}/include/indimail/valias_insert.h
%attr(644,root,root)                    %{_prefix}/include/indimail/valias_select.h
%attr(644,root,root)                    %{_prefix}/include/indimail/valias_update.h
%attr(644,root,root)                    %{_prefix}/include/indimail/variables.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vdelfiles.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vfilter_delete.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vfilter_display.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vfilter_filterNo.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vfilter_header.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vfilter_insert.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vfilter_select.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vfilter_update.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vfstab.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vget_lastauth.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vgetpasswd.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vhostid_delete.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vhostid_insert.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vhostid_select.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vhostid_update.h
%attr(644,root,root)                    %{_prefix}/include/indimail/VlimitInLookup.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vlimits.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vmake_maildir.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vpriv.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vquota_select.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vset_lastauth.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vset_lastdeliver.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vsmtp_delete_domain.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vsmtp_delete.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vsmtp_insert.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vsmtp_select.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vsmtp_update.h
%attr(644,root,root)                    %{_prefix}/include/indimail/vupdate_rules.h
%attr(644,root,root)                    %{_prefix}/include/indimail/wildmat.h
%attr(644,root,root)                    %{_prefix}/include/indimail/load_mysql.h

%{_libdir}/libeps.a
%{_libdir}/libindimail.a

%{_libdir}/libeps.so
%{_libdir}/libindimail.so

%{_pkg_config_path}/libindimail.pc

%files -n libindimail
%defattr(-, root, root, 0755)
# Shared libraries (omit for architectures that don't support them)
%{_libdir}/libeps.so.1
%{_libdir}/libeps.so.1.0.0
%{_libdir}/libindimail.so.3
%{_libdir}/libindimail.so.3.0.0

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -fr %{buildroot}
%{__rm} -fr %{_builddir}/%{name}-%{version}
%if %{undefined nodebug}
%{__rm} -f %{_builddir}/debugfiles.list %{_builddir}/debuglinks.list \
  %{_builddir}/debugsourcefiles.list %{_builddir}/debugsources.list \
  %{_builddir}/elfbins.list
%endif

#            install   erase   upgrade  reinstall
# pretrans      0        -         0
# pre           1        -         2         2
# post          1        -         2         2
# preun         -        0         1         -
# postun        -        0         1         -
# posttrans     0        -         0
# The scriptlets in %%pre and %%post are respectively run before and after a package is installed.
# The scriptlets %%preun and %%postun are run before and after a package is uninstalled.
# The scriptlets %%pretrans and %%posttrans are run at start and end of a transaction.
# On upgrade, the scripts are run in the following order:
#
#   1. pretrans of new package
#   2. pre of new package
#   3. (package install)
#   4. post of new package
#   5. preun of old package
#   6. (removal of old package)
#   7. postun of old package
#   8. posttrans of new package

### SCRIPTLET ###############################################################################
%verifyscript
ID=$(id -u)
if [ $ID -ne 0 ] ; then
  echo "You are not root" 1>&2
  exit 1
fi
%{_prefix}/sbin/svctool --check-install --servicedir=%{servicedir} \
  --qbase=%{qbase} --qcount=%{qcount} --qstart=1

%if 0%{?suse_version} >= 1120
  %verify_permissions -e %{_prefix}/bin/vdeluser
  %verify_permissions -e %{_prefix}/bin/vadduser
  %verify_permissions -e %{_prefix}/bin/vaddaliasdomain
  %verify_permissions -e %{_prefix}/bin/vrenamedomain
  %verify_permissions -e %{_prefix}/bin/vsetuserquota
  %verify_permissions -e %{_prefix}/bin/vmoveuser
  %verify_permissions -e %{_prefix}/bin/vdeldomain
  %verify_permissions -e %{_prefix}/bin/vadddomain
  %verify_permissions -e %{_prefix}/bin/vdominfo
  %verify_permissions -e %{_prefix}/bin/vrenameuser
  %verify_permissions -e %{_prefix}/bin/printdir
  %verify_permissions -e %{_prefix}/bin/vmoduser
  %verify_permissions -e %{_prefix}/bin/vcfilter
  %verify_permissions -e %{_prefix}/bin/vbulletin
  %verify_permissions -e %{libexecdir}/sq_vacation
  %verify_permissions -e %{libexecdir}/imapmodules/authshadow
%endif

### SCRIPTLET ###############################################################################
%pretrans
argv1=$1
ID=$(id -u)
if [ $ID -ne 0 ] ; then
  echo "You are not root" 1>&2
  exit 1
fi

# stop indimail services before upgrade
if [ -d /run ] ; then
  rundir=/run/svscan
elif [ -d /var/run ] ; then
  rundir=/var/run/svscan
else
  rundir=%{servicedir}
fi
for i in mrtg mysql.3306 indisrvr.4000 inlookup.infifo \
qmail-poppass.106 qmail-logfifo
do
  %{_prefix}/bin/svstat %{servicedir}/$i >/dev/null 2>&1
  if [ $? -eq 0 ] ; then
    %{__mkdir_p} ${rundir}/$i
    touch ${rundir}/$i/.down
    %{_prefix}/bin/svc -d %{servicedir}/$i
  fi
done

if [ %noproxy -eq 0 ] ; then
  for i in proxy-imapd.4143 proxy-imapd-ssl.9143 \
    proxy-pop3d.4110 proxy-pop3d-ssl.9110
  do
    %{_prefix}/bin/svstat %{servicedir}/$i >/dev/null 2>&1
    if [ $? -eq 0 ] ; then
      %{__mkdir_p} ${rundir}/$i
      touch ${rundir}/$i/.down
      %{_prefix}/bin/svc -d %{servicedir}/$i
    fi
  done
fi

# initialize setup log file
if [ -f %{libexecdir}/iupgrade.sh ] ; then
(
  echo "Running Custom Installation Script for pretrans"
  /bin/sh %{libexecdir}/iupgrade.sh pretrans noargs %{version} $*
) > /var/log/indimail-setup.log 2>&1
fi

### SCRIPTLET ###############################################################################
%pre
argv1=$1
ID=$(id -u)
if [ $ID -ne 0 ] ; then
  echo "You are not root" 1>&2
  exit 1
fi
if [ -z "$argv1" ] ; then
  argv1=0
fi
# we are doing upgrade
if [ $argv1 -eq 2 ] ; then
  (
  if [ -f %{libexecdir}/iupgrade.sh ] ; then
    echo "Running Custom Upgrade Script for pre upgrade"
    /bin/sh %{libexecdir}/iupgrade.sh pre upgrade %{version} $*
  fi
  ) >> /var/log/indimail-setup.log 2>&1
  exit 0
fi
(
echo "Checking for mandatory user/group mysql.."
case "%{_host}" in
  *-*-darwin*)
  /usr/bin/dscl . -list /Groups/mysql > /dev/null || (echo "group mysql does not exist. Aborting..." && false)
  if [ $? -ne 0 ] ; then
    exit 1
  fi
  /usr/bin/dscl . -list /Users/mysql > /dev/null || (echo "user mysql does not exist. Aborting..." && false)
  if [ $? -ne 0 ] ; then
    exit 1
  fi
  ;;
  *)
  /usr/bin/getent group  mysql > /dev/null || (echo "group mysql does not exist. Aborting..." && false)
  if [ $? -ne 0 ] ; then
    exit 1
  fi
  /usr/bin/getent passwd mysql > /dev/null || (echo "user  mysql does not exist. Aborting..." && false)
  if [ $? -ne 0 ] ; then
    exit 1
  fi
esac
#
# Create a users and groups. Do not report any problems if they already
# exists.
#
nscd_up=`ps -ef |grep nscd |grep -v grep|wc -l`
if [ $nscd_up -ge 1 ] ; then
  if [ -x %{_sysconfdir}/init.d/nscd ] ; then
    %{_sysconfdir}/init.d/nscd stop
  elif [ -f %{_sysconfdir}/lib/systemd/system/multi-user.target/nscd.service ] ; then
    /bin/systemctl start nscd.service
  fi
fi
echo "Adding IndiMail users/groups"
/usr/bin/getent group %groupname  > /dev/null || /usr/sbin/groupadd -r -g %gid %groupname || true
if [ $? = 4 ] ; then
  /usr/sbin/groupadd %groupname
fi
# add for roundcube/php to access certs
/usr/bin/getent group apache    > /dev/null && /usr/sbin/usermod -aG qmail apache || true

/usr/bin/getent passwd %username > /dev/null || /usr/sbin/useradd -r -g %groupname -u %uid -d %{indimaildir} %username || true
if [ $? = 4 ] ; then
  /usr/sbin/useradd -r -g %groupname -d %{indimaildir} %username
fi

if [ $nscd_up -ge 1 ] ; then
  if [ -x %{_sysconfdir}/init.d/nscd ] ; then
    %{_sysconfdir}/init.d/nscd start
  elif [ -f %{_sysconfdir}/lib/systemd/system/multi-user.target/nscd.service ] ; then
    /bin/systemctl start nscd.service
  fi
fi
) >> /var/log/indimail-setup.log 2>&1

### SCRIPTLET ###############################################################################
%post
argv1=$1
ID=$(id -u)
if [ $ID -ne 0 ] ; then
  echo "You are not root" 1>&2
  exit 1
fi

if [ -z "$argv1" ] ; then
  argv1=0
fi
if [ $argv1 -eq 2 ] ; then # upgrade
  (
  echo "doing post upgrade activities"
  if [ "%{_libdir}" != "/usr/lib64" -a "%{_libdir}" != "/usr/lib" ] ; then
    /sbin/ldconfig
  fi
  if [ -f %{libexecdir}/iupgrade.sh ] ; then
    echo "Running Custom Upgrade Script for post upgrade"
    /bin/sh %{libexecdir}/iupgrade.sh post upgrade %{version} $*
  fi

  # start indimail services after upgrade
  if [ -d /run ] ; then
    rundir=/run/svscan
  elif [ -d /var/run ] ; then
    rundir=/var/run/svscan
  else
    rundir=%{servicedir}
  fi
  for i in mrtg mysql.3306 indisrvr.4000 inlookup.infifo \
  qmail-poppass.106 qmail-logfifo
  do
    %{_prefix}/bin/svok %{servicedir}/$i >/dev/null 2>&1
    if [ $? -eq 0 -a -f ${rundir}/$i/.down ] ; then
      %{__rm} -f ${rundir}/$i/.down
      %{_prefix}/bin/svc -u %{servicedir}/$i
    fi
  done
  if [ %noproxy -eq 0 ] ; then
    for i in proxy-imapd.4143 proxy-imapd-ssl.9143 \
      proxy-pop3d.4110 proxy-pop3d-ssl.9110
    do
      %{_prefix}/bin/svok %{servicedir}/$i >/dev/null 2>&1
      if [ $? -eq 0 -a -f ${rundir}/$i/.down ] ; then
        %{__rm} -f ${rundir}/$i/.down
        %{_prefix}/bin/svc -u %{servicedir}/$i
      fi
    done
  fi

  #selinux
  %{_prefix}/sbin/svctool --servicedir=%{servicedir} --config=iselinux

  # refresh indimail services
  %{_prefix}/sbin/svctool --servicedir=%{servicedir} --refreshsvc="$svc_list"
  indlib=`ls -d %{_libdir}/libindimail.so.*.*.* 2>/dev/null`
  for port in 25 465 587
  do
    if [ -n "$indlib" -a -f "$indlib" ] ; then
      echo $indlib > %{servicedir}/qmail-smtpd.$port/variables/VIRTUAL_PKG_LIB
    fi
  done
  if [ -n "$indlib" -a -f "$indlib" ] ; then
    echo $indlib > %{servicedir}/qmail-send.25/variables/VIRTUAL_PKG_LIB
  fi
  ) >> /var/log/indimail-setup.log 2>&1
  exit 0
fi

echo "Doing Post Install"
echo ""
echo "1. Configure %{logdir} for multilog"
echo "2. Configure %{servicedir}"
echo "3. Configure IndiMail settings"
echo "4. Configure %{sysconfdir}/indimail.cnf for MySQL service"
echo "5. Configure MySQL DB in %{indimaildir}/mysqldb/data"
echo "6. Configure indisrvr, inlookup, poppass service"
echo "7. Configure tcprules database for popass"
echo "8. Configure selinux configuration"
echo "9. Configure default cron entries"
echo ""

(
# Recreate ld.so links and cache
if [ "%{_libdir}" != "/usr/lib64" -a "%{_libdir}" != "/usr/lib" ] ; then
  if [ -d %{_sysconfdir}/ld.so.conf.d ] ; then
    echo %{_libdir} > %{_sysconfdir}/ld.so.conf.d/indimail-%{_arch}.conf
  fi
  /sbin/ldconfig
fi

%if %build_on_obs == 1
  default_domain=%{defaultDomain}
%else
  if [ -x /usr/bin/uname -o -x /bin/uname ] ; then
    default_domain=$([ -n "$HOSTNAME" ] && echo "$HOSTNAME" || `uname -n`)
  else
    default_domain=$([ -n "$HOSTNAME" ] && echo "$HOSTNAME" || echo %{defaultDomain})
  fi
%endif

if [ %noproxy -eq 0 ] ; then
%ifarch x86_64
%global imap_pop3_mem 104857600
%global imapspop3_mem 104857600
%else
%global imap_pop3_mem 52428800
%global imapspop3_mem 52428800
%endif
%{_prefix}/sbin/svctool --imap=4143 --servicedir=%{servicedir} --localip=0 --maxdaemons=40 \
  --maxperip=25 --query-cache --default-domain=$default_domain --memory=%{imap_pop3_mem} \
  --proxy=143 --starttls --tlsprog=%{_prefix}/bin/sslerator --infifo=infifo
%{_prefix}/sbin/svctool --imap=9143 --servicedir=%{servicedir} --localip=0 --maxdaemons=40 \
  --maxperip=25 --query-cache --default-domain=$default_domain --memory=%{imapspop3_mem} \
  --proxy=143 --ssl --infifo=infifo
%{_prefix}/sbin/svctool --pop3=4110 --servicedir=%{servicedir} --localip=0 --maxdaemons=40 \
  --maxperip=25 --query-cache --default-domain=$default_domain --memory=%{imap_pop3_mem} \
  --proxy=110 --starttls --tlsprog=%{_prefix}/bin/sslerator --infifo=infifo
%{_prefix}/sbin/svctool --pop3=9110 --servicedir=%{servicedir} --localip=0 --maxdaemons=40 \
  --maxperip=25 --query-cache --default-domain=$default_domain --memory=%{imapspop3_mem} \
  --proxy=110 --ssl --infifo=infifo

# add courier-imap auth module authindi
echo "adding authindi as Proxy IMAP/POP3 auth module"
for i in `ls -d %{servicedir}/proxy-pop3d* %{servicedir}/proxy-imapd*`
do
  if [ -s $i/variables/IMAPMODULES ] ; then
    grep authindi $i/variables/IMAPMODULES > /dev/null
    if [ $? -ne 0 ] ; then
      AUTHM="`cat $i/variables/IMAPMODULES` authindi"
      echo $AUTHM > $i/variables/IMAPMODULES
    fi
  fi
done
fi

# add courier-imap auth module authindi
echo "adding authindi as IMAP/POP3 auth module"
for i in `ls -d %{servicedir}/qmail-pop3d* %{servicedir}/qmail-imapd*`
do
  if [ -s $i/variables/IMAPMODULES ] ; then
    grep authindi $i/variables/IMAPMODULES > /dev/null
    if [ $? -ne 0 ] ; then
      AUTHM="`cat $i/variables/IMAPMODULES` authindi"
      echo $AUTHM > $i/variables/IMAPMODULES
    fi
  fi
done

# add checkpassword auth module vchkpass
echo "adding vchkpass as SMTP auth module"
for i in 465 587
do
  if [ -s %{servicedir}/qmail-smtpd.$i/variables/AUTHMODULES ] ; then
    grep vchkpass %{servicedir}/qmail-smtpd.$i/variables/AUTHMODULES > /dev/null
    if [ $? -ne 0 ] ; then
      AUTHM="`cat %{servicedir}/qmail-smtpd.$i/variables/AUTHMODULES` /usr/sbin/vchkpass"
      echo $AUTHM > %{servicedir}/qmail-smtpd.$i/variables/AUTHMODULES
    fi
  fi
done

for i in logfifo inlookup indisrvr mrtg mysql.3306
do
  %{__mkdir_p} %{logdir}/$i
  %{__chown} -R qmaill:nofiles %{logdir}/$i
done

if [ %noproxy -eq 0 ] ; then
  for i in proxyIMAP.4143 proxyPOP3.4110
  do
    %{__mkdir_p} %{logdir}/$i
    %{__chown} -R qmaill:nofiles %{logdir}/$i
  done
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

# fifolog service
%{_prefix}/sbin/svctool --fifologger=$logfifo --servicedir=%{servicedir}

# mrtg service
%{_prefix}/sbin/svctool --mrtg=/var/www/html/mailmrtg --servicedir=%{servicedir}

echo "Creating default mysql.host, tcprules, bogofilter-qfe, default domain dir"
%{_prefix}/sbin/svctool --config=indimail --mysqlhost=localhost --mysqluser=indimail  \
  --mysqlpass=ssh-1.5- --mysqlsocket=%{mysqlSocket} --default-domain=$default_domain

# MySQL
if [ -x %{mysqlPrefix}/libexec/mysqld -o -x %{mysqlPrefix}/sbin/mysqld -o -x %{mysqlPrefix}/bin/mysqld ] ; then
  error=`ps -e|grep mysqld|grep -v grep|wc -l` # another mysqld instance running ?
  echo "Creating Database/Service for MySQL"
  # MySQL Config Creation
  %{_prefix}/sbin/svctool --config=mysql   --mysqlPrefix=%{mysqlPrefix} --mysqlsocket=%{mysqlSocket} \
      --databasedir=%{indimaildir}/mysqldb
  # MySQL Database Creation
  %{_prefix}/sbin/svctool --config=mysqldb --mysqlPrefix=%{mysqlPrefix} \
      --databasedir=%{indimaildir}/mysqldb --base_path=%{mbase} --mysqlsocket="%{mysqlSocket}".tmp
  # MySQL Supervise creation
  %{_prefix}/sbin/svctool --mysql=3306 --servicedir=%{servicedir} --mysqlPrefix=%{mysqlPrefix} \
    --databasedir=%{indimaildir}/mysqldb --config=%{sysconfdir}/indimail.cnf --default-domain=$default_domain
  if [ ! -f %{indimaildir}/mysqldb/data/indimail/indimail.frm -a ! -f %{indimaildir}/mysqldb/data/indimail/indimail.ibd ] ; then
    error=1
  fi
  if [ $error -gt 0 ] ; then
    echo "Disabling mysqld service"
    touch %{servicedir}/mysql.3306/down
  fi
else
  echo "WARNING!!! Did not find mysqld in %{mysqlPrefix}/{libexec,sbin}. Skipping MySQL configuration" 1>&2
fi

%if 0%{?suse_version} >= 1120
%if 0%{?set_permissions:1} > 0
  %set_permissions %{_prefix}/bin/printdir
  %set_permissions %{_prefix}/bin/vaddaliasdomain
  %set_permissions %{_prefix}/bin/vadddomain
  %set_permissions %{_prefix}/bin/vadduser
  %set_permissions %{_prefix}/bin/vbulletin
  %set_permissions %{_prefix}/bin/vcfilter
  %set_permissions %{_prefix}/bin/vdeldomain
  %set_permissions %{_prefix}/bin/vdeluser
  %set_permissions %{_prefix}/bin/vdominfo
  %set_permissions %{_prefix}/bin/vmoduser
  %set_permissions %{_prefix}/bin/vmoveuser
  %set_permissions %{_prefix}/bin/vrenamedomain
  %set_permissions %{_prefix}/bin/vrenameuser
  %set_permissions %{_prefix}/bin/vsetuserquota
  %set_permissions %{libexecdir}/sq_vacation
%else
  %run_permissions
%endif
%endif

# IndiMail Daemons
#indisrvr
%{_prefix}/sbin/svctool --indisrvr=4000 --servicedir=%{servicedir} \
  --localip=0 --maxdaemons=40 --maxperip=25 --avguserquota=2097152 \
  --certfile=%{sysconfdir}/certs/servercert.pem --ssl \
  --hardquota=52428800 --base_path=%{mbase}

#inlookup
%{_prefix}/sbin/svctool --inlookup=infifo --servicedir=%{servicedir} --cntrldir=control \
  --threads=5 --activeDays=60 --query-cache --password-cache --use-btree

#poppass
%ifarch x86_64
%global poppass_mem   104857600
%else
%global poppass_mem   52428800
%endif
%{_prefix}/sbin/svctool --poppass=106 --localip=0 --maxdaemons=40 --maxperip=25 \
  --memory=%{poppass_mem} \
  --certfile=%{sysconfdir}/certs/servercert.pem --ssl \
  --setpassword=%{_prefix}/sbin/vsetpass --servicedir=%{servicedir}

echo "Creating default indimail tcp access control files"
# rebuild cdb for poppass
for j in `/bin/ls %{sysconfdir}/tcp/tcp*.poppass 2>/dev/null`
do
  t1=`date +'%s' -r $j`
  if [ -f $j.cdb ] ; then
    t2=`date +'%s' -r $j.cdb`
  else
    t2=0
  fi
  if [ $t1 -gt $t2 ] ; then
    echo "Creating CDB $j.cdb"
    %{_prefix}/bin/tcprules $j.cdb $j.tmp < $j && /bin/chmod 664 $j.cdb \
      && %{__chown} indimail:indimail $j.cdb
  fi
done
#update VIRTUAL_PKG_LIB for smtp service
indlib=`ls -d %{_libdir}/libindimail.so.*.*.* 2>/dev/null`
for port in 25 465 587
do
  if [ -n "$indlib" -a -f "$indlib" ] ; then
    echo $indlib > %{servicedir}/qmail-smtpd.$port/variables/VIRTUAL_PKG_LIB
  fi
done
if [ -n "$indlib" -a -f "$indlib" ] ; then
  echo $indlib > %{servicedir}/qmail-send.25/variables/VIRTUAL_PKG_LIB
fi

# turn off automatic refresh for services during first time installation
svc_list=""
for i in mrtg mysql.3306 indisrvr.4000 inlookup.infifo \
qmail-poppass.106 qmail-logfifo
do
  svc_list="$svc_list %{servicedir}/$i"
  # save variables
  %{_prefix}/sbin/svctool --servicedir=%{servicedir} --service-name=$i \
    --export-variables=%{servicedir}/$i/variables/.variables  --force
done
if [ $noproxy -eq 0 ] ; then
for i in proxy-imapd.4143 proxy-imapd-ssl.9143 \
  proxy-pop3d.4110 proxy-pop3d-ssl.9110
do
  svc_list="$svc_list %{servicedir}/$i"
  %{_prefix}/sbin/svctool --servicedir=%{servicedir} --service-name=$i \
    --export-variables=%{servicedir}/$i/variables/.variables  --force
done
fi

%{_prefix}/sbin/svctool --servicedir=%{servicedir} --norefreshsvc="0 $svc_list"

# selinux
%{_prefix}/sbin/svctool --servicedir=%{servicedir} --config=iselinux

if [ -f %{sysconfdir}/cronlist.i -a -d %{_sysconfdir}/cron.d ] ; then
  echo "adding cron entries"
  %{__cp} %{sysconfdir}/cronlist.i %{_sysconfdir}/cron.d
fi

if [ -f %{libexecdir}/iupgrade.sh ] ; then
  echo "Running Custom Installation Script for post install"
  /bin/sh %{libexecdir}/iupgrade.sh post install %{version} $*
fi
) >> /var/log/indimail-setup.log 2>&1

if [ -f %{_sysconfdir}/init/svscan.conf -o -f %{_sysconfdir}/event.d/svscan ] ; then
  echo "1. Execute /sbin/initctl emit qmailstart to start services"
  count=1
elif [ -f %{_sysconfdir}/systemd/system/multi-user.target.wants/svscan.service ] ; then
  echo "1. Execute /bin/systemctl start svscan to start services"
  count=1
else
  echo "1. Execute %{_prefix}/sbin/initsvc -on"
  echo "2. Execute /sbin/init q to start services"
  count=2
fi

count=`expr $count + 1`
echo "$count. Change your default domain in %{sysconfdir}/control/defaultdomain"
count=`expr $count + 1`
echo "$count. You can optionally run the following command to verify installation"
echo "   sudo rpm -V indimail"

if [ ! -f %{sysconfdir}/certs/servercert.pem ] ; then
count=`expr $count + 1`
echo "$count. You need to create CERTS for STARTTLS."
echo "   Run the following command to create Certificate for TLS/SSL"
echo "   %{_prefix}/sbin/svctool --config=cert --postmaster=postmaster@$default_domain --common_name=$default_domain"
fi

echo
echo "Check /var/log/indimail-setup.log for the detailed installation log!!!"

### SCRIPTLET ###############################################################################
%preun
argv1=$1
ID=$(id -u)
if [ $ID -ne 0 ] ; then
  echo "You are not root" 1>&2
  exit 1
fi

(
if [ -z "$argv1" ] ; then
  argv1=0
fi
# we are doing upgrade
if [ $argv1 -eq 1 ] ; then
  (
  if [ -f %{libexecdir}/iupgrade.sh ] ; then
    echo "Running Custom Un-Installation Script for preun upgrade"
    /bin/sh %{libexecdir}/iupgrade.sh preun upgrade %{version} "$argv1"
  fi
  ) >> /var/log/indimail-setup.log 2>&1
  exit 0
fi
if [ -f %{_prefix}/bin/svok ] ; then
  %{_prefix}/bin/svok %{servicedir}/.svscan/log 2>/dev/null
  if [ $? -eq 0 ] ; then
    if test -f %{_sysconfdir}/init/svscan.conf
    then
      echo "Giving IndiMail exactly 5 seconds to exit nicely"
      /sbin/initctl emit qmailstop > /dev/null 2>&1
    elif test -f %{_sysconfdir}/event.d/svscan
    then
      echo "Giving IndiMail exactly 5 seconds to exit nicely"
      /sbin/initctl emit qmailstop > /dev/null 2>&1
    elif test -f %{_sysconfdir}/systemd/system/multi-user.target.wants/svscan.service
    then
      echo "Giving IndiMail exactly 5 seconds to exit nicely"
      /bin/systemctl stop svscan > /dev/null 2>&1
    elif test -x %{_prefix}/sbin/initsvc
    then
      echo "Giving IndiMail exactly 5 seconds to exit nicely"
      %{_prefix}/sbin/initsvc -off
    fi
    sleep 5
  fi
fi

if [ -f %{libexecdir}/iupgrade.sh ] ; then
  echo "Running Custom Un-Installation Script for preun pre-uninstall"
  /bin/sh %{libexecdir}/iupgrade.sh preun uninstall %{version} "$argv1"
fi
) >> /var/log/indimail-setup.log 2>&1

### SCRIPTLET ###############################################################################
%postun
argv1=$1
ID=$(id -u)
if [ $ID -ne 0 ] ; then
  echo "You are not root" 1>&2
  exit 1
fi
if [ -x /usr/bin/uname -o -x /bin/uname ] ; then
  default_domain=$([ -n "$HOSTNAME" ] && echo "$HOSTNAME" || `uname -n`)
else
  default_domain=$([ -n "$HOSTNAME" ] && echo "$HOSTNAME" || echo %{defaultDomain})
fi
if [ -z "$argv1" ] ; then
  argv1=0
fi
# we are doing upgrade
if [ $argv1 -eq 1 ] ; then
  (
  if [ "%{_libdir}" != "/usr/lib64" -a "%{_libdir}" != "/usr/lib" ] ; then
    echo "recreating ld.so cache"
    /sbin/ldconfig
  fi
  if [ -f %{libexecdir}/iupgrade.sh ] ; then
    echo "Running Custom Un-Installation Script for postun upgrade"
    /bin/sh %{libexecdir}/iupgrade.sh postun upgrade %{version} $*
  fi
  ) >> /var/log/indimail-setup.log 2>&1
  exit 0
fi

(
# remove all virtual domains
for i in `ls %{indimaildir}/domains`
do
  grep -wv "^+$i-" %{sysconfdir}/users/assign > %{sysconfdir}/users/assign.tmp
  %{__mv} %{sysconfdir}/users/assign.tmp %{sysconfdir}/users/assign
done
if [ -x %{_prefix}/sbin/qmail-newu ] ; then
  %{_prefix}/sbin/qmail-newu
fi
%{__rm} -rf %{indimaildir}/domains/$default_domain
for port in 465 25 587
do
  > %{servicedir}/qmail-smtpd.$port/variables/VIRTUAL_PKG_LIB
done

%{__rm} -f %{sysconfdir}/indimail.mrtg.ok %{sysconfdir}/system.mrtg.ok
echo "removing startup services"
for i in indisrvr.4000 inlookup.infifo mysql.3306 \
qmail-logfifo qmail-poppass.106 mrtg
do
  if [ -d %{servicedir}/$i -o -L %{servicedir}/$i ] ; then
    touch %{servicedir}/$i/down
    svc -dx %{servicedir}/$i
  fi
  if [ -d %{servicedir}/log/$i -o -L %{servicedir}/log/$i ] ; then
    touch %{servicedir}/$i/log/down
    svc -dx %{servicedir}/$i/log
  fi
  if [ -d %{servicedir}/$i -o -L %{servicedir}/$i ] ; then
    %{__rm} -rf %{servicedir}/$i
  fi
done

if [ %noproxy -eq 0 ] ; then
  for i in proxy-imapd.4143 proxy-imapd-ssl.9143 \
    proxy-pop3d.4110 proxy-pop3d-ssl.9110
  do
    if [ -d %{servicedir}/$i -o -L %{servicedir}/$i ] ; then
      touch %{servicedir}/$i/down
      svc -dx %{servicedir}/$i
    fi
    if [ -d %{servicedir}/log/$i -o -L %{servicedir}/log/$i ] ; then
      touch %{servicedir}/$i/log/down
      svc -dx %{servicedir}/$i/log
    fi
    if [ -d %{servicedir}/$i -o -L %{servicedir}/$i ] ; then
      %{__rm} -rf %{servicedir}/$i
    fi
  done
fi

count=`/bin/ls %{servicedir} 2>/dev/null| /usr/bin/wc -l`
if [ $count -eq 0 ] ; then # ignore disabled services
  %{__rm} -rf %{servicedir}
fi

if [ -d %{_sysconfdir}/cron.d ] ; then
  echo "removing cron entries"
  %{__rm} -f %{_sysconfdir}/cron.d/cronlist.i
fi

echo "removing logs"
%{__rm} -f %{indimaildir}/mysqldb/logs/logisam.log
%{__rm} -f %{indimaildir}/mysqldb/logs/logquery
%{__rm} -f %{indimaildir}/mysqldb/logs/logslow
if [ -h %{logdir} ] ; then
  log_dir=`/bin/ls -ld %{logdir} | /usr/bin/awk '{print $10}'`
else
  log_dir=%{logdir}
fi

for i in indisrvr.4000 inlookup.infifo \
mrtg mysql.3306 poppass.106
do
  %{__rm} -rf $log_dir/$i
done

if [ %noproxy -eq 0 ] ; then
  for i in proxyIMAP.4143 proxyIMAP.9143 \
    proxyPOP3.4110 proxyPOP3.9110
  do
    %{__rm} -rf $log_dir/$i
  done
fi

if [ "%{_libdir}" != "/usr/lib64" -a "%{_libdir}" != "/usr/lib" ] ; then
  echo "recreating ld.so cache"
  /sbin/ldconfig
fi

if [ -x /usr/sbin/selinuxenabled ] ; then
  /usr/sbin/selinuxenabled
  if [ $? -eq 0 -a -x /usr/sbin/semodule ] ; then
    echo "disabling selinux module"
    /usr/sbin/semodule -r indimail
  fi
fi

if [ -f %{libexecdir}/iupgrade.sh ] ; then
  echo "Running Custom Un-Installation Script for postun uninstall"
  /bin/sh %{libexecdir}/iupgrade.sh postun uninstall %{version} $*
fi
) >> /var/log/indimail-setup.log 2>&1

### SCRIPTLET ###############################################################################
%posttrans
argv1=$1
ID=$(id -u)
if [ $ID -ne 0 ] ; then
  echo "You are not root" 1>&2
  exit 1
fi
if [ -f %{libexecdir}/iupgrade.sh ] ; then
(
  echo "Running Custom Installation Script for posttrans"
  /bin/sh %{libexecdir}/iupgrade.sh posttrans noargs %{version} $*
) >> /var/log/indimail-setup.log 2>&1
fi
%{_prefix}/sbin/svctool --fixsharedlibs

%post -n libindimail
if [ "%{_libdir}" != "/usr/lib64" -a "%{_libdir}" != "/usr/lib" ] ; then
  /sbin/ldconfig
fi

%postun -n libindimail
if [ "%{_libdir}" != "/usr/lib64" -a "%{_libdir}" != "/usr/lib" ] ; then
  /sbin/ldconfig
fi

# fix changelog for openSUSE buildservice
%changelog
* Sun Mar 21 2021 04:44:28 +0530 indimail-virtualdomains@indimail.org 3.4-1.1%{?dist}
Release 3.4 Start 14/02/2021
01. sql_adddomain.c,, sql_setpw.c : replaced CREATE TABLE statements with
    create_table() function
02. post install: save variables
03. indisrvr.c, tls.c - renamed SSL_CIPHER to TLS_CIPHER_LIST
04. tls.c, tls.h, auth_admin.c - updated datatypes
05. tls.c, tls.h - added cafile argument to tls_init()
06. auth_admin.c - tls_init() changed for cafile argument
07. auth_admin.c, tls.c - added option to match host with common name
08. adminclient.c - added -m option to match host with common name
09. adminclient.c - added -C option to specify cafile
10. proxylogin.c - added option to specify CAFILE and match host with common
    name
11. tls.c, tls.h - refactored tls code
12. auth_admin.c, indisrvr.c: use functions from tls.c
13. tls.c: use set_essential_fd() to avoid deadlock
14. vpriv_insert.c: fixed SQL syntax error
15. Changes for making code github action, added workflow for CI
16. indimail.h - allow inclusion without having mysql installed