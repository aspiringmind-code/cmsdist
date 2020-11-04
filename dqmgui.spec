### RPM cms dqmgui V1_6.22
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

%define tag df93a2c4cfa9e3ae494340c3d2f2c197ff3f367a
%define branch dqm-gui-based-on-eos-files
%define github_user andrius-k
Source: git+https://github.com/%{github_user}/cmssw.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
Requires: root boost python3
Requires: py3-aiohttp py3-aiosqlite py3-async-lru

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build ; mkdir -p ../build/DQMServices
cp -r DQMServices/DQMGUI ../build/DQMServices
cd ../build

CFLAGS="--std=c++1z -O2 -fPIC -DGNU_GCC -D_GNU_SOURCE -D_GLIBCXX_USE_CXX11_ABI=0 -DBOOST_DISABLE_ASSERTS"
LDFLAGS="-Wl,-E -Wl,--hash-style=gnu"
ROOTLIBS="-lCore -lRIO -lNet -lHist -lMatrix -lThread -lTree -lMathCore -lGpad -lGraf3d -lGraf -lPhysics -lPostscript -lASImage"
OTHERLIBS="-ldl -ljpeg -lpng"
INCLUDE="-I. -I${ROOT_ROOT}/include -I${BOOST_ROOT}/include"
LIBDIR="-L. -L$(echo ${LD_LIBRARY_PATH} | sed 's|:| -L|g')"
g++ -c $CFLAGS ${INCLUDE} DQMServices/DQMGUI/src/DQMRenderPlugin.cc
g++ -c $CFLAGS ${INCLUDE} DQMServices/DQMGUI/bin/render.cc
g++ --shared -Wl,-E -Wl,-z,defs ${LDFLAGS} ${LIBDIR} ${ROOTLIBS} ${OTHERLIBS} DQMRenderPlugin.o -o librenderplugin.so
g++                             ${LDFLAGS} ${LIBDIR} ${ROOTLIBS} ${OTHERLIBS} render.o -o render  -lrenderplugin -lstdc++fs

%install
mkdir -p %i/bin %i/lib %i/${PYTHON3_LIB_SITE_PACKAGES}
cd ../build
cp -r DQMServices %{i}/
cp render %i/bin/
cp librenderplugin.so %i/lib
rm -rf %i/${PYTHON3_LIB_SITE_PACKAGES}
ln -s ../../DQMServices/DQMGUI/python %i/${PYTHON3_LIB_SITE_PACKAGES}
