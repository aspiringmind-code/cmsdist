### RPM external ucx 1.14.x
%define branch v1.14.x
%define tag bb39346ac1aebc67cb88c4419429de78a1260bda
Source: git+https://github.com/openucx/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/v%{realversion}.tar.gz
BuildRequires: autotools
Requires: cuda gdrcopy
Requires: numactl
Requires: rdma-core
%ifarch x86_64
Requires: rocm
%endif
Requires: xpmem
AutoReq: no

%prep
%setup -q -n %{n}-%{realversion}

# regenerate the configure files and Makefiles
./autogen.sh

./configure \
  --prefix=%i \
  --disable-dependency-tracking \
  --enable-openmp \
  --enable-shared \
  --disable-static \
  --enable-ucg \
  --disable-doxygen-doc \
  --disable-doxygen-man \
  --disable-doxygen-html \
  --enable-compiler-opt \
  --enable-cma \
  --enable-mt \
  --with-pic \
  --with-gnu-ld \
  --with-avx \
  --with-sse41 \
  --with-sse42 \
  --without-go \
  --without-java \
  --with-cuda=$CUDA_ROOT \
%ifarch x86_64
  --with-rocm=$ROCM_ROOT \
%else
  --without-rocm \
%endif
  --with-gdrcopy=$GDRCOPY_ROOT \
  --with-verbs=$RDMA_CORE_ROOT \
  --with-rc \
  --with-ud \
  --with-dc \
  --with-mlx5-dv \
  --with-ib-hw-tm \
  --with-dm \
  --with-rdmacm=$RDMA_CORE_ROOT \
  --without-knem \
  --with-xpmem=$XPMEM_ROOT \
  --without-ugni \
  CFLAGS="-Wno-error=array-bounds" \
  CPPFLAGS="-I$NUMACTL_ROOT/include" \
  LDFLAGS="-L$NUMACTL_ROOT/lib"

%build
make %{makeprocesses} 

%install
make install

# remove pkg-config to avoid rpm-generated dependency on /usr/bin/pkg-config
rm -rf %{i}/lib/pkgconfig

# remove the libtool library files
rm -f %{i}/lib/lib*.la
rm -f %{i}/lib/ucx/lib*.la

# remove the UCX examples
rm -rf %{i}/share/ucx/examples

%post
%{relocateConfig}lib/cmake/ucx/*.cmake
