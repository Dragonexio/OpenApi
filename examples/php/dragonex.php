<?php

include "./base.php";

class DragonExV1 extends Base {
	//
	function __construct() {
	}

	// 
	function createNewToken() {
		$path = "/api/v1/token/new/";
		return $this->sendPOST($path, array(), null);
	}

	//
	function tokenStatus() {
		$path = "/api/v1/token/status/";
		return $this->sendPOST($path, array(), null);
	}

	//
	function getAllCoins() {
		$path = "/api/v1/coin/all/";
		return $this->sendGET($path, null, null);
	}

	//
	function getUserOwnCoins() {
		$path = "/api/v1/user/own/";
		return $this->sendPOST($path, array(), null);
	}

	//
	function getAllSymbos() {
		$path = "/api/v1/symbol/all/";
		return $this->sendGET($path, null, null);
	}

	//
	function getMarketLine($symbolID, $startTime, $searchDirection, $c, $klineType) {
                $path = "/api/v1/market/kline/";
                $params = array(
                        'symbol_id' => $symbolID,
                        'st' => $startTime,
                        'direction' => $searchDirection,
                        'count' => $c,
                        'kline_type' => $klineType
                );
                return $this->sendGET($path, $params, null);
        }

	//
	function getMarketBuy($symbolID) {
                $path = "/api/v1/market/buy/";
                $params = array("symbol_id" => $symbolID);
                return $this->sendGET($path, $params, null);
        }

	//
	function getMarketReal($symbolID) {
                $path = "/api/v1/market/real/";
                $params = array("symbol_id" => $symbolID);
                return $this->sendGET($path, $params, null);
        }

	//
	function addOrderBuy($symbolID, $price, $volume) {
                $path = "/api/v1/order/buy/";
                $data = array(
			'symbol_id' => $symbolID,
			'price' => strval($price),
			'volume' => strval($volume)
		);
                return $this->sendPOST($path, $data, null);
        }

	//
	function addOrderSell($symbolID, $price, $volume) {
		$path = "/api/v1/order/sell/";
		$data = array(
			'symbol_id' => $symbolID,
			'price' => strval($price),
			'volume' => strval($volume)
		);
                return $this->sendPOST($path, $data, null);
	}

	//
	function cancelOrder($symbolID, $orderID) {
                $path = "/api/v1/order/cancel/";
                $data = array('symbol_id' => $symbolID, 'order_id' => $orderID);
                return $this->sendPOST($path, $data, null);
        }

	//
	function getOrderDetail($symbolID, $orderID) {
                $path = '/api/v1/order/detail/';
                $data = array('symbol_id' => $symbolID, 'order_id' => $orderID);
                return $this->sendPOST($path, $data, null);
        }

	//
	function getUserOrderHistory($symbolID, $searchDirection, $startTime, $c, $s) {
                $path = '/api/v1/order/history/';
                $data = array(
                        'symbol_id' => $symbolID,
                        'direction' => $searchDirection,
                        'start' => $startTime,
                        'count' => $c,
                        'status' => $s
                );
                return $this->sendPOST($path, $data, null);
        }

	//
	function getuserDealHistory($symbolID, $searchDirection, $startTime, $c) {
                $path = "/api/v1/deal/history/";
                $data = array(
                        "symbol_id" => $symbolID,
                        "direction" => $searchDirection,
                        "start" => $startTime,
                        "count" => $c 
                );
                return $this->sendPOST($path, $data, null);
        }
}

