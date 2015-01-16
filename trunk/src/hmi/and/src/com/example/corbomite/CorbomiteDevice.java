package com.example.corbomite;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.concurrent.locks.ReentrantLock;

import android.bluetooth.BluetoothSocket;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;

class CorbomiteDevice implements Runnable {
	ReentrantLock lock = new ReentrantLock();
	Handler lineHandler = null;
	Handler busyHandler = null;
	BluetoothSocket sck = null;
	BufferedReader istream = null;
	BufferedWriter ostream = null;
	String lineBuf = new String();
	String txBuf = new String();
	boolean isBusy = false;

	boolean lookForPrompt = true;
	int initialized = 1;
	String frameStart = "#";
	String frameEnd = "\r\n";
	
	public CorbomiteDevice(Handler lhandler, Handler bhandler){
		lineHandler = lhandler;
		busyHandler = bhandler;
	}
	public void sendData(String data)
	{
		if(ostream != null){
			try {
				ostream.write(data.toCharArray());
				ostream.flush();
				Log.i("rawsend", "Sending:"+ data);
			} catch (IOException e) {
				// TODO Auto-generated catch block
				Log.i("comm", "Data transmission failed");
				e.printStackTrace();
			}
		} else {
			Log.i("comm", "Bluetooth socket is not initialized");
		}
	}
	public void disconnect()
	{
		System.out.println("Waiting for thread lock");
		lock.lock();
		System.out.println("Disconnecting");
		if(sck != null){
			try {
				sck.close();
				sck = null;
				istream = null;
				ostream = null;
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			
		}
		lock.unlock();
	}
	
	public void setBlutoothSocket(BluetoothSocket s){
		System.out.println("Waiting for lock in order to set socket");
		lock.lock();
		System.out.println("Setting socket");
		sck = s;
		try {
			istream = new BufferedReader(new InputStreamReader(sck.getInputStream()));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		try {
			ostream = new BufferedWriter(new OutputStreamWriter( sck.getOutputStream()));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		lock.unlock();
	}
	
	public void connected()
	{
		System.out.println("Waiting for lock for init flag");
		lock.lock();
		System.out.println("Done");
		initialized = 0;
		lock.unlock();
	}
	
	public void sendCommandline(String line)
	{
		Message m = new Message();
		Bundle b = new Bundle();
		if(line.length()>0){
			//System.out.println("Sending"+line);
			b.putString("string", line);
			m.setData(b);
			lineHandler.sendMessage(m);
		}
	}
	
	public void sendBusyStatus(boolean busy){
		Message m = new Message();
		Bundle b = new Bundle();
		if(busy && isBusy != busy){
			b.putString("string", "busy");
			Log.i("comm", "Device is busy");
		}else if(isBusy != busy){
			b.putString("string", "idle");
			Log.i("comm", "Device is idle");
		}
		if(isBusy != busy){
			m.setData(b);
			isBusy = busy;	
			busyHandler.sendMessage(m);
		}
		
	}
	
	public String getFrameFromPayload(){

		int fs = lineBuf.indexOf(frameStart);
		
		//Log.i("rawbuf", lineBuf);
		if(fs < 0)
			return new String();
		
		int fs2 = lineBuf.indexOf(frameStart,fs+frameStart.length());
		if(fs2>0){
			Log.i("comm", "Two frame starts without frame end: "+lineBuf.substring(0,fs2+frameStart.length()));
			lineBuf = lineBuf.substring(fs2);
			//Log.i("rawbuf", "trimmed to"+lineBuf);
			return new String("");
		}
		
		
		int fe = lineBuf.indexOf(frameEnd, fs);
		if(fe < 0){
			//sendBusyStatus(true);
			return new String("");
		}
		
		String payload = lineBuf.substring(fs+frameStart.length(), fe);
		if(payload.equals("busy")){
			sendBusyStatus(true);
			return "";
		}
		if(payload.equals("idle")){
			sendBusyStatus(false);
			return "";
		}
		//Log.i("frames", payload);
		Log.i("comm", "Framed data: "+payload);
		lineBuf = lineBuf.substring(fe);
		//Log.i("rawbuf", "trimmed to"+lineBuf);
		//sendBusyStatus(false);
		return payload;
	}
	
	public void parseDataStream()
	{
		String payload = getFrameFromPayload();
		if(payload.equals(""))
			return;
		else
			sendCommandline(payload);
	}
	
	public void transmitData(String data){
		lock.lock();
		sendBusyStatus(true);
		System.out.println("Adding data to txbuf: "+data);
		txBuf+=frameStart+data+frameEnd;
		lock.unlock();
	}
	
	public void transmitDataIfIdle(String data){
		lock.lock();
		if(!isBusy && txBuf.length()==0){
			System.out.println("Adding data to txbuf: "+data);
			sendBusyStatus(true);
			txBuf+=frameStart+data+frameEnd;
		}
		lock.unlock();
	}
	
	public void run(){
		System.out.println("Starting thread");
		while(true){
			lock.lock();
			try {
				if(istream != null){
					if(istream.ready()){
						lineBuf += (char)istream.read();
						
						if(lineBuf.indexOf("#idle\r\n")>=0 && lookForPrompt){
							lookForPrompt = false;
							sendBusyStatus(false);
						}
						parseDataStream();
					}
				}
				} catch (IOException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			if(initialized == 0){
				Log.i("comm", "Sending info");
				sendData("#info\r\n");
				sendBusyStatus(true);
				Log.i("comm", "Setting busy status");
				initialized = 1;
			} else {
				if(txBuf.length()>0){
					sendData(txBuf);	
					sendBusyStatus(true);
					txBuf = "";
				}
				
			}
			lock.unlock();
		}
	}
}
