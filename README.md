# PackageToRojo

Simple script that converts an rbxmx into a Rojo project while respecting PackageLinks.

Will descend down the instance tree of an .rbxmx and place PackageLinks, ModuleScripts, and Folders respectively until another instance type is found.
At this point, it and its descendants will be converted into an rbxmx.

## Getting Started

Ensure that you have Rojo installed, and that it is on your system PATH.

Ensure that your Rojo version is 7.4.0 or 7.4.1. (Cannot guarantee that it will work for other versions.)

Ensure that you have the package dependencies from the Pipfile.

Create an `input` folder in this directory.
Place .rbxmx files into the `input` folder.
Run `PackageToRojo.py`.

Voila! Your projects should be generated in a new folder called `output`.
