package genericbiz.extensions.menuitem;

import genericbiz.AppManager;

import org.j4me.ui.MenuItem;

public class GenericBizWizardMenuItem implements MenuItem {
	String text;
	int wizardID;
	boolean setValue;
	String key;
	Object value;

	public GenericBizWizardMenuItem(String text, int wizardID) {
		this.text = text;
		this.wizardID = wizardID;
		this.setValue = false;
	}

	public void setValue(String key, Object value) {
		this.key = key;
		this.value = value;
		this.setValue = true;
	}
	
	public String getText() {
		return this.text;
	}

	public void onSelection() {
		if(this.setValue) {
            //Removed: store info in db: wizardId, key, value
		}
		AppManager.runWizard(this.wizardID);
	}
}
