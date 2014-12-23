package com.example.corbomite;

import android.os.Bundle;
import android.os.Handler;
import android.os.Message;


public class BusyHandler extends Handler {
	MainActivity m = null;
	  @Override
	  public void handleMessage(Message msg) {
		  Bundle b = msg.getData();
		  String stat = b.getString("string");
		  if(stat.equals("busy"))
		  		m.setBusyStatus(true);
		  else
			  	m.setBusyStatus(false);
	     }
	  public void setMainActivity(MainActivity mainActivity){
		  m = mainActivity;
	  }
}
