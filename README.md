# Mobile Wheels

## What is this list?

[This site](http://beeware.org/mobile-wheels/) shows the [Android](https://docs.python.org/3/using/android.html) and [iOS](https://docs.python.org/3/using/ios.html) support of the top 360 most-downloaded binary packages on [PyPI](https://pypi.org/), i.e., packages that need to be compiled for each architecture and operating system:

* Dark green packages with a ✓ icon offer wheels compiled for Android or iOS.
* Light green packages with a 🐍 icon offer pure Python wheels, but no wheels compiled for Android or iOS (yet!). The pure Python wheels will probably work on mobile, but may have lower performance.
* Orange packages with a ✗ icon are not available for Android or iOS (yet!).
* Packages that only offer pure Python wheels are not listed. These packages will probably work on mobile already.

Packages that are known to be deprecated are not included (for example, pycrypto). If your package is incorrectly listed, or you see any other problem with this page, please create an issue or a pull request.

## My package is orange. What can I do?
The recommended way to build mobile-compatible wheels is to use [cibuildwheel](https://cibuildwheel.pypa.io/en/stable/). Despite the name, this tool is not limited to CI environments; it can be run locally on macOS and Linux machines. For more details, see the Android and iOS sections of the [cibuildwheel documentation](https://cibuildwheel.pypa.io/en/stable/platforms/).

## Thanks
This is a derivative work of [Free-Threaded Wheels](https://hugovk.github.io/free-threaded-wheels) and [Python Wheels](https://pythonwheels.com/). The top 360 list comes from [Top PyPI Packages](https://hugovk.github.io/top-pypi-packages/).
