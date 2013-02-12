%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:             babel
Version:          0.1.0
Release:          1%{?dist}
Summary:          A Bibliography Manager

License:          GPLv3+
Group:            Applications/Engineering
URL:              http://github.com/FabriceSalvaire/Babel

Source0:           http://github.com/downloads/FabriceSalvaire/Babel/%{name}-%{version}.tar.gz

BuildArch:        noarch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:    python-devel desktop-file-utils

Requires:         PyQt4 >= 4.9

%description
...

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

desktop-file-install --vendor fedora            \
    --add-category Engineering                  \
    --delete-original                           \
    --dir %{buildroot}%{_datadir}/applications/ \
    %{buildroot}%{_datadir}/applications/babel.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/

%clean
rm -rf %{buildroot}

%post
ln -sf %{_datadir}/Babel/icons/babel.svg %{_datadir}/icons/hicolor/scalable/apps/babel.svg 
# The shell pattern "command || :" return always success
touch --no-create %{_datadir}/icons/hicolor || :
update-desktop-database &> /dev/null || :

%postun
rm %{_datadir}/icons/hicolor/scalable/apps/babel.svg 
touch --no-create %{_datadir}/icons/hicolor || :
update-desktop-database &> /dev/null || :

%files
%defattr(-,root,root,-)
%{_bindir}/babel
%{_datadir}/Babel/
%{_datadir}/applications/fedora-babel.desktop
# datadir/icons/hicolor/scalable/apps/babel.svg 
%{python_sitelib}/Babel/
%{python_sitelib}/%{name}-%{version}-py?.?.egg-info

%changelog
* Mon Nov  5 2012 Fabrice Salvaire <fabrice.salvaire@orange.fr> - 0.1.0-1
- Initial package.
# End SPEC
