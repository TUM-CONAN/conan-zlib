from conans import ConanFile
import os
from conans.tools import download, unzip
from conans import CMake


class ZlibConan(ConanFile):
    name = "zlib"
    version = "1.2.12"
    ZIP_FOLDER_NAME = "zlib-%s" % version
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = ["CMakeLists.txt", "FindZLIB.cmake"]
    url="http://github.com/ulricheck/conan-zlib"
    license="http://www.zlib.net/zlib_license.html"
    description="A Massively Spiffy Yet Delicately Unobtrusive Compression Library (Also Free, Not to Mention Unencumbered by Patents)"
    
    def config(self):
        del self.settings.compiler.libcxx 

    def source(self):
        zip_name = "zlib-%s.tar.gz" % self.version
        download("http://downloads.sourceforge.net/project/libpng/zlib/%s/%s" % (self.version, zip_name), zip_name)
        unzip(zip_name)
        os.unlink(zip_name)
        os.rename(self.ZIP_FOLDER_NAME, "sources")

    def build(self):
        """ Define your project building. You decide the way of building it
            to reuse it later in any other project.
        """
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        """ Define your conan structure: headers, libs, bins and data. After building your
            project, this method is called to create a defined structure:
        """
        # Copy findZLIB.cmake to package
        self.copy("FindZLIB.cmake", ".", ".")
        
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
