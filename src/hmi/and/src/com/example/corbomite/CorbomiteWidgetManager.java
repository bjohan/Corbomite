package com.example.corbomite;

import java.util.ArrayList;
import java.util.List;


public abstract class CorbomiteWidgetManager {
	public CorbomiteDevice dev;
	public LayoutManager layout;
	public List<CorbomiteReference> widgets = new ArrayList<CorbomiteReference>();
	
	public CorbomiteWidgetManager(CorbomiteDevice d, LayoutManager l){
		setCorbomiteDevice(d);
		setLayoutManager(l);
	}
	
	
	public void setLayoutManager(LayoutManager l){
		layout = l;
	}
	
	public void setCorbomiteDevice(CorbomiteDevice d){
		dev = d;
	}
	
	public void add(CorbomiteReference widget){
		widgets.add(widget);
	}
	
	CorbomiteReference findByName(String s){
		for(CorbomiteReference w: widgets){
			if(w.name.equals(s)){
				return w;
			}
		}
		return null;
	}
	
	CorbomiteReference findByObject(Object object){
		for(CorbomiteReference w: widgets){
			if(w.object == object){
				return w;
			}
		}
		return null;
	}
	
	CorbomiteReference getLast(Object object){
		if (widgets.size() == 0)
			return null;
		return widgets.get(widgets.size()-1);
	}
	
	public void send(String s){
		if(dev != null){
			dev.transmitData(s);
		} else {
			System.out.println("Corbomite device is null");
		}
	}
	
	public void sendIfIdle(String s){
		if(dev != null){
			dev.transmitDataIfIdle(s);
		} else {
			System.out.println("Corbomite device is null");
		}
	}
}
