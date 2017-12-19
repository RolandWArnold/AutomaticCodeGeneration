package genericbiz.extensions.internals.filteredlist;

import java.util.Vector;

public class StringFilter {
	String resource_name;
	Vector tree;
	String[] indexStrings;
	String[] codeStrings;
	int[] indexNumbers;
	String totalInput;
	Vector inputStrings; // "my word" -> "my", "word"
	Vector referenceMatches; // [1,2,4], [4,7]
	NodeHandler nodeHandler;
	int[] unionList;

	public StringFilter(String resource_name) {
		this.resource_name = resource_name;
		TreeMaker treeMaker = new TreeMaker(resource_name);
		tree = treeMaker.getTree();
		indexStrings = treeMaker.getIndexArray();
		codeStrings = treeMaker.getCodeArray();
		this.indexNumbers = new int[indexStrings.length];
		for(int i = 0; i < indexNumbers.length; i++) {
			this.indexNumbers[i] = i;
		}
		nodeHandler = new NodeHandler(tree, indexNumbers);
		clear();
	}
	
	public String resource() {
		return this.resource_name;
	}

	public String getTotalInput() {
		return totalInput;
	}

	public void clear() {
		unionList = null;
		nodeHandler.clear();
		totalInput = "";
		inputStrings = new Vector();// "my word" -> "my", "word"
		referenceMatches = new Vector();// [1,2,4], [4,7]
	}

	public String[] getCurrentMatches() {
		if(totalInput.length() == 0) // special case we can handle quickly
			return indexStrings;
		int[] refs = nodeHandler.getCurrentMatches(unionList);
		String[] strings = new String[refs.length];
		for(int i = 0; i < refs.length; i++) {
			strings[i] = indexStrings[refs[i]];
		}
		return strings;
	}
	
	//Binary search for codeString based on keyString
	public String getStringCode(String key) {
		int lower = 0;
		int upper = indexStrings.length;
		while(true) {
			int middle = (upper + lower) / 2;
			int result = key.compareTo(indexStrings[(upper + lower) / 2]);
			if(result < 0)
				upper = middle;
			else if(result > 0)
				lower = middle;
			else
				return codeStrings[middle];
		}
	}
	
//	void rawPrint(int[] arr) {
//		if(arr != null) {
//			for(int i = 0; i < arr.length; i++) {
//				System.out.print(arr[i]);
//				System.out.print(" ");
//			}
//			System.out.println();
//		}
//	}
	
	public String[] addChar(char c) {
		totalInput += c;
		if(c != ' ') {
			nodeHandler.addChar(c);
		} else if(nodeHandler.getWord().length() > 0) {
			inputStrings.addElement(nodeHandler.getWord());
			unionList = nodeHandler.getCurrentMatches(unionList);
			referenceMatches.addElement(unionList);
			nodeHandler.clear();
		}
		return getCurrentMatches();
	}

	public String[] popChar() {
		if(totalInput.length() <= 1) {
			clear();
			return getCurrentMatches();
		}
		char deletedC = totalInput.charAt(totalInput.length() - 1);
		totalInput = totalInput.substring(0, totalInput.length() - 1);
		char lastC = totalInput.charAt(totalInput.length() - 1);
		if(deletedC == ' ' && lastC == ' ') {
			return getCurrentMatches();
		} else if(deletedC != ' ' && lastC != ' ') {
			nodeHandler.popChar();
			return getCurrentMatches();
		} else if(deletedC == ' ' && lastC != ' ') {
			nodeHandler.setWord((String)inputStrings.lastElement());
			inputStrings.removeElementAt(inputStrings.size() - 1);
			referenceMatches.removeElementAt(referenceMatches.size() - 1);
			if(referenceMatches.size() != 0) {
				unionList = (int[])referenceMatches.lastElement();
			} else {
				unionList = null;
			}
		} else {
			nodeHandler.popChar();
		}
		return getCurrentMatches();
	}
}
