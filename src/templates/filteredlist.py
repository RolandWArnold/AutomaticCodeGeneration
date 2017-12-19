#!/usr/bin/env python

import os.path
from template import LType

class FilteredList(LType):
    def write(self, parent_wizard=None, parent_screen=None, echo=True):
        package = self.packageName(parent_wizard.name)
        screenid = self.screenID(self.ctype, self.name, parent_wizard.name)
        title = self.properties.get("title", parent_wizard.properties.get("title", ""))
        storagekey = self.properties["write"]
        conditional = ""
        if "back_if_value" in self.properties:
            con = self.properties["back_if_value"].split()
            con[0] = con[0].lstrip("{")
            con[1] = con[1].rstrip("}")
            target_ctype, target_name = tuple(con[2].split(":"))
            target_id = self.screenID(target_ctype, target_name, parent_wizard.name)
            wizardid = "wizard.getWizardID()" if parent_wizard.name == con[0] else self.wizardID(con[0])
            conditional = '\n\n\t\tthis.setConditional(%s, "%s", %s);' % (wizardid, con[1], target_id)
        order = ", true" if self.properties.get("order") == "numberFirst" else ""
        dict = {"name" : self.name, "screenid" : screenid, "storagekey" : storagekey,
                "title" : title, "package" : package, "conditional" : conditional, "order" : order}
        path = os.path.join("wizard", self.packageName(parent_wizard.name), "%s.java" % self.getOwnClassName())
        self.write_file(path, """package genericbiz.wizard.%(package)s;

import genericbiz.extensions.GenericBizFilteredList;
import genericbiz.extensions.GenericBizWizard;
import genericbiz.id.*;

public class %(name)sFilteredList extends GenericBizFilteredList {
	public %(name)sFilteredList(GenericBizWizard wizard) {
		super(wizard, %(screenid)s,
					"%(title)s", ""/*removed for copyright: get value for: \"%(name)s\" */, "%(storagekey)s"%(order)s);%(conditional)s
	}
}
""" % dict, echo)
