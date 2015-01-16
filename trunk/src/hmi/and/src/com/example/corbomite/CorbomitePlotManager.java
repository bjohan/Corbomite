package com.example.corbomite;

import android.app.Activity;
import android.graphics.Point;
import android.opengl.GLSurfaceView;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.Display;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.LinearLayout;



public class CorbomitePlotManager extends CorbomiteWidgetManager {

	public CorbomitePlotManager(CorbomiteDevice d, LayoutManager l) {
		super(d, l);
	}

	
	
	public void removeAll(){
		for(CorbomiteReference w:widgets){
			if(w!=null)
				if(w.object!=null)
					if((ViewGroup) ((CorbomitePlotRenderer)w.object).getParent()!=null)
							((ViewGroup) ((CorbomitePlotRenderer)w.object).getParent()).removeView((CorbomitePlotRenderer)w.object);
		}
		widgets.clear();
	}
	
	public CorbomitePlotRenderer addPlot(String name, int widthWeight, int height){
		LinearLayout l = layout.getLayout();
		Activity act= layout.getActivity();
		CorbomitePlotRenderer plotView = new CorbomitePlotRenderer(act);
		
		DisplayMetrics metrics = new DisplayMetrics();
		act.getWindowManager().getDefaultDisplay().getMetrics(metrics);

		int h=metrics.heightPixels;
		
		plotView.setLayoutParams(new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, height*h/100, 1));
	    l.addView(plotView);

	    add(new CorbomiteReference(name, plotView));
	    Log.i("plot","Added plot "+name);
	    return plotView;
	}

	
	
	public int parsePayload(String commandLine) {
		String delims = "[ ]+";
		String[] tokens = commandLine.split(delims);
		if(tokens[0].equals("plot")){
			String i = layout.getInformation();
			if(!i.equals(""))
				layout.addText(i);
			layout.continueLine = false;
			
			layout.setLastPlot(addPlot("", layout.w, layout.h));
			return 1;
		}
		if(tokens[0].equals("tin")){
			CorbomitePlotRenderer p = layout.getLastPlot();
			if(p == null){
				layout.setLastPlot(addPlot("", layout.w, layout.h));
				p = layout.getLastPlot();
			}
			
			String i = layout.getInformation();
			p.addTrace(tokens[1]);
			Log.i("plot", "Adding trace "+tokens[1]);
			return 1;
		}
		
		if(tokens.length >= 2){
			CorbomitePlotRenderer p = layout.getLastPlot();
			if(p != null){
				Trace t = p.getTraceByName(tokens[0]);
				if(t != null ){
					//Log.i("plot", "fond trace"+tokens[0]);
					if(tokens[1].equals("clr")){
						Log.i("plot", "clearing trace"+t.name);
						t.clear();
					return 1;
					}else if(tokens.length >= 3){
						t.add(tokens[1], tokens[2]);
						//Log.i("plot", "adding data to trace"+t.name);
						p.invalidate();
						return 1;
					}
				}
			}
		}
		
		/*if(tokens.length >= 2){
			CorbomiteReference r = findByName(tokens[0]);
			//Log.i("plot", "Looking for "+tokens[0]);
			if(r!=null){
				Log.i("plot", "Plot found "+tokens[0]);
				Trace trace = ((CorbomitePlotRenderer) r.object).getTraceByName(tokens[1]);
				if(trace == null){
					Log.i("plot", "Command for unknown trace, creating");
					((CorbomitePlotRenderer) r.object).addTrace(tokens[1]);
					trace = ((CorbomitePlotRenderer) r.object).getTraceByName(tokens[1]);
				}
				if(trace != null){
					if(tokens[2].indexOf("add")>=0){
						//Log.i("plot", "Adding trace coordinates");
						trace.add(tokens[3], tokens[4]);

					} else if(tokens[2].indexOf("col")>=0){
						trace.setRgb(Integer.parseInt(tokens[3]),Integer.parseInt(tokens[4]),Integer.parseInt(tokens[5]));
						//trace.clear();
					} else if(tokens[2].indexOf("clr")>=0){
						trace.clear();
					} else if(tokens[2].indexOf("leg")>=0){
						trace.setLegend(tokens[3]);
						//trace.clear();
					} else {
						Log.i("plot", "wtf, uknown command! "+ tokens[2]);
					}
				} else {
				
					Log.i("plot", "No trace in "+tokens[0]+" named "+tokens[1]);
				}
				((CorbomitePlotRenderer)r.object).invalidate();
				return 1;
			}
		}*/
		return 0;
	}

}
