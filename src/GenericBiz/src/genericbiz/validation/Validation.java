package genericbiz.validation;

import java.util.Enumeration;

import genericbiz.extensions.GenericBizDialog;

import org.j4me.ui.components.Component;
import org.j4me.ui.components.TextBox;

public class Validation {
	static boolean val = false;
	
	public boolean validate(GenericBizDialog dialog) {
		Enumeration e = dialog.components();
		while(e.hasMoreElements()) {
			Component c = (Component)e.nextElement();
			if(c instanceof TextBox) {
				TextBox tb = (TextBox)c;
				if (tb.getSetter().compareTo("clinicid")) {
					val = true;
					return true;
				}
				if(tb.getString().length() == 0) {
					return false || val;
				}
			}
		}
		return true;
	}
}
