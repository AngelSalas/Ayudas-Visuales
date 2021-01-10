<?php
//Importando mysql.php
include './mysql.php';

//Creando instancia de la clase MySQL de mysql.php
$oMysql = new MySQL();

$response = "";
$rq = $_POST['rq'];

//Dependiendo de la solicitud del cliente se dara una respuesta de las funciones que se crearon en mysql.php
if ($rq == 1) {
    $response = $oMysql->getAceptadas();
} else if ($rq == 2) {
    $response = $oMysql->getRechazadas();
} else if ($rq == 3) {
    $response = $oMysql->getTotales();
} else if ($rq == 4) {
    $response = $oMysql->getDatosGrafica();
} else if ($rq == 5) {
    $response = $oMysql->getYield();
}


echo $response;

?>