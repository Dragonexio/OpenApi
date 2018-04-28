package com.dragonex.openapi;

public class Main {
	public static void main(String[] args) {
		
		new Thread(new Runnable() {
			@Override
			public void run() {
				System.out.println("start!");
				String access_key = "Pretend to have access_key";
				String secret_key = "Pretend to have secret_key";
				// get token
				String hasTokenJson = HttpUtils.sendPost(access_key, secret_key, HostConstant.MAIN_HOST, HostConstant.GET_TOKEN);
				
				// set token
				HttpParams.setToken("Pretend to have token");
				// get token status
				String tokenStatusJson = HttpUtils.sendPost(access_key, secret_key, HostConstant.MAIN_HOST, HostConstant.CHECK_TOKEN_STATUS);


			}
		}).start();

	}
}