#
# Conditional build:
%bcond_with	tests		# disable all tests for now to avoid linking QuickCheck
%bcond_with	prof		# disable profiling symbols

%define		pkg_name	ShellCheck
Summary:	Shell script analysis tool
Name:		shellcheck
Version:	0.3.7
Release:	0.1
License:	AGPL v3+
Group:		Development
Source0:	https://hackage.haskell.org/package/%{pkg_name}-%{version}/%{pkg_name}-%{version}.tar.gz
# Source0-md5:	5e570545d9168e085c465e0fd8902340
Patch0:		ShellCheck-disable-TemplateHaskell-runTests.patch
URL:		http://www.shellcheck.net/about.html
BuildRequires:	ghc-Cabal-devel
BuildRequires:	ghc-rpm-macros
# Begin cabal-rpm deps:
BuildRequires:	chrpath
BuildRequires:	ghc-containers-devel
BuildRequires:	ghc-directory-devel
BuildRequires:	ghc-json-devel
BuildRequires:	ghc-mtl-devel
BuildRequires:	ghc-parsec-devel
BuildRequires:	ghc-regex-tdfa-devel
BuildRequires:	ghc-transformers-devel
%if %{with tests}
BuildRequires:	ghc-QuickCheck-devel
%endif
# End cabal-rpm deps
BuildRequires:	pandoc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The goals of ShellCheck are:
- To point out and clarify typical beginner's syntax issues, that
  causes a shell to give cryptic error messages.
- To point out and clarify typical intermediate level semantic
  problems, that causes a shell to behave strangely and
  counter-intuitively.
- To point out subtle caveats, corner cases and pitfalls, that may
  cause an advanced user's otherwise working script to fail under future
  circumstances.

%package -n ghc-%{pkg_name}
Summary:	Haskell %{pkg_name} library

%description -n ghc-%{pkg_name}
This package provides the Haskell %{pkg_name} shared library.

%package -n ghc-%{pkg_name}-devel
Summary:	Haskell %{pkg_name} library development files
Requires:	ghc-compiler = %{ghc_version}
Provides:	ghc-%{pkg_name}-static = %{version}-%{release}
Requires(post):	ghc-compiler = %{ghc_version}
Requires(postun):	ghc-compiler = %{ghc_version}
Requires:	ghc-%{pkg_name} = %{version}-%{release}

%description -n ghc-%{pkg_name}-devel
This package provides the Haskell %{pkg_name} library development
files.

%prep
%setup -q
%if %{without tests}
%patch0 -p1
%endif

%build
LANG=en_US.utf8
%ghc_lib_build

pandoc -s -t man shellcheck.1.md -o shellcheck.1

%check
%if %{with tests}
%cabal test
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ghc_lib_install

cp -p shellcheck.1 $RPM_BUILD_ROOT%{_mandir}/man1/shellcheck.1

%ghc_fix_dynamic_rpath shellcheck

%clean
rm -rf $RPM_BUILD_ROOT

%post -n ghc-%{pkg_name}-devel
%ghc_pkg_recache

%postun -n ghc-%{pkg_name}-devel
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE
%doc README.md
%attr(755,root,root) %{_bindir}/shellcheck
%{_mandir}/man1/shellcheck.1*

%files -n ghc-%{pkg_name} -f ghc-%{pkg_name}.files
%defattr(644,root,root,755)
%doc LICENSE

%files -n ghc-%{pkg_name}-devel -f ghc-%{pkg_name}-devel.files
%defattr(644,root,root,755)
%doc README.md
