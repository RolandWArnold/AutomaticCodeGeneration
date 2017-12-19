#!/usr/bin/env python

import re, sys, os, os.path

class LType(object):
    def __init__(self, root, ctype, name, children, properties):
        self.root = root
        self.ctype = ctype.replace("Pointer", "")
        self.name = name
        self.children = children
        self.properties = properties
        self.properties["index"] = self.properties.get("index", 0)
        if ctype == "Wizard":
            self.root.registerWizard(self)
    
    def _write(self, parent_wizard=None, parent_screen=None, echo=True):
        self.write(parent_wizard, parent_screen, echo)
        if not parent_wizard:
            [child._write(self, parent_screen, echo) for child in self.children]
        elif not parent_screen:
            [child._write(parent_wizard, self, echo) for child in self.children]
        else:
            [child._write(parent_wizard, parent_screen, echo) for child in self.children]
    
    def write(self, parent_wizard=None, parent_screen=None, echo=True):
        """Derived classes should override this is they create files"""
        print "Failed to implement method 'write' in %s" % self
        sys.exit(-1)
    
    def write_file(self, path, contents, echo=True):
        self.root.write_file(path, contents, echo)
    
    def __repr__(self):
        return "%s - %s - index: %s - children: %s" % (self.ctype, self.name, self.properties.get("index", 0), len(self.children))
    
    def __cmp__(self, other):
        if str(self) == str(other):
            return 0
        else:
            return 1 if str(other) < str(self) else -1
    
    def packageName(self, wizard):
        return wizard.lower()
    
    def wizardID(self, wizardname):
        id = self.upperunderscore(wizardname + "Wizard")
        self.root.registerWizardID(id)
        return "WizardID.%s" % id
    
    def screenID(self, wizardname, ctype, screenname):
        id = self.upperunderscore(wizardname + screenname + ctype[:1].upper() + ctype[1:] + "Screen")
        self.root.registerScreenID(id)
        return "ScreenID.%s" % id
    
    def getOwnClassName(self):
        return self.getClassName(self.ctype, self.name)
    
    def getClassName(self, ctype, text):
        text = "".join("".join(re.findall("[A-Za-z\d ]*", text)).split()[:4]).replace(" ", "")
        return text[:1].upper() + text[1:] + ctype
    
    def upperunderscore(self, s):
        "UserIDNumber -> USER_ID_NUMBER"
        li = []
        prev = s[-1] if s else ""
        for c in s[:-1][::-1]:
            if c.isupper() and prev[:1].islower():
                li.append(c + prev)
                prev = ""
            elif c.islower() and prev[:1].isupper():
                li.append(prev)
                prev = c
            else:
                prev = c + prev
        if prev:
            li.append(prev)
        return "_".join([s.upper() for s in li[::-1]])
