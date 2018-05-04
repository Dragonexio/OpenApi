
const base = require('./base');

// 
class DragonExV1 extends base.Base {
	constructor(accessKey, secretKey, host) {
		super(accessKey, secretKey, host);
	}

	//
	createNewToken(callback) {
		let path = "/api/v1/token/new/";
		return this.sendPOST(path, {}, null, callback);
	}

	//
	tokenStatus(callback) {
		let path = "/api/v1/token/status/";
		this.sendPOST(path, {}, null, callback);
	}

	//
	getAllCoins(callback) {
		let path = "/api/v1/coin/all/";
		this.sendGET(path, null, null, callback);
	}

	//
	getUserOwnCoins(callback) {
		let path = "/api/v1/user/own/";
		this.sendPOST(path, {}, null, callback);
	}

	//
	getAllSymbos(callback) {
		let path = "/api/v1/symbol/all/";
		this.sendGET(path, null, null, callback);
	}

	//
	getMarketLine(symbolID, startTime, searchDirection, count, klineType) {
		let path = "/api/v1/market/kline/";
		let params = {
			'symbol_id': symbolID,
			'st': startTime,
			'direction': searchDirection,
			'count': count,
                  	'kline_type': klineType
		};
		this.sendGET(path, params, null, callback);
	}

	//
	getMarketBuy(symbolID, callback) {
		let path = "/api/v1/market/buy/";
		let params = {"symbol_id": symbolID};
		this.sendGET(path, params, null, callback);
	}

	//
	getMarketSell(symbolID, callback) {
		let path = "/api/v1/market/sell/";
		let params = {"symbol_id": symbolID};
		this.sendGET(path, params, null, callback);
	}

	//
	getMarketReal(symbolID, callback) {
		let path = "/api/v1/market/real/";
		let params = {"symbol_id": symbolID};
		this.sendGET(path, params, null, callback);
	}

	//
	addOrderBuy(symbolID, price, volume, callback) {
		let path = "/api/v1/order/buy/";
		let data = {'symbol_id': symbolID, 'price': price.toString(), 'volume': volume.toString()};
		this.sendPOST(path, data, null, callback);
	}

	//
	addOrderSell(symbolID, price, volume, callback) {
		let path = "/api/v1/order/sell/";
		let data = {'symbol_id': symbolID, 'price': price.toString(), 'volume': volume.toString()};
		this.sendPOST(path, data, null, callback);

	}

	//
	cancelOrder(symbolID, orderID, callback) {
		let path = "/api/v1/order/cancel/";
		let data = {'symbol_id': symbolID, 'order_id': orderID};
		this.sendPOST(path, data, null, callback);
	}

	//
	getOrderDetail(symbolID, orderID, callback) {
		let path = '/api/v1/order/detail/';
		let data = {'symbol_id': symbolID, 'order_id': orderID};
		this.sendPOST(path, data, null, callback);
	}

	//
	getUserOrderHistory(symbolID, searchDirection, startTime, count, s, callback) {
		let path = '/api/v1/order/history/';
		let data = {
			'symbol_id': symbolID,
			'direction': searchDirection,
			'start': startTime,
			'count': count,
                	'status': s
		};
		this.sendPOST(path, data, null, callback);
	}

	//
	getuserDealHistory(symbolID, searchDirection, startTime, count, callback) {
		let path = "/api/v1/deal/history/";
		let data = {
			"symbol_id": symbolID,
			"direction": searchDirection,
			"start": startTime,
			"count": count
		};
		this.sendPOST(path, data, null, callback);
	}
}

module.exports = {
	DragonExV1: DragonExV1
};
