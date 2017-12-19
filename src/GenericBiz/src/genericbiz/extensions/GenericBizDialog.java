package genericbiz.extensions;

import java.util.Enumeration;

import genericbiz.extensions.menuitem.GenericBizScreenMenuItem;
import genericbiz.extensions.menuitem.GenericBizWizardMenuItem;
import genericbiz.validation.ErrorSharedDialog;
import genericbiz.validation.Validation;

import org.j4me.ui.Dialog;
import org.j4me.ui.UIManager;
import org.j4me.ui.components.CheckBox;
import org.j4me.ui.components.Component;
import org.j4me.ui.components.MenuOption;
import org.j4me.ui.components.RadioButton;
import org.j4me.ui.components.TextBox;

public abstract class GenericBizDialog extends Dialog implements GenericBizScreen {
	protected GenericBizWizard wizard;
	protected int screenid;
	protected boolean noback;
	protected int conditionalWizardID;
	protected String conditional;
	protected int conditionalScreenID;

	public GenericBizDialog(GenericBizWizard wizard, int screenid, String title) {
		this(wizard, screenid, title, false);
	}

	public GenericBizDialog(GenericBizWizard wizard, int screenid, String title, boolean noback) {
		setTitle(title);
		this.wizard = wizard;
		this.screenid = screenid;
		this.noback = noback;
		if(this.noback) {
			setMenuText(null, UIManager.getTheme().getMenuTextForOK());
		}
		this.conditional = null;
	}
	
	public void setConditional(int conditionalWizardID, String conditional, int conditionalScreenID) {
		this.conditionalWizardID = conditionalWizardID;
		this.conditional = conditional;
		this.conditionalScreenID = conditionalScreenID;
	}

	public void showNotify() {
		if(this.components().hasMoreElements() && !get(getSelected()).acceptsInput()) {
			focusFirst();
		}
	}

	protected void acceptNotify() {
		if(!new Validation().validate(this)) {
			new ErrorSharedDialog(this, "Invalid input!\nPlease retry.").show();
		} else {
			Enumeration e = this.components();
			while(e.hasMoreElements()) {
				Component c = (Component)e.nextElement();
				if(c instanceof TextBox) {
					TextBox tb = (TextBox)c;
					this.wizard.setItem(tb.getSetter(), tb.getString());
				} else if(c instanceof RadioButton) {
					RadioButton rb = (RadioButton)c;
					this.wizard.setItem(rb.getSetter(), rb.getSelectedValue());
				} else if(c instanceof CheckBox) {
					CheckBox cb = (CheckBox)c;
					this.wizard.setItem(cb.getSetter(), cb.isChecked() ? "Y" : "N");
				}
			}
			if(get(getSelected()) instanceof MenuOption) {
				((MenuOption)get(getSelected())).select();
			} else {
				this.wizard.next(screenid);
			}
		}
	}

	protected void declineNotify() {
		if(!this.noback) {
			if(this.conditional != null && true) {// Removed for copyright: get if db has(this.conditionalWizardID, this.conditional)
				this.wizard.current(this.conditionalScreenID);
			} else {
				this.wizard.prev(this.screenid);
			}
		}
	}

	public int getScreenID() {
		return this.screenid;
	}

	public void appendScreenOption(String text, int screenID) {
		append(new MenuOption(new GenericBizScreenMenuItem(text, this.wizard,
				screenID)));
	}

	public void appendScreenOption(String text, int screenID, String key,
			Object value) {
		GenericBizScreenMenuItem itm = new GenericBizScreenMenuItem(text,
				this.wizard, screenID);
		itm.setValue(key, value);
		append(new MenuOption(itm));
	}

	public void appendWizardOption(String text, int wizardID) {
		append(new MenuOption(new GenericBizWizardMenuItem(text, wizardID)));
	}

	public void appendWizardOption(String text, int wizardID, String key,
			Object value) {
		GenericBizWizardMenuItem itm = new GenericBizWizardMenuItem(text, wizardID);
		itm.setValue(key, value);
		append(new MenuOption(itm));
	}

	protected void keyPressed(int key) {
		boolean goToFirst = false;
		boolean goToLast = false;
		// Wrap the scroll around the screen?
		if(key == DOWN) {
			if(getSelected() == size() - 1) {
				goToFirst = true;
			}
		} else if(key == UP) {
			if(getSelected() == 0 && size() > 1) {
				goToLast = true;
			}
		}
		super.keyPressed(key);
		
		// Were we going to the first or last menu choice?
		// Only do these after super.keyPressed(). Otherwise
		// keyPressed() will scroll again so we'll actually wind
		// up on the second or second-to-last menu choice.
		if(goToFirst) {
			focusFirst();
		} else if(goToLast) {
			focusLast();
		} else if(!hasVerticalScrollbar() && this.size() > 0 && !this.get(this.getSelected()).acceptsInput()) {
			if(key == DOWN) {
				focusFirst();
			} else if(key == UP) {
				focusLast();
			}
		}
	}

	private void focusFirst() {
//		System.out.println("Focusfirst");
		Enumeration e = this.components();
		while(e.hasMoreElements()) {
			Component c = (Component)e.nextElement();
			if(c.acceptsInput()) {
//				System.out.println(c);
				setSelected(c);
				return;
			}
		}
	}

	private void focusLast() {
//		System.out.println("Focuslast");
		for(int i = this.size() - 1; i >= 0; i--) {
			if(this.get(i).acceptsInput()) {
//				System.out.println(i + " " + this.get(i));
				setSelected(i);
				break;
			}
		}
	}
}
