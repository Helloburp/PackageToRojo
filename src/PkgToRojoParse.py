
# import xml.etree.ElementTree as ET
import src.PkgToRojoData as PkgToRojoData
import lxml.etree as ET



def get_value_from_property_elem(elem: ET.ElementBase, type: str="string"):
    val = None
    if elem.text == None:
        for sub_elem in elem.iter():
            if sub_elem.text == None:
                continue
            val = sub_elem.text
    else:
        val = elem.text
    
    if val != None:
        if type == "int":
            val = int(val)
        elif type == "float":
            val = float(val)
        elif type == "bool":
            val = True if val == "true" else False
    
    return val


def get_property_from_item_elem(root_elem: ET.ElementBase, name, type: str="string"):
    properties = root_elem.find("Properties")
    for elem in properties.iter():
        property_name = elem.get("name")
        if property_name != name:
            continue

        return get_value_from_property_elem(elem, type)
    
    return None
    


def get_properties(root_elem: ET.ElementBase, target_properties: dict[str, str]):
    vals = {}

    properties = root_elem.find("Properties")
    for elem in properties.iter():
        property_name = elem.get("name")
        if not (property_name in target_properties.keys()):
            continue

        val = get_value_from_property_elem(elem, target_properties[property_name])

        if val != None:
            vals[property_name] = val
    
    return vals


def get_module_properties(elem):
    return get_properties(elem, PkgToRojoData.module_script_properties)


def get_packagelink_properties(elem: ET.ElementBase):
    return get_properties(elem, PkgToRojoData.packagelink_properties)

def get_module_source(elem: ET.ElementBase):
    source = get_property_from_item_elem(elem, "Source", "string")
    source = source if source else ""

    return source