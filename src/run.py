#!/usr/bin/python

import sys, re, os, os.path

from parseflow import YaccFlow

from templates.appmanager import AppManager
from templates.screenid import ScreenID
from templates.wizardid import WizardID

class CreateOutput(object):
    def __init__(self, fname, writeScreenIDs=True, writeWizardIDs=True, writeAppMgr=True):
        self.shared = {}
        self.screenids = set()
        self.wizardids = set()
        self.wizards = set()
        echo = False
        tree = YaccFlow(fname, self).tree
        if tree:
            [container._write(echo=echo) for container in tree]
            if writeScreenIDs:
                ScreenID(self, sorted(list(self.screenids)), echo=echo)
            if writeWizardIDs:
                WizardID(self, sorted(list(self.wizardids)), echo=echo)
            if writeAppMgr:
                AppManager(self, sorted(list(self.wizards)), echo=echo)
        else:
            print("No elements found! Exiting.")

    def registerScreenID(self, id):
        self.screenids.add(id)

    def registerWizardID(self, id):
        self.wizardids.add(id)

    def registerWizard(self, wizard):
        self.wizards.add(wizard)

    def write_file(self, path, contents, echo=True):
        path = os.path.join("generated", path.lstrip("/"))
        if echo:
            msg = "File: '%s'" % path
            print("%s\n%s\n%s" % (len(msg) * "=", msg, len(msg) * "="))
            print(contents)
        d = os.path.dirname(path)
        if not os.path.exists(d):
            os.makedirs(d)
        with open(path, "w") as f:
            f.write(contents)

if __name__ == "__main__":
    output = CreateOutput(
            "input.generic" if len(sys.argv) <= 1 else sys.argv[1], writeAppMgr=True, writeWizardIDs=True, writeScreenIDs=True)
