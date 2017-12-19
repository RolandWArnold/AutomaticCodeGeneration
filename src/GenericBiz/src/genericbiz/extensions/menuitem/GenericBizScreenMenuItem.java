package genericbiz.extensions.menuitem;

import genericbiz.extensions.GenericBizWizard;

import org.j4me.ui.MenuItem;

public class GenericBizScreenMenuItem implements MenuItem {
	String text;
	GenericBizWizard wizard;
	int screenID;
	int valueWizardID;
	String key;
	Object value;
	boolean setValueOnSelection;

	public GenericBizScreenMenuItem(String text, GenericBizWizard wizard, int screenID) {
		this.text = text;
		this.wizard = wizard;
		this.screenID = screenID;
		this.setValueOnSelection = false;
	}

	public void setValue(String key, Object value) {
		this.setValue(this.wizard.getWizardID(), key, value);
	}
	
	public void setValue(int wizardid, String key, Object value) {
		this.valueWizardID = wizardid;
		this.key = key;
		this.value = value;
		this.setValueOnSelection = true;
	}
	
	public String getText() {
		return this.text;
	}

	public void onSelection() {
		if(this.setValueOnSelection) {
            //Removed: store info in db: wizardId, key, value
		}
		this.wizard.current(this.screenID);
	}
}
