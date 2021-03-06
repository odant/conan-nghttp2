# nghttp2 Conan package
# Dmitriy Vetutnev, Odant, 2018


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
        "arch": ["x86_64", "x86", "mips"]
    }
    options = {
        "shared": [True],
        "fPIC": [True, False],
        "dll_sign": [True, False]
    }
    default_options = "shared=True", "fPIC=True", "dll_sign=True"
    generators = "cmake"
    exports_sources = "src/*", "CMakeLists.txt", "FindNGHTTP2.cmake", "version.patch"
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
        self.requires("openssl/1.1.0h@%s/stable" % self.user)
        self.requires("boost/[>=1.54.0]@%s/stable" % self.user)

    def build_requirements(self):
        self.build_requires("zlib/[>=1.2.3]@%s/stable" % self.user)
        #
        if get_safe(self.options, "dll_sign"):
            self.build_requires("windows_signtool/[~=1.0]@%s/stable" % self.user)

    def source(self):
        tools.patch(patch_file="version.patch")

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
        self.copy("FindNGHTTP2.cmake", dst=".", src=".")
        # Headers
        self.copy("*.h", dst="include", src="src/src/includes")
        self.copy("*.h", dst="include", src="src/lib/includes")
        # Libraries
        self.copy("*.lib", dst="lib", keep_path=False, excludes="*http-parser*")
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False, excludes="*http-parser*")
        # PDB
        self.copy("*nghttp2.pdb", dst="bin", keep_path=False)
        self.copy("*nghttp2d.pdb", dst="bin", keep_path=False)
        self.copy("*nghttp264.pdb", dst="bin", keep_path=False)
        self.copy("*nghttp264d.pdb", dst="bin", keep_path=False)
        self.copy("*nghttp2_asio.pdb", dst="bin", keep_path=False)
        self.copy("*nghttp2_asiod.pdb", dst="bin", keep_path=False)
        self.copy("*nghttp2_asio64.pdb", dst="bin", keep_path=False)
        self.copy("*nghttp2_asio64d.pdb", dst="bin", keep_path=False)
        # Sign DLL
        if get_safe(self.options, "dll_sign"):
            import windows_signtool
            pattern = os.path.join(self.package_folder, "bin", "*.dll")
            for fpath in glob.glob(pattern):
                fpath = fpath.replace("\\", "/")
                for alg in ["sha1", "sha256"]:
                    is_timestamp = True if self.settings.build_type == "Release" else False
                    cmd = windows_signtool.get_sign_command(fpath, digest_algorithm=alg, timestamp=is_timestamp)
                    self.output.info("Sign %s" % fpath)
                    self.run(cmd)
        
    def package_info(self):
        # Libraries
        self.cpp_info.libs = ["nghttp2", "nghttp2_asio"]
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            if self.settings.arch == "x86_64":
                self.cpp_info.libs[0] += "64"
                self.cpp_info.libs[1] += "64"
            if self.settings.build_type == "Debug":
                self.cpp_info.libs[0] += "d"
                self.cpp_info.libs[1] += "d"
        # Defines
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            self.cpp_info.defines = ["NOMINMAX", "ssize_t=int"]
