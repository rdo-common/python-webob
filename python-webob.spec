%if 0%{?fedora}
%global with_python3 1
%{!?py3ver: %global py3ver %(%{__python3} -c "import sys ; print(sys.version[:3])")}
%endif

%{!?py2ver: %global py2ver %(%{__python} -c "import sys ; print sys.version[:3]")}
%global with_tests 1

%global modname webob

Name:           python-webob
Summary:        WSGI request and response object
Version:        1.7.2
Release:        2%{?dist}
License:        MIT
Group:          System Environment/Libraries
URL:            http://pythonpaste.org/webob/
Source0:        https://files.pythonhosted.org/packages/source/W/WebOb/WebOb-%{version}.tar.gz
Source1:        README.Fedora

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if 0%{?with_tests}
BuildRequires:  python-nose
BuildRequires:  python-dtopt
BuildRequires:  python-tempita
BuildRequires:  python-webtest
BuildRequires:  python2-pytest
%endif # with_tests

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?with_tests}
BuildRequires:  python3-nose
BuildRequires:  python3-pytest
%endif # with_tests
%endif

Provides: python2-webob = %{version}-%{release}
Provides: python-webob1.2 = %{version}-%{release}
Obsoletes: python-webob1.2 < 1.2.3-7

%description
WebOb provides wrappers around the WSGI request environment, and an object to 
help create WSGI responses. The objects map much of the specified behavior of 
HTTP, including header parsing and accessors for other standard parts of the 
environment.

%if 0%{?with_python3}
%package -n python3-webob
Summary:        WSGI request and response object
Group:          System Environment/Libraries

Requires:       python3

Provides: python3-webob1.2 = %{version}-%{release}
Obsoletes: python3-webob1.2 < 1.2.3-7

%description -n python3-webob
WebOb provides wrappers around the WSGI request environment, and an object to 
help create WSGI responses. The objects map much of the specified behavior of 
HTTP, including header parsing and accessors for other standard parts of the 
environment.
%endif

%prep
%setup -q -n WebOb-%{version}
cp -p %{SOURCE1} .
# Disable performance_test, which requires repoze.profile, which isn't
# in Fedora.
%{__rm} -f tests/performance_test.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
#%{__chmod} 0644 %{buildroot}%{python3_sitelib}/WebOb-%{version}-*.egg/%{modname}/*.py
popd
%endif

%{__mkdir} -p %{buildroot}%{python_sitelib}
%{__python} setup.py install --skip-build --root %{buildroot}
#%{__chmod} 0644 %{buildroot}%{python_sitelib}/WebOb-%{version}-*.egg/%{modname}/*.py

%check
%if 0%{?with_tests}
%{__python} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif
%endif # with_tests

%files
%doc docs/* README.Fedora
%{python_sitelib}/webob/
%{python_sitelib}/WebOb-%{version}-py%{py2ver}.egg-info

%if 0%{?with_python3}
%files -n python3-webob
%doc docs/* README.Fedora
%{python3_sitelib}/webob/
%{python3_sitelib}/WebOb-%{version}-py%{py3ver}.egg-info
%endif

%changelog
* Wed Jan 29 2020 Yatin Karel <ykarel@redhat.com> - 1.7.2-2
- Provides python2-webob

* Sat Mar 25 2017 Kevin Fenzi <kevin@scrye.com> - 1.7.2-1
- Update to 1.7.2. Fixes bug #1432922

* Sat Feb 25 2017 Kevin Fenzi <kevin@scrye.com> - 1.7.1-1
- Update to 1.7.1. Fixes bug #1413950

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 28 2016 Kevin Fenzi <kevin@scrye.com> - 1.7.0-1
- Update to 1.7.0. Fixes bug #1408197

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.6.2-2
- Rebuild for Python 3.6

* Wed Nov 09 2016 Kevin Fenzi <kevin@scrye.com> - 1.6.2-1
- Update to 1.6.2. Fixes bug #1385661

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue May 31 2016 Nils Philippsen <nils@redhat.com>
- fix source URL

* Sun May 22 2016 Luke Macken <lmacken@redhat.com> - 1.6.1-1
- Update to 1.6.1. Fixes bug #1338436

* Sun Apr 10 2016 Kevin Fenzi <kevin@scrye.com> - 1.6.0-1
- Update to 1.6.0. Fixes bug #1300180

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 1.4.2-1
- Upstream 1.4.2

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 15 2015 Ralph Bean <rbean@redhat.com> - 1.4.1-1
- new version

* Wed Aug 27 2014 Luke Macken <lmacken@redhat.com> - 1.4-1
- Update to 1.4

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 15 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.3-10
- Enable tests again.

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4
- Set up macro for test bootstrap

* Mon Jan  6 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.2.3-8
- And correct the obs_ver again as a later version was built
- Add obsoletes for the python3-webob1.2 package as well

* Mon Sep 16 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.2.3-7
- correct python-webob1.2 obs_ver

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May  7 2013 Luke Macken <lmacken@redhat.com> - 1.2.3-5
- Remove the python-wsgiproxy build requirement (#960463)

* Tue Apr  2 2013 Luke Macken <lmacken@redhat.com> - 1.2.3-4
- Rebase with and obsolete the python-webob1.2 forward-compat package

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 10 2013 Pádraig Brady <P@draigBrady.com> - 1.2.3-2
- Update to WebOb-1.2.3

* Wed Jan 09 2013 Matthias Runge <mrunge@redhat.com> - 1.1.1-4
- fix deprecation warning (rhbz#801312)
- minor spec cleanup

* Thu Nov 29 2012 Ralph Bean <rbean@redhat.com> - 1.2.1-9
- Trying pyver again with py2ver and py3ver.  Getting ugly.

* Thu Nov 29 2012 Ralph Bean <rbean@redhat.com> - 1.2.1-8
- Hardcode python3 version

* Thu Nov 29 2012 Ralph Bean <rbean@redhat.com> - 1.2.1-7
- Forced rebuild.

* Tue Oct 16 2012 Ralph Bean <rbean@redhat.com> - 1.2.1-6
- Use pyver macro to use the correct easy-install.

* Tue Oct 16 2012 Ralph Bean <rbean@redhat.com> - 1.2.1-5
- Forced rebuild.

* Mon Aug 06 2012 Ralph Bean <rbean@redhat.com> - 1.2.1-4
- Modernized the with_python3 conditional.
- Updated README.Fedora from 1.0.x to 1.2.1.

* Mon Aug 06 2012 Ralph Bean <rbean@redhat.com> - 1.2.1-3
- Removed unreferenced %%global pypiname.
- Changed %%check invocation from "nosetests" to "python setup.py test"
- Added python3 support.

* Mon Aug 06 2012 Ralph Bean <rbean@redhat.com> - 1.2.1-2
- Typofix BR: python-setuptools-devel -> python-setuptools

* Mon Aug 06 2012 Ralph Bean <rbean@redhat.com> - 1.2.1-1
- Fork from python-webob1.0 for forward-compat python-webob1.2.
- Some modernization of the spec file.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 14 2011 Luke Macken <lmacken@redhat.com> - 1.1.1-1
- Update to the latest stable release
- Remove wsgiproxy, tempita, and dtopt from our build requirements

* Thu Nov 17 2011 Steve Traylen <steve.traylen@cern.ch> - 1.0.8-3
- Rename package from python-webob10 to python-webob1.0

* Thu Nov 17 2011 Steve Traylen <steve.traylen@cern.ch> - 1.0.8-2
- Fedora package adapted to parallel installable on el6.

* Wed Aug 17 2011 Nils Philippsen <nils@redhat.com> - 1.0.8-1
- Update to 1.0.8 for TurboGears 2.1.1 which needs 1.0.7 (#663117)

* Mon Mar 21 2011 Luke Macken <lmacken@redhat.com> - 1.0.5-1
- Update to 1.0.5, which restores Python 2.4 support

* Thu Feb 24 2011 Luke Macken <lmacken@redhat.com> - 1.0.3-1
- Update to 1.0.3

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Ricky Zhou <ricky@fedoraproject.org> - 1.0-1
- Upstream released new version.

* Sun Jul 25 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.9.8-4
- Reenable tests since python-webtest is now available

* Sun Jul 25 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.9.8-3
- Disable tests. We need to bootstrap against python-webtest

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed May 05 2010 Luke Macken <lmacken@redhat.com> - 0.9.8-1
- Latest upstream release
- Get the test suite running

* Tue Jan 19 2010 Ricky Zhou <ricky@fedoraproject.org> - 0.9.7.1-1
- Upstream released new version.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 14 2009 Ricky Zhou <ricky@fedoraproject.org> - 0.9.6.1-2
- Change define to global.
- Remove unnecessary BuildRequires on python-devel.

* Tue Mar 10 2009 Ricky Zhou <ricky@fedoraproject.org> - 0.9.6.1-1
- Upstream released new version.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

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
