package genericbiz.util;

import java.io.InputStream;
import java.io.InputStreamReader;

public class FileReader {
	String filename = null;
	
	public FileReader(String filename) {
		this.filename = filename;
	}
	
	public String readFile() {
		InputStream input = this.getClass().getResourceAsStream(filename);
		if(input == null)
			return null;
		InputStreamReader reader = new InputStreamReader(input);
		int len = 0;
		char[] data = new char[64];
		StringBuffer buff = new StringBuffer();
		try {
			while ((len = reader.read(data)) != -1) {
				buff.append(data, 0, len);
			}
		} catch(Exception e) {
		} finally {
			try {
				reader.close();
			} catch (Exception e) {
			}
		}
		return buff.toString();
	}
}
