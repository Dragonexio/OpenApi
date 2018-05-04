<?php

class Base
{
	private $token = '';

	function __construct() {
	}

	function getURL($path) {
		return Host . $path;
	}

	function sendGET($path, $params, $headers) {
		if (!$headers)
			$headers = $this->defaultHeaders("GET", $path, NULL);

		$url = $this->getURL($path);
		if ($params) {
			$arr = [];
			foreach ($params as $key => $val)
				array_push($arr, $key . '=' . $val);

			$url = $url . "?" . join("&", $arr);
		}

		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, $url);
		curl_setopt($ch, CURLOPT_HEADER, 0);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
		$ret = curl_exec($ch);
		curl_close($ch);
		return $ret;
	}

	function sendPOST($path, $data, $headers) {
		if (!$headers)
			$headers = $this->defaultHeaders("POST", $path, NULL);

		var_dump($headers);

		$jsStr = json_encode($data);
		$url = $this->getURL($path);

		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, $url);
		curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
		curl_setopt($ch, CURLOPT_HEADER, 0);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
		curl_setopt($ch, CURLOPT_POSTFIELDS, $jsStr);
		$ret = curl_exec($ch);
		curl_close($ch);
		return $ret;
	}

	function defaultHeaders($method, $path, $data) {
		$headers = array(
			"Date" => gmdate('D, d M Y H:i:s \G\M\T'),
			"Content-Type" => "application/json",
			"token" => $this->getToken()
		);

		if ($data !== null)
			$headers["Content-sha1"] = sha1($data);

		$headers['Auth'] = $this->auth($method, $path, $headers);
		$lastHeaders = [];
		foreach ($headers as $k => $v)
			$lastHeaders[] = $k . ": " . $v;

		return $lastHeaders;
	}

	function auth($method, $path, $headers) {
		$newHeaders = [];
		foreach ($headers as $key => $item) {
			$newHeaders[strtolower($key)] = $item;
		}

		$contentMD5 = "";
		if (array_key_exists('content-sha1', $newHeaders))
			$contentMD5 = $newHeaders['content-sha1'];

		$contentType = "";
		if (array_key_exists('content-type', $newHeaders))
			$contentType = $newHeaders['content-type'];

		$date = "";
		if (array_key_exists('date', $newHeaders))
			$date = $newHeaders['date'];

		$dragonHeaders = [];
		foreach ($newHeaders as $key => $item) {
			if (strstr($item, "dragonex-") !== false) {
				array_push($dragonHeaders, $key .":". $item);
			}
		}

		$canonicalizedDragonExHeaders = "";
		if (array_count_values($dragonHeaders) > 0) {
			arsort($dragonHeaders);
			$canonicalizedDragonExHeaders = join("\n", $dragonHeaders);
		}

		$stss = [
			strtoupper($method),
			$contentMD5,
			$contentType,
			$date,
			$canonicalizedDragonExHeaders
		];

		$sToSign = $this->sign(join("\n", $stss).$path);
		var_dump($sToSign);
		return AccessKey . ":" . $sToSign;
	}

	function sign($stss) {
		return base64_encode(hash_hmac("sha1", $stss, SecretKey, true));
	}

	function getToken() {
		return $this->token;
	}

	function setToken($val) {
		$this->token = $val;
	}
}


class HTTPResponse {
	private $code;
	private $ok = false;
	private $msg = "";
	private $data = array();

	function __construct($body) {
		$d = json_decode($body, true);
		$this->setCode($d['code']);
		$this->msg = $d['msg'];
		$this->data = $d['data'];
	}

	function getData() {
		return $this->data;
	}

	function getMsg() {
		return $this->msg;
	}

	function getOK() {
		return $this->ok;
	}

	function setCode($code) {
		if ($code === 1)
			$this->ok = true;
		$this->code = $code;
	}

	function getCode() {
		return $this->code;
	}
}

