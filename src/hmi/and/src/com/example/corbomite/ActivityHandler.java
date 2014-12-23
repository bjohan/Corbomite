package com.example.corbomite;

import android.os.Bundle;
import android.os.Handler;
import android.os.Message;

public class ActivityHandler extends Handler {
	MainActivity m = null;
	  @Override
	  public void handleMessage(Message msg) {
		  Bundle b = msg.getData();
		  m.parsePayload(b.getString("string"));
	     }
	  public void setMainActivity(MainActivity mainActivity){
		  m = mainActivity;
	  }
}
