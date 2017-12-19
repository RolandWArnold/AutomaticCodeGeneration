package genericbiz.extensions;

import genericbiz.AppManager;

public abstract class GenericBizWizard {
	protected GenericBizScreen currentScreen;
	protected int wizardid;

	public GenericBizWizard(int wizardid) {
		this.wizardid = wizardid;
	}

	public abstract void startWizard();

	public abstract void next(int screenid);

	public abstract void prev(int screenid);

	public abstract void current(int screenid);

	protected void cancelWizard() {
		AppManager.runPreviousWizard();
	}

	protected void endWizard() {
		AppManager.runPreviousWizard();
	}

	protected void setScreen(GenericBizScreen screen) {
		try {
			currentScreen = screen;
			currentScreen.show();
		} catch(Exception e) {
			e.printStackTrace();
		}
	}

	public void checkStartWizard() {
		if(getScreenID() != -1)
			this.currentScreen.show();
		else
			startWizard();
	}
	
	public int getWizardID() {
		return this.wizardid;
	}

	public int getScreenID() {
		return currentScreen == null ? -1 : currentScreen.getScreenID();
	}

	public void clear() {
		//removed for copyright: clear db for wizardid
		this.currentScreen = null;
	}
	public void clearAll() {
        //removed for copyright
	}

	public boolean hasItem(Object key) {
        //removed for copyright
        return false;
	}
	
	public boolean hasItems(Object[] keys) {
        //removed for copyright
        return false;
	}
	
	public String getString(Object key) {
        //removed for copyright
        return "";
	}
	
	public String getString(Object key, String fallback) {
        //removed for copyright
        return "";
	}

	public Object getItem(Object key) {
        //removed for copyright
        return null;
	}

	public Object getItem(Object key, Object fallback) {
        //removed for copyright
        return null;
	}

	public void setItem(Object key, Object value) {
        //removed for copyright
	}
	
	public void setOtherWizardItem(int otherWizardID, Object key, Object value) {
        //removed for copyright
	}
	
	public Object removeItem(Object key) {
        //removed for copyright
        return null;
	}
}
