from conans import ConanFile
import os
from conans.tools import download, unzip
from conans import CMake


class ZlibConan(ConanFile):
    name = "zlib"
    version = "1.2.11"
    ZIP_FOLDER_NAME = "zlib-%s" % version
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = ["CMakeLists.txt", "FindZLIB.cmake"]
    url="http://github.com/ulricheck/conan-recipies"
    license="http://www.zlib.net/zlib_license.html"
    description="A Massively Spiffy Yet Delicately Unobtrusive Compression Library (Also Free, Not to Mention Unencumbered by Patents)"
    
    def config(self):
        del self.settings.compiler.libcxx 

    def source(self):
        zip_name = "zlib-%s.tar.gz" % self.version
        download("http://downloads.sourceforge.net/project/libpng/zlib/%s/%s" % (self.version, zip_name), zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        """ Define your project building. You decide the way of building it
            to reuse it later in any other project.
        """
        defs = {}
        if self.options.shared:
            defs['BUILD_SHARED_LIBS'] = 'ON'
        cmake = CMake(self)
        cmake.configure(source_dir="./%s" % self.ZIP_FOLDER_NAME, build_dir="./_build", defs=defs)
        cmake.build()
        cmake.install()

    def package(self):
        """ Define your conan structure: headers, libs, bins and data. After building your
            project, this method is called to create a defined structure:
        """
        # Copy findZLIB.cmake to package
        self.copy("FindZLIB.cmake", ".", ".")
        
        # Copying zlib.h, zutil.h, zconf.h
        self.copy("*.h", "include", "%s" % (self.ZIP_FOLDER_NAME), keep_path=False)
        self.copy("*.h", "include", "%s" % ("_build"), keep_path=False)

        # Copying static and dynamic libs
        if self.settings.os == "Windows":
            if self.options.shared:
                self.copy(pattern="*.dll", dst="bin", src="_build", keep_path=False)
                self.copy(pattern="*zlibd.lib", dst="lib", src="_build", keep_path=False)
                self.copy(pattern="*zlib.lib", dst="lib", src="_build", keep_path=False)
                self.copy(pattern="*zlib.lib", dst="lib", src="_build", keep_path=False)
                self.copy(pattern="*zlib.dll.a", dst="lib", src="_build", keep_path=False)
            else:
                self.copy(pattern="*zlibstaticd.*", dst="lib", src="_build", keep_path=False)
                self.copy(pattern="*zlibstatic.*", dst="lib", src="_build", keep_path=False)
        else:
            if self.options.shared:
                if self.settings.os == "Macos":
                    self.copy(pattern="*.dylib", dst="lib", keep_path=False)
                else:
                    self.copy(pattern="*.so*", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
            else:
                self.copy(pattern="*.a", dst="lib", src="%s/_build" % self.ZIP_FOLDER_NAME, keep_path=False)
                self.copy(pattern="*.a", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            if self.options.shared:
                if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
                    self.cpp_info.libs = ['zlibd']
                else:
                    self.cpp_info.libs = ['zlib']
            else:
                if self.settings.build_type == "Debug" and  self.settings.compiler == "Visual Studio":
                    self.cpp_info.libs = ['zlibstaticd']
                else:
                    self.cpp_info.libs = ['zlibstatic']
        else:
            self.cpp_info.libs = ['z']
