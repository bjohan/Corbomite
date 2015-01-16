package com.example.corbomite;

public class Point {
	float x;
	float y;
	
	public Point(){
		x = y = 0;
	}
	
	public Point(float x, float y){
		this.x=x;
		this.y=y;
	}
	
	public Point(String x, String y){
		this.x=Float.parseFloat(x);
		this.y=Float.parseFloat(y);
	}
}
