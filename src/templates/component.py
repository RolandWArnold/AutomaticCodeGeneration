#!/usr/bin/env python

import re, sys, os.path
from template import LType

class Component(LType):
    dct = {"Checkbox":"CheckBox", "Label":"Label", "Combobox":"RadioButton", "Textbox":"TextBox", "Picture":"Picture", "Whitespace":"Whitespace", 
           "HorizontalRule":"HorizontalRule","Version":"Label"}
    
    def write(self, *args):
        """Does nothing"""
    
    def getImports(self):
        return set(["import org.j4me.ui.components.%s;" % self.dct[self.ctype]]) if self.ctype in self.dct else set()
    
    def getDecl(self):
        return "\n\t{0} {1} = new {0}();".format(self.dct[self.ctype], self.getOwnComponentName()) if self.ctype in self.dct else ""
    
    def getInit(self):
        return self.getSetLabel()
    
    def getAppend(self, *ignored):
        return "\n\t\tappend(%s);" % self.getOwnComponentName();
    
    def getSetLabel(self):
        return '\n\t\t%s.setLabel("%s");' % (self.getOwnComponentName(), self.name)
    
    def getAbstractMethods(self, *ignored):
        return ""
    
    def getAcceptDecline(self, *ignored):
        return ""
    
    def getShowAppend(self, *ignored):
        return ""
    
    def getHideNotify(self, *ignored):
        return ""
    
    def getOwnComponentName(self):
        parts = "".join(re.findall("[A-Za-z ]*", self.name)).split()[:4]
        if not parts:
            name = self.ctype[:1].lower() + self.ctype[1:]
        else:
            name = parts[0].lower() + " ".join(parts[1:]).title().replace(" ", "") + self.ctype
        index = self.properties["index"]
        return "%s%s" % (name, index) if index != 0 else name

class Whitespace(Component):
    def getDecl(self):
        return "\n\t{0} {1} = new {0}({2});".format(self.dct[self.ctype], self.getOwnComponentName(), self.name)
    
    def getInit(self):
        return ""

class HorizontalRule(Component):
    def getDecl(self):
        return "\n\t{0} {1} = new {0}({2});".format(self.dct[self.ctype], self.getOwnComponentName(), self.name)
    
    def getInit(self):
        return ""

class Picture(Component):
    def getImports(self):
        if "read" in self.properties:
            return set(["import javax.microedition.lcdui.Graphics;", "import javax.microedition.lcdui.Image;"]).union(Component.getImports(self))
        else: #filename in self.properties
            return set(["import javax.microedition.lcdui.Graphics;", "import java.io.IOException;"]).union(Component.getImports(self))
    
    def getInit(self):
        return '\n\t\t%s.setHorizontalAlignment(Graphics.HCENTER);' % self.getOwnComponentName()
    
    def getAppend(self, *ignored):
        name = self.getOwnComponentName()
        comment = " // Only append if you can actually set the image."
        if "read" in self.properties:
            prop = self.properties["read"]
            append = Component.getAppend(self, *ignored).strip()
            dict = {"name" : name, "comment" : comment, "prop" : prop, "append" : append}
            return \
"""
		try {
			Image img = (Image)this.wizard.getItem("%(prop)s");
			if(img != null) {
				%(name)s.setImage(img);
				%(append)s %(comment)s
			}
		} catch(Exception e) {
			e.printStackTrace();
		}""" % dict
        else: #filename in self.properties
            return '\n\t\ttry {\n\t\t\t%s.setImage("%s");\n\t\t\t%s%s\n\t\t} catch(IOException e) {\n\t\t\te.printStackTrace();\n\t\t}' %\
                    (self.getOwnComponentName(), self.properties["filename"], Component.getAppend(self, *ignored).strip(), comment)

class Label(Component):
    def getInit(self):
        value = '"%s"' % self.name
        if "read" in self.properties:
            value = 'this.wizard.getString("%s")' % self.properties["read"]
        elif "call" in self.properties:
            value = 'this.%s()' % self.properties["call"].split(":")[1]
        return '\n\t\t%s.setLabel(%s);' % (self.getOwnComponentName(), value)
    
    def getAbstractMethods(self, *ignored):
        if not "call" in self.properties:
            return ""
        else:
            return '\n\n\tprotected abstract %s %s();' % tuple(self.properties["call"].split(":"))

class Checkbox(Component):
    def getDecl(self):
        return "\n\t{0} {1} = new {0}(\"{2}\");".format(self.dct[self.ctype], self.getOwnComponentName(), self.properties["write"])

class ComboOption(Component):
    def getAppend(self, *ignored):
        return 'append("%s");' % self.name;

class Combobox(Component):
    def getDecl(self):
        return "\n\t{0} {1} = new {0}(\"{2}\");".format(self.dct[self.ctype], self.getOwnComponentName(), self.properties["write"])
    
    def getInit(self):
        return "%s\n\t\t%s" % (self.getSetLabel(), "\n\t\t".join(["%s.%s" % (self.getOwnComponentName(), child.getAppend()) for child in self.children]))

class Textbox(Component):
    def getImports(self):
        return set(["import javax.microedition.lcdui.TextField;", "import genericbiz.validation.Validation;"]).union(Component.getImports(self))
    
    def getDecl(self):
        validation = "Validation.%s" % {None : "NORMAL_VALIDATION",
                                    "none" : "NO_VALIDATION",
                                    "yyyymm" : "YYYYMM_VALIDATION",
                                    "yyyymmdd" : "YYYYMMDD_VALIDATION",
                                    "nonzero" : "NON_ZERO"}[self.properties.get("validation")]
        return "\n\t{0} {1} = new {0}(\"{2}\", {3});".format(self.dct[self.ctype], self.getOwnComponentName(), self.properties["write"], validation)
    
    def getInit(self):
        maxsize = "%s.setMaxSize(%s);\n\t\t" % (self.getOwnComponentName(), self.properties["maxsize"]) if "maxsize" in self.properties else ""
        constraint = self.properties.get("fieldtype", "ANY").upper()
        return "%s\n\t\t%s%s.setModifierConstraint(TextField.%s, true);" % (self.getSetLabel(), maxsize, self.getOwnComponentName(), constraint)

class MenuItem(Component):
    def getImports(self):
        return set(["import genericbiz.id.WizardID;"]) if "targetwizard" in self.properties else set(["import genericbiz.id.ScreenID;"])
    
    def getInit(self):
        return ""
    
    def getAppend(self, parent_wizard):
        keyval = ""
        if "write" in self.properties:
            keyval = ', "%s", "%s"' % tuple(self.properties["write"].split(":"))
        if "targetwizard" in self.properties:
            return '\n\t\tappendWizardOption("%s", %s%s);' % (self.name, self.wizardID(self.properties["targetwizard"]), keyval)
        elif "targetdialog" in self.properties:
            ctype, name = self.properties["targetdialog"].split(":")
            return '\n\t\tappendScreenOption("%s", %s%s);' % (self.name, self.screenID(ctype, name, parent_wizard.name), keyval)
        else:
            print "Missing target type!", self
        return ""

class Totals(Component):
    def getImports(self):
        return set(["import org.j4me.ui.components.Label;", "import java.util.Hashtable;", "import java.util.Vector;",
            "import genericbiz.id.WizardID;"])
    
    def getDecl(self):
        return "\n\tLabel %sLabel = new Label();" % self.ctype.lower()
    
    def getInit(self):
        return ""
    
    def getAppend(self, *ignored):
        return '\n\t\tappend(%sLabel);' % self.ctype.lower();

    def getShowAppend(self, parent_dialog):
        txt1, txt2 = self.properties["text"].split("{sum}")
        txt = '"%s" + _totalsAmount + "%s"' % (txt1, txt2)
        dct = {"txt" : txt}
        if parent_dialog.name == "NotesTotals":
            return \
"""
		try {
			int _totalsAmount = 0;
			Vector salesList = new Vector;//copyright removal: actually get Vector from db with WizardID.NOTES_WIZARD, "notesList", new Vector()
			for(int i = 0; i < salesList.size(); i++) {
				Hashtable notesList_hash = (Hashtable)notesList.elementAt(i);
				_totalsAmount += Integer.parseInt((String)notesList_hash.get("price_of"));
			}
			totalsLabel.setLabel(%(txt)s);
		}
		catch (Exception e) {
			System.out.println(e);
			totalsLabel.setLabel("Formatting Error! Unable to calculate total.");
		}""" % dct
        else:
			print "################\nThis totals value '%s' has not been implemented in component.py################\n" % parent_dialog.name

class ItemList(Component):
    def getImports(self):
        return set(["import java.util.Hashtable;", "import java.util.Vector;",
            "import org.j4me.ui.components.Label;", "import org.j4me.ui.components.HorizontalRule;", "import genericbiz.id.WizardID;",
            "import javax.microedition.lcdui.Graphics;", "import genericbiz.extensions.menuitem.GenericBizEditListMenuItem;",
            "import org.j4me.ui.components.MenuOption;"])
    
    def getInit(self):
        return ""
    
    def getAppend(self, *ignored):
        return ""
    
    def getHideNotify(self, parent_wizard):
        wizardname, list_name = self.properties["test"].strip("{}").split()
        wizardid = "wizard.getWizardID()" if parent_wizard.name == wizardname else self.wizardID(wizardname)
        dct = {"item_list_name" : list_name, "wizardid" : wizardid}
        return \
"""
		Vector %(item_list_name)s = new Vector();//copyright removal: Get Vector from DB with %(wizardid)s, "%(item_list_name)s"
		if(%(item_list_name)s != null && %(item_list_name)s.size() > 0) {
			for(int i = %(item_list_name)s.size() + 1; i >= 0; i--)
				delete(size() - 1);
		}""" % dct

    def getShowAppend(self, parent_wizard):
        pattern = ""
        lst = re.findall("([^{}]*)(\{[^{}]*\})([^{}]*)", self.properties["pattern"])
        for tpl in lst:
            for itm in tpl:
                if not itm:
                    continue
                elif not itm.startswith("{"):
                    pattern += '\t\t\t\t\t"%s" +\n' % itm
                elif itm.find(".") != -1:
                    itm = itm.strip("{}")
                    pattern += '\t\t\t\t\t%s_hash.get("%s") +\n' % (self.name, itm[itm.find(".") + 1:])
                else:
                    itm = itm.strip("{}")
                    pattern += '\t\t\t\t\tgetString("%s") +\n' % (itm[itm.find(".") + 1:])
        wizardname, list_name = self.properties["test"].strip("{}").split()
        wizardid = "wizard.getWizardID()" if parent_wizard.name == wizardname else self.wizardID(wizardname)
        dct = {"item_list_name" : list_name, "title" : "Edit %s" % self.properties["title"], "label_string" : pattern, "wizardid" : wizardid}
        return \
"""
		
		Vector %(item_list_name)s = new Vector();//copyright removal: Get Vector from DB with %(wizardid)s, "%(item_list_name)s"
		if(%(item_list_name)s != null && %(item_list_name)s.size() > 0) {
			append(new HorizontalRule());
			Label _title_label = new Label("%(title)s");
			_title_label.setHorizontalAlignment(Graphics.HCENTER);
			append(_title_label);
			for(int i = %(item_list_name)s.size() - 1; i >= 0; i--) {
				Hashtable %(item_list_name)s_hash = (Hashtable)%(item_list_name)s.elementAt(i);
				append(new MenuOption(new GenericBizEditListMenuItem(this, "" + \n%(label_string)s\t\t\t\t\t"", %(item_list_name)s, i)));
			}
		}""" % dct
