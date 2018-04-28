package com.dragonex.openapi;

public class HostConstant {
	
	public static String MAIN_HOST = "https://openapi.dragonex.im";
	
	// get token
	public static String GET_TOKEN = "/api/v1/token/new/";
	
	// check token status(POST)
	public static String CHECK_TOKEN_STATUS = "/api/v1/token/status/";
	
	// get all the coin(GET)
	public static String GET_COIN_ALL ="/api/v1/coin/all/";
	
	// get the currency information that the user has.(POST)
	public static String GET_USER_COIN ="/api/v1/user/own/";
}
