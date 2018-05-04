
const base = require('./base');
const dv1 = require('./dragonex');
const http = require('http');


const AccessKey = "my_access_key"; // 需替换
const SecretKey = "my_secret_key"; // 需替换

const Host = "openapi.dragonex.im";


let dragonex = new dv1.DragonExV1(AccessKey, SecretKey, Host);

/*dragonex.createNewToken((res) => {
	let html = '';
	res.on('data', (data) => {
		html += data;
	});
	res.on('end', () => {
		console.log(html);
	});
});*/

// 获取token后，替换
dragonex.setToken("mytoken");
dragonex.getUserOwnCoins((res) => {
	let html = '';
	res.on('data', (data) => {
		html += data;
	});
	res.on('end', () => {
		let resp = new base.HTTPResponse(html);
		console.log(resp.getData());
	});
});

