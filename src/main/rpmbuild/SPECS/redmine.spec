Name: %{_name}
Version: %{_version}
Release: %{_release}
Summary: Redmine
License: None
BuildArch: %{_arch}
AutoReqProv: No
Source0: redmine-%{version}
Source1: Gemfile
#Source1: Gemfile.local
Source2: Gemfile.lock
Source3: unicorn.rb
Source4: sysvinit

%define __spec_install_post %{nil}
%define debug_package %{nil}
%define __os_install_post %{_dbpath}/brp-compress

%define homedir /home/redmine
%define appdir %{homedir}/redmine

%description
Redmine is a flexible project management web application. Written using the Ruby on Rails
framework, it is cross-platform and cross-database.  Redmine is open source and released
under the terms of the GNU General Public License v2 (GPL).

%install
rm -rf %{buildroot}
install -dm 750 %{buildroot}%{homedir}

# Redmine directory
cp -r %{SOURCE0}/ %{buildroot}%{appdir}
cp %{SOURCE1} %{buildroot}%{appdir} # Gemfile
#cp %{SOURCE1} %{buildroot}%{appdir} # Gemfile.local
cp %{SOURCE2} %{buildroot}%{appdir} # Gemfile.lock
cp %{SOURCE3} %{buildroot}%{appdir}/config/unicorn.rb
cp %{buildroot}%{appdir}/config/database.yml{.example,}
pushd %{buildroot}%{appdir} >/dev/null
bundle install --deployment --without development test
popd >/dev/null

# Redmine initd script
install -dm 755 %{buildroot}/etc/init.d
cp %{SOURCE4} %{buildroot}/etc/init.d/redmine

%pre
getent group redmine > /dev/null || groupadd -r redmine
getent passwd redmine > /dev/null || \
    useradd -r -g redmine -s /bin/false -c "Redmine" redmine

%files
%defattr(-,redmine,redmine,-)
%{homedir}
%attr(755,root,root) /etc/init.d/redmine

%changelog
* Wed Sep 10 2014 Eduardo Ito <ed@fghijk.net> - 2.5.2-1
- Initial release
