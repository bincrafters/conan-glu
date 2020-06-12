from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration
import os


class GluConan(ConanFile):
    name = "glu"
    # version = "virtual"
    description = "Virtual package for GLU - the OpenGL Utility Library"
    topics = ("conan", "opengl", "gl", "glu", "utility")
    url = "https://github.com/bincrafters/conan-glu"
    homepage = "https://opengl.org"
    license = "None"  # TODO: Relax hooks about license attribute for virtual packages? How?

    # TODO: Add check if system_libs are installed if provider=system?
    # TODO: Write a test_package

    settings = {"os"}
    options = {
        "provider": ["system", "conan"],
    }
    default_options = {
        "provider": "system",
    }

    requires = ("opengl/system")

    def configure(self):
        if self.settings.os == "Windows" and self.options.provider != "system":
            # While we could just raise an error, this would make the consumption of this package much harder
            # And since the entire idea of this package is to abstract away OpenGL support
            # it is probably better to force the value of the option
            self.output.warning("On Windows only opengl:provider=system is supported! Forcing option")
            self.options.provider = "system"

        if self.settings.os == "Macos" and self.options.provider != "system":
            self.output.warning("On macOS only opengl:provider=system is supported! Forcing option")
            self.options.provider = "system"

    def system_requirements(self):
        if self.options.provider == "system":
            # Note: If you want to disable installation on your system
            # set CONAN_SYSREQUIRES_MODE to disabled
            if self.settings.os == "Linux" and tools.os_info.is_linux:
                if tools.os_info.with_apt or tools.os_info.with_yum:
                    installer = tools.SystemPackageTool()
                    packages = []
                    packages_apt = ["libglu1-mesa-dev"]
                    packages_yum = ["mesa-libGLU-devel"]

                    if tools.os_info.with_apt:
                        packages = packages_apt
                    elif tools.os_info.with_yum:
                        packages = packages_yum
                    for package in packages:
                        installer.install(package)

    def requirements(self):
        if self.options.provider == "conan":
            self.requires("mesa-glu/9.0.1@bincrafters/stable")
           
    def package_info(self):
        if self.options.provider == "system":
            if self.settings.os == "Windows":
                self.cpp_info.system_libs.append("glu32")
            if self.settings.os == "Macos":
                self.cpp_info.system_libs.extend(["GLU"])
            if self.settings.os == "Linux":
                self.cpp_info.system_libs.append("GLU")
