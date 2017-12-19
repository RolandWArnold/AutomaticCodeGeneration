package genericbiz.extensions.internals.filteredlist;

import java.util.Vector;

public class NodeHandler {
	Vector root;
	Vector cache = new Vector();
	Vector trail = new Vector();
	int[] indexNumbers;
	int offset = 0;
	String input = "";

	public NodeHandler(Vector root, int[] indexArray) {
		this.root = root;
		this.indexNumbers = indexArray;
	}

	int[] setWord(String word) {
		clear();
		for(int i = 0; i < word.length(); i++)
			addChar(word.charAt(i));
		return getCurrentMatches();
	}

	String getWord() {
		return input;
	}
	
	int[] getCurrentMatches() {
		return getCurrentMatches(null);
	}

	int[] getCurrentMatches(int[] whiteList) {
		if(whiteList == null)
			return (cache.size() < 1) ? indexNumbers :
				(int[])cache.lastElement();
		else
			return (cache.size() < 1) ? whiteList :
				union((int[])cache.lastElement(), whiteList);
	}
	
	int[] union(int[] one, int[] two) {
		if(one == null || two == null)
			return null;
		int[] smaller = one;
		int[] bigger = two;
		if(one.length > two.length) {
			smaller = two;
			bigger = one;
		}
		for(int i = 0; i < one.length; i++)
			for(int j = i; j < one.length; j++)
				if(one[i] > one[j]) {
					int tmp = one[i];
					one[i] = one[j];
					one[j] = tmp;
				}
		for(int i = 0; i < two.length; i++)
			for(int j = i; j < two.length; j++)
				if(two[i] > two[j]) {
					int tmp = two[i];
					two[i] = two[j];
					two[j] = tmp;
				}
		int[] tmp = new int[smaller.length];
		int count = 0;
		int j = -1;
		for(int i = 0; i < smaller.length; i++) {
			while(++j < bigger.length) {
				if(smaller[i] == bigger[j]) {
					tmp[count++] = smaller[i];
					break;
				}
				else if(smaller[i] < bigger[j]) {
					j--;
					break;
				}
			}
		}
		//System.arraycopy(children, 0, newChildren, 0, children.length);
		int[] result = new int[count]; //no way of returning a portion of an array
		for(int i = 0; i < count; i++)
			result[i] = tmp[i];
		for(int i = 0; i < result.length; i++)
			for(int k = i; k < result.length; k++)
				if(result[i] > result[k]) {
					int val = result[i];
					result[i] = result[k];
					result[k] = val;
				}
		return result;
	}
    
	void clear() {
		input = "";
		offset = 0;
		trail.removeAllElements();
		cache.removeAllElements();
	}

	void addChar(char c) {
		input += c;
		if(input.length() == 1) { /* i.e. the first character */
			for(int i = 0; i < root.size(); i++) {
				Node n = (Node)root.elementAt(i);
				if(n != null && n.value.charAt(0) == c) {
					offset = 0;
					trail.addElement(n);
					cache.addElement(n.refs);
					return;
				}
			}
			trail.addElement(null);
			cache.addElement(new int[0]);
			return;
		} else if(trail.lastElement() == null) { /* no match on previous */
			trail.addElement(null);
			return;
		} else {
			Node current = (Node)trail.lastElement();
			if(offset < current.value.length() - 1) { /* stay on current node */
				if(current.value.charAt(offset + 1) == c) {
					offset++;
					return;
				}
				trail.addElement(null);
				cache.addElement(new int[0]);
				return;
			} else { /* look for match in children */
				for(int i = 0; i < current.children.length; i++) {
					Node n = current.children[i];
					if(n != null && n.value.charAt(0) == c) {
						offset = 0;
						trail.addElement(n);
						cache.addElement(n.refs);
						return;
					}
				}
				trail.addElement(null);
				cache.addElement(new int[0]);
				return;
			}
		}
	}

	void popChar() {
		if(input.length() <= 1) { /* input already empty */
			input = "";
			offset = 0;
			trail.removeAllElements();
			cache.removeAllElements();
		} else {
			input = input.substring(0, input.length() - 1);
			if(trail.lastElement() == null) {
				trail.removeElementAt(trail.size() - 1);
				if(trail.lastElement() != null) {
					cache.removeElementAt(cache.size() - 1);
				}
			} else if(offset == 0) {
				trail.removeElementAt(trail.size() - 1);
				if(trail.lastElement() != null) {
					offset = ((Node)trail.lastElement()).value.length() - 1;
					cache.removeElementAt(cache.size() - 1);
				}
			} else if(offset > 0) {
				offset -= 1;
			}
		}
	}
}
