<?php
// Datos de la base de datos
	$usuarioBD = "remote";
	$passBD = "1309";
	$ipBD = "192.168.100.106";
	$nombreBD = "Visuales";

	// creación de la conexión a la base de datos con mysql_connect()
	$conexion = mysqli_connect($ipBD,$usuarioBD,$passBD) or die ("No se ha podido conectar al servidor de Base de datos");
	
	// Selección del a base de datos a utilizar
	$db = mysqli_select_db( $conexion, $nombreBD ) or die ( "Upps! Pues va a ser que no se ha podido conectar a la base de datos" );
?>