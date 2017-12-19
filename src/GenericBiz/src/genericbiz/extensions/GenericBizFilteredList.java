package genericbiz.extensions;

import java.util.Timer;
import java.util.TimerTask;

import genericbiz.extensions.internals.filteredlist.StringFilter;

import org.j4me.ui.DeviceScreen;
import org.j4me.ui.MenuItem;
import org.j4me.ui.Theme;
import org.j4me.ui.UIManager;
import org.j4me.ui.components.Label;
import org.j4me.ui.components.Whitespace;

public class GenericBizFilteredList extends GenericBizDialog {
	final int DEFAULT_BOTTOM_SPACE = 5;
	final int TIMING_MILLISECONDS = 900;
	
	Whitespace bottomSpacer = new Whitespace(DEFAULT_BOTTOM_SPACE);
	Label inputLabel = new Label("");
	int listIndex = 0;
	boolean mustScroll = false;
	char current = Character.MAX_VALUE; //-> unused
	Timer keyTimer = null;
	StringFilter list;
	String storagekey;
	int availableHeight = 0;
	String[] matches;
	
	public GenericBizFilteredList(GenericBizWizard wizard, int screenid, String title, StringFilter sflist, String storagekey) {
		super(wizard, screenid, title);
		this.list = sflist;
		this.list.clear();
		this.storagekey = storagekey;
		setMenuText("Cancel", "Clear");
		setSpacing(0);
		setMenuOptions(this.list.getCurrentMatches());
	}
	
	void setMenuOptions(String[] matches) {
		if(this.availableHeight == 0)
			this.availableHeight = getHeight() - DEFAULT_BOTTOM_SPACE - inputLabel.getPreferredSize(
				new Theme(), getWidth(), getHeight())[1];
		this.matches = matches;
		int remainingHeight = this.availableHeight;
		this.listIndex = 0;
		this.mustScroll = false;
		deleteAll();
		for(int i = 0; i < this.matches.length; i++) {
			GenericBizFLMenuOption option = new GenericBizFLMenuOption(new MenuItemAdapter(this.matches[i]));
			int h = option.getPreferredSize(UIManager.getTheme(), getWidth(), getHeight())[1];
			if(h > remainingHeight) {
				this.mustScroll = true;
				break;
			}
			else {
				remainingHeight -= h;
				append(option);
			}
		}
		this.bottomSpacer.setSpacing(remainingHeight);
		append(this.bottomSpacer);
		this.inputLabel.setLabel(this.list.getTotalInput());
		append(this.inputLabel);
		repaint();
	}

	/**
	 * This relies on the always 2 line TODO hack in label to work prettily each time.
	 */
	private void scrollUp() {
		GenericBizFLMenuOption option = new GenericBizFLMenuOption(new MenuItemAdapter(this.matches[this.listIndex]));
		delete(size() - 3);
		insert(option, 0);
		setSelected(0);
		repaint();
	}

	/**
	 * This relies on the always 2 line TODO hack in label to work prettily each time.
	 */
	private void scrollDown() {
		GenericBizFLMenuOption option = new GenericBizFLMenuOption(new MenuItemAdapter(this.matches[this.listIndex]));
		delete(0);
		insert(option, size() - 2);
		setSelected(size() - 3);
		repaint();
	}
	
	private class MenuItemAdapter implements MenuItem {
		String text;
		
		public MenuItemAdapter(String text) {
			this.text = text;
		}

		public String getText() {
			return this.text;
		}

		public void onSelection() {
			wizard.setItem(storagekey, this.text);
			wizard.setItem(storagekey + "_code", list.getStringCode(this.text));
			wizard.next(screenid);
		}
	}
	
	// Our backspace key
	protected void acceptNotify() {
		setMenuOptions(this.list.popChar());
	}
	
	protected void keyPressed(int key) {
		synchronized(this) {
			if (keyTimer != null) {
				keyTimer.cancel();
				keyTimer = null;
			}
		}
		boolean scrollup = false;
		boolean scrolldown = false;
		switch (key) {
		case DeviceScreen.UP:
			if(mustScroll) {
				this.listIndex--;
				if(this.listIndex < 0)
					this.listIndex = this.matches.length - 1;
				//whitespace + input label -> 2
				scrollup = (getSelected() == 0);
			}
			break;
		case DeviceScreen.DOWN: 
			if(mustScroll) {
				this.listIndex++;
				if(this.listIndex >= this.matches.length)
					this.listIndex = 0;
				//whitespace + input label + zero-index -> 3
				scrolldown = (getSelected() == size() - 3);
			}
			break;
		case DeviceScreen.KEY_NUM1:
			handleKey("11");
			break;
		case DeviceScreen.KEY_NUM2:
			handleKey("abc2a");
			break;
		case DeviceScreen.KEY_NUM3:
			handleKey("def3d");
			break;
		case DeviceScreen.KEY_NUM4:
			handleKey("ghi4g");
			break;
		case DeviceScreen.KEY_NUM5:
			handleKey("jkl5j");
			break;
		case DeviceScreen.KEY_NUM6:
			handleKey("mno6m");
			break;
		case DeviceScreen.KEY_NUM7:
			handleKey("pqrs7p");
			break;
		case DeviceScreen.KEY_NUM8:
			handleKey("tuv8t");
			break;
		case DeviceScreen.KEY_NUM9:
			handleKey("wxyz9w");
			break;
		case DeviceScreen.KEY_NUM0:
			handleKey(" 0 ");
			break;
		case DeviceScreen.KEY_POUND: //emulator sucks a bit?
			handleKey("  ");
			break;
		}
		if(!scrollup && !scrolldown)
			super.keyPressed(key);
		else if(scrollup)
			scrollUp();
		else //scroll-down
			scrollDown();
	}

	private synchronized void handleKey(String keySearchSpace) {
		// this wraps characters around if they're repeated rapidly
		int position = keySearchSpace.indexOf(this.current) + 1;
		this.current = keySearchSpace.charAt(position);
		if(position != 0)
			this.list.popChar();
		setMenuOptions(this.list.addChar(this.current));
		keyTimer = new Timer();
		keyTimer.schedule(new TimerTask() {
			public synchronized void run() {
				current = Character.MAX_VALUE;
			}
		}, TIMING_MILLISECONDS);
	}
}
