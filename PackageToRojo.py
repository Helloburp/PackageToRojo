# Converts an rbxmx into a Rojo project while respecting packagelinks.

# NOTES:
# Will descend down the tree and place packagelinks and modulescripts respectively
#   until a non-modulescript instance is found.
#   At this point, it and its descendants will be converted into an rbxmx.
# 
# Each ModuleScript will be given a meta file that will set its GUID for package parity.

import copy, subprocess, json, shutil, glob
from pathlib import Path

import src.PkgToRojoData as PkgToRojoData
from src.PkgToRojoParse import ET, get_packagelink_properties, get_module_properties, get_module_source, get_property_from_item_elem

parser = ET.XMLParser(strip_cdata=False)


#
# subprocess
#

def cmd_run(command, cwd=None, wait=True):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=cwd)
    if wait:
        process.wait()
    return process


#
# qualifiers
#

def should_elem_be_rbxmx(elem: ET.ElementBase):
    return not (elem.get("class") in PkgToRojoData.non_rbxmx_classes.keys())


def does_elem_have_children(elem: ET.ElementBase):
    return len(elem.findall("Item")) > 0


#
# constructors
#

# script_name is the filename of the script WITHIN the path, WITHOUT the extension of .luau
def new_script_meta_json_in_folder(path: str, script_name: str, elem: ET.ElementBase):
    with open(f"{path}/{script_name}.meta.json","w") as file:
        meta = copy.deepcopy(PkgToRojoData.script_meta)
        meta["properties"] = get_module_properties(elem)
        json.dump(meta, file, indent=2)


# Creates a new script IN the path, and a meta.json file.
def new_leaf_script_in_folder(path: str, script_name: str, elem: ET.ElementBase):
    with open(f"{path}/{script_name}.luau", "w") as script:
        script.write(get_module_source(elem))
    
    # Currently disabled because it unfortunately doesn't fix the package commiting issue.
    # new_script_meta_json_in_folder(path, script_name, elem)


# Creates a new .model.json INSIDE the path representing a packagelink.
def new_packagelink_json_model_in_folder(path: str, elem: ET.ElementBase):
    with open(f"{path}/PackageLink.model.json","w") as file:
        model = copy.deepcopy(PkgToRojoData.packagelink_model)
        model["Properties"] = get_packagelink_properties(elem)
        json.dump(model, file, indent=2)
    


# Creates a new folder AT the path, then an init.luau inside, and a init.meta.json file.
def new_parent_script(path: str, elem: ET.ElementBase):
    new_folder(path)
    new_leaf_script_in_folder(path, "init", elem)


# Creates a new folder AT the path.
def new_folder(path: str, elem: ET.ElementBase | None = None):
    Path(path).mkdir(parents=True, exist_ok=True)


# Creates a new .rbxmx IN the path.
def new_rbxmx_in_folder(path: str, rbxmx_name: str, elems: list[ET.ElementBase]):
    root = ET.fromstring(PkgToRojoData.rbxmx_wrapper)
    for elem in elems:
        root.append(elem)

    rbxmx_path = f"{path}/{rbxmx_name}.rbxmx"

    with open(rbxmx_path,"w"):
        tree = ET.ElementTree(root)
        tree.write(rbxmx_path, encoding="utf-8")


#
# process
#
        

def sanitize_str(string: str):
    string = string.replace("/", "-")
    string = string.replace(".", "-")
    return string

def rojo_init(project_name, rbxmx_root: ET.ElementBase):

    def recurse(path: str, elem: ET.ElementBase):
        my_class = elem.get("class")
        my_name = sanitize_str(get_property_from_item_elem(elem, "Name"))
        deeper_path = f"{path}/{my_name}"

        if not my_class:
            return
        
        if should_elem_be_rbxmx(elem):
            new_rbxmx_in_folder(path, my_name, [elem])
            return
        
        if my_class == "ModuleScript":
            if not does_elem_have_children(elem):
                new_leaf_script_in_folder(path, my_name, elem)
                return
            else:
                new_parent_script(deeper_path, elem)
        elif my_class == "Folder":
            new_folder(deeper_path, elem)
        elif my_class == "PackageLink":
            new_packagelink_json_model_in_folder(path, elem)
            return
        
        for sub_elem in elem.findall("Item"):
            recurse(deeper_path, sub_elem)

    valid, root_module = validate_rbxmx_input(rbxmx_root)
    if not valid:
        raise(ValueError(f"{project_name} is invalid .rbxmx input."))
    
    new_folder("output")
    
    project_path = f"output/{project_name}"

    if Path(project_path).exists():
        shutil.rmtree(project_path)

    new_folder(project_path)


    cmd_run("rojo init", project_path)

    # Clear irrelevant children from default Rojo config
    shutil.rmtree(f"{project_path}/src/client")
    shutil.rmtree(f"{project_path}/src/shared")
    shutil.rmtree(f"{project_path}/src/server")

    # Project .json
    with open(f"{project_path}/default.project.json", "w") as file:
        my_settings = copy.deepcopy(PkgToRojoData.project_settings)
        my_settings["name"] = project_name
        json.dump(my_settings, file, indent=2)
    
    if root_module.get("class") == "ModuleScript":
        new_leaf_script_in_folder(f"{project_path}/src", "init", root_module)
    
    for item in root_module.findall("Item"):
        recurse(f"{project_path}/src", item)


# Ensures that the input rbxmx can be converted into a rojo project.
# It is only valid IF there is only one root instance, AND that instance is of a valid class.
def validate_rbxmx_input(root: ET.ElementBase):
    root_items = root.findall("Item")
    if len(root_items) > 1 or len(root_items) == 0:
        return False
    
    root_item = root_items[0]
    return not should_elem_be_rbxmx(root_item), root_items[0]


def run(file_path):
    file_name = Path(file_path).name

    if not Path(file_path).exists():
        print(f"{file_path} is not a valid .rbxmx file.")
        return
    
    i = file_name.find(".rbxmx")

    if i < 0 or i != len(file_name) - len(".rbxmx"):
        print("Not a valid .rbxmx file.")
        return
    
    project_name = file_name[0:i]
    
    with open(file_path, "r") as file:
        root = ET.fromstring(file.read(), parser)
        if not validate_rbxmx_input(root):
            print(".rbxmx exists, but its root is not a valid class.")
            return
        
        rojo_init(project_name, root)


def get_rbxmx_in_directory(dir: str):
    files = glob.glob(f"{dir}/*.rbxmx")
    return files


def run_input():
    new_folder("input")
    rbxmx_paths = get_rbxmx_in_directory("input")
    for rbxmx_path in rbxmx_paths:
        run(rbxmx_path)


run_input()