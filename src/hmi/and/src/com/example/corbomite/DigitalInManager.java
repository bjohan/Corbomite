package com.example.corbomite;

import android.app.Activity;
import android.util.Log;
import android.view.ViewGroup;
import android.widget.CheckBox;
import android.widget.LinearLayout;

public class DigitalInManager extends CorbomiteWidgetManager {

	public DigitalInManager(CorbomiteDevice d, LayoutManager l) {
		super(d, l);
		// TODO Auto-generated constructor stub
	}
	public void removeAll(){
		for(CorbomiteReference w:widgets){
			if(w!=null)
				if(w.object!=null)
					if((ViewGroup) ((CheckBox)w.object).getParent()!=null)
							((ViewGroup) ((CheckBox)w.object).getParent()).removeView((CheckBox)w.object);
		}
		widgets.clear();
	}
	
	public void addCheckBox(String name){
		 LinearLayout l = layout.getLayout();
		 Activity act= layout.getActivity();
		 CheckBox box = new CheckBox(act); //(act, null,android.R.attr.progressBarStyleHorizontal);
		 box.setLayoutParams(new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT, layout.w));
		 box.setEnabled(false);
	     l.addView(box);
	     add(new CorbomiteReference(name, box));
	     Log.i("DigitalIn","Added checkbox: "+name);
	}
	
	public int parsePayload(String commandLine) {
		String delims = "[ ]+";
		String[] tokens = commandLine.split(delims);
		int current;
		
		if(tokens[0].equals("din")){
			String infoText = layout.getInformation();
			if(infoText.equals(""))
				infoText = tokens[1];
			layout.addText(infoText);
			layout.continueLine = true;
			addCheckBox(tokens[1]);
			return 1;
		}
		
		if(tokens.length >= 2){
			CorbomiteReference r = findByName(tokens[0]);
			if(r!=null){
				try{
					current = Integer.parseInt(tokens[1]);
				}catch (NumberFormatException e){
					Log.i("DigitalIn","Current was not a number: "+tokens[1]);
					return 0;
				}
				((CheckBox)r.object).setChecked(current!= 0);
				if(tokens.length > 2)
					Log.i("DigitalIn", "Warning: more than two tokens: "+commandLine);
				return 1;
			}
		}
		return 0;
	}
}
