package genericbiz.validation;

import javax.microedition.lcdui.Graphics;

import genericbiz.extensions.GenericBizScreen;

import org.j4me.ui.Dialog;
import org.j4me.ui.Theme;
import org.j4me.ui.components.Label;

public class ErrorSharedDialog extends Dialog {
	GenericBizScreen prev;
	Label label = new Label();

	public ErrorSharedDialog(GenericBizScreen prev, String text) {
		this.prev = prev;
		setTitle("Error");
		setMenuText("", new Theme().getMenuTextForOK());

		label.setHorizontalAlignment(Graphics.HCENTER);
		label.setLabel("\n\n" + text);

		append(label);
	}

	protected void declineNotify() {}
	
	protected void acceptNotify() {
		this.prev.show();
	}
}
