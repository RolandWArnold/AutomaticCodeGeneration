#!/usr/bin/env python

import os.path
from template import LType

class WizardPointer(LType):
    def write(self, parent_wizard=None, parent_screen=None, echo=True):
        pass

class Wizard(LType):
    def nextCase(self, source, target):
        source_id = self.screenID(source.ctype, source.name, self.name)
        target_id = self.screenID(target.ctype, target.name, self.name)
        return """\n\t\tcase %s:\n\t\t\tcurrent(%s);\n\t\t\tbreak;""" % (source_id, target_id)

    def prevCase(self, source, target):
        source_id = self.screenID(source.ctype, source.name, self.name)
        target_id = self.screenID(target.ctype, target.name, self.name)
        return """\n\t\tcase %s:\n\t\t\tcurrent(%s);\n\t\t\tbreak;""" % (source_id, target_id)

    def currentCase(self, source, importset):
        source_id = self.screenID(source.ctype, source.name, self.name)
        if source.ctype == "Wizard" or source.ctype == "WizardPointer":
            importset.add("import genericbiz.AppManager;")
            return """\n\t\tcase %s:\n\t\t\tAppManager.runWizard(%s);\n\t\t\tbreak;""" % (source_id, self.wizardID(source.name))
        source_class = self.getClassName(source.ctype, source.name)
        if source.ctype == "SendInfoInstance":
            source_class = "SendInfoDialog"
            importset.add("import genericbiz.sharedscreens.*;")
            rpc_call = source.properties["rpc_call"]
            wizard_namespace = source.properties.get("wizard_namespace", None)
            if wizard_namespace is None:
                return """\n\t\tcase %s:\n\t\t\tsetScreen(new %s(this, %s, "%s"));\n\t\t\tbreak;""" % (source_id, source_class, source_id, rpc_call)
            else:
                return """\n\t\tcase %s:\n\t\t\tsetScreen(new %s(this, %s, "%s", %s));\n\t\t\tbreak;""" % (source_id, 
                                                                                                           source_class,
                                                                                                           source_id,
                                                                                                           rpc_call,
                                                                                                           self.wizardID(wizard_namespace))
        else:
            return """\n\t\tcase %s:\n\t\t\tsetScreen(new %s(this));\n\t\t\tbreak;""" % (source_id, source_class)

    def endCase(self, source):
        source_class = self.screenID(source.ctype, source.name, self.name)
        return """\n\t\tcase %s:\n\t\t\tendWizard();\n\t\t\tbreak;""" % source_class

    def cancelCase(self, source):
        source_class = self.screenID(source.ctype, source.name, self.name)
        return """\n\t\tcase %s:\n\t\t\tcancelWizard();\n\t\t\tbreak;""" % source_class
    
    def write(self, parent_wizard=None, parent_screen=None, echo=True):
        register = self.wizardID(self.name)
        package = self.packageName(self.name)
        classname = self.getOwnClassName()
        importset = set(["import genericbiz.extensions.*;", "import genericbiz.id.*;"])
        firstchild = self.children[0]
        firstpage = self.screenID(firstchild.ctype, firstchild.name, self.name)
        nextcases = []
        prevcases = []
        currentcases = []
        for i in range(len(self.children)):
            child = self.children[i]
            currentcases.append(self.currentCase(child, importset))
            if i == len(self.children) - 1:
                nextcases.append(self.endCase(child))
            else:
                nextcases.append(self.nextCase(child, self.children[i + 1]))
            if i == 0:
                prevcases.append(self.cancelCase(child))
            else:
                inst = self.children[i - 1] if self.children[i - 1].ctype != "SendInfoInstance" else self.children[i - 2]
                prevcases.append(self.prevCase(child, inst))
        
        imports = "\n".join(sorted(list(importset)))
        dict = {"package" : package, "classname" : classname, "firstpage" : firstpage,
                "thenextcases" : "".join(nextcases), "theprevcases" : "".join(prevcases), "thecurrentcases" : "".join(currentcases),
                "wizardid" : register, "imports" : imports}
        
        self.write_file(os.path.join("wizard", package, "%s.java" % classname), """package genericbiz.wizard.%(package)s;

%(imports)s

public class %(classname)s extends GenericBizWizard {
	
	public %(classname)s() {
		super(%(wizardid)s);
	}
	
	public void startWizard() {
		current(%(firstpage)s);
	}

	public void next(int screenid) {
		switch(screenid) {%(thenextcases)s
		default:
			System.out.println("Warning: Unhandled screenid (" + screenid
					+ ") in %(classname)s.next()");
		}
	}

	public void prev(int screenid) {
		switch(screenid) {%(theprevcases)s
		default:
			System.out.println("Warning: Unhandled screenid (" + screenid
					+ ") in %(classname)s.prev()");
		}
	}

	public void current(int screenid) {
		switch(screenid) {%(thecurrentcases)s
		default:
			System.out.println("Warning: Unhandled screenid (" + screenid
					+ ") in %(classname)s.current()");
			endWizard();
		}
	}
}
""" % dict, echo=False)
