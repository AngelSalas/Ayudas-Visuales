<?php
	error_reporting(E_ALL ^ E_NOTICE);
	require_once('../Layouts/Layout.php');	
	require_once('../Conexion.php');
	
	//Creamos la variable where para que el query sea dinamico
	$where="";

	//Obteniendo los valores de los campos con el id especificado cuando se genera un POST
	$parte=$_POST['idParte'];
	$familia=$_POST['idFamilia'];
	$version=$_POST['idVersion'];

	//Se ejecutara cuando se presione el boton con el id buscar y form con metodo POST
	if (isset($_POST['buscar']))
	{
		//Se realizan todas las combinaciones posibles para el filtrado mediante un query
		if (empty($_POST['idParte']) && empty($_POST['idFamilia']))
		{
			$where="where Version like'".$version."%'";
		}
		else if (empty($_POST['idParte']) && empty($_POST['idVersion'])) 
		{
			$where="where Familia like'".$familia."%'";
		}
		else if (empty($_POST['idVersion']) && empty($_POST['idFamilia'])) 
		{
			$where="where NumeroParte like '".$parte."%'";
		}
		else if (empty($_POST['idParte'])) 
		{
			$where="where Version like'".$version."%' and Familia like'".$familia."%'";
		}
		else if (empty($_POST['idFamilia'])) 
		{
			$where="where NumeroParte like '".$parte."%' and Version like'".$version."%'";
		}
		else if (empty($_POST['idVersion'])) 
		{
			$where="where Familia like'".$familia."%' and NumeroParte like '".$parte."%'";
		}
		else
		{
			$where="where Familia like'".$familia."%' and NumeroParte like '".$parte."%' and Version like'".$version."%'";
		}
	}

	//Se guarda la consulta
	$consulta = "SELECT * FROM Diagrama $where";
	
	//Se ejecuta la consulta
	$resultado = mysqli_query( $conexion, $consulta ) or die ( "Algo ha ido mal en la consulta a la base de datos");
?>

<!DOCTYPE html>
<HTML>
	<HEAD>
		<TITLE>Diagramas</TITLE>
	</HEAD>
	<BODY>
		<div class="container-fluid bg-dark ">
			<br>
			<div class="row justify-content-center align-items-center minh-100">
		    	<h5 class="page-header text-white">Opciones para filtrar contenido</h5>
		    </div>
		    <!-- Se crean los inputs para los filtrados que se necesiten y se les asigna un id-->
		    <div class="row justify-content-center align-items-center minh-100">
		    	<form method="POST" class="row justify-content-center align-items-center minh-100">
				  	<div class="input-group col-md-11 ">
						<div class="input-group-prepend">
						<span class="input-group-text">Parte</span>
						</div>
						<input type="text" aria-label="First name" class="form-control" placeholder="Numero de parte" name="idParte">
						<div class="input-group-prepend">
						<span class="input-group-text">Familia</span>
						</div>
						<input type="text" aria-label="Last name" class="form-control" placeholder="Familia o area" name="idFamilia">
						<div class="input-group-prepend">
						<span class="input-group-text">Version</span>
						</div>
					    <input type="text" aria-label="Last name" class="form-control" placeholder="Version del diagrama" name="idVersion">
						<div class="input-group-append">
		    				<button class="btn btn-outline-success" type="submit" name="buscar">Filtrar</button>
		  				</div>
					</div>
				</form>
			</div>
		  	<br>
		  	<div class="row justify-content-center align-items-center minh-100">
		    	<h5 class="page-header text-white">Diagramas registrados</h5>
		    </div>
	    </div>
	    <!-- Se crea la tabla con las columnas necesarias-->
		<div class="table-responsive">
			<table class="table table-hover">
				<thead class="thead-dark">
					<tr>
						<th scope="col">ID Diagrama</th>
						<th scope="col">Numero de parte</th>
						<th scope="col">Familia o area</th>
						<th scope="col">Version</th>
						<th scope="col">Ruta de imagen</th>
					</tr>
				</thead>
				<?php	
				//Mientras se encuentre un registro seguira el ciclo
				while ($columna = mysqli_fetch_array( $resultado ))
				{?>
					<!-- Se crea una fila por cada ciclo con los datos de la consulta-->
					<tbody>
					<th scope="row"><?php echo $columna["DiagramaID"] ?> </th>
					<td> <?php echo $columna["NumeroParte"] ?></td>
					<td> <?php echo $columna["Familia"] ?></td>
					<td> <?php echo $columna["Version"] ?></td>
					<td> <?php echo $columna["RutaImagen"] ?></td>
					</tbody>
					<?php
				}
				?>
			</table> 
		</div>
		<?php
		mysqli_close( $conexion );
		?>
	</BODY>
</HTML>