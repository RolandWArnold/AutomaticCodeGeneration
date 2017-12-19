#!/usr/bin/env python

import os.path
from template import LType

class BaseDialog(LType):
    def write(self, parent_wizard=None, parent_screen=None, echo=True):
        classname =  self.getOwnClassName()
        importset = set(["import genericbiz.extensions.GenericBizDialog;", "import genericbiz.extensions.GenericBizWizard;"])
        [importset.update(child.getImports()) for child in self.children]
        imports = "\n".join(sorted(list(importset)))
        declarations = "".join([child.getDecl() for child in self.children])
        appends = "".join([child.getAppend(parent_wizard) for child in self.children])
        title = self.properties.get("title", "")
        abstractmethods = "".join([child.getAbstractMethods(parent_wizard) for child in self.children])
        abstract = "abstract " if abstractmethods else ""
        inits = "".join([child.getInit() for child in self.children])
        acceptdecline = "".join([child.getAcceptDecline() for child in self.children])
        if inits:
            inits += "\n"
        dict = {"classname" : classname, "imports" : imports, "abstractmethods" : abstractmethods, "abstract" : abstract,
            "declarations" : declarations, "inits" : inits, "appends" : appends, "title" : title, "acceptdecline" : acceptdecline}
        self.write_file(os.path.join("sharedscreens", "%s.java" % classname), """package genericbiz.sharedscreens;

%(imports)s

public %(abstract)sclass %(classname)s extends GenericBizDialog {%(declarations)s

	public %(classname)s(GenericBizWizard wizard, int screenid) {
		this(wizard, screenid, "%(title)s", false);
	}
	
	public %(classname)s(GenericBizWizard wizard, int screenid, boolean noback) {
		this(wizard, screenid, "%(title)s", noback);
	}
	
	public %(classname)s(GenericBizWizard wizard, int screenid, String title) {
		this(wizard, screenid, title, false);
	}
	
	// You can specify a different title here
	public %(classname)s(GenericBizWizard wizard, int screenid, String title, boolean noback) {
		super(wizard, screenid, title, noback);
		%(inits)s%(appends)s
	}%(abstractmethods)s
}
""" % dict, echo)
