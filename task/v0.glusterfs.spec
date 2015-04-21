
%global _hardened_build 1

%global _for_fedora_koji_builds 1

# uncomment and add '%' to use the prereltag for pre-releases
# global prereltag alpha

# if you wish to compile an rpm without rdma support, compile like this...
# rpmbuild -ta @PACKAGE_NAME@-@PACKAGE_VERSION@.tar.gz --without rdma
#%{?_without_rdma:%global _without_rdma --disable-ibverbs}

# No RDMA Support on s390(x)
#%ifarch s390 s390x
#%global _without_rdma --disable-ibverbs
#%endif

# if you wish to compile an rpm without epoll...
# rpmbuild -ta @PACKAGE_NAME@-@PACKAGE_VERSION@.tar.gz --without epoll
#%{?_without_epoll:%global _without_epoll --disable-epoll}

# if you wish to compile an rpm with fusermount...
# rpmbuild -ta @PACKAGE_NAME@-@PACKAGE_VERSION@.tar.gz --with fusermount
# %{?_with_fusermount:%global _with_fusermount --enable-fusermount}

# if you wish to compile an rpm without geo-replication support, compile like this...
# rpmbuild -ta @PACKAGE_NAME@-@PACKAGE_VERSION@.tar.gz --without georeplication
#%{?_without_georeplication:%global _without_georeplication --disable-geo-replication}

%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} >= 6 )
%global           SWIFTVER 1.7.4
%if ( 0%{_for_fedora_koji_builds} )
%global           UFOVER 1.1
%else
%global           UFOVER @PACKAGE_VERSION@
%endif
%global           _with_ufo true
%endif

%if ( 0%{?fedora} && 0%{?fedora} > 16 ) || ( 0%{?rhel} && 0%{?rhel} > 6 )
%global           _with_systemd true
%endif

Summary:          Cluster File System
%if ( 0%{_for_fedora_koji_builds} )
Name:             glusterfs
Version:          3.3.1
Release:          15%{?prereltag:.%{prereltag}}%{?dist}
%else
Name:             @PACKAGE_NAME@
Version:          @PACKAGE_VERSION@
Release:          1%{?dist}
%endif
License:          GPLv3+ and (GPLv2 or LGPLv3+)
Group:            System Environment/Base
%if ( 0%{_for_fedora_koji_builds} )
Vendor:           Red Hat
%endif
URL:              http://www.gluster.org//docs/index.php/GlusterFS

%if ( 0%{_for_fedora_koji_builds} )
Source0:          http://download.gluster.org/pub/gluster/glusterfs/3.3/%{version}/glusterfs-%{version}%{?prereltag}.tar.gz
%else
Source0:          @PACKAGE_NAME@-@PACKAGE_VERSION@.tar.gz
%endif
#Source1:          glusterd.sysconfig
#Source2:          glusterfsd.sysconfig
#Source3:          umount.glusterfs
#Source4:          glusterfs-fuse.logrotate
#Source5:          glusterd.logrotate
#Source6:          glusterfsd.logrotate
#Patch0:           %{name}-3.2.5.configure.ac.patch
#Patch1:           %{name}-3.3.0.libglusterfs.Makefile.patch
#Patch2:           %{name}-3.3.1.rpc.rpcxprt.rdma.name.c.patch

BuildRoot:        %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

#Source10:         glusterd.service
#Source11:         glusterfsd.service
#Source12:         glusterd.init
#Source13:         glusterfsd.init

#%if ( 0%{?_with_systemd:1} )
#%global glusterd_service %{S:%{SOURCE10}}
#%global glusterfsd_service %{S:%{SOURCE11}}
#BuildRequires:    systemd-units
#Requires(post):   systemd-units
#Requires(preun):  systemd-units
#Requires(postun): systemd-units
#%define _init_enable()  /bin/systemctl enable %1.service ;
#%define _init_disable() /bin/systemctl disable %1.service ;
#%define _init_restart() /bin/systemctl try-restart %1.service ;
#%define _init_stop()    /bin/systemctl stop %1.service ;
#%define _init_install() %{__install} -D -p -m 0644 %1 %{buildroot}%{_unitdir}/%2.service ;
# can't seem to make a generic macro that works
#%define _init_glusterd   %{_unitdir}/glusterd.service
#%define _init_glusterfsd %{_unitdir}/glusterfsd.service
#%define _init_gluster_swift_account    %{_unitdir}/gluster-swift-account.service
#%define _init_gluster_swift_object    %{_unitdir}/gluster-swift-object.service
#%define _init_gluster_swift_container    %{_unitdir}/gluster-swift-container.service
#%define _init_gluster_swift_proxy %{_unitdir}/gluster-swift-proxy.service
#%else
#%if ( 0%{_for_fedora_koji_builds} )
#%global glusterd_service %{S:%{SOURCE12}}
#%global glusterfsd_service %{S:%{SOURCE13}}
#%endif

Requires(post):   /sbin/chkconfig
Requires(preun):  /sbin/service
Requires(preun):  /sbin/chkconfig
Requires(postun): /sbin/service
%define _init_enable()  /sbin/chkconfig --add %1 ;
%define _init_disable() /sbin/chkconfig --del %1 ;
%define _init_restart() /sbin/service %1 condrestart &>/dev/null ;
%define _init_stop()    /sbin/service %1 stop &>/dev/null ;
%define _init_install() %{__install} -D -p -m 0755 %1 %{buildroot}%{_sysconfdir}/init.d/%2 ;
# can't seem to make a generic macro that works
#%define _init_glusterd   %{_sysconfdir}/init.d/glusterd
#%define _init_glusterfsd %{_sysconfdir}/init.d/glusterfsd


%define _init_gluster_swift_account %{_sysconfdir}/init.d/gluster-swift-account
%define _init_gluster_swift_object  %{_sysconfdir}/init.d/gluster-swift-object
%define _init_gluster_swift_container  %{_sysconfdir}/init.d/gluster-swift-container
%define _init_gluster_swift_proxy  %{_sysconfdir}/init.d/gluster-swift-proxy
#%endif

BuildRequires:    bison flex
BuildRequires:    gcc make automake libtool
BuildRequires:    ncurses-devel readline-devel
BuildRequires:    libxml2-devel openssl-devel
BuildRequires:    libaio-devel
#BuildRequires:    systemtap-sdt-devel lvm2-devel # glusterfs-3.4.x
%if ( 0%{?suse_version} )
BuildRequires:    python-devel
%else
BuildRequires:    python-ctypes
%endif


%description
GlusterFS is a clustered file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package includes the glusterfs binary, the glusterfsd daemon and the
gluster command line, libglusterfs and glusterfs translator modules common to
both GlusterFS server and client framework.


%if ( 0%{?_with_ufo:1} )
%package swift

Summary:          GlusterFS OpenStack Object Storage
Group:            Applications/System
License:          ASL 2.0
BuildArch:        noarch

%if ( 0%{_for_fedora_koji_builds} )
Source20:         http://launchpad.net/swift/folsom/%{SWIFTVER}/+download/swift-%{SWIFTVER}.tar.gz
%else
Source20:         swift-%{SWIFTVER}.tar.gz
%endif

Source30:         gluster-swift-account.service
Source31:         gluster-swift-container.service
Source32:         gluster-swift-object.service
Source33:         gluster-swift-proxy.service
Source34:         gluster-swift-account@.service
Source35:         gluster-swift-container@.service
Source36:         gluster-swift-object@.service
Source37:         gluster-swift.tmpfs
Source40:         gluster-swift-account.init
Source41:         gluster-swift-container.init
Source42:         gluster-swift-object.init
Source43:         gluster-swift-proxy.init
Source44:         gluster-swift-functions
# these first appeared in openstack-swift-1.7.4-2.fc19
Source50:         gluster-swift-account-replicator.service
Source51:         gluster-swift-account-replicator@.service
Source52:         gluster-swift-account-auditor.service
Source53:         gluster-swift-account-auditor@.service
Source54:         gluster-swift-account-reaper.service
Source55:         gluster-swift-account-reaper@.service
Source56:         gluster-swift-container-replicator.service
Source57:         gluster-swift-container-replicator@.service
Source58:         gluster-swift-container-auditor.service
Source59:         gluster-swift-container-auditor@.service
Source60:         gluster-swift-container-updater.service
Source61:         gluster-swift-container-updater@.service
Source62:         gluster-swift-object-replicator.service
Source63:         gluster-swift-object-replicator@.service
Source64:         gluster-swift-object-auditor.service
Source65:         gluster-swift-object-auditor@.service
Source66:         gluster-swift-object-updater.service
Source67:         gluster-swift-object-updater@.service
Source68:         gluster-swift-object-expirer.service
Source69:         gluster-swift-object-expirer@.service
# these first appeared in openstack-swift-1.7.4-1.fc18 and -1.7.4-2.el6
Source70:         account-server.conf
Source71:         container-server.conf
Source72:         object-server.conf
Source73:         proxy-server.conf
Source74:         swift.conf

#Patch20:          0001-Use-updated-parallel-install-versions-of-epel-packag.patch
#Patch21:          0002-Add-fixes-for-building-the-doc-package.patch
#Patch22:          glusterfs-3.3.1.swift.constraints.backport-1.7.4.patch
#Patch23:          glusterfs-3.4.0.swift.egginfo-grizzly.patch
#Patch24:          0002-Add-fixes-for-building-the-doc-package.patch.180
#BuildRoot:        %(mktemp -ud %{_tmppath}/swift-%{SWIFTVER}-%{release}-XXXXXX)

%if ( 0%{?_with_systemd:1} )
%global glusterswiftaccount_service %{S:%{SOURCE30}}
%global glusterswiftcontainer_service %{S:%{SOURCE31}}
%global glusterswiftobject_service %{S:%{SOURCE32}}
%global glusterswiftproxy_service %{S:%{SOURCE33}}
%else
%global glusterswiftaccount_service %{S:%{SOURCE40}}
%global glusterswiftcontainer_service %{S:%{SOURCE41}}
%global glusterswiftobject_service %{S:%{SOURCE42}}
%global glusterswiftproxy_service %{S:%{SOURCE43}}
%endif

BuildRequires:    dos2unix
BuildRequires:    python-devel
BuildRequires:    python-setuptools
BuildRequires:    python-netifaces
%if ( 0%{?rhel} && 0%{?rhel} < 7 )
BuildRequires:    python-webob1.0
BuildRequires:    python-paste-deploy1.5
Requires:         python-webob1.0
Requires:         python-paste-deploy1.5
%else
BuildRequires:    python-webob
BuildRequires:    python-paste-deploy
Requires:         python-webob
Requires:         python-paste-deploy
%endif
#Requires:         %{name} = %{version}-%{release}
Requires:         python-configobj
Requires:         python-eventlet >= 0.9.8
Requires:         python-greenlet >= 0.3.1
Requires:         python-simplejson
Requires:         pyxattr
Requires:         python-setuptools
Requires:         python-netifaces

Conflicts:        openstack-swift


%description swift

OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.
Objects are written to multiple hardware devices in the data center, with the
OpenStack software responsible for ensuring data replication and integrity
across the cluster. Storage clusters can scale horizontally by adding new nodes,
which are automatically configured. Should a node fail, OpenStack works to
replicate its content from other active nodes. Because OpenStack uses software
logic to ensure data replication and distribution across different devices,
inexpensive commodity hard drives and servers can be used in lieu of more
expensive equipment.


%package swift-account
Summary:          A swift account server
Group:            Applications/System
License:          ASL 2.0
BuildArch:        noarch
Requires:         %{name}-swift = %{version}-%{release}

%description swift-account
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name}-swift account server.


%package swift-container
Summary:          A swift container server
Group:            Applications/System
License:          ASL 2.0
BuildArch:        noarch
Requires:         %{name}-swift = %{version}-%{release}

%description swift-container
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name}-swift container server.

%package swift-object
Summary:          A swift object server
Group:            Applications/System
License:          ASL 2.0
BuildArch:        noarch
Requires:         %{name}-swift = %{version}-%{release}
Requires:         rsync >= 3.0

%description swift-object
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name}-swift object server.

%package swift-proxy
Summary:          A swift proxy server
Group:            Applications/System
License:          ASL 2.0
BuildArch:        noarch
Requires:         %{name}-swift = %{version}-%{release}

%description swift-proxy
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name}-swift proxy server.


%package swift-doc
Summary:          Documentation for %{name}
Group:            Documentation
BuildArch:        noarch
# Required for generating docs
BuildRequires:    python-eventlet
BuildRequires:    python-simplejson
%if ( 0%{?rhel} && 0%{?rhel} < 7 )
BuildRequires:    python-webob1.0
BuildRequires:    python-sphinx10
%else
BuildRequires:    python-webob
BuildRequires:    python-sphinx
%endif
BuildRequires:    pyxattr

%description swift-doc
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains documentation files for %{name}-swift.

%package ufo
Summary:          GlusterFS Unified File and Object Storage.
Group:            Applications/System
License:          ASL 2.0
BuildArch:        noarch
Requires:         %{name}-swift = %{version}-%{release}
Requires:         memcached
Requires:         openssl
Requires:         python
Obsoletes:        glusterfs-swift-plugin < 3.3.1-4
Obsoletes:        glusterfs-swift-ufo <= 3.3.1-4

%if ( 0%{_for_fedora_koji_builds} )
Source15:         http://download.gluster.org/pub/gluster/glusterfs/3.3/%{version}/UFO/gluster-swift-ufo-%{UFOVER}%{?prereltag}.tar.gz
%else
Source15:         gluster-swift-ufo-@PACKAGE_VERSION@.tar.gz
%endif
#Patch15:          %{name}-3.3.1.ufo.gluster.swift.common.DiskFile-1.7.4.patch
#Patch16:          %{name}-3.3.1.ufo.gluster.multi-volume.backport-1.1.patch

%description ufo
Gluster Unified File and Object Storage unifies NAS and object storage
technology. This provides a system for data storage that enables users to access
the same data as an object and as a file, simplifying management and controlling
storage costs.

%endif

%prep
%setup -q -n %{name}-%{version}%{?prereltag}
#%if ( 0%{_for_fedora_koji_builds} )
#%patch0 -p0
#%patch1 -p0
#%if ( "%{version}" == "3.3.1" )
#%patch2 -p1
#%endif
#%endif

%if ( 0%{?_with_ufo:1} )
# unpack swift-1.x.y
%setup -q -T -D -n %{name}-%{version}%{?prereltag} -a 20
# unpack gluster ufo
%setup -q -T -D -n %{name}-%{version}%{?prereltag} -a 15

cd swift-%{SWIFTVER}
# apply Fedora openstack-swift patches to Swift as appropriate
#%if ( 0%{?rhel} && 0%{?rhel} < 7 )
#%patch20 -p1
#%if "%{SWIFTVER}" == "1.7.4"
#%patch21 -p1
#%else
#%patch24 -p1
#%endif
#%endif
# apply our own patches to Swift, as appropriate
#%if "%{SWIFTVER}" == "1.7.4"
#%patch22 -p1
#%else
#%patch23 -p1
#%endif
# apply our fix for UFO 1.1 (tarball snapshot circa 7 Dec, 2012)
%if ( 0%{_for_fedora_koji_builds} )
%if ( "%{UFOVER}" == "1.1" )
cd ../
pwd
#%patch15
#%patch16 -p1
%endif
%endif
%endif

%build

# Remove rpath
#sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
#sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

#%{__make} %{?_smp_mflags}

%if ( 0%{?_with_ufo:1} )
cd swift-%{SWIFTVER}
%{__python} setup.py build
%{__mkdir_p} doc/build
%if ( 0%{?fedora} )
%{__python} setup.py build_sphinx
%endif
cd ..
cd ufo
%{__python} setup.py build
cd ..
%endif

%install
%{__rm} -rf %{buildroot}
#%{__make} install DESTDIR=%{buildroot}



%if ( 0%{?_with_ufo:1} )
cd swift-%{SWIFTVER}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
# common swift .service or .init files
%_init_install %{glusterswiftaccount_service} gluster-swift-account
%_init_install %{glusterswiftcontainer_service} gluster-swift-container
%_init_install %{glusterswiftobject_service} gluster-swift-object
%_init_install %{glusterswiftproxy_service} gluster-swift-proxy
%if ( 0%{?_with_systemd:1} )
# extra systemd .service files
%_init_install %{SOURCE34} gluster-swift-account@
%_init_install %{SOURCE35} gluster-swift-container@
%_init_install %{SOURCE36} gluster-swift-object@
%if ( 0%{?fedora} && 0%{?fedora} > 18 )
# more extra systemd .service files in f19
%_init_install %{SOURCE50} gluster-swift-account-replicator
%_init_install %{SOURCE51} gluster-swift-account-replicator@
%_init_install %{SOURCE52} gluster-swift-account-auditor
%_init_install %{SOURCE53} gluster-swift-account-auditor@
%_init_install %{SOURCE54} gluster-swift-account-reaper
%_init_install %{SOURCE55} gluster-swift-account-reaper@
%_init_install %{SOURCE56} gluster-swift-container-replicator
%_init_install %{SOURCE57} gluster-swift-container-replicator@
%_init_install %{SOURCE58} gluster-swift-container-auditor
%_init_install %{SOURCE59} gluster-swift-container-auditor@
%_init_install %{SOURCE60} gluster-swift-container-updater
%_init_install %{SOURCE61} gluster-swift-container-updater@
%_init_install %{SOURCE62} gluster-swift-object-replicator
%_init_install %{SOURCE63} gluster-swift-object-replicator@
%_init_install %{SOURCE64} gluster-swift-object-auditor
%_init_install %{SOURCE65} gluster-swift-object-auditor@
%_init_install %{SOURCE66} gluster-swift-object-updater
%_init_install %{SOURCE67} gluster-swift-object-updater@
%_init_install %{SOURCE68} gluster-swift-object-expirer
%_init_install %{SOURCE69} gluster-swift-object-expirer@
%endif
%else
# Init helper functions
%{__install} -p -D -m 644 %{SOURCE44} %{buildroot}%{_datarootdir}/gluster-swift/functions
# Init scripts
%_init_install %{glusterswiftaccount_service} gluster-swift-account
%_init_install %{glusterswiftcontainer_service} gluster-swift-container
%_init_install %{glusterswiftobject_service} gluster-swift-object
%_init_install %{glusterswiftproxy_service} gluster-swift-proxy
%endif
# Misc other
%{__install} -d -m 755 %{buildroot}%{_sysconfdir}/swift
%{__install} -d -m 755 %{buildroot}%{_sysconfdir}/swift/account-server
%{__install} -d -m 755 %{buildroot}%{_sysconfdir}/swift/container-server
%{__install} -d -m 755 %{buildroot}%{_sysconfdir}/swift/object-server
%{__install} -d -m 755 %{buildroot}%{_sysconfdir}/swift/proxy-server
# Config files
#%if ( 0%{?fedora} && 0%{?fedora} > 17 )
# these first appeared in openstack-swift-1.7.4-1.fc18
#install -p -D -m 660 %{SOURCE70} %{buildroot}%{_sysconfdir}/swift/account-server.conf
#install -p -D -m 660 %{SOURCE71} %{buildroot}%{_sysconfdir}/swift/container-server.conf
#install -p -D -m 660 %{SOURCE72} %{buildroot}%{_sysconfdir}/swift/object-server.conf
#install -p -D -m 660 %{SOURCE73} %{buildroot}%{_sysconfdir}/swift/proxy-server.conf
#install -p -D -m 660 %{SOURCE74} %{buildroot}%{_sysconfdir}/swift/swift.conf
#%endif
# Install pid directory
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/run/swift
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/run/swift/account-server
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/run/swift/container-server
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/run/swift/object-server
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/run/swift/proxy-server
%if ( 0%{?_with_systemd:1} )
# Swift run directories
%{__mkdir_p} %{buildroot}%{_sysconfdir}/tmpfiles.d
install -p -m 0644 %{SOURCE37} %{buildroot}%{_sysconfdir}/tmpfiles.d/gluster-swift.conf
%endif
# man pages
install -d -m 755 %{buildroot}%{_mandir}/man5
for m in doc/manpages/*.5; do
  install -p -m 0644 $m %{buildroot}%{_mandir}/man5
done
install -d -m 755 %{buildroot}%{_mandir}/man1
for m in doc/manpages/*.1; do
  install -p -m 0644 $m %{buildroot}%{_mandir}/man1
done
cd ..
cd ufo
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
cd ..
%{__mkdir_p} %{buildroot}%{_sysconfdir}/swift
cp -r ufo/etc/* %{buildroot}%{_sysconfdir}/swift/
%{__mkdir_p} %{buildroot}%{_bindir}
cp ufo/bin/gluster-swift-gen-builders %{buildroot}%{_bindir}/
%endif
# Remove tests
%{__rm} -rf %{buildroot}/%{python_sitelib}/test
%clean
%{__rm} -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig


%if ( 0%{?_with_ufo:1} )
%files swift
%defattr(-,root,root,-)
%doc swift-%{SWIFTVER}/AUTHORS
%doc swift-%{SWIFTVER}/LICENSE
%doc swift-%{SWIFTVER}/README
%doc swift-%{SWIFTVER}/etc/dispersion.conf-sample
%doc swift-%{SWIFTVER}/etc/drive-audit.conf-sample
%doc swift-%{SWIFTVER}/etc/object-expirer.conf-sample
%doc swift-%{SWIFTVER}/etc/swift.conf-sample
%{_mandir}/man5/dispersion.conf.5*
%{_mandir}/man1/swift-dispersion-populate.1*
%{_mandir}/man1/swift-dispersion-report.1*
%{_mandir}/man1/swift.1*
%{_mandir}/man1/swift-get-nodes.1*
%{_mandir}/man1/swift-init.1*
%{_mandir}/man1/swift-orphans.1*
%{_mandir}/man1/swift-recon.1*
%{_mandir}/man1/swift-ring-builder.1*
%if ( 0%{?_with_systemd:1} )
%config(noreplace) %{_sysconfdir}/tmpfiles.d/gluster-swift.conf
%else
%dir %{_datarootdir}/gluster-swift/functions
%endif
%dir %{_sysconfdir}/swift
#%if ( 0%{?fedora} && 0%{?fedora} > 17 )
#%config(noreplace) %attr(660, root, swift) %{_sysconfdir}/swift/swift.conf
#%endif
%dir %attr(0755, swift, swift) %{_localstatedir}/run/swift
%dir %{python_sitelib}/swift
%{_bindir}/swift-account-audit
%{_bindir}/swift-bench
%{_bindir}/swift-drive-audit
%{_bindir}/swift-get-nodes
%{_bindir}/swift-init
%{_bindir}/swift-ring-builder
%{_bindir}/swift-dispersion-populate
%{_bindir}/swift-dispersion-report
%{_bindir}/swift-recon*
%{_bindir}/swift-object-expirer
%{_bindir}/swift-oldies
%{_bindir}/swift-orphans
%{_bindir}/swift-form-signature
%{_bindir}/swift-temp-url
%{python_sitelib}/swift/*.py*
%{python_sitelib}/swift/common
%{python_sitelib}/swift-%{SWIFTVER}-*.egg-info

%files swift-account
%defattr(-,root,root,-)
%doc swift-%{SWIFTVER}/etc/account-server.conf-sample
%{_mandir}/man5/account-server.conf.5*
%{_mandir}/man1/swift-account-auditor.1*
%{_mandir}/man1/swift-account-reaper.1*
%{_mandir}/man1/swift-account-replicator.1*
%{_mandir}/man1/swift-account-server.1*
%_init_gluster_swift_account
%if ( 0%{?_with_systemd:1} )
%{_unitdir}/gluster-swift-account*.service
%endif
%dir %attr(0755, swift, swift) %{_localstatedir}/run/swift/account-server
%dir %{_sysconfdir}/swift/account-server
%{_bindir}/swift-account-auditor
%{_bindir}/swift-account-reaper
%{_bindir}/swift-account-replicator
%{_bindir}/swift-account-server
%{python_sitelib}/swift/account

%files swift-container
%defattr(-,root,root,-)
%doc swift-%{SWIFTVER}/etc/container-server.conf-sample
%{_mandir}/man5/container-server.conf.5*
%{_mandir}/man1/swift-container-auditor.1*
%{_mandir}/man1/swift-container-replicator.1*
%{_mandir}/man1/swift-container-server.1*
%{_mandir}/man1/swift-container-sync.1*
%{_mandir}/man1/swift-container-updater.1*
%_init_gluster_swift_container
%if ( 0%{?_with_systemd:1} )
%{_unitdir}/gluster-swift-container*.service
%endif
%dir %attr(0755, swift, swift) %{_localstatedir}/run/swift/container-server
%dir %{_sysconfdir}/swift/container-server
%{_bindir}/swift-container-auditor
%{_bindir}/swift-container-server
%{_bindir}/swift-container-replicator
%{_bindir}/swift-container-updater
%{_bindir}/swift-container-sync
%{python_sitelib}/swift/container

%files swift-object
%defattr(-,root,root,-)
%doc swift-%{SWIFTVER}/etc/object-server.conf-sample
%doc swift-%{SWIFTVER}/etc/rsyncd.conf-sample
%{_mandir}/man5/object-server.conf.5*
%{_mandir}/man5/object-expirer.conf.5*
%{_mandir}/man1/swift-object-auditor.1*
%{_mandir}/man1/swift-object-expirer.1*
%{_mandir}/man1/swift-object-info.1*
%{_mandir}/man1/swift-object-replicator.1*
%{_mandir}/man1/swift-object-server.1*
%{_mandir}/man1/swift-object-updater.1*
%_init_gluster_swift_object
%if ( 0%{?_with_systemd:1} )
%{_unitdir}/gluster-swift-object*.service
%endif
%dir %attr(0755, swift, swift) %{_localstatedir}/run/swift/object-server
%dir %{_sysconfdir}/swift/object-server
%{_bindir}/swift-object-auditor
%{_bindir}/swift-object-info
%{_bindir}/swift-object-replicator
%{_bindir}/swift-object-server
%{_bindir}/swift-object-updater
%{python_sitelib}/swift/obj

%files swift-proxy
%defattr(-,root,root,-)
%doc swift-%{SWIFTVER}/etc/proxy-server.conf-sample
%{_mandir}/man5/proxy-server.conf.5*
%{_mandir}/man1/swift-proxy-server.1*
%_init_gluster_swift_proxy
%dir %attr(0755, swift, swift) %{_localstatedir}/run/swift/proxy-server
%dir %{_sysconfdir}/swift/proxy-server
%{_bindir}/swift-proxy-server
%{python_sitelib}/swift/proxy

%files swift-doc
%defattr(-,root,root,-)
%doc swift-%{SWIFTVER}/LICENSE

%files ufo
%defattr(-,root,root,-)
%{python_sitelib}/gluster
%{python_sitelib}/gluster_swift_ufo-*-*.egg-info
%{_bindir}/gluster-swift-gen-builders
%{_sysconfdir}/swift/*-gluster
%{_sysconfdir}/swift/*/1.conf-gluster
%endif



%if ( 0%{?_with_ufo:1} )
%pre swift
getent group swift >/dev/null || groupadd -r swift -g 160
getent passwd swift >/dev/null || \
useradd -r -g swift -u 160 -d %{_sharedstatedir}/swift -s /sbin/nologin \
-c "OpenStack Swift Daemons" swift
exit 0

%pre swift-account

if [ -f /etc/swift/account-server/1.conf ]; then
    echo "warning: /etc/swift/account-server/1.conf saved as /etc/swift/account-server/1.conf.rpmsave"
    cp /etc/swift/account-server/1.conf /etc/swift/account-server/1.conf.rpmsave
fi


%post swift-account
%_init_enable gluster-swift-account


%preun swift-account
if [ $1 = 0 ] ; then
    %_init_stop gluster-swift-account
    %_init_disable gluster-swift-account
fi


%postun swift-account
if [ "$1" -ge "1" ] ; then
    %_init_restart gluster-swift-account
fi


%pre swift-container

if [ -f /etc/swift/container-server/1.conf ]; then
    echo "warning: /etc/swift/container-server/1.conf saved as /etc/swift/container-server/1.conf.rpmsave"
    cp /etc/swift/container-server/1.conf /etc/swift/container-server/1.conf.rpmsave
fi


%post swift-container
%_init_enable gluster-swift-container


%preun swift-container
if [ $1 = 0 ] ; then
    %_init_stop gluster-swift-container
    %_init_disable gluster-swift-container
fi


%postun swift-container
if [ "$1" -ge "1" ] ; then
    %_init_restart gluster-swift-container
fi


%pre swift-object

if [ -f /etc/swift/object-server/1.conf ]; then
    echo "warning: /etc/swift/object-server/1.conf saved as /etc/swift/object-server/1.conf.rpmsave"
    cp /etc/swift/object-server/1.conf /etc/swift/object-server/1.conf.rpmsave
fi


%post swift-object
%_init_enable gluster-swift-object


%preun swift-object
if [ $1 = 0 ] ; then
    %_init_stop gluster-swift-object
    %_init_disable gluster-swift-object
fi


%postun swift-object
if [ "$1" -ge "1" ] ; then
    %_init_restart gluster-swift-object
fi


%pre swift-proxy

if [ -f /etc/swift/proxy-server.conf ]; then
    echo "warning: /etc/swift/proxy-server.conf saved as /etc/swift/proxy-server.conf.rpmsave"
    cp /etc/swift/proxy-server.conf /etc/swift/proxy-server.conf.rpmsave
fi


%post swift-proxy
%_init_enable gluster-swift-proxy


%preun swift-proxy
if [ $1 = 0 ] ; then
    %_init_stop gluster-swift-proxy
    %_init_disable gluster-swift-proxy
fi


%postun swift-proxy
if [ "$1" -ge "1" ] ; then
    %_init_restart gluster-swift-proxy
fi
%endif


%changelog
* Mon May 13 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.1-15
- hardened build, i.e. PIE. RHBZ 955283

