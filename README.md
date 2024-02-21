# PackageToRojo
Simple script that converts an rbxmx into a Rojo project while respecting PackageLinks.

Will descend down the instance tree of an .rbxmx and place PackageLinks, ModuleScripts, and Folders respectively until another instance type is found.
At this point, it and its descendants will be converted into an rbxmx.


## Getting Started
Ensure that you have Rojo installed, and that it is on your system PATH.

Ensure that your Rojo version is 7.4.0. (Cannot guarantee that it will work for other versions.)

Install the `xmlx` Python library. (Used to parse the rbxmx files)

Create an `input` folder in this directory.
Place .rbxmx files into the `input` folder.
Run the script.

Voila! Your projects should be generated in a new folder called `output`.