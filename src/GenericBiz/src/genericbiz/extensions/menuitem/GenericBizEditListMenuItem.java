package genericbiz.extensions.menuitem;

import java.util.Vector;

import genericbiz.extensions.GenericBizDialog;
import genericbiz.extensions.GenericBizItemEditor;

import org.j4me.ui.MenuItem;

public class GenericBizEditListMenuItem implements MenuItem {
	GenericBizDialog dialog;
	String text;
	Vector items;
	int index;

	public GenericBizEditListMenuItem(GenericBizDialog dialog, String text, Vector items, int index) {
		this.dialog = dialog;
		this.text = text;
		this.items = items;
		this.index = index;
	}

	public String getText() {
		return this.text;
	}

	public void onSelection() {
		new GenericBizItemEditor(this.dialog, this.text, this.items, this.index).show();
	}
}
