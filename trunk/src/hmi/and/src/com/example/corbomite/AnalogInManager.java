package com.example.corbomite;

import android.app.Activity;
import android.util.Log;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.ProgressBar;

public class AnalogInManager extends CorbomiteWidgetManager{
	public AnalogInManager(CorbomiteDevice d, LayoutManager l){
		super(d, l);
	}
	public void removeAll(){
		for(CorbomiteReference w:widgets){
			if(w!=null)
				if(w.object!=null)
					if((ViewGroup) ((ProgressBar)w.object).getParent()!=null)
							((ViewGroup) ((ProgressBar)w.object).getParent()).removeView((ProgressBar)w.object);
		}
		widgets.clear();
	}
	public int setValue(String name, int value) {
		CorbomiteReference r = findByName(name);
		if(r!=null){
			((ProgressBar)(r.object)).setProgress(value);
			return 1;
		}
		return 0;
	}
	
	public void addProgressBar(String name, int max, int current, int weight){
		 LinearLayout l = layout.getLayout();
		 Activity act= layout.getActivity();
		 ProgressBar bar = new ProgressBar(act, null,android.R.attr.progressBarStyleHorizontal);
		 bar.setLayoutParams(new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT, weight));
		 bar.setIndeterminate(false);
		 bar.setMax(max);
		 bar.setProgress(current);
	     l.addView(bar);
	     add(new CorbomiteReference(name, bar));
	     Log.i("AnalogIn","Added pbar: "+name+" max: "+Integer.toString(max)+" current: "+Integer.toString(current));
	}
	
	public int parsePayload(String commandLine) {
		String delims = "[ ]+";
		String[] tokens = commandLine.split(delims);
		int max;
		int current;
		
		if(tokens[0].equals("ain")){
			try{
				max = Integer.parseInt(tokens[6]);
			}catch (NumberFormatException e){
				Log.i("AnalogIn","Max was not a number: "+tokens[6]);
				return 0;
			}
			try{
				current = Integer.parseInt(tokens[5]);
			}catch (NumberFormatException e){
				Log.i("AnalogIn","Current was not a number: "+tokens[4]);
				return 0;
			}
			String i = layout.getInformation();
			if(!i.equals(""))
				layout.addText(i);
			addProgressBar(tokens[1], max, 0, layout.w);
			return 1;
		}
		
		
		if(tokens.length >= 2){
			CorbomiteReference r = findByName(tokens[0]);
			if(r!=null){
				try{
					current = Integer.parseInt(tokens[1]);
				}catch (NumberFormatException e){
					Log.i("AnalogIn","Current was not a number: "+tokens[1]);
					return 0;
				}
				((ProgressBar)r.object).setProgress(current);
				if(tokens.length > 2)
					Log.i("AnalogIn", "Warning: more than two tokens: "+commandLine);
				return 1;
			}
		}
		return 0;
	}
}
