
%define gc_version 7.1

Name:           libatomic_ops
Version:        1.2
Release:        8.gc.1%{?dist}
Summary:        Atomic memory update operations

Group:          Development/Libraries
License:        GPLv2+ and MIT
URL:            http://www.hpl.hp.com/research/linux/atomic_ops/
%if 0%{?gc_version:1}
Source0:        http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/gc-%{gc_version}.tar.gz
%else
Source0:       http://www.hpl.hp.com/research/linux/atomic_ops/download/%{name}-%{version}.tar.gz
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1: libatomic_ops-1.2-ppclwzfix.patch
Patch2: libatomic_ops-1.2-s390-include.patch

# No debug information gets generated from a static lib, so
# debuginfo will be empty.
%define debug_package %{nil}

%description
Provides implementations for atomic memory update operations on a
number of architectures. This allows direct use of these in reasonably
portable code. Unlike earlier similar packages, this one explicitly
considers memory barrier semantics, and allows the construction of code
that involves minimum overhead across a variety of architectures.


%package devel
Summary:   Atomic memory update operations
Group:     Development/Libraries
Provides:  %{name}-static = %{version}-%{release}
%description devel
Provides implementations for atomic memory update operations on a
number of architectures. This allows direct use of these in reasonably
portable code. Unlike earlier similar packages, this one explicitly
considers memory barrier semantics, and allows the construction of code
that involves minimum overhead across a variety of architectures.


%prep
%setup -q -n gc-%{gc_version}/libatomic_ops-%{version}
%if ! 0%{?gc_version:1}
# already fixed in gc version
%patch1 -p1
%endif
%patch2 -p1


%build
%configure

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# omit dup'd docs
rm -rf $RPM_BUILD_ROOT%{_datadir}/libatomic_ops/{COPYING,*.txt}


%clean
rm -rf $RPM_BUILD_ROOT


%files devel
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%doc doc/*.txt
%{_includedir}/atomic_ops.h
%{_includedir}/atomic_ops_malloc.h
%{_includedir}/atomic_ops_stack.h
%{_includedir}/atomic_ops/
%{_libdir}/libatomic_ops.a
%{_libdir}/libatomic_ops_gpl.a


%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.2-8.gc.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.2-8.gc
- use gc tarball, tag gc release

* Thu Jul 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.2-7
- devel: Provides: %%name-static ...
- consolidate %%doc's
- %%files: track libs

* Wed May 20 2009 Dan Horak <dan[t]danny.cz> - 1.2-6
- added fix for s390

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 22 2008 Jon Stanley <jonstanley@gmail.com> - 1.2-4
- Fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2-3
- Autorebuild for GCC 4.3

* Tue May 29 2007 Pierre Ossman <drzeus@drzeus.cx> 1.2-2
- Added fix for PPC AO_load_acquire.

* Fri Nov 10 2006 Pierre Ossman <drzeus@drzeus.cx> 1.2-1
- Update to 1.2.

* Sat Sep  9 2006 Pierre Ossman <drzeus@drzeus.cx> 1.1-2
- Fix naming of package.
- General cleanup of spec file.

* Wed Aug 30 2006 Pierre Ossman <drzeus@drzeus.cx> 1.1-1
- Initial package for Fedora Extras.
