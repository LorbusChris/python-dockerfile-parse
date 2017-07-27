%if 0%{?rhel} && 0%{?rhel} <= 7
%bcond_with python3
%if 0%{?rhel} <= 6
%{!?python2_version: %global python2_version %(%{__python2} -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?_licensedir:%global license %%doc}
%endif
%else
%bcond_without python3
%endif

%bcond_without tests

%global srcname dockerfile-parse
%global modname %(n=%{srcname}; echo ${n//-/_})

Name:           python-%{srcname}
Version:        0.0.5
Release:        10%{?dist}

Summary:        Python library for Dockerfile manipulation
License:        BSD
URL:            https://github.com/DBuildService/dockerfile-parse
Source0:        %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz

# Patch to handle inheriting ENV vars from parent Dockerfiles
#
# Upstream PRs (merged into single patch here):
#   https://github.com/DBuildService/dockerfile-parse/pull/21
#   https://github.com/DBuildService/dockerfile-parse/pull/22
Patch0:         dockerfile-parse-0.0.5-parent_env.patch

BuildArch:      noarch

%description
%{summary}.

%package -n python2-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{srcname}}
BuildRequires:  python2-devel
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:  python-setuptools
BuildRequires:  pytest
%else
BuildRequires:  python2-setuptools
BuildRequires:  python2-pytest
%endif

%description -n python2-%{srcname}
%{summary}.

Python 2 version.

%if %{with python3}
%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with tests}
BuildRequires:  python3-pytest
%endif

%description -n python3-%{srcname}
%{summary}.

Python 3 version.
%endif

%prep
%setup -n %{srcname}-%{version}

%patch0 -p1

%build
%py2_build
%if %{with python3}
%py3_build
%endif

%install
%py2_install
%if %{with python3}
%py3_install
%endif

%if %{with tests}
%check
export LANG=C.UTF-8
py.test-%{python2_version} -v tests
%if %{with python3}
py.test-%{python3_version} -v tests
%endif
%endif

%files -n python2-%{srcname}
%license LICENSE
%doc README.md
%{python2_sitelib}/%{modname}-*.egg-info/
%{python2_sitelib}/%{modname}/

%if %{with python3}
%files -n python3-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{modname}-*.egg-info/
%{python3_sitelib}/%{modname}/
%endif

%changelog
* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.0.5-8
- Rebuild for Python 3.6

* Tue Dec 06 2016 Adam Miller <maxamillion@fedoraproject.org> - 0.0.5-7
- Patch to handle inheriting parent Dockerfile ENVs

* Wed Sep 07 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.0.5-6
- Modernize spec
- Trivial fixes

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.5-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Nov 06 2015 Jiri Popelka <jpopelka@redhat.com> - 0.0.5-2
- %%check section

* Mon Sep 21 2015 Jiri Popelka <jpopelka@redhat.com> - 0.0.5-1
- 0.0.5

* Thu Aug 27 2015 Jiri Popelka <jpopelka@redhat.com> - 0.0.4-1
- 0.0.4

* Tue Jun 30 2015 Jiri Popelka <jpopelka@redhat.com> - 0.0.3-2
- define macros for RHEL-6

* Fri Jun 26 2015 Jiri Popelka <jpopelka@redhat.com> - 0.0.3-1
- 0.0.3

* Fri Jun 26 2015 Jiri Popelka <jpopelka@redhat.com> - 0.0.2-1
- 0.0.2

* Thu Jun 18 2015 Jiri Popelka <jpopelka@redhat.com> - 0.0.1-1
- initial release
