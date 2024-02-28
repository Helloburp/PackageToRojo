

non_rbxmx_classes = {
    "PackageLink": True,
    "ModuleScript": True,
    "Script": True,
    "LocalScript": True,
    "Folder": True,
}

# The names of properties to to put in a meta json
client_script_properties = {
    "Disabled": "bool",
    # "ScriptGuid": "string",
}

server_script_properties = {
    "Disabled": "bool",
    "RunContext": "string"
}


packagelink_properties = {
    "AutoUpdate": "bool",
    "DefaultName": "string",
    "ModifiedState": "int",
    "PackageIdSerialize": "string",
    "VersionIdSerialize": "int",
}

project_settings = {
    "name": "ERROR",
    "tree": {
        "$path": "src",
    }
}


script_meta = {
    # FILLED BY SCRIPT: Properties of related module
    "properties": {}
}

packagelink_model = {
    "ClassName": "PackageLink",

    # FILLED BY SCRIPT: Properties of package link
    "Properties": {}
}


rbxmx_wrapper = '''<roblox xmlns:xmime="http://www.w3.org/2005/05/xmlmime" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.roblox.com/roblox.xsd" version="4">
	<Meta name="ExplicitAutoJoints">true</Meta>
	<External>null</External>
	<External>nil</External>
</roblox>
'''