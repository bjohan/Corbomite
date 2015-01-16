package com.example.corbomite;

import java.util.List;
import com.example.corbomite.R;

import android.os.Bundle;
import android.app.Activity;
import android.app.AlertDialog;
import android.bluetooth.BluetoothSocket;
import android.content.DialogInterface;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.Spinner;
import android.widget.AdapterView.OnItemSelectedListener;

public class MainActivity extends Activity implements OnItemSelectedListener{

	ActivityHandler commandHandler = new ActivityHandler();
	BusyHandler busyHandler = new BusyHandler();
	CorbomiteDevice corbomiteDevice = new CorbomiteDevice(commandHandler, busyHandler);
	Thread corbomiteThread = new Thread( corbomiteDevice);
	
	public LinearLayout currentLayout = null;
	LayoutManager layoutManager = new LayoutManager(corbomiteDevice, this);
	StringInManager stringInManager = new StringInManager(corbomiteDevice, layoutManager);
	AnalogInManager barManager = new AnalogInManager(corbomiteDevice, layoutManager);
	EventOutManager buttonManager = new EventOutManager(corbomiteDevice, layoutManager);
	AnalogOutManager analogOutManager = new AnalogOutManager(corbomiteDevice, layoutManager);
	AnalogInManager analogInManager = new AnalogInManager(corbomiteDevice, layoutManager);
	DigitalOutManager digitalOutManager = new DigitalOutManager(corbomiteDevice, layoutManager);
	DigitalInManager digitalInManager = new DigitalInManager(corbomiteDevice, layoutManager);
	TextBoxManager textBoxManager = new TextBoxManager(corbomiteDevice, layoutManager);
	CorbomitePlotManager plotManager = new CorbomitePlotManager(corbomiteDevice, layoutManager);
	BluetoothManager bluetoothManager = new BluetoothManager();
	
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		
		setContentView(R.layout.activity_main);
		
		buildBluetoothList();
		commandHandler.setMainActivity(this);
		busyHandler.setMainActivity(this);
		layoutManager.addLayout();
		layoutManager.setTextManager(stringInManager);
		corbomiteThread.start();
		//plotManager.addSeekBar("Plotten");
		//buttonManager.addButton("ralf", "rilf", 1);
		//parsePayload("layout\r\nbutton ralf 1 riasdflf 1");
		System.out.println("Application started");
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}
	
	public void setBusyStatus(boolean busy){
		ProgressBar pbar = (ProgressBar) findViewById(R.id.busyIndicator);
		if(busy){
			System.out.println("Showing spinner");
			pbar.setVisibility(View.VISIBLE);
		}
		else{
			System.out.println("Hiding spinning thingy");
			pbar.setVisibility(View.INVISIBLE);
		}
	}
	
	public void buildBluetoothList()
	{	

		List<String> devNames = bluetoothManager.getPairedDevicesNames();
		devNames.add("Disconnect");
		System.out.println("Listing devices");
		setBusyStatus(true);
		if(devNames.size() > 0){
			ArrayAdapter<String> dataAdapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_item, devNames);
			dataAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
			
			Spinner devList = (Spinner) findViewById(R.id.bonded_device_list);
			devList.setAdapter(dataAdapter);
			devList.setOnItemSelectedListener(this);
		} else {
			System.out.println("No devices found");
			msbox("Error", "No paired bluetooth devices. Enable bluetooth and connect");
		}
		setBusyStatus(false);
	}
	
	
	public void msbox(String str,String str2)
	{
	    AlertDialog.Builder dlgAlert  = new AlertDialog.Builder(this);                      
	    dlgAlert.setTitle(str); 
	    dlgAlert.setMessage(str2); 
	    dlgAlert.setPositiveButton("OK",new DialogInterface.OnClickListener() {
	        public void onClick(DialogInterface dialog, int whichButton) {
	             finish(); 
	        }
	   });
	    dlgAlert.setCancelable(true);
	    dlgAlert.create().show();
	}
	
	public void removeAllWidgets(){
		buttonManager.removeAll();
		analogInManager.removeAll();
		analogOutManager.removeAll();
		digitalInManager.removeAll();
		digitalOutManager.removeAll();
		stringInManager.removeAll();
		textBoxManager.removeAll();
		layoutManager.removeAll( );
		plotManager.removeAll();
		layoutManager.addLayout();
	}
	
	@Override
	public void onItemSelected(AdapterView<?> parent, View view, int pos,
			long id) {
		System.out.println("Disconnecting");
		corbomiteDevice.disconnect();
		removeAllWidgets();
		setBusyStatus(false);
		String selected = (String) parent.getItemAtPosition(pos);
		//plotManager.addSeekBar("Plotten");
		//parsePayload("layout\r\nbutton ralf 1 riasdflf 1");
		if(selected.equals("Disconnect"))
			return;
		if(selected.equals("Retry")){
			buildBluetoothList();
			return;
		}
			
		if(selected != null){
			setBusyStatus(true);
			BluetoothSocket sock = 	bluetoothManager.getSocketByName(selected);
			if (sock != null){
				corbomiteDevice.setBlutoothSocket(sock);
				corbomiteDevice.connected();
			}
			setBusyStatus(false);
		}
		
	}

	@Override
	public void onNothingSelected(AdapterView<?> arg0) {
		// TODO Auto-generated method stub
		
	}
	
	public void parsePayload(String payload)
	{
		int responders = 0;
		if(payload.length()>0){
			if(payload.indexOf("deleteall")== 0){
					removeAllWidgets();
					responders += 1;
			} else {
				responders+=layoutManager.parsePayload(payload);
				responders+=buttonManager.parsePayload(payload);
				responders+=analogInManager.parsePayload(payload);
				responders+=analogOutManager.parsePayload(payload);
				responders+=stringInManager.parsePayload(payload);
				responders+=textBoxManager.parsePayload(payload);
				responders+=digitalOutManager.parsePayload(payload);
				responders+=digitalInManager.parsePayload(payload);
				responders+=plotManager.parsePayload(payload);
				Log.i("responders", Integer.toString(responders)+" widgets responded to payload: "+payload);	
			}
		}
	}
}
