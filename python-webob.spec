%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-webob
Summary:        WSGI request and response object
Version:        0.9.5
Release:        1%{?dist}
License:        MIT
Group:          System Environment/Libraries
URL:            http://pythonpaste.org/webob/
Source0:        http://pypi.python.org/packages/source/W/WebOb/WebOb-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools-devel
BuildRequires:  python-nose
BuildRequires:  python-dtopt
BuildRequires:  python-tempita
BuildRequires:  python-wsgiproxy

%description
WebOb provides wrappers around the WSGI request environment, and an object to 
help create WSGI responses. The objects map much of the specified behavior of 
HTTP, including header parsing and accessors for other standard parts of the 
environment.

%prep
%setup -q -n WebOb-%{version}
# Disable the tests that require python-webtest
# (which depends on python-webob to begin with)
%{__rm} -f tests/test_request.py
# Disable conftest, which assumes that WebOb is already installed
%{__rm} -f tests/conftest.py


%build
%{__python} setup.py build


%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}


%clean
%{__rm} -rf %{buildroot}


%check
./test


%files
%defattr(-,root,root,-)
%doc docs/*
%{python_sitelib}/webob/
%{python_sitelib}/WebOb*.egg-info/

%changelog
* Tue Jan 06 2009 Luke Macken <lmacken@redhat.com> 0.9.5-1
- Update to 0.9.5

* Sat Dec 06 2008 Ricky Zhou <ricky@fedoraproject.org> 0.9.4-1
- Upstream released new version.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.9.3-3
- Rebuild for Python 2.6

* Tue Sep 30 2008 Ricky Zhou <ricky@fedoraproject.org> 0.9.3-2
- Add BuildRequires on python-tempita.

* Tue Sep 30 2008 Ricky Zhou <ricky@fedoraproject.org> 0.9.3-1
- Upstream released new version.

* Thu Jul 17 2008 Ricky Zhou <ricky@fedoraproject.org> 0.9.2-2
- Remove conftest from the tests.

* Fri Jun 27 2008 Ricky Zhou <ricky@fedoraproject.org> 0.9.2-1
- Upstream released new version.
- Rename to python-webob, as mentioned in the Python package naming
  guidelines.
- Clean up spec.
- Add %%check section.

* Sat Mar 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.9-1
- Initial package for Fedora
