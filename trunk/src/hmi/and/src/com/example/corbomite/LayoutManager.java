package com.example.corbomite;

import android.app.Activity;
import android.util.Log;
import android.view.ViewGroup;
import android.view.ViewGroup.LayoutParams;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.example.corbomite.R;

public class LayoutManager extends CorbomiteWidgetManager {

	LinearLayout current = null;
	Activity activity = null;
	int w = 1;
	int h = 1;
	String information = "";
	boolean continueLine = false;
	StringInManager textManager = null;
	CorbomitePlotRenderer lastPlot = null;
	
	public void setLastPlot(CorbomitePlotRenderer p){
		lastPlot = p;
	}
	
	CorbomitePlotRenderer getLastPlot(){
		return lastPlot;
	}
	
	public void setTextManager(StringInManager m){
		textManager = m;
	}
	
	
	public LayoutManager(CorbomiteDevice d, Activity mainActivity) {
		super(d, null);
		activity = mainActivity;
	}
	
	public void removeAll(){
		for(CorbomiteReference w:widgets){
			if(w!=null)
				if(w.object!=null)
					if((ViewGroup) ((LinearLayout)w.object).getParent()!=null)
							((ViewGroup) ((LinearLayout)w.object).getParent()).removeView((LinearLayout)w.object);
		}
		widgets.clear();
	}
	
	public void addText(String text){
		boolean c = continueLine;
		if(textManager!= null)
			textManager.addText("", text, 1);
		continueLine = c;
	}
	
	public int parsePayload(String commandLine) {
		String delims = "[ ]+";
		String[] tokens = commandLine.split(delims);
		if(tokens[0].equals("w")){
			w = Integer.parseInt(tokens[1]);
			h = Integer.parseInt(tokens[2]);
			Log.i("hints", "Weight hint: width:"+Integer.toString(w)+" height: "+Integer.toString(h));
			return 1;
		} else if(tokens[0].equals("info")){
			information = commandLine.substring(commandLine.indexOf("info")+5);
			Log.i("hints", "Information hint: "+information);
			return 1;
		}else if (tokens[0].equals("cont")){
			Log.i("hints", "Line continuation");
			continueLine = true;
			return 1;
		}
		return 0;
	}
	
	public void addLayout(){
		LinearLayout l = (LinearLayout)activity.findViewById(R.id.configurable_layout);
		LinearLayout nl = new LinearLayout(activity);
		nl.setLayoutParams(new LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT));
		nl.setOrientation(LinearLayout.HORIZONTAL);
		l.addView(nl);
		current = nl;
	}
	
	public String getInformation(){
		String a = information;
		information = "";
		return a;
	}
	

	public LinearLayout getLayout(){
		if(continueLine){
			Log.i("layout","Line continuation hint");
			continueLine = false;
			return current;
		}else{
			Log.i("layout","Creating nu line, no line continuation hint.");
			addLayout();
			return current;
		}
			
	}
	
	public Activity getActivity(){
		return activity;
	}
}
