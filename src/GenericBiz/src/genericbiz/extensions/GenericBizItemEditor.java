package genericbiz.extensions;

import java.util.Vector;

import org.j4me.ui.Dialog;
import org.j4me.ui.Theme;
import org.j4me.ui.components.Label;

public class GenericBizItemEditor extends Dialog {
	GenericBizScreen prev;
	Vector items;
	int index;

	public GenericBizItemEditor(GenericBizScreen prev, String text, Vector items, int index) {
		this.prev = prev;
		this.items = items;
		this.index = index;
		setTitle("Edit List");
		setMenuText(new Theme().getMenuTextForCancel(), "Remove");
		append(new Label("Do you wish to remove this item from the list?\n"));
		append(new Label(text));
	}

	protected void declineNotify() {
		this.prev.show();
	}

	protected void acceptNotify() {
		this.items.removeElementAt(this.index);
		this.prev.show();
	}
}
