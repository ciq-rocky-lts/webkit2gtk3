## NOTE: Lots of files in various subdirectories have the same name (such as
## "LICENSE") so this short macro allows us to distinguish them by using their
## directory names (from the source tree) as prefixes for the files.
%global add_to_license_files() \
        mkdir -p _license_files ; \
        cp -p %1 _license_files/$(echo '%1' | sed -e 's!/!.!g')

Name:           webkit2gtk3
Version:        2.38.5
Release:        2%{?dist}.6
Summary:        GTK Web content engine library

License:        LGPLv2
URL:            http://www.webkitgtk.org/
Source0:        http://webkitgtk.org/releases/webkitgtk-%{version}.tar.xz
Source1:        https://webkitgtk.org/releases/webkitgtk-%{version}.tar.xz.asc
# Use the keys from https://webkitgtk.org/verifying.html
# $ gpg --import aperez.key carlosgc.key
# $ gpg --export --export-options export-minimal D7FCF61CF9A2DEAB31D81BD3F3D322D0EC4582C3 5AA3BC334FD7E3369E7C77B291C559DBE4C9123B > webkitgtk-keys.gpg
Source2:        webkitgtk-keys.gpg

# https://bugs.webkit.org/show_bug.cgi?id=193749
Patch0:         evolution-shared-secondary-process.patch

# https://bugs.webkit.org/show_bug.cgi?id=235367
Patch1:         icu60.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=2209208
Patch2:         CVE-2023-28204.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=2185745
Patch3:         CVE-2023-28205.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=2209214
Patch4:         CVE-2023-32373.patch
Patch5:         CVE-2023-42917.patch

BuildRequires:  bison
BuildRequires:  cmake
BuildRequires:  flex
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  git
BuildRequires:  gperf
BuildRequires:  hyphen-devel
BuildRequires:  libatomic
BuildRequires:  ninja-build
BuildRequires:  perl(English)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(JSON::PP)
BuildRequires:  python3
BuildRequires:  ruby
BuildRequires:  rubygem-json
BuildRequires:  rubygems

BuildRequires:  pkgconfig(atspi-2)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(egl)
%ifarch aarch64 s390x
# On aarch64 and s390x enchant-2 is not available (gnome-less)
BuildRequires:  pkgconfig(enchant)
%else
BuildRequires:  pkgconfig(enchant-2)
%endif
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(libopenjp2)
BuildRequires:  pkgconfig(libpcre)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libseccomp)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libtasn1)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libwoff2dec)
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(upower-glib)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wpe-1.0)
BuildRequires:  pkgconfig(wpebackend-fdo-1.0)
BuildRequires:  pkgconfig(xt)

# If Geoclue is not running, the geolocation API will not work.
Recommends:     geoclue2

# Needed for various GStreamer elements.
Recommends:     gstreamer1-plugins-bad-free
Recommends:     gstreamer1-plugins-good

# Obsolete libwebkit2gtk from the webkitgtk3 package
Obsoletes:      libwebkit2gtk < 2.5.0
Provides:       libwebkit2gtk = %{version}-%{release}

# This package was renamed, so obsolete the old webkitgtk4 package
Obsoletes:      webkitgtk4 < %{version}-%{release}
Provides:       webkitgtk4 = %{version}-%{release}

# GTK+ 2 plugins support was removed in 2.25.3
Obsoletes:      webkit2gtk3-plugin-process-gtk2 < %{version}-%{release}
Provides:       webkit2gtk3-plugin-process-gtk2 = %{version}-%{release}
Obsoletes:      webkitgtk4-plugin-process-gtk2 < %{version}-%{release}
Provides:       webkitgtk4-plugin-process-gtk2 = %{version}-%{release}

# Don't build documentation anymore to avoid gi-docgen dependency
Obsoletes:      webkit2gtk3-doc < %{version}-%{release}
Provides:       webkit2gtk3-doc = %{version}-%{release}

# We're supposed to specify versions here, but these libraries don't do
# normal releases. Accordingly, they're not suitable to be system libs.
Provides:       bundled(angle)
Provides:       bundled(xdgmime)

# Require the jsc subpackage
Requires:       %{name}-jsc%{?_isa} = %{version}-%{release}

# Filter out provides for private libraries
%global __provides_exclude_from ^%{_libdir}/webkit2gtk-4\\.0/.*\\.so$

%description
WebKitGTK is the port of the portable web rendering engine WebKit to the
GTK platform.

This package contains WebKit2 based WebKitGTK for GTK 3.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-jsc%{?_isa} = %{version}-%{release}
Requires:       %{name}-jsc-devel%{?_isa} = %{version}-%{release}
Obsoletes:      webkitgtk4-devel < %{version}-%{release}
Provides:       webkitgtk4-devel = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries, build data, and header
files for developing applications that use %{name}.

%package        jsc
Summary:        JavaScript engine from %{name}
Obsoletes:      webkitgtk4-jsc < %{version}-%{release}
Provides:       webkitgtk4-jsc = %{version}-%{release}

%description    jsc
This package contains JavaScript engine from %{name}.

%package        jsc-devel
Summary:        Development files for JavaScript engine from %{name}
Requires:       %{name}-jsc%{?_isa} = %{version}-%{release}
Obsoletes:      webkitgtk4-jsc-devel < %{version}-%{release}
Provides:       webkitgtk4-jsc-devel = %{version}-%{release}

%description    jsc-devel
The %{name}-jsc-devel package contains libraries, build data, and header
files for developing applications that use JavaScript engine from %{name}.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1 -n webkitgtk-%{version} -S git

# Remove bundled libraries
rm -rf Source/ThirdParty/gtest/
rm -rf Source/ThirdParty/qunit/

%build
# Increase the DIE limit so our debuginfo packages could be size optimized.
# Decreases the size for x86_64 from ~5G to ~1.1G.
# https://bugzilla.redhat.com/show_bug.cgi?id=1456261
%global _dwz_max_die_limit 250000000
# The _dwz_max_die_limit is being overridden by the arch specific ones from the
# redhat-rpm-config so we need to set the arch specific ones as well - now it
# is only needed for x86_64.
%global _dwz_max_die_limit_x86_64 250000000

# Decrease debuginfo even on ix86 because of:
# https://bugs.webkit.org/show_bug.cgi?id=140176
%ifarch s390x %{arm} %{ix86} %{power64} %{mips}
# Decrease debuginfo verbosity to reduce memory consumption even more
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')
%endif

# bmalloc and JIT are disabled on aarch64 only in RHEL because of the nonstandard
# page size that's causing problems there. WebKit's build system sets appropriate
# defaults for all other architectures, and all other distros except RHEL.
mkdir -p %{_target_platform}
pushd %{_target_platform}
%cmake \
  -GNinja \
  -DPORT=GTK \
  -DCMAKE_BUILD_TYPE=Release \
  -DENABLE_JIT=OFF \
  -DENABLE_BUBBLEWRAP_SANDBOX=OFF \
  -DUSE_SOUP2=ON \
  -DENABLE_DOCUMENTATION=OFF \
  -DENABLE_GAMEPAD=OFF \
%if 0%{?rhel}
%ifarch aarch64
  -DUSE_64KB_PAGE_BLOCK=ON \
%endif
%endif
  ..
popd

# Show the build time in the status
export NINJA_STATUS="[%f/%t][%e] "
%ninja_build -C %{_target_platform}

%install
%ninja_install -C %{_target_platform}

%find_lang WebKit2GTK-4.0

# Finally, copy over and rename various files for %%license inclusion
%add_to_license_files Source/JavaScriptCore/COPYING.LIB
%add_to_license_files Source/ThirdParty/ANGLE/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/src/common/third_party/smhasher/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/src/third_party/libXNVCtrl/LICENSE
%add_to_license_files Source/WebCore/LICENSE-APPLE
%add_to_license_files Source/WebCore/LICENSE-LGPL-2
%add_to_license_files Source/WebCore/LICENSE-LGPL-2.1
%add_to_license_files Source/WebInspectorUI/UserInterface/External/CodeMirror/LICENSE
%add_to_license_files Source/WebInspectorUI/UserInterface/External/Esprima/LICENSE
%add_to_license_files Source/WebInspectorUI/UserInterface/External/three.js/LICENSE
%add_to_license_files Source/WTF/icu/LICENSE
%add_to_license_files Source/WTF/wtf/dtoa/COPYING
%add_to_license_files Source/WTF/wtf/dtoa/LICENSE

%files -f WebKit2GTK-4.0.lang
%license _license_files/*ThirdParty*
%license _license_files/*WebCore*
%license _license_files/*WebInspectorUI*
%license _license_files/*WTF*
%{_libdir}/libwebkit2gtk-4.0.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/WebKit2-4.0.typelib
%{_libdir}/girepository-1.0/WebKit2WebExtension-4.0.typelib
%{_libdir}/webkit2gtk-4.0/
%{_libexecdir}/webkit2gtk-4.0/
%exclude %{_libexecdir}/webkit2gtk-4.0/MiniBrowser
%exclude %{_libexecdir}/webkit2gtk-4.0/jsc
%{_bindir}/WebKitWebDriver

%files devel
%{_libexecdir}/webkit2gtk-4.0/MiniBrowser
%{_includedir}/webkitgtk-4.0/
%exclude %{_includedir}/webkitgtk-4.0/JavaScriptCore
%exclude %{_includedir}/webkitgtk-4.0/jsc
%{_libdir}/libwebkit2gtk-4.0.so
%{_libdir}/pkgconfig/webkit2gtk-4.0.pc
%{_libdir}/pkgconfig/webkit2gtk-web-extension-4.0.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/WebKit2-4.0.gir
%{_datadir}/gir-1.0/WebKit2WebExtension-4.0.gir

%files jsc
%license _license_files/*JavaScriptCore*
%{_libdir}/libjavascriptcoregtk-4.0.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/JavaScriptCore-4.0.typelib

%files jsc-devel
%{_libexecdir}/webkit2gtk-4.0/jsc
%dir %{_includedir}/webkitgtk-4.0
%{_includedir}/webkitgtk-4.0/JavaScriptCore/
%{_includedir}/webkitgtk-4.0/jsc/
%{_libdir}/libjavascriptcoregtk-4.0.so
%{_libdir}/pkgconfig/javascriptcoregtk-4.0.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/JavaScriptCore-4.0.gir

%changelog
* Tue Jul 11 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.38.5-1.5
- Disable JIT
  Resolves: #2218789
  Resolves: #2218799

* Thu May 25 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.38.5-1.4
- Add patch for CVE-2023-28204
  Resolves: #2209744
- Add patch for CVE-2023-32373
  Resolves: #2209727

* Fri Apr 14 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.38.5-1.3
- Restore libwpe and wpebackend-fdo dependencies
  Related: #2185741 (sort of)

* Wed Apr 12 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.38.5-1.2
- Disable libwpe and wpebackend-fdo dependencies
  Related: #2185741 (sort of)

* Tue Apr 11 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.38.5-1.1
- Add patch for CVE-2023-28205
  Resolves: #2185741

* Wed Feb 15 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.38.5-1
- Update to 2.38.5
  Related: #2127468

* Thu Feb 02 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.38.4-1
- Update to 2.38.4
  Related: #2127468

* Thu Dec 22 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.38.3-1
- Update to 2.38.3
  Related: #2127468

* Fri Nov 04 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.38.2-1
- Update to 2.38.2
  Related: #2127468

* Wed Nov 02 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.38.1-2
- Fix crashes on aarch64
  Enable WPE renderer
  Related: #2127468

* Thu Oct 27 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.38.1-1
- Update to 2.38.1
  Related: #2127468

* Wed Aug 24 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.36.7-1
- Update to 2.36.7
  Related: #2061994

* Tue Aug 09 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.36.6-1
- Update to 2.36.6
  Related: #2061994

* Tue Aug 02 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.36.5-2
- Fix Eclipse after update to 2.36.5
  Related: #2061994

* Thu Jul 28 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.36.5-1
- Update to 2.36.5
  Related: #2061994
  Resolves: #2099334

* Tue Jul 05 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.36.4-1
- Update to 2.36.4
  Related: #2061994

* Thu Jun 02 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.36.3-1
- Update to 2.36.3
- Related: #2061994
- Resolves: #2092748

* Wed May 18 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.36.2-1
- Update to 2.36.2
  Related: #2061994

* Thu Apr 21 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.36.1-1
- Update to 2.36.1
  Related: #2061994
- Resolves: #2075492
- Resolves: #2075494
- Resolves: #2075496

* Thu Feb 17 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.34.6-1
- Update to 2.34.6
  Related: #1985042

* Wed Feb 09 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.34.5-1
- Update to 2.34.5
- Related: #1985042

* Fri Jan 21 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.34.4-1
- Update to 2.34.4
- Resolves: #1985042

* Tue Sep 28 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.32.4-1
- Update to 2.32.4
- Related: #1985042
- Resolves: #2006429

* Fri Jul 23 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.32.3-1
- Update to 2.32.3
- Related: #1937416

* Tue Jul 13 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.32.2-1
- Update to 2.32.2
- Related: #1937416

* Mon May 10 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.32.1-1
- Update to 2.32.1
- Related: #1937416

* Fri Apr 30 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.32.0-1
- Update to 2.32.0
- Related: #1937416

* Tue Dec 15 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.30.4-1
- Update to 2.30.4
- Related: #1883304

* Wed Nov 25 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.30.3-1
- Update to 2.30.3
- Related: #1883304

* Thu Oct 29 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.30.2-2
- Try to fix coverity build by disabling docs (thanks to Kamil Dudka <kdudka@redhat.com>!)
- Related: #1883304

* Mon Oct 26 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.30.2-1
- Update to 2.30.2
- Related: #1883304

* Tue Oct 20 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.30.1-1
- Update to 2.30.1
- Related: #1883304

* Mon Aug 03 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.28.4-1
- Update to 2.28.4
- Related: #1817143

* Thu May 21 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.28.2-2
- Related: rhbz#1817143 Properly remove webkit2gtk3-plugin-process-gtk2 package

* Thu May 14 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.28.2-1
- Resolves: rhbz#1817143 Update to 2.28.2

* Mon Oct 14 2019 Eike Rathke <erack@redhat.com> - 2.24.4-3
- Related: rhbz#1748890 Bump NVR

* Fri Sep 27 2019 Eike Rathke <erack@redhat.com> - 2.24.4-1
- Resolves: rhbz#1748890 Update to 2.24.4

* Tue Jul 09 2019 Eike Rathke <erack@redhat.com> - 2.24.3-1
- Resolves: rhbz#1728277 Update to 2.24.3

* Wed May 22 2019 Eike Rathke <erack@redhat.com> - 2.24.2-2
- Related: rhbz#1696708 Use enchant instead of enchant-2 on aarch64 and s390x

* Tue May 21 2019 Eike Rathke <erack@redhat.com> - 2.24.2-1
- Resolves: rhbz#1696708 Rebase to 2.24.2
- Resolves: rhbz#1592271 Switch to Python 3 for build

* Tue Feb 12 2019 Eike Rathke <erack@redhat.com> - 2.22.6-1
- Resolves: rhbz#1676489 Update to 2.22.6

* Fri Jan 25 2019 Eike Rathke <erack@redhat.com> - 2.22.5-2
- Resolves: rhbz#1666984 Fix gigacage

* Tue Dec 18 2018 Eike Rathke <erack@redhat.com> - 2.22.5-1
- Update to 2.22.5

* Tue Oct 30 2018 Tomas Popela <tpopela@redhat.com> - 2.22.3-1
- Update to 2.22.3
- Resolves: rhbz#1641009

* Mon Sep 24 2018 Tomas Popela <tpopela@redhat.com> - 2.22.2-1
- Update to 2.22.2
- Resolves: rhbz#1625602

* Thu Sep 20 2018 Tomas Popela <tpopela@redhat.com> - 2.22.1-1
- Update to 2.22.1
- Resolves: rhbz#1625602

* Tue Sep 11 2018 Tomas Popela <tpopela@redhat.com> - 2.22.0-2
- Backport patches from RHEL 7
- Resolves: rhbz#1625602

* Wed Sep 05 2018 Tomas Popela <tpopela@redhat.com> - 2.22.0-1
- Update to 2.22.0
- Resolves: rhbz#1625602

* Tue Jul 17 2018 Tomas Popela <tpopela@redhat.com> - 2.20.3-3
- Update the python2 patch

* Mon Jun 18 2018 Tomas Popela <tpopela@redhat.com> - 2.20.3-3
- Export the python2 env variable
- Resolves: rhbz#1592264

* Mon Jun 11 2018 Tomas Popela <tpopela@redhat.com> - 2.20.3-1
- Update to 2.20.3

* Thu May 24 2018 Tomas Popela <tpopela@redhat.com> - 2.20.2-4
- Explicitly specify python2 over python and add python2 to BR

* Tue May 22 2018 Tomas Popela <tpopela@redhat.com> - 2.20.2-3
- aarch64 on RHEL 8 does have a 64kb page size
- Resolves: rhbz#1578576

* Tue May 22 2018 Tomas Popela <tpopela@redhat.com> - 2.20.2-2
- Temporary disable JIT and BMalloc on aarch64 due to Gigacage problems
- Resolves: rhbz#1578576

* Tue May 15 2018 Tomas Popela <tpopela@redhat.com> - 2.20.2-1
- Update to 2.20.2
- Resolves: rhbz#1577388

* Tue Apr 10 2018 Tomas Popela <tpopela@redhat.com> - 2.20.1-1
- Update to 2.20.1

* Mon Mar 12 2018 Kalev Lember <klember@redhat.com> - 2.20.0-2
- Bump webkitgtk4 obsoletes versions

* Mon Mar 12 2018 Tomas Popela <tpopela@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Tue Mar 06 2018 Tomas Popela <tpopela@redhat.com> - 2.19.92-1
- Update to 2.19.92

* Wed Feb 21 2018 Tomas Popela <tpopela@redhat.com> - 2.19.91-1
- Update to 2.19.91

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.19.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Tomas Popela <tpopela@redhat.com> - 2.19.90-1
- Update to 2.19.90

* Tue Jan 30 2018 Tomas Popela <tpopela@redhat.com> - 2.19.6-3
- Remove obsoleted ldconfig scriptlets

* Wed Jan 17 2018 Tomas Popela <tpopela@redhat.com> - 2.19.6-1
- Update to 2.19.6

* Thu Jan 11 2018 Tomas Popela <tpopela@redhat.com> - 2.19.5-2
- This package was formerly named webkitgtk4
