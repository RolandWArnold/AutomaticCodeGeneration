#!/usr/bin/env python

import os.path
from template import LType

stacked_values_str = """
		
		String[] _stacked_values_array = { %(hashitems)s };
		//Section removed for copyright reasons: check if database has items based on wizard.getWizardID() and the stackname
		"""

on_notify_str = """\n\t\n\tpublic void hideNotify() {%(notify_vals)s\n\t\tsuper.hideNotify();\n\t}\n"""

on_show_str = """\n\t\n\tpublic void show() {%(stacked_value)s%(show_append)s\n\t\tsuper.show();\n\t}\n"""

class Dialog(LType):
    def write(self, parent_wizard=None, parent_screen=None, echo=True):
        package = self.packageName(parent_wizard.name)
        classname =  self.getOwnClassName()
        screenid = self.screenID(self.ctype, self.name, parent_wizard.name)
        importset = set(["import genericbiz.extensions.GenericBizDialog;", "import genericbiz.extensions.GenericBizWizard;", "import genericbiz.id.ScreenID;"])
        [importset.update(child.getImports()) for child in self.children]
        declarations = "".join([child.getDecl() for child in self.children])
        appends = "".join([child.getAppend(parent_wizard) for child in self.children])
        title = self.properties.get("title", parent_wizard.properties.get("title", ""))
        acceptdecline = "".join([child.getAcceptDecline() for child in self.children])
        noback = ", true" if self.properties.get("movement", "") == "noback" else ""
        add_show = False
        stacked_value = ""
        if "stackvalues" in self.properties:
            add_show = True
            importset.update(["import java.util.Hashtable;", "import java.util.Vector;"])
            dict = {}
            vals = self.properties["stackvalues"].split()
            wizardname = vals[0].lstrip("{")
            stackname = vals[1].rstrip("}")
            wizardid = "wizard.getWizardID()" if parent_wizard.name == wizardname else self.wizardID(wizardname)
            stacked_value = stacked_values_str % {"hashitems" : '"%s"' % '", "'.join(vals[2:]), "wizardid" : wizardid, "stackname" : stackname}
        onnotify = ""
        on_show_appends = ""
        if "ItemList" in [c.ctype for c in self.children]:
            add_show = True
            onnotify = on_notify_str % {"notify_vals" : "".join([child.getHideNotify(self) for child in self.children])}
            on_show_appends = "".join([child.getShowAppend(self) for child in self.children])
        elif "Totals" in [c.ctype for c in self.children]:
            add_show = True
            on_show_appends = "".join([child.getShowAppend(self) for child in self.children])
        show = ""
        if add_show:
            show = on_show_str % {"stacked_value" : stacked_value, "show_append" : on_show_appends}
            on_show_appends = "".join([child.getShowAppend(self) for child in self.children])
        conditional = ""
        if "back_if_value" in self.properties:
            con = self.properties["back_if_value"].split()
            con[0], con[1] = con[0].lstrip("{"), con[1].rstrip("}")
            target_ctype, target_name = tuple(con[2].split(":"))
            target_id = self.screenID(target_ctype, target_name, parent_wizard.name)
            wizardid = "wizard.getWizardID()" if parent_wizard.name == con[0] else self.wizardID(con[0])
            conditional = '\n\n\t\tthis.setConditional(%s, "%s", %s);' % (wizardid, con[1], target_id)
        inits = "".join([child.getInit() for child in self.children])
        imports = "\n".join(sorted(list(importset)))
        dict = {"package" : package, "classname" : classname, "screenid" : screenid, "imports" : imports, "noback" : noback,
            "declarations" : declarations, "inits" : inits, "appends" : appends, "title" : title, "acceptdecline" : acceptdecline,
            "conditional" : conditional, "onnotify" : onnotify, "show" : show}
        self.write_file(os.path.join("wizard", package, "%s.java" % classname), """package genericbiz.wizard.%(package)s;

%(imports)s

public class %(classname)s extends GenericBizDialog {%(declarations)s

	public %(classname)s(GenericBizWizard wizard) {
		super(wizard, %(screenid)s, "%(title)s"%(noback)s);%(conditional)s%(inits)s%(appends)s
	}%(onnotify)s%(show)s%(acceptdecline)s
}
""" % dict, echo)
