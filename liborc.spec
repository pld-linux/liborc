# TODO:
# - java (requires maven)
# - libhdfspp?
#
# Conditional build:
%bcond_with	java		# Java library
%bcond_with	avx512		# AVX512 x86 instructions

Summary:	Apache ORC - small, fast columnar storage for Hadoop workloads
Summary(pl.UTF-8):	Apache ORC - małym, szybki kolumnowy format przechowywania danych dla zadań Hadoopa
Name:		liborc
Version:	2.1.3
Release:	1
License:	Apache v2.0
Group:		Libraries
Source0:	https://downloads.apache.org/orc/orc-%{version}/orc-%{version}.tar.gz
# Source0-md5:	9f49814d56198551d223156b8498b537
Source1:	https://downloads.apache.org/orc/orc-format-1.1.0/orc-format-1.1.0.tar.gz
# Source1-md5:	45ddc8bbdacc0f2b8b1bd570b8a692c2
Patch0:		%{name}-shared.patch
URL:		https://orc.apache.org/
BuildRequires:	cmake >= 3.12.0
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	lz4-devel
BuildRequires:	protobuf-devel
BuildRequires:	snappy-devel
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ORC is a self-describing type-aware columnar file format designed for
Hadoop workloads. It is optimized for large streaming reads, but with
integrated support for finding required rows quickly. Storing data in
a columnar format lets the reader read, decompress, and process only
the values that are required for the current query. Because ORC files
are type-aware, the writer chooses the most appropriate encoding for
the type and builds an internal index as the file is written.
Predicate pushdown uses those indexes to determine which stripes in a
file need to be read for a particular query and the row indexes can
narrow the search to a particular set of 10,000 rows. ORC supports the
complete set of types in Hive, including the complex types: structs,
lists, maps, and unions.

%description -l pl.UTF-8
ORC to samoopisujący się, uwzględniający typy format kolumnowy,
zaprojektowany do zadań Hadoopa. Jest zoptymalizowany pod kątem dużych
odczytów strumieniowych, ale ma zintegrowaną obsługę szybkiego
wyszukiwania potrzebnych wierszy. Przechowywanie danych w formacie
kolumnowym pozwala czytelnikom czytać, dekompresować i przetwarzać
tylko wartości potrzebne przy aktualnym zapytaniu. Ponieważ pliki ORC
uwzględniają typy, piszący wybiera najbardziej odpowiednie kodowanie
dla tupu i tworzy wewnętrzny indeks przy zapisie pliku. Optymalizacja
predicate pushdown wykorzystuje te indeksy do określenia, które pasy
danych muszą być odczytane z pliku do określonego zapytania, a indeksy
wierszy pozwalają zawęzić wyszukiwanie do około 10000 wierszy. ORC
obsługuje kompletny zbiór typów Hive, w tym typy złożone: struktury,
listy, mapy i unie.

%package devel
Summary:	Header files for Apache ORC library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Apache ORC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:7

%description devel
Header files for Apache ORC library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Apache ORC.

%prep
%setup -q -n orc-%{version}
%patch -P0 -p1

%build
install -d build
cd build
export ORC_FORMAT_URL="%{SOURCE1}"
%cmake .. \
	-DBUILD_CPP_TESTS=OFF \
	%{?with_avx512:-DBUILD_ENABLE_AVX512=ON} \
	%{!?with_java:-DBUILD_JAVA=OFF} \
	-DBUILD_POSITION_INDEPENDENT_LIB=ON \
	-DINSTALL_VENDORED_LIBS=OFF \
	-DLZ4_HOME=/usr \
	-DORC_PREFER_STATIC_GMOCK=OFF \
	-DORC_PREFER_STATIC_LZ4=OFF \
	-DORC_PREFER_STATIC_PROTOBUF=OFF \
	-DORC_PREFER_STATIC_SNAPPY=OFF \
	-DORC_PREFER_STATIC_ZSTD=OFF \
	-DORC_PREFER_STATIC_ZLIB=OFF \
	-DPROTOBUF_HOME=/usr \
	-DSNAPPY_HOME=/usr \
	-DZLIB_HOME=/usr \
	-DZSTD_HOME=/usr

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# too common names, add prefix
%{__mv} $RPM_BUILD_ROOT%{_bindir}/{,orc-}csv-import
%{__mv} $RPM_BUILD_ROOT%{_bindir}/{,orc-}timezone-dump

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NOTICE README.md
%attr(755,root,root) %{_bindir}/orc-contents
%attr(755,root,root) %{_bindir}/orc-csv-import
%attr(755,root,root) %{_bindir}/orc-memory
%attr(755,root,root) %{_bindir}/orc-metadata
%attr(755,root,root) %{_bindir}/orc-scan
%attr(755,root,root) %{_bindir}/orc-statistics
%attr(755,root,root) %{_bindir}/orc-timezone-dump
%attr(755,root,root) %{_libdir}/liborc.so.*.*.*
%ghost %{_libdir}/liborc.so.2

%files devel
%defattr(644,root,root,755)
%{_libdir}/liborc.so
%{_includedir}/orc
%{_libdir}/cmake/orc
