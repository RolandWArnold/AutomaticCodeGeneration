package genericbiz.extensions;

import org.j4me.ui.MenuItem;
import org.j4me.ui.Theme;
import org.j4me.ui.components.MenuOption;

public class GenericBizFLMenuOption extends MenuOption {

	public GenericBizFLMenuOption(MenuItem choice) {
		super(choice);
	}

	/**
	 * Returns the size of the menu text.
	 * 
	 * @param theme is the application's <code>Theme</code>.
	 * @param viewportWidth is the width of the screen in pixels.
	 * @param viewportHeight is the height of the screen in pixels.
	 * @return An array with two elements where the first is the width
	 *  in pixels and the second is the height.
	 */
	protected int[] getPreferredTextSize (Theme theme, int viewportWidth, int viewportHeight)
	{
		text.setBreakNeatly(false);
		text.setFont(theme.getMiniMonoFont());
		text.setLabel(getLabel());
		return text.getPreferredSize( theme, viewportWidth, viewportHeight );
	}
}
