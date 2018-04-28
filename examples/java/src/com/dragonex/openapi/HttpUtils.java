package com.dragonex.openapi;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

public class HttpUtils {
	
	public static String sendPost(String access_key, String secret_key, String mainHost, String path) {
		String uri = mainHost + path;
		String result = null;
		InputStream in = null;
		try {
			URL url = new URL(uri);
			HttpURLConnection urlcon = (HttpURLConnection) url.openConnection();
			urlcon.setRequestMethod("POST");
			
			HashMap<String, String> headers = HttpParams.getHttpHeaders(access_key, secret_key, "POST", path, "");
			for (Map.Entry<String, String> entry : headers.entrySet()) {
				urlcon.setRequestProperty(entry.getKey(), entry.getValue());
			}

			urlcon.connect();
			in = urlcon.getInputStream();
			BufferedReader buffer = new BufferedReader(new InputStreamReader(in, "UTF-8"));
			StringBuilder sb = new StringBuilder();
			String line = null;
			while ((line = buffer.readLine()) != null) {
				sb.append(line);
			}
			result = sb.toString();
		} catch (Exception e) {
			System.out.println("[request error][address��" + uri + "][error msg��" + e.getMessage() + "]");
		} finally {
			try {
				if (null != in)
					in.close();
			} catch (Exception e2) {
				System.out.println("[close stream error][error msg��" + e2.getMessage() + "]");
			}
		}
		return result;
	}

	/**
	 * 
	 * @param uri
	 * @param param JSON
	 * @param charset
	 * @return
	 */
	public static String sendPost(String access_key, String secret_key, String mainHost, String path, String jsonData) {
		String uri = mainHost + path;
		String result = null;
		PrintWriter out = null;
		InputStream in = null;
		try {
			URL url = new URL(uri);
			HttpURLConnection urlcon = (HttpURLConnection) url.openConnection();
			urlcon.setDoInput(true);
			urlcon.setDoOutput(true);
			urlcon.setUseCaches(false);
			urlcon.setRequestMethod("POST");
			HashMap<String, String> headers = HttpParams.getHttpHeaders(access_key, secret_key, "POST", path, jsonData);
			for (Map.Entry<String, String> entry : headers.entrySet()) {
				urlcon.setRequestProperty(entry.getKey(), entry.getValue());
			}
			urlcon.connect();
			out = new PrintWriter(urlcon.getOutputStream());
			out.print(jsonData);
			out.flush();
			in = urlcon.getInputStream();
			BufferedReader buffer = new BufferedReader(new InputStreamReader(in, "UTF-8"));
			StringBuffer bs = new StringBuffer();
			String line = null;
			while ((line = buffer.readLine()) != null) {
				bs.append(line);
			}
			result = bs.toString();
		} catch (Exception e) {
			System.out.println("[request error][address��" + path + "][params��" + jsonData + "][error msg��" + e.getMessage() + "]");
		} finally {
			try {
				if (null != in)
					in.close();
				if (null != out)
					out.close();
			} catch (Exception e2) {
				System.out.println("[close stream error][error msg��" + e2.getMessage() + "]");
			}
		}
		return result;
	}
}
