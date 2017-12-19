#!/usr/bin/env python

import os, os.path, re

class WizardID(object):
    def __init__(self, root, li, echo=True):
        self.root = root
        self.ids = []
        for l in li:
            self.ids.append("\n\tpublic static final int %s = %d;" % (l, len(self.ids) + 10000))
        self.root.write_file(os.path.join("id", "WizardID.java"), self.get_contents(), echo)
    
    def get_contents(self):
        return """package genericbiz.id;

public class WizardID {%s
}
""" % "".join(self.ids)
