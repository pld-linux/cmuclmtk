#
# Conditional build:
%bcond_without	perl		# perl package
%bcond_without	static_libs	# static library
#
Summary:	CMU-Cambridge Language Modeling Toolkit
Summary(pl.UTF-8):	CMU-Cambridge Language Modeling Toolkit - narzędzia do tworzenia modeli językowych
Name:		cmuclmtk
Version:	0.7
Release:	2
License:	BSD, parts for research only
Group:		Libraries
Source0:	http://downloads.sourceforge.net/cmusphinx/%{name}-%{version}.tar.gz
# Source0-md5:	21bfb116d309e43e61def3692f98cdac
Patch0:		%{name}-missing.patch
URL:		https://cmusphinx.github.io/
%if %{with perl}
BuildRequires:	perl-devel
BuildRequires:	rpm-perlprov
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CMU-Cambridge Language Modeling Toolkit.

%description -l pl.UTF-8
CMU-Cambridge Language Modeling Toolkit - narzędzia do tworzenia
modeli językowych.

%package devel
Summary:	Header files for CMU-C LM Toolkit library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki CMU-C LM Toolkit
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for CMU-C LM Toolkit library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki CMU-C LM Toolkit.

%package static
Summary:	Static CMU-C LM Toolkit library
Summary(pl.UTF-8):	Statyczna biblioteka CMU-C LM Toolkit
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static CMU-C LM Toolkit library.

%description static -l pl.UTF-8
Statyczna biblioteka CMU-C LM Toolkit.

%package -n perl-Text-CMU-LMTraining
Summary:	Text::CMU::LMTraining - module for language model training
Summary(pl.UTF-8):	Text::CMU::LMTraining - moduł do trenowania modeli językowych
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}

%description -n perl-Text-CMU-LMTraining
Text::CMU::LMTraining package contains language training modules.

%description -n perl-Text-CMU-LMTraining -l pl.UTF-8
Pakiet Text::CMU::LMTraining zawiera moduły do trenowania modeli
językowych.

%prep
%setup -q
%patch -P0 -p1

%build
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%if %{with perl}
cd perl
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

%{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcmuclmtk.la

%if %{with perl}
%{__make} -C perl pure_install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README TODO doc/{change_log.html,toolkit*}
%attr(755,root,root) %{_bindir}/binlm2arpa
%attr(755,root,root) %{_bindir}/evallm
%attr(755,root,root) %{_bindir}/idngram2lm
%attr(755,root,root) %{_bindir}/idngram2stats
%attr(755,root,root) %{_bindir}/lm_combine
%attr(755,root,root) %{_bindir}/lm_interpolate
%attr(755,root,root) %{_bindir}/mergeidngram
%attr(755,root,root) %{_bindir}/ngram2mgram
%attr(755,root,root) %{_bindir}/text2idngram
%attr(755,root,root) %{_bindir}/text2wfreq
%attr(755,root,root) %{_bindir}/text2wngram
%attr(755,root,root) %{_bindir}/wfreq2vocab
%attr(755,root,root) %{_bindir}/wngram2idngram
%attr(755,root,root) %{_libdir}/libcmuclmtk.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcmuclmtk.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcmuclmtk.so
%{_includedir}/cmuclmtk

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcmuclmtk.a
%endif

%if %{with perl}
%files -n perl-Text-CMU-LMTraining
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cmu_build_vocab
%attr(755,root,root) %{_bindir}/cmu_lm_train
%attr(755,root,root) %{_bindir}/cmu_ngram_interp
%attr(755,root,root) %{_bindir}/cmu_ngram_pronounce
%attr(755,root,root) %{_bindir}/cmu_ngram_test
%attr(755,root,root) %{_bindir}/cmu_ngram_train
%attr(755,root,root) %{_bindir}/cmu_normalize_text
%dir %{perl_vendorlib}/Text/CMU
%{perl_vendorlib}/Text/CMU/InputFilter
%{perl_vendorlib}/Text/CMU/NGramModel
%{perl_vendorlib}/Text/CMU/InputFilter.pm
%{perl_vendorlib}/Text/CMU/LMTraining.pm
%{perl_vendorlib}/Text/CMU/NGramFactory.pm
%{perl_vendorlib}/Text/CMU/NGramModel.pm
%{perl_vendorlib}/Text/CMU/Smoothing.pm
%{perl_vendorlib}/Text/CMU/Vocabulary.pm
%attr(755,root,root) %{perl_vendorlib}/Text/CMU/class_tagger.pl
%attr(755,root,root) %{perl_vendorlib}/Text/CMU/unihan_to_sphinx.pl
%attr(755,root,root) %{perl_vendorlib}/Text/CMU/lm_changecase.pl
%{_mandir}/man1/cmu_build_vocab.1p*
%{_mandir}/man1/cmu_lm_train.1p*
%{_mandir}/man1/cmu_ngram_interp.1p*
%{_mandir}/man1/cmu_ngram_pronounce.1p*
%{_mandir}/man1/cmu_ngram_test.1p*
%{_mandir}/man1/cmu_ngram_train.1p*
%{_mandir}/man1/cmu_normalize_text.1p*
%{_mandir}/man3/Text::CMU::InputFilter*.3pm*
%{_mandir}/man3/Text::CMU::LMTraining.3pm*
%{_mandir}/man3/Text::CMU::NGramFactory.3pm*
%{_mandir}/man3/Text::CMU::NGramModel*.3pm*
%{_mandir}/man3/Text::CMU::Smoothing.3pm*
%{_mandir}/man3/Text::CMU::Vocabulary.3pm*
%endif
