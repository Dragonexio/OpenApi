package com.dragonex.openapi;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.TimeZone;

public class HttpParams {
	
	private static final SimpleDateFormat GMT_FORMAT = new SimpleDateFormat("EEE, dd MMM yyyy HH:mm:ss 'GMT'", Locale.US);
	
	private static Map<String, String> sHttpHeaders = new HashMap<>();
	
	private static boolean HAS_CUSTOM_KEY = false;
	
	static {
		GMT_FORMAT.setTimeZone(TimeZone.getTimeZone("GMT+0"));
		initHttpHeader();
	}
	
	private static void initHttpHeader() {
		sHttpHeaders.put("Connection", "Keep-Alive");
		sHttpHeaders.put("Charset", "UTF-8");
		sHttpHeaders.put("Content-Type", "application/json");
		
		if  (HAS_CUSTOM_KEY) {  // not indispensable
			sHttpHeaders.put("dragonex-atruth", "DragonExIsTheBest");
			sHttpHeaders.put("dragonex-b", "best");
		}
		
	}
	
	public static void setToken(String token) {
		sHttpHeaders.put("token", token);
	}
	
	private static String getSign(String secret_key,String method,String path,HashMap headers) {
		StringBuilder sb = new StringBuilder();
		sb.append(method).append("\n");
		
		if (headers.containsKey("Content-Sha1")) {
			sb.append(headers.get("Content-Sha1"));
		}
		
		sb.append("\n")
		.append(headers.get("Content-Type")).append("\n")
		.append(headers.get("date")).append("\n");
		
		if (HAS_CUSTOM_KEY) {
			sb.append("dragonex-atruth:").append(headers.get("dragonex-atruth")).append("\n");
			sb.append("dragonex-b:").append(headers.get("dragonex-b")).append("\n");
		}
		
		sb.append(path);
		
		String hamcsha1 = EncryptionUtil.hamcsha1(sb.toString().getBytes(),secret_key.getBytes());
		return hamcsha1;
	}
	
	private static String getSha1(String jsonData) {
		return EncryptionUtil.encryptSHA1ToString(jsonData.getBytes());
	}
	
	/**
	 * get request headers
	 */
	public static HashMap getHttpHeaders(String access_key,String secret_key, String method, String path, String jsonData){
		HashMap<String,String> headers = new HashMap<>();
        headers.putAll(sHttpHeaders);
        
        headers.put("date", GMT_FORMAT.format(new Date()));
        if (!Util.TextIsEmpty(jsonData)) {
        	headers.put("Content-Sha1", getSha1(jsonData));
        }
        String sign = getSign(secret_key,method,path,headers);
        String auth = String.format("%s:%s", access_key,sign);
        headers.put("auth",auth);
        return headers;
	}
}
