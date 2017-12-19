package genericbiz.extensions.internals.filteredlist;

public class Node {
	Node[] children;
	int[] refs;
	String value;

	public Node(Node[] children, int[] refs, String value) {
		this.children = children;
		this.refs = refs;
		this.value = value;
	}
}
