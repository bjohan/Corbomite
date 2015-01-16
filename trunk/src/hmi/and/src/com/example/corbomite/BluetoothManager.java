package com.example.corbomite;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.UUID;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;

public class BluetoothManager {
	
	public String getString( BluetoothDevice device)
	{
		return device.getName().toString()+'\n'+device.getAddress();
	}
	
	public List<String> getPairedDevicesNames()
	{
		List<String> devNames = new ArrayList<String>();
		
		BluetoothAdapter mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
		
    	if (mBluetoothAdapter == null) {
    		devNames.add("No default bluetooth adapter");
    		return devNames;
    	} 
		
		Set<BluetoothDevice> pairedDevices = mBluetoothAdapter.getBondedDevices();
		
		System.out.println("Listing devices");

		if(pairedDevices.size() > 0){
			for(BluetoothDevice device : pairedDevices){
				devNames.add(getString(device));
			}
			
		} else {
			devNames.add("No paired devices");
			devNames.add("Retry");
		}
		return devNames;
	}
	
	public BluetoothSocket getSocketByName(String name) {
		BluetoothDevice mmDevice = null;
		BluetoothAdapter mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
		if(mBluetoothAdapter == null)
			return null;
		Set<BluetoothDevice> pairedDevices = mBluetoothAdapter.getBondedDevices();
		
		if(pairedDevices.size() > 0){
			for(BluetoothDevice device : pairedDevices){
				if (name.equals(getString(device))){
					mmDevice = device;
					break;
				}
			}
		}
		if(mmDevice == null)
			return null;
		
		System.out.println(mmDevice.getName().toString()+' '+mmDevice.getAddress());
		if(mmDevice.getName().equals("linvor")){
			BluetoothSocket mmSocket = null;
			try {
				System.out.println("Attempting to open bt rfcomm socket");
				UUID uuid = UUID.fromString("00001101-0000-1000-8000-00805f9b34fb"); //Standard SerialPortService ID
		        mmSocket = mmDevice.createRfcommSocketToServiceRecord(uuid);
		        mmSocket.connect();
		        return mmSocket;
			} catch (Exception e) {
				System.out.println("Something went horribly wrong");
				return null;
			} finally {
				
			}
		}
		return null;
	}
	
}
