<?php

// 需要替换
define("AccessKey", "my access key");
define("SecretKey", "my secret key");

define("Host", "https://openapi.dragonex.im");


include "./dragonex.php";


$dex = new DragonExV1();
var_dump($dex->getAllCoins());
echo "\n";

// 需要替换
$dex->setToken("mytoken");

$d = $dex->getUserOwnCoins();
$h = new HTTPResponse($d);
var_dump($h);

echo "\n";


