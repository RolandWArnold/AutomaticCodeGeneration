package genericbiz.extensions.internals.filteredlist;

import java.util.Vector;

import genericbiz.util.LineReader;

public class TreeMaker {
	Vector root;
	String[] fullstrings;
	String[] codes;
	String[] values;

	public TreeMaker(String resource_name) {
		LineReader reader = new LineReader(resource_name);
		Vector v = new Vector();
		String line;
		while((line = reader.readLine()) != null) {
			if(line.startsWith("#-#-#-#"))
				break;
			v.addElement(line);
		}
		fullstrings = new String[v.size() / 2];
		codes = new String[v.size() / 2];
		for(int i = 0; i < v.size(); i += 2) {
			fullstrings[i/2] = (String) v.elementAt(i);
			codes[i/2] = (String) v.elementAt(i + 1);
		}
		v = new Vector();
		while((line = reader.readLine()) != null) {
			if(line.startsWith("#-#-#-#"))
				break;
			v.addElement(line);
		}
		values = new String[v.size()];
		for(int i = 0; i < v.size(); i++) {
			values[i] = (String) v.elementAt(i);
		}
		root = new Vector();
		while((line = reader.readLine()) != null) {
			root.addElement(makeNodes(line, values));
		}
	}

	Vector getTree() {
		return root;
	}

	String[] getIndexArray() {
		return fullstrings;
	}
	
	String[] getCodeArray() {
		return codes;
	}

	Node makeNodes(String line, String[] values) {
		int[] refs = getRefs(line.substring(line.indexOf('|') + 1));
		Vector nodeSubstrings = getNodeSubstrings(line);
		Vector nodeVector = new Vector();
		if(hasNullNode(line))
			nodeVector.addElement(null);
		for(int i = 0; i < nodeSubstrings.size(); i++) {
			nodeVector.addElement(makeNodes((String) nodeSubstrings.elementAt(i), values));
		}
		Node[] nodeArray = new Node[nodeVector.size()];
		for(int i = 0; i < nodeVector.size(); i++)
			nodeArray[i] = (Node) nodeVector.elementAt(i);
		String value = values[getStringIndex(line)];
		return new Node(nodeArray, refs, value);
	}

	Vector getNodeSubstrings(String line) {
		Vector v = new Vector();
		int transition = 0;
		int start = 0;
		for(int i = 0; i < line.length(); i++) {
			if(line.charAt(i) == '[') {
				if(transition++ == 0)
					start = i + 1;
			} else if(line.charAt(i) == ']') {
				if(transition-- == 1)
					v.addElement(line.substring(start, i));
			}
		}
		return v;
	}
	
	int getStringIndex(String line) {
		return Integer.parseInt(line.substring(0, line.indexOf('|')));
	}
	
	int[] getRefs(String line) {
		Vector nums = new Vector();
		for(int i = 0; i < line.length(); i++) {
			if(line.charAt(i) == ',')
				continue;
			if(line.charAt(i) != ',' && !Character.isDigit(line.charAt(i)))
				break;
			int start = i;
			while(Character.isDigit(line.charAt(i + 1)))
				i++;
			nums.addElement(Integer.valueOf(line.substring(start, i + 1)));
		}
		int[] arr = new int[nums.size()];
		for(int i = 0; i < nums.size(); i++) {
			arr[i] = ((Integer) nums.elementAt(i)).intValue();
		}
		return arr;
	}

	boolean hasNullNode(String line) {
		int firstdot = line.indexOf('.');
		int firstbracket = line.indexOf('[');
		return (firstdot > -1 && firstbracket == -1) || firstdot < firstbracket;
	}
}
