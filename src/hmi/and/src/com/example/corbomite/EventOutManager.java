package com.example.corbomite;

import android.app.Activity;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.LinearLayout;

public class EventOutManager extends CorbomiteWidgetManager implements View.OnClickListener{	
	
	public EventOutManager(CorbomiteDevice d, LayoutManager l){
		super(d, l);
	}
	
	public void onClick(View v) {
		CorbomiteReference r = findByObject(v);
		if(r != null){
				send(r.name);
				Log.i("EventOut","Button was pressed, sending: "+r.name);
		}
	}
	
	public void removeAll(){
		for(CorbomiteReference w:widgets){
			if(w!=null)
				if(w.object!=null)
					if((ViewGroup) ((Button)w.object).getParent()!=null)
						((ViewGroup) ((Button)w.object).getParent()).removeView((Button)w.object);
		}
		widgets.clear();
	}
	
	public void addButton(String name, String text, int weight){
		if(text.equals("internal"))
			return;
		 Log.i("EventOut", "Name: "+name+" Text: "+text);
		 LinearLayout l = layout.getLayout();
		 Activity act= layout.getActivity();
		 Button btn = new Button(act);
		 btn.setLayoutParams(new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT, weight));
		 btn.setOnClickListener(this);
	     btn.setText(text);
	     btn.setId(3);
	     l.addView(btn);
	     add(new CorbomiteReference(name, btn));
	     System.out.println("Added button "+name);
	}

	public int parsePayload(String commandLine) {
		String delims = "[ ]+";
		String[] tokens = commandLine.split(delims);
		
		if(tokens.length >= 2){
			if(tokens[1].equals("info")) //Ignore out event
				return 0;
			if(tokens[0].equals("eout")){
				String text = layout.getInformation();
				if(text.equals(""))
					text = tokens[1];
				Log.i("EventOut", "Adding button with text: "+ text);
				addButton(tokens[1], text, layout.w);
				return 1;
			}
		
			CorbomiteReference r = findByName(tokens[0]);
			if(r!=null){
				Log.i("EventOut", "Got event "+tokens[0]);
				((Button) r.object).setText(commandLine.substring(commandLine.indexOf(tokens[1])));
				return 1;
			} 
		}
		return 0;
	}

}
