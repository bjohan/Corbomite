package com.example.corbomite;


import java.util.ArrayList;
import java.util.List;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.util.Log;
import android.widget.ImageView;

public class CorbomitePlotRenderer extends ImageView{
		
		private int w = 0;
		private int h = 0;
		
		private float xmin = Float.NaN;
		private float xmax = Float.NaN;
		private float ymin = Float.NaN;
		private float ymax = Float.NaN;
		private float xs = 1;
		private float ys = 1;
		private float xo = 0;
		private float yo = 0;

		
		private List<Trace> traces = new ArrayList<Trace>();
	
	 	public CorbomitePlotRenderer(Context context) {
	        super(context);
	    }
	 	
	 
	 	public void addTrace(String name){
	 		traces.add(new Trace(name));
	 	}
	 	
	 	@Override
	 	protected void onSizeChanged(int w, int h, int oldw, int oldh){
	 		this.w = w;
	 		this.h = h;
	 		super.onSizeChanged(w, h, oldw, oldh);
	 	}
	 
	    @Override
	    protected void onDraw(Canvas canvas) {
	        // TODO Auto-generated method stub
	        Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);
	        super.onDraw(canvas);
	        computeScale();
	        drawScale(canvas);
	        
	        //Draw legend
	        int offs = 20;
	        for(Trace t : traces){
	        	p.setARGB(255, t.r, t.g, t.b);
	        	canvas.drawText(t.legend,w-30, offs, p);
	        	offs+=20;
	        }
	        for(Trace t : traces){
	        	p.setARGB(255, t.r, t.g, t.b);
	        	Point lpo = null; 
	        	for(Point po : t.trace){
	        		if(lpo != null)
	        			drawGraphLine(lpo.x, lpo.y, po.x, po.y, p, canvas);
	        		lpo = po;
	        	}
	        }
	    }
	    
	    protected void drawGraphLine(float x0, float y0, float x1, float y1, Paint p, Canvas c){
	    	c.drawLine((int)(x0*xs+xo), h-(int)(y0*ys+yo), (int)(x1*xs+xo), h-(int)(y1*ys+yo), p);
	    }
	    protected void drawGraphText(String t, float x, float y, Paint p, Canvas c){
	    	c.drawText(t, (int)(x*xs+xo), h-(int)(y*ys+yo),p);
	    	
	    }
	    
	    protected void drawScale(Canvas canvas){
	    	float pixelsMin = 40;
	    	float pixelsMax = 100;
	    	
	    	float minGrat = pixelsMin/xs;
	    	float maxGrat = pixelsMax/xs;
	    	float scaleRes = get125NumberInRange(minGrat, maxGrat);
	    	float scaleStart = (float) (Math.ceil(xmin/scaleRes)*scaleRes);
	    	float scaleStop = (float) (Math.ceil(xmax/scaleRes)*scaleRes);
	    	Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);
	    	drawXScale(scaleStart, scaleRes, scaleStop, p, canvas);
	    	
	    	minGrat = pixelsMin/ys;
	    	maxGrat = pixelsMax/ys;
	    	scaleRes = get125NumberInRange(minGrat, maxGrat);
	    	scaleStart = (float) (Math.ceil(ymin/scaleRes)*scaleRes);
	    	scaleStop = (float) (Math.ceil(ymax/scaleRes)*scaleRes);
	    	
	    	drawYScale(scaleStart, scaleRes, scaleStop, p, canvas);
	    }
	    
	    protected void drawXScale(float start, float step, float stop, Paint p, Canvas c){
	    	if(start != start || step!=step || stop!=stop) return;
	    	if(step < 0 ) return;
	    	
	    	while(start <= stop){
	    		drawGraphLine(start, ymin, start, ymax, p, c);
	    		drawGraphText(Float.toString(start), start, ymin, p, c);
	    		start+=step;
	    	}
	    }
	    
	    protected void drawYScale(float start, float step, float stop, Paint p, Canvas c){
	    	if(start != start || step!=step || stop!=stop) return;
	    	if(step < 0 ) return;
	    	
	    	while(start <= stop){
	    		drawGraphLine(xmin, start, xmax, start, p, c);
	    		drawGraphText(Float.toString(start), xmin, start, p, c);
	    		start+=step;
	    	}
	    }
	    
	    protected float get125NumberInRange(float min, float max){
	    	if(min!= min || max != max) return 1;
	    	float num = (float) Math.pow(10,Math.floor(Math.log10(min)));
	    	
	    	Log.i("scale", "In 125 Min:"+Float.toString(min)+" max "+Float.toString(max)+" num "+Float.toString(num));
	     	if(num <= 0)
	    		return 1.0f;
	    	while(true){
	    		if(num >= min)
	    			return num;
	    		if(num*2>=min)
	    			return num*2;
	    		if(num*5>=min)
	    			return num*5;
	    		num*=10;
	    	}
	    }
	    
	    protected void computeScale(){
	    	//Find min and max
	    	xmin = Float.NaN;
	    	xmax = Float.NaN;
	    	ymin = Float.NaN;
	    	ymax = Float.NaN;
	    	for(Trace t : traces){
	    		for(Point p : t.trace){
	    			if(xmin != xmin){
	    				xmin = xmax = p.x;
	    				ymin = ymax = p.y;
	    			}
	    			if(p.x < xmin)
	    				xmin = p.x;
	    			if(p.x > xmax)
	    				xmax =p.x;
	    				
	    			if(p.y < ymin)
	    				ymin = p.y;
	    			if(p.y > ymax)
	    				ymax =p.y;
	    		}
	    	}
	    	
	    	xs = w/(xmax-xmin);
		    ys = h/(ymax-ymin);
		    xo = -xmin*xs;
		    yo = -ymin*ys;
		    
	    }
		
		public Trace getTraceByName(String name){
			//Log.i("plot", "looking for: "+name);
			for(Trace t : traces){
				//Log.i("plot", "comparing to: "+t.name);
				if(t.name.equals(name))
					return t;
			}
			return null;
		}
}
