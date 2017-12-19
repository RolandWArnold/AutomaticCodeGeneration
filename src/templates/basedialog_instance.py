#!/usr/bin/env python

import os.path
from template import LType

class BaseDialogInstance(LType):
    def write(self, parent_wizard=None, parent_screen=None, echo=True):
        package = self.packageName(parent_wizard.name)
        screenid = self.screenID(self.ctype, self.name, parent_wizard.name)
        classname =  self.getOwnClassName()
        classbasename = self.getClassName("BaseDialog", self.name)
        importset = set(["import genericbiz.extensions.GenericBizWizard;", "import genericbiz.id.ScreenID;", "import genericbiz.sharedscreens.%s;" % classbasename])
        [importset.update(child.getImports()) for child in self.children]
        imports = "\n".join(sorted(list(importset)))
        title = self.properties.get("title", parent_wizard.properties.get("title", ""))
        title = ', "%s"' % title if title else ""
        noback = ", true" if self.properties.get("movement", "") == "noback" else ""
        implementedmethods = ""
        if "reply" in self.properties:
            ret, rest = self.properties["reply"].split(":")
            meth, val = rest.split(" ", 1)
            implementedmethods = '\n\n\tprotected %s %s() {\n\t\treturn "%s";\n\t}' % (ret, meth, val)
        dict = {"package" : package, "classname" : classname, "classbasename" : classbasename, "imports" : imports, "noback" : noback,
        "implementedmethods" : implementedmethods, "title" : title, "screenid" : screenid}
        self.write_file(os.path.join("wizard", package, "%s.java" % classname), """package genericbiz.wizard.%(package)s;

%(imports)s

public class %(classname)s extends %(classbasename)s {
	public %(classname)s(GenericBizWizard wizard) {
		super(wizard, %(screenid)s%(title)s%(noback)s);
	}%(implementedmethods)s
}
""" % dict, echo)
