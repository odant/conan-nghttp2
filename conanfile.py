from conans import ConanFile, CMake, tools
from conans.errors import ConanException
import os, glob


def get_safe(options, name):
    try:
        return getattr(options, name, None)
    except ConanException:
        return None


class Nghttp2Conan(ConanFile):
    name = "nghttp2"
    version = "1.30.90"
    license = "MIT"
    description = "nghttp2 is an implementation of HTTP/2 and its header compression algorithm HPACK in C"
    url = "https://github.com/odant/conan-nghttp2"
    settings = {
        "os": ["Windows", "Linux"],
        "compiler": ["Visual Studio", "gcc"],
        "build_type": ["Debug", "Release"],
        "arch": ["x86_64", "x86"]
    }
    options = {
        "shared": [True],
        "fPIC": [True, False],
        "dll_sign": [True, False]
    }
    default_options = "shared=True", "fPIC=True", "dll_sign=True"
    generators = "cmake"
    exports_sources = "src/*", "CMakeLists.txt"
    no_copy_source = True
    build_policy = "missing"

    def configure(self):
        # Only C++11
        if self.settings.compiler.get_safe("libcxx") == "libstdc++":
            raise ConanException("This package is only compatible with libstdc++11")
        # Sign only shared on Windows
        if self.settings.os != "Windows" or not self.options.shared:
            del self.options.dll_sign

    def requirements(self):
        self.requires("openssl/[~=1.1.0g]@%s/testing" % self.user)
        self.requires("boost/[~=1.66.0]@%s/testing" % self.user)

    def build_requirements(self):
        self.build_requires("zlib/[~=1.2.11]@%s/stable" % self.user)
        if get_safe(self.options, "dll_sign"):
            self.build_requires("find_windows_signtool/[~=1.0]@%s/stable" % self.user)

    def build(self):
        cmake = CMake(self)
        #if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
        #    _win32_winnt = "0x0600" # Default Windows Vista
        #    toolset = str(self.settings.compiler.get_safe("toolset"))
        #    if toolset.endswith("_xp"):
        #        _win32_winnt = "0x0502" if self.settings.arch == "x86_64" else "0x0501"
        #    cmake.definitions["CMAKE_CXX_FLAGS:STRING"] = "/D WIN32 /D _WINDOWS /D_WIN32_WINNT=%s" % _win32_winnt
        #    cmake.definitions["CMAKE_C_FLAGS:STRING"] = "/D WIN32 /D _WINDOWS /D_WIN32_WINNT=%s" % _win32_winnt
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="src/src/includes")
        self.copy("*.h", dst="include", src="src/lib/includes")
        self.copy("*.lib", dst="lib", keep_path=False, excludes="*http-parser*")
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*nghttp2.pdb", dst="bin", keep_path=False)
        self.copy("*nghttp2d.pdb", dst="bin", keep_path=False)
        self.copy("*nghttp2_asio.pdb", dst="bin", keep_path=False)
        self.copy("*nghttp2_asiod.pdb", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False, excludes="*http-parser*")
        # Sign DLL
        if get_safe(self.options, "dll_sign"):
            with tools.pythonpath(self):
                from find_windows_signtool import find_signtool
                signtool = '"' + find_signtool(str(self.settings.arch)) + '"'
                params =  "sign /a /t http://timestamp.verisign.com/scripts/timestamp.dll"
                pattern = os.path.join(self.package_folder, "bin", "*.dll")
                for fpath in glob.glob(pattern):
                    self.output.info("Sign %s" % fpath)
                    self.run("%s %s %s" %(signtool, params, fpath))
        
    def package_info(self):
        self.cpp_info.libs = ["nghttp2", "nghttp2_asio"]

        if (self.settings.os == "Windows" and self.settings.compiler == "Visual Studio"):
            self.cpp_info.defines = ["NOMINMAX", "ssize_t=int"]
            if self.settings.build_type == "Debug":
                self.cpp_info.libs[0] += "d"
                self.cpp_info.libs[1] += "d"

