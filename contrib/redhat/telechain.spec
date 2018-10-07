Name:           telechain
Version:        0.6.3
Release:        1%{?dist}
Summary:        Telechain Wallet
Group:          Applications/Internet
Vendor:         Telechain
License:        GPLv3
URL:            https://www.telechain.io
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  autoconf automake libtool gcc-c++ openssl-devel >= 1:1.0.2d libdb4-devel libdb4-cxx-devel miniupnpc-devel boost-devel boost-static
Requires:       openssl >= 1:1.0.2d libdb4 libdb4-cxx miniupnpc logrotate

%description
Telechain Wallet

%prep
%setup -q

%build
./autogen.sh
./configure
make

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT/etc/telechain $RPM_BUILD_ROOT/etc/ssl/tlc $RPM_BUILD_ROOT/var/lib/tlc/.telechain $RPM_BUILD_ROOT/usr/lib/systemd/system $RPM_BUILD_ROOT/etc/logrotate.d
%{__install} -m 755 src/telechaind $RPM_BUILD_ROOT%{_bindir}
%{__install} -m 755 src/telechain-cli $RPM_BUILD_ROOT%{_bindir}
%{__install} -m 600 contrib/redhat/telechain.conf $RPM_BUILD_ROOT/var/lib/tlc/.telechain
%{__install} -m 644 contrib/redhat/telechaind.service $RPM_BUILD_ROOT/usr/lib/systemd/system
%{__install} -m 644 contrib/redhat/telechaind.logrotate $RPM_BUILD_ROOT/etc/logrotate.d/telechaind
%{__mv} -f contrib/redhat/tlc $RPM_BUILD_ROOT%{_bindir}

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pretrans
getent passwd tlc >/dev/null && { [ -f /usr/bin/telechaind ] || { echo "Looks like user 'tlc' already exists and have to be deleted before continue."; exit 1; }; } || useradd -r -M -d /var/lib/tlc -s /bin/false tlc

%post
[ $1 == 1 ] && {
  sed -i -e "s/\(^rpcpassword=MySuperPassword\)\(.*\)/rpcpassword=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)/" /var/lib/tlc/.telechain/telechain.conf
  openssl req -nodes -x509 -newkey rsa:4096 -keyout /etc/ssl/tlc/telechain.key -out /etc/ssl/tlc/telechain.crt -days 3560 -subj /C=US/ST=Oregon/L=Portland/O=IT/CN=telechain.tlc
  ln -sf /var/lib/tlc/.telechain/telechain.conf /etc/telechain/telechain.conf
  ln -sf /etc/ssl/tlc /etc/telechain/certs
  chown tlc.tlc /etc/ssl/tlc/telechain.key /etc/ssl/tlc/telechain.crt
  chmod 600 /etc/ssl/tlc/telechain.key
} || exit 0

%posttrans
[ -f /var/lib/tlc/.telechain/addr.dat ] && { cd /var/lib/tlc/.telechain && rm -rf database addr.dat nameindex* blk* *.log .lock; }
sed -i -e 's|rpcallowip=\*|rpcallowip=0.0.0.0/0|' /var/lib/tlc/.telechain/telechain.conf
systemctl daemon-reload
systemctl status telechaind >/dev/null && systemctl restart telechaind || exit 0

%preun
[ $1 == 0 ] && {
  systemctl is-enabled telechaind >/dev/null && systemctl disable telechaind >/dev/null || true
  systemctl status telechaind >/dev/null && systemctl stop telechaind >/dev/null || true
  pkill -9 -u tlc > /dev/null 2>&1
  getent passwd tlc >/dev/null && userdel tlc >/dev/null 2>&1 || true
  rm -f /etc/ssl/tlc/telechain.key /etc/ssl/tlc/telechain.crt /etc/telechain/telechain.conf /etc/telechain/certs
} || exit 0

%files
%doc COPYING
%attr(750,tlc,tlc) %dir /etc/telechain
%attr(750,tlc,tlc) %dir /etc/ssl/tlc
%attr(700,tlc,tlc) %dir /var/lib/tlc
%attr(700,tlc,tlc) %dir /var/lib/tlc/.telechain
%attr(600,tlc,tlc) %config(noreplace) /var/lib/tlc/.telechain/telechain.conf
%attr(4750,tlc,tlc) %{_bindir}/telechain-cli
%defattr(-,root,root)
%config(noreplace) /etc/logrotate.d/telechaind
%{_bindir}/telechaind
%{_bindir}/tlc
/usr/lib/systemd/system/telechaind.service

%changelog
* Thu Aug 31 2017 Aspanta Limited <info@aspanta.com> 0.6.3
- There is no changelog available. Please refer to the CHANGELOG file or visit the website.
