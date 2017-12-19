package genericbiz.util;

import java.util.Vector;

public class LineReader {
	Vector lines = null;
	int position;

	public LineReader(String filename) {
		String filteredList = null;
		try
		{
			filteredList = Database.getDatabase().Get(filename);
			System.out.println(filteredList);
		} catch(Exception e) {
			e.printStackTrace();
		}
		
		String contents = null;
		if(filteredList == null) {
			contents = new FileReader("/genericbiz/storage/" + filename + ".flist").readFile();
		}
		else {
			contents = filteredList;
		}
		
		if (contents != null) {
			lines = new Vector();
			position = 0;

			int marker = 0, i = 0;
			for (i = 0; i < contents.length(); i++) {
				if (contents.charAt(i) == '\n') {
					lines.addElement(contents.substring(marker, i));
					marker = i + 1;
				}
			}
			if (marker < i)
				lines.addElement(contents.substring(marker, i));
		}
	}

	public String readLine() {
		return (lines == null || position >= lines.size()) ? null :
			(String)lines.elementAt(position++);
	}
	
	public void rewind() {
		position = 0;
	}
}
