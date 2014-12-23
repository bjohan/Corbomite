package com.example.corbomite;


import android.app.Activity;
import android.util.Log;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.SeekBar;
import android.widget.SeekBar.OnSeekBarChangeListener;

public class AnalogOutManager extends CorbomiteWidgetManager implements OnSeekBarChangeListener {
	public AnalogOutManager(CorbomiteDevice d, LayoutManager l){
		super(d, l);
	}
	
	public int setValue(String name, int value) {
		CorbomiteReference r = findByName(name);
		if(r!=null) {
			((SeekBar)r.object).setProgress(value);
			return 1;
		}
		return 0;
	}
	public void removeAll(){
		for(CorbomiteReference w:widgets){
			if(w!=null)
				if(w.object!=null)
					if((ViewGroup) ((SeekBar)w.object).getParent()!=null)
						((ViewGroup) ((SeekBar)w.object).getParent()).removeView((SeekBar)w.object);
		}
		widgets.clear();
	}
	public void addSeekBar(String name, int max, int current, int weight){
		LinearLayout l = layout.getLayout();
		Activity act= layout.getActivity();
		SeekBar bar = new SeekBar(act);
		bar.setLayoutParams(new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT,weight));
		bar.setIndeterminate(false);
		bar.setMax(max);
		bar.setProgress(current);
		bar.setOnSeekBarChangeListener(this);
	    l.addView(bar);
	    add(new CorbomiteReference(name, bar));
	    Log.i("AnalogOut", "Added seekbar "+name);
	}

	@Override
	public void onProgressChanged(SeekBar seekBar, int progress,
			boolean fromUser) {
		Log.i("AnalogOut", "seekbar released");
		CorbomiteReference r = findByObject(seekBar);
		if(r!= null){
			if(fromUser)
				send(r.name+" "+((SeekBar)r.object).getProgress());
			Log.i("AnalogOut", "Sending: "+r.name+" "+((SeekBar)r.object).getProgress());
		} 
		
	}

	@Override
	public void onStartTrackingTouch(SeekBar seekBar) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onStopTrackingTouch(SeekBar seekBar) {
		Log.i("AnalogOut", "seekbar released");
		CorbomiteReference r = findByObject(seekBar);
		if(r!= null){
			send(r.name+" "+((SeekBar)r.object).getProgress());
			Log.i("AnalogOut", "Sending: "+r.name+" "+((SeekBar)r.object).getProgress());
		}
	}

	
	public int parsePayload(String commandLine) {
		String delims = "[ ]+";
		String[] tokens = commandLine.split(delims);
		int current;
		int max;
		int min;
		if(tokens[0].equals("aout")){
			try{
				max = Integer.parseInt(tokens[6]);
			}catch (NumberFormatException e){
				Log.i("AnalogOut", "Max was not a number: "+tokens[6]);
				return 0;
			}
			try{
				current = Integer.parseInt(tokens[5]);
			}catch (NumberFormatException e){
				Log.i("AnalogOut", "Current was not a number: "+tokens[5]);
				return 0;
			}
			boolean c = layout.continueLine;
			String i = layout.getInformation();
			if(!i.equals(""))
				layout.addText(i);
			layout.continueLine = c;
			addSeekBar(tokens[1], max, 0, layout.w);
			return 1;
		}else if(tokens.length >= 2){
			CorbomiteReference r = findByName(tokens[0]);
			if(r!=null){
				try{
					current = Integer.parseInt(tokens[1]);
				}catch (NumberFormatException e){
					Log.i("AnalogOut", "Current was not a number: "+tokens[1]);
					return 0;
				}
				((SeekBar)r.object).setProgress(current);
				if(tokens.length > 2)
					Log.i("AnalogOut", "Warning: more than two tokens: "+commandLine);
				return 1;
			}
		}
		return 0;
	}
}
