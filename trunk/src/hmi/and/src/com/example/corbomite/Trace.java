package com.example.corbomite;

import java.util.ArrayList;
import java.util.List;

public class Trace {
	List<Point> trace = new ArrayList<Point>();
	String name = null;
	String legend = "";
	public int r = 0;
	public int g = 0;
	public int b = 0;
	
	public void setRgb(int r, int g, int b){
 		this.r = r;
 		this.g = g;
 		this.b = b;
 	}
 	
	
	public Trace(String name){
		this.name = name;
	}
	
	public void setLegend(String legend){
		this.legend = legend;
	}
	
	public void clear(){
		trace.clear();
	}
	public void add(Point p){
		trace.add(p);
	}
	public void add(String x, String y){
		trace.add(new Point(x, y));
	}
}
