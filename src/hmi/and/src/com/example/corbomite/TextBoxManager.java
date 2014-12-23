package com.example.corbomite;

import android.app.Activity;
import android.util.Log;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.LinearLayout;



public class TextBoxManager extends CorbomiteWidgetManager {

	public TextBoxManager(CorbomiteDevice d, LayoutManager l) {
		super(d, l);
	}
	
	public void addTextBox(String name, String text, int lines, int weight){
		LinearLayout l = layout.getLayout();
		Activity act= layout.getActivity();
		EditText txt = new EditText(act);
		txt.setLayoutParams(new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT, 1f));
		txt.setText(text);
		txt.setLines(lines);
		
	    l.addView(txt);
	    add(new CorbomiteReference(name, txt));
	    System.out.println("Added text "+name);
	}
	
	public void removeAll(){
		for(CorbomiteReference w:widgets){
			if(w!=null)
				if(w.object!=null)
					if((ViewGroup) ((EditText)w.object).getParent()!=null)
						((ViewGroup) ((EditText)w.object).getParent()).removeView((EditText)w.object);
		}
		widgets.clear();
	}
	
	public int parsePayload(String commandLine) {
		String delims = "[ ]+";
		String[] tokens = commandLine.split(delims);
		if(tokens[0].equals("tio")){
			addTextBox(tokens[1], "", layout.h, layout.w);
			return 1;
		}
		if(tokens.length>=2){
			CorbomiteReference r = findByName(tokens[0]);
			if(r!= null){
				Log.i("TextIo", "Found widget "+tokens[0]);
				Log.i("TextIo", "CommandLine->"+commandLine);
				int i = commandLine.indexOf(tokens[0])+tokens[0].length()+1;
				
				String action = commandLine.substring(i,i+3);
				Log.i("TextIo","Action: "+action+" at "+Integer.toString(i));
				String text = new String("");
				if(commandLine.length()>i+3)
					text = commandLine.substring(i+3);
				
				if(action.equals("set")){
					((EditText)r.object).setText(text);
					((EditText)r.object).setSelection(((EditText)r.object).getText().length());
					return 1;
					
				}
				
				if(action.equals("app")){
					((EditText)r.object).append(text);
					((EditText)r.object).setSelection(((EditText)r.object).getText().length());
					return 1;
				}
			}
		}
		return 0;
	}

}
