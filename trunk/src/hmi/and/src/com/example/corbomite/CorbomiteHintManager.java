package com.example.corbomite;

import android.widget.SeekBar;

public class CorbomiteHintManager extends CorbomiteWidgetManager{

	public CorbomiteHintManager(CorbomiteDevice d, LayoutManager l) {
		super(d, l);
		// TODO Auto-generated constructor stub
	}

	
	public int parsePayload(String commandLine) {
		String delims = "[ ]+";
		String[] tokens = commandLine.split(delims);

		if(tokens[0].equals("info")){
			
			//addSeekBar(tokens[1], max, 0, 1);
			return 1;
		}else if(tokens.length >= 2){
			CorbomiteReference r = findByName(tokens[0]);
			if(r!=null){
			}
		}
		return 0;
	}

}
