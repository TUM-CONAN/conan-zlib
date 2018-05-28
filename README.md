# conan-zlib

[Conan.io](https://conan.io) package for ZLIB library. 

## Add Remote

    $ conan remote add camposs "https://conan.campar.in.tum.de/api/conan/conan-camposs"

## For Users: Use this package

### Basic setup

    $ conan install zlib/1.2.11@camposs/stable
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    zlib/1.2.11@camposs/stable

    [options]
    zlib:shared=true # false
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    $ mkdir build && cd build && conan install .. 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.

## For Packagers: Publish this Package

The example below shows the commands used to publish to campar conan repository. To publish to your own conan respository (for example, after forking this git repository), you will need to change the commands below accordingly. 

## Build packages

    $ conan create . camposs/stable    

## Upload packages to server

    $ conan upload zlib/1.2.11@camposs/stable --all -r camposs    
