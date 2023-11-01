# % global setools_pre_ver rc
# % global gitver f1e5b20

%global sepol_ver 2.9-1
%global selinux_ver 2.9-1

%bcond_without     networkx

Name:           setools
Version:        4.3.0
Release:        3%{?setools_pre_ver:.%{setools_pre_ver}}%{?dist}
Summary:        Policy analysis tools for SELinux

License:        GPLv2
URL:            https://github.com/SELinuxProject/setools/wiki
Source0:        https://github.com/SELinuxProject/setools/archive/%{version}%{?setools_pre_ver:-%{setools_pre_ver}}.tar.gz
Source1:        setools.pam
Source2:        apol.desktop
Patch0001:      0001-Support-old-boolean-names-in-policy-queries.patch
Patch0002:      0002-Make-seinfo-output-predictable.patch
Patch1001:      1001-Do-not-use-Werror-during-build.patch
Patch1002:      1002-Do-not-export-use-setools.InfoFlowAnalysis-and-setoo.patch
Patch1003:      1003-Require-networkx-on-package-level.patch
Patch1004:      1004-Do-not-use-NoteNotFound-as-it-s-not-implemented-in-n.patch

Obsoletes:      setools < 4.0.0, setools-devel < 4.0.0
BuildRequires:  flex,  bison
BuildRequires:  glibc-devel, gcc, git
BuildRequires:  libsepol-devel >= %{sepol_ver}, libsepol-static >= %{sepol_ver}
BuildRequires:  qt5-qtbase-devel
BuildRequires:  swig
BuildRequires:  python3-Cython
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  libselinux-devel

# BuildArch:      
Requires:       %{name}-console = %{version}-%{release}
%if %{with networkx}
Requires:       %{name}-console-analyses = %{version}-%{release}
Requires:       %{name}-gui = %{version}-%{release}
%endif

%description
SETools is a collection of graphical tools, command-line tools, and
Python modules designed to facilitate SELinux policy analysis.

%package     console
Summary:     Policy analysis command-line tools for SELinux
License:     GPLv2
Requires:    python3-setools = %{version}-%{release}
Requires:    libselinux >= %{selinux_ver}

%description console
SETools is a collection of graphical tools, command-line tools, and
libraries designed to facilitate SELinux policy analysis.

This package includes the following console tools:

  sediff       Compare two policies to find differences.
  seinfo       List policy components.
  sesearch     Search rules (allow, type_transition, etc.)


%if %{with networkx}
%package     console-analyses
Summary:     Policy analysis command-line tools for SELinux
License:     GPLv2
Requires:    python3-setools = %{version}-%{release}
Requires:    libselinux >= %{selinux_ver}
Requires:    python3-networkx

%description console-analyses
SETools is a collection of graphical tools, command-line tools, and
libraries designed to facilitate SELinux policy analysis.

This package includes the following console tools:

  sedta        Perform domain transition analyses.
  seinfoflow   Perform information flow analyses.
%endif


%package     -n python3-setools
Summary:     Policy analysis tools for SELinux  
Obsoletes:   setools-libs < 4.0.0, setools-libs-tcl
Recommends:  libselinux-python3
# Remove before F30
Provides: %{name}-python3 = %{version}-%{release}
Provides: %{name}-python3%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-python3 < %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} >= 8
Requires:    platform-python-setuptools
%else
Requires:    python3-setuptools
%endif

%description -n python3-setools
SETools is a collection of graphical tools, command-line tools, and
Python 3 modules designed to facilitate SELinux policy analysis.


%if %{with networkx}
%package     gui
Summary:     Policy analysis graphical tools for SELinux
Requires:    python3-setools = %{version}-%{release}
Requires:    python3-qt5
Requires:    python3-networkx

%description gui
SETools is a collection of graphical tools, command-line tools, and
Python modules designed to facilitate SELinux policy analysis.
%endif


%prep
%autosetup -p 1 -S git -n setools-%{version}%{?setools_pre_ver:-%{setools_pre_ver}}


%build
# Remove CFLAGS=... for noarch packages (unneeded)
%set_build_flags
%{__python3} setup.py build


%install
%{__python3} setup.py install --root %{buildroot}

%if %{without networkx}
rm -f %{buildroot}%{_bindir}/sedta %{buildroot}%{_bindir}/seinfoflow \
  %{buildroot}%{_mandir}*/man1/sedta* %{buildroot}%{_mandir}*/man1/sedinfoflow* \
rm -rf %{buildroot}%{_bindir}/apol %{buildroot}%{python3_sitearch}/setoolsgui \
  %{buildroot}%{_mandir}*/man1/apol*
%endif

%check
%if %{?_with_check:1}%{!?_with_check:0}
%{__python3} setup.py test
%endif


%files

%files console
%{_bindir}/sediff
%{_bindir}/seinfo
%{_bindir}/sesearch
%{_mandir}/man1/sediff*
%{_mandir}/man1/seinfo*
%{_mandir}/man1/sesearch*
%{_mandir}/ru/man1/sediff*
%{_mandir}/ru/man1/seinfo*
%{_mandir}/ru/man1/sesearch*

%if %{with networkx}
%files console-analyses
%{_bindir}/sedta
%{_bindir}/seinfoflow
%{_mandir}/man1/sedta*
%{_mandir}/man1/seinfoflow*
%{_mandir}/ru/man1/sedta*
%{_mandir}/ru/man1/seinfoflow*
%endif

%files -n python3-setools
%license COPYING COPYING.GPL COPYING.LGPL
%{python3_sitearch}/setools
%{python3_sitearch}/setools-*

%if %{with networkx}
%files gui
%{_bindir}/apol
%{python3_sitearch}/setoolsgui
%{_mandir}/man1/apol*
%{_mandir}/ru/man1/apol*
%endif

%changelog
* Tue Nov 30 2021 Vit Mojzis <vmojzis@redhat.com> - 4.3.0-3}
- Make seinfo output predictable (#2019961)

* Tue Jun 30 2020 Vit Mojzis <vmojzis@redhat.com> - 4.3.0-2
- Support old boolean names in policy queries (#1595572, #1581848)

* Fri Apr 03 2020 Vit Mojzis <vmojzis@redhat.com> - 4.3.0-1
- SETools 4.3.0 release (#1820079)
- Revised sediff method for TE rules. This drastically reduced memory and run time.
- Added infiniband context support to seinfo, sediff, and apol.
- Added apol configuration for location of Qt assistant.
- Fixed sediff issue where properties header would display when not requested.
- Fixed sediff issue with type_transition file name comparison.
- Fixed permission map socket sendto information flow direction.
- Added methods to TypeAttribute class to make it a complete Python collection.
- Genfscon now will look up classes rather than using fixed values which
  were dropped from libsepol.
- setools requires -console, -console-analyses and -gui packages (#1820078)

* Sat Nov 30 2019 Petr Lautrbach <plautrba@redhat.com> - 4.2.2-2
- Build setools-console-analyses and setools-gui (#1731519)

* Mon Jul 08 2019 Vit Mojzis <vmojzis@redhat.com> - 4.2.2-1
- SETools 4.2.2 release

* Mon May 13 2019 Vit Mojzis <vmojzis@redhat.com> - 4.2.1-3
- Use %set_build_flags instead of %optflags

* Mon May 06 2019 Vit Mojzis <vmojzis@redhat.com> - 4.2.1-2
- SELinuxPolicy: Create a map of aliases on policy load (#1672631)

* Tue Mar 26 2019 Petr Lautrbach <plautrba@redhat.com> - 4.2.1-1
- SETools 4.2.1 release (#1581761, #1595582)

* Fri Nov 16 2018 Lumír Balhar <lbalhar@redhat.com> - 4.2.0-2
- Require platform-python-setuptools instead of python3-setuptools
- Resolves: rhbz#1650548

* Tue Nov 13 2018 Petr Lautrbach <plautrba@redhat.com> - 4.2.0-1
- SETools 4.2.0 release

* Mon Oct 01 2018 Vit Mojzis <vmojzis@redhat.com> - 4.2.0-0.3.rc
- Update upstream source to 4.2.0-rc

* Wed Aug 22 2018 Petr Lautrbach <plautrba@redhat.com> - 4.1.1-11
- Fix SCTP patch - https://github.com/SELinuxProject/setools/issues/9

* Thu Jun 14 2018 Petr Lautrbach <plautrba@redhat.com> - 4.1.1-10
- Move gui python files to -gui subpackage
- Do not build gui and console-analyses by default

* Wed Jun  6 2018 Petr Lautrbach <plautrba@redhat.com> - 4.1.1-9
- Don't build the Python 2 subpackage (#1567362)

* Thu Apr 26 2018 Vit Mojzis <vmojzis@redhat.com> - 4.1.1-8
- Add support for SCTP protocol (#1568333)

* Thu Apr 19 2018 Iryna Shcherbina <shcherbina.iryna@gmail.com> - 4.1.1-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 04 2017 Petr Lautrbach <plautrba@redhat.com> - 4.1.1-5
- setools-python2 requires python2-enum34

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.1.1-4
- Add Provides for the old name without %%_isa

* Thu Aug 10 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.1.1-3
- Python 2 binary package renamed to python2-setools
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3
- Python 3 binary package renamed to python3-setools

* Thu Aug 10 2017 Petr Lautrbach <plautrba@redhat.com> - 4.1.1-2
- bswap_* macros are defined in byteswap.h

* Mon Aug 07 2017 Petr Lautrbach <plautrba@redhat.com> - 4.1.1-1
- New upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 22 2017 Petr Lautrbach <plautrba@redhat.com> - 4.1.0-3
- setools-python{,3} packages should have a weak dependency on libselinux-python{,3}
  (#1447747)

* Thu Feb 23 2017 Petr Lautrbach <plautrba@redhat.com> - 4.1.0-2
- Move python networkx dependency to -gui and -console-analyses
- Ship sedta and seinfoflow in setools-console-analyses

* Wed Feb 15 2017 Petr Lautrbach <plautrba@redhat.com> - 4.1.0-1
- New upstream release.
