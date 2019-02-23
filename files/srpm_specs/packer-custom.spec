%global provider        github
%global provider_tld    com
%global project         hashicorp
%global repo            packer
# https://github.com/hashicorp/packer
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global build_subdir    src

%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%endif

Name:		packer
Version:	1.3.4
Release:	1%{?dist}
Summary:	Create machine and container images for multiple platforms
License:	MPLv2.0
URL:		https://www.packer.io/

Source:		https://github.com/hashicorp/packer/archive/v%{version}.tar.gz

ExclusiveArch:	%{go_arches}

BuildRequires:	compiler(go-compiler)
BuildRequires:	golang-github-hashicorp-go-uuid-devel
BuildRequires:	golang-github-hashicorp-go-checkpoint-devel
BuildRequires:	golang-github-hashicorp-go-cleanhttp-devel
BuildRequires:	golang-github-mitchellh-cli-devel
BuildRequires:	golang-github-kardianos-osext-devel

%description
Packer is a tool for creating machine and container images for
multiple platforms from a single source configuration.

%prep
# Go modules use some nutty permissions that prevent rm -rf from automatically cleaning old builds.
# failed builds will also litter old modules around, so both prep and clean must clear them.
OLDGOPATH=$GOPATH
#export GOPATH=%{buildroot}/%{name}-%{version}/%{build_subdir}:%{_builddir}/%{name}-%{version}/%{build_subdir}
export GOPATH=%{_builddir}/%{name}-%{version}/%{build_subdir}
go clean --modcache
export GOPATH=$OLDGOPATH
%setup -q -n %{name}-%{version}

# %%{gopath} = /usr/share/gocode
%build
mkdir -p %{_builddir}/%{name}-%{version}/%{build_subdir}/%{provider_prefix}
ln -s %{_builddir}/%{name}-%{version} %{_builddir}/%{name}-%{version}/%{build_subdir}/%{provider_prefix}
export GOPATH=$(pwd)/%{build_subdir}:%{gopath}
# Quick hack to get around checksum mismatch due to golang update. See https://github.com/golang/go/issues/29278
rm go.sum
%gobuild -o bin/packer

%install
install -d %{buildroot}%{_bindir}
# The name "packer" for the binary competes with other Fedora packages
install -m 755 bin/packer %{buildroot}%{_bindir}/packerio

%files
%license LICENSE
%doc README.md
%{_bindir}/packerio

%clean
export GOPATH=%{_builddir}/%{name}-%{version}/%{build_subdir}
go clean --modcache
rm -rf %{buildroot}

%changelog
* Fri Feb 22 2019 Jason Glass <8622213+herd-the-cats@users.noreply.github.com> - 1.3.3-1
- Update to 1.3.4. Added buildroot and module cleanup.

* Tue Nov 27 2018 Greg Hellings <greg.hellings@gmail.com> - 1.3.2-1
- New upstream 1.3.2-1

* Tue Mar 20 2018 Greg Hellings <greg.hellings@gmail.com> - 1.2.1-2
- Change to source build

* Tue Mar 20 2018 Greg Hellings <greg.hellings@gmail.com> - 1.2.1-1
- Update to 1.2.1

* Thu May 05 2016 Josef Strzibny <strzibny@strzibny.name> - 0.10.0-1
- Update to 0.10.0

* Tue Oct 27 2015 Josef Stribny <jstribny@redhat.com> - 0.8.6-1
- Initial package
