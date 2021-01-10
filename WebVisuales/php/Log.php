<?php
	error_reporting(E_ALL ^ E_NOTICE);
	require_once('../Layouts/Layout.php');	
	require_once('../Conexion.php');
	
	//Creamos la variable where para que el query sea dinamico
	$where="";

	//Obteniendo los valores de los campos con el id especificado cuando se genera un POST
	$empleado=$_POST['idEmpleado'];
	$diagrama=$_POST['idDiagrama'];
	$fecha=$_POST['idFecha'];

	//Se ejecutara cuando se presione el boton con el id buscar y form con metodo POST
	if (isset($_POST['buscar']))
	{
		//Se realizan todas las combinaciones posibles para el filtrado mediante un query
		if (empty($_POST['idDiagrama']) && empty($_POST['idFecha']))
		{
			$where="where FKEmpleadoID like'".$empleado."%'";
		}
		else if (empty($_POST['idEmpleado']) && empty($_POST['idFecha'])) 
		{
			$where="where FKDiagramaID like'".$diagrama."%'";
		}
		else if (empty($_POST['idEmpleado']) && empty($_POST['idDiagrama'])) 
		{
			$where="where Fecha between '".$fecha."' and '".$fecha." 23:59:59'";
		}
		else if (empty($_POST['idFecha'])) 
		{
			$where="where FKDiagramaID like'".$diagrama."%' and FKEmpleadoID like'".$diagrama."%'";
		}
		else if (empty($_POST['idDiagrama'])) 
		{
			$where="where FKEmpleadoID like'".$diagrama."%' and Fecha between '".$fecha."' and '".$fecha." 23:59:59'";
		}
		else if (empty($_POST['idEmpleado'])) 
		{
			$where="where FKDiagramaID like'".$diagrama."%' and Fecha between '".$fecha."' and '".$fecha." 23:59:59'";
		}
		else
		{
			$where="where FKEmpleadoID like'".$empleado."%' and FKDiagramaID like'".$diagrama."%' and FKDiagramaID like'".$diagrama."%' and Fecha between '".$fecha."' and '".$fecha." 23:59:59'";
		}
	}

	//Se guarda la consulta
	$consulta = "SELECT * FROM Log $where";
	
	//Se ejecuta la consulta
	$resultado = mysqli_query( $conexion, $consulta ) or die ( "Algo ha ido mal en la consulta a la base de datos");
?>

<!DOCTYPE html>
<HTML>
	<HEAD>
		<TITLE>Log</TITLE>
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
						<span class="input-group-text">ID Empleado</span>
						</div>
						<input type="text" aria-label="First name" class="form-control" placeholder="ID del empleado" name="idEmpleado">
						<div class="input-group-prepend">
						<span class="input-group-text">ID Diagrama</span>
						</div>
						<input type="text" aria-label="Last name" class="form-control" placeholder="ID del diagrama" name="idDiagrama">
						<div class="input-group-prepend">
						<span class="input-group-text">Fecha</span>
						</div>
					    <input type="text" aria-label="Last name" class="form-control" placeholder="AAAA-MM-DD" name="idFecha">
						<div class="input-group-append">
		    				<button class="btn btn-outline-success" type="submit" name="buscar">Filtrar</button>
		  				</div>
					</div>
				</form>
			</div>
		  	<br>
		  	<div class="row justify-content-center align-items-center minh-100">
		    	<h5 class="page-header text-white">Log de operaciones</h5>
		    </div>
	    </div>
	    <!-- Se crea la tabla con las columnas necesarias-->
		<div class="table-responsive">
			<table class="table table-hover">
				<thead class="thead-dark">
					<tr>
						<th scope="col">ID Log</th>
						<th scope="col">Fecha</th>
						<th scope="col">ID Empleado</th>
						<th scope="col">ID Diagrama</th>
						<th scope="col">No. Orden</th>
						<th scope="col">Partes Totales</th>
						<th scope="col">Partes Aceptadas</th>
						<th scope="col">Partes Rechazadas</th>
					</tr>
				</thead>
				<?php	
				//Mientras se encuentre un registro seguira el ciclo
				while ($columna = mysqli_fetch_array( $resultado ))
				{?>
					<!-- Se crea una fila por cada ciclo con los datos de la consulta-->
					<tbody>
					<th scope="row"><?php echo $columna["LogID"] ?> </th>
					<td> <?php echo $columna["Fecha"] ?></td>
					<td> <?php echo $columna["FKEmpleadoID"] ?></td>
					<td> <?php echo $columna["FKDiagramaID"] ?></td>
					<td> <?php echo $columna["NumOrden"] ?></td>
					<td> <?php echo $columna["Partes"] ?></td>
					<td> <?php echo $columna["PartesAc"] ?></td>
					<td> <?php echo $columna["PartesRe"] ?></td>
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