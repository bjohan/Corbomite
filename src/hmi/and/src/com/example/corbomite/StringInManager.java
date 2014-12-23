package com.example.corbomite;

import android.app.Activity;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

public class StringInManager extends CorbomiteWidgetManager{

	public StringInManager(CorbomiteDevice d, LayoutManager l){
		super(d, l);
	}
	
	public int setText(String name, String text) {
		CorbomiteReference r = findByName(name);
		if(r!= null){
			((TextView) r.object).setText(text);
			return 1;
		} else
			System.out.println("No text named "+name);
		return 0;
	}
	
	public void removeAll(){
		for(CorbomiteReference w:widgets){
			if(w!=null)
				if(w.object!=null)
					if((ViewGroup) ((TextView)w.object).getParent()!=null)
						((ViewGroup) ((TextView)w.object).getParent()).removeView((TextView)w.object);
		}
		widgets.clear();
	}
	
	public void addText(String name, String text, int weight){
		LinearLayout l = layout.getLayout();
		Activity act= layout.getActivity();
		TextView txt = new TextView(act);
		txt.setLayoutParams(new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT, weight));
		txt.setText(text);
	    l.addView(txt);
	    add(new CorbomiteReference(name, txt));
	    System.out.println("Added text "+name);
	}
	
	public int parsePayload(String commandLine) {
		String delims = "[ ]+";
		String[] tokens = commandLine.split(delims);
		if(tokens[0].equals("sin")){
			addText(tokens[1], "", layout.w);
			return 1;
		}
		if(tokens.length >= 1){
			CorbomiteReference r = findByName(tokens[0]);
			String text = "";
			if(tokens.length>=2)
				text=commandLine.substring(commandLine.indexOf(tokens[1]));
			if(r!=null){
				((TextView) r.object).setText(text);
				return 1;
			}
		}
		return 0;
	}
}
