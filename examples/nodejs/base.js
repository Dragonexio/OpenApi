
const http = require('https');
const moment = require('moment');
const crypto = require('crypto');
const url = require('url');


var GMT_FORMAT = "ddd, DD MMM YYYY HH:mm:ss";

class Base {
	constructor(accessKey, secretKey, host) {
		this.accessKey = accessKey;
		this.secretKey = secretKey;
		this.host = host;
	}

	//
	getURL(path) {
		return this.host + path;
	}

	//
	sendGET(path, params, headers, callback) {
		let url = null;
		if (params !== null) {
			let ps = new url.URLSearchParams(params);
			url = path + "?" + ps.toString();
		}

		if (headers == null)
			headers = this.defaultHeaders('GET', path, null);

		let options = {  
			hostname: this.host,
			port: 443,
			path: url ? url : path,
			method: 'GET',
			headers: headers
		};
		let req = http.request(options, callback);
		req.end();
	}

	//
	sendPOST(path, data, headers, callback) {
		let jsData = JSON.stringify(data);
		if (headers == null)
			headers = this.defaultHeaders('POST', path, jsData);

		let req = http.request({
			hostname: this.host,
			port: 443,
			path: path,
			method: "POST",
			headers: headers
		}, callback);
		req.write(jsData);
		req.end();
	}
	
	//
	defaultHeaders(method, path, data) {
		let headers = {
			'Date': moment().utc().format(GMT_FORMAT) + " GMT",
			'Content-Type': 'application/json',
			'token': this.getToken()
		};

		if (data != null)
			headers['Content-sha1'] = this.sha1(data);

		headers['Auth'] = this.auth(method, path, headers);
		return headers;
	}

	//
	sha1(data) {
		let sha1 = crypto.createHash('sha1');
		sha1.update(data);
		return sha1.digest('hex');
	}

	//
	auth(method, path, headers) {
		let newHeaders = new Map();
		for (let k in headers) {
			let v = headers[k];
			newHeaders.set(k.toLowerCase(), v);
		}

		let contentMd5 = newHeaders.get('content-sha1') || "";
		let contentType = newHeaders.get('content-type') || "";
		let date = newHeaders.get('date') || "";

		let dragonHeaders = [];
		for (let [k, v] of newHeaders.entries()) {
			if (k.indexOf("dragonex-") > -1) 
				dragonHeaders.push(k + ":" + v);
		}

		dragonHeaders.sort();
		let canonicalizedDragonExHeaders = "";
		if (dragonHeaders.length !== 0)
			canonicalizedDragonExHeaders = dragonHeaders.join("\n");

		let stss = [
			method.toUpperCase(),
			contentMd5,
			contentType,
			date,
			canonicalizedDragonExHeaders
		];

		let sToSign = this.sign(stss.join("\n") + path, this.secretKey);
		return this.accessKey + ":" + sToSign;
	}

	sign(stss, secretKey) {
		return crypto.createHmac('sha1', secretKey).update(stss).digest().toString('base64');
	}

	//
	getToken() {
		return this.token || "";
	}

	// 
	setToken(val) {
		this.token = val;
	}
}


//
class HTTPResponse {
	constructor(body) {
		let d = JSON.parse(body)
		this.msg = d['msg'];
		this.data = d['data'];
		this.setCode(parseInt(d['code']));
	}

	getOK() {
		return this.ok;
	}

	getCode() {
		return this.code;
	}

	setCode(v) {
		this.code = v;
		this.ok = (v===1);
	}

	getMsg() {
		return this.msg;
	}

	setMsg(m) {
		this.msg = m;
	}

	getData() {
		return this.data;
	}

	setData(v) {
		this.data = v;
	}
}

module.exports = {
	Base: Base,
	HTTPResponse: HTTPResponse
};


