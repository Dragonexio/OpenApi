package com.dragonex.openapi;

import java.security.InvalidKeyException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

public class EncryptionUtil {
	
    private static final char hexDigits[] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'};
    private static MessageDigest messagedigest = null;
    
    static {
    	init();
    }
    
    private static void init() {
        try {
            messagedigest = MessageDigest.getInstance("MD5");
        } catch (NoSuchAlgorithmException e) {
        	e.printStackTrace();
        }
    }
    
    /**
     * generate md5 string
     *
     * @param s
     * @return
     */
    public synchronized static String getMD5String(String s) {
        try {
            return getMD5String(s.getBytes());
        }catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }
    
    public synchronized static String getMD5String(byte[] bytes) {
        if (bytes == null || bytes.length == 0) {
            return null;
        }
        if (messagedigest == null) {
            init();
        }
        if (messagedigest == null) {
            return "";
        }
        messagedigest.update(bytes);
        return bytes2HexString(messagedigest.digest());
    }
    
	/**
     * SHA1 Encryption
     *
     * @param data 
     * @return
     */
    public static String encryptSHA1ToString(byte[] data) {
        return bytes2HexString(encryptSHA1(data));
    }
	
	/**
     * SHA1 Encryption
     *
     * @param data
     * @return
     */
    public static byte[] encryptSHA1(byte[] data) {
        return hashTemplate(data, "SHA1");
    }
	
    private static byte[] hashTemplate(byte[] data, String algorithm) {
        if (data == null || data.length <= 0) return null;
        try {
            MessageDigest md = MessageDigest.getInstance(algorithm);
            md.update(data);
            return md.digest();
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
            return null;
        }
    }
    
    
    public static String hamcsha1(byte[] data, byte[] key) 
    {
          try {
              SecretKeySpec signingKey = new SecretKeySpec(key, "HmacSHA1");
              Mac mac = Mac.getInstance("HmacSHA1");
              mac.init(signingKey);
              byte[] rawHmac = Base64.getEncoder().encode(mac.doFinal(data));
              return new String(rawHmac);
          } catch (NoSuchAlgorithmException e) {
               e.printStackTrace();
          } catch (InvalidKeyException e) {
               e.printStackTrace();
          }
         return null;
     }
    
    
    
    /**
     * byteArr to hexString
     */
    private static String bytes2HexString(byte[] bytes) {
        if (bytes == null) return null;
        int len = bytes.length;
        if (len <= 0) return null;
        char[] ret = new char[len << 1];
        for (int i = 0, j = 0; i < len; i++) {
            ret[j++] = hexDigits[bytes[i] >>> 4 & 0x0f];
            ret[j++] = hexDigits[bytes[i] & 0x0f];
        }
        return new String(ret);
    }
    
}
