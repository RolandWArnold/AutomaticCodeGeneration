#!/usr/bin/env python

import os, os.path, re

class AppManager(object):
	def __init__(self, root, wizards, echo):
		includes = []
		declarations = []
		cases = []
		for w in wizards:
			includes.append("\nimport genericbiz.wizard.%s.%sWizard;" % (w.packageName(w.name), w.name))
			declarations.append("\n\tprivate static %sWizard %s = new %sWizard();" % (w.name, self.getOwnComponentName(w.name), w.name))
			cases.append("\n\t\tcase %s:\n\t\t\tcurrentWizard = %s;\n\t\t\tbreak;" % (w.wizardID(w.name), self.getOwnComponentName(w.name)))
		root.write_file("AppManager.java", self.get_appmgr_contents("".join(includes), "".join(declarations), "".join(cases)), echo=echo)
	
	def getOwnComponentName(self, text):
		return text[:1].lower() + "".join(re.findall("[\d\w\ ]", " ".join(text.split()[:4]))).title().replace(" ", "")[1:] + "Wizard"
	
	def get_appmgr_contents(self, includes, declarations, cases):
		return """package genericbiz;

import java.util.*;
import javax.microedition.midlet.MIDlet;
import javax.microedition.midlet.MIDletStateChangeException;

import genericbiz.extensions.GenericBizWizard;
import genericbiz.id.WizardID;
%s

import org.json.me.*;
import org.j4me.ui.UIManager;

/*
 * This is the main class that starts everything, and allows our wizards to play 
 * tag with each other. It also checks and runs our IMEI-setting dialog if this
 * property isn't set in the db.  
 */
 
public class AppManager extends MIDlet {

	private static AppManager appManagerInstance;
	private static Vector wizardStack = new Vector();
	%s
	
	private static GenericBizWizard currentWizard;
	
	public AppManager getAppManager() {
		if(appManagerInstance == null)
			appManagerInstance = new AppManager();
		return appManagerInstance;
	}
	
	public AppManager() {
		UIManager.init(this);
		
		try {
			// For copyright reasons code has been removed 
			// that checked a database to see if the user was registered,
			// and then displayed either the register screen to record the IMEI number
			currentWizard = entergenericbizWizard;
			currentWizard.checkStartWizard();
		} catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	public static void runPreviousWizard() {
		if(currentWizard != entergenericbizWizard) {
			currentWizard.clear();
		}
		if(wizardStack.size() > 0) {
			currentWizard = (GenericBizWizard)wizardStack.lastElement();
			wizardStack.removeElementAt(wizardStack.size() - 1);
		} else {
			currentWizard = entergenericbizWizard;
		}
		currentWizard.checkStartWizard();
	}
	
	public static void runWizard(int nextWizard) {
		if(currentWizard != entergenericbizWizard) {
			wizardStack.addElement(currentWizard);
			if(nextWizard == WizardID.START_GENERIC_BIZ_APP_WIZARD) {
				for(int i = wizardStack.size() - 1; i >= 0; i--) {
					((GenericBizWizard)wizardStack.lastElement()).clear();
					wizardStack.removeElementAt(i);
				}
			}
		}
		switch(nextWizard) {%s
		}
		if(currentWizard == null) {
			System.out.println("Oops: " + nextWizard);
		}
		currentWizard.checkStartWizard();
	}
	
	protected void destroyApp(boolean arg0) throws MIDletStateChangeException {}
	
	protected void pauseApp() {}
	
	protected void startApp() throws MIDletStateChangeException {}
}
""" % (includes, declarations, cases)
