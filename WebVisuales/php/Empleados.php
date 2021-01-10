<?php
	error_reporting(E_ALL ^ E_NOTICE);
	require_once('../Layouts/Layout.php');	
	require_once('../Conexion.php');	

	//Creamos la variable where para que el query sea dinamico
	$where="";

	//Obteniendo los valores de los campos con el id especificado cuando se genera un POST
	$nombre=$_POST['idNombre'];
	$numero=$_POST['idNumero'];

	//Se ejecutara cuando se presione el boton con el id buscar y form con metodo POST
	if (isset($_POST['buscar']))
	{
		//Se realizan todas las combinaciones posibles para el filtrado mediante un query
		if (empty($_POST['idNombre'])) 
		{
			$where="where NumEmpleado like'".$numero."%'";
		}
		else if (empty($_POST['idNumero'])) 
		{
			$where="where Nombre like'".$nombre."%'";
		}
		else
		{
			$where="where NumEmpleado like'".$numero."%' and Nombre like'".$nombre."%'";
		}
	}

	//Se guarda la consulta
	$consulta = "SELECT * FROM Empleado $where";
	
	//Se ejecuta la consulta
	$resultado = mysqli_query( $conexion, $consulta ) or die ( "Algo ha ido mal en la consulta a la base de datos");

?>

<!DOCTYPE html>
<HTML>
	<HEAD>
		<TITLE>Empleados</TITLE>
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
				  	<div class="input-group col-md-12 ">
						<div class="input-group-prepend">
						<span class="input-group-text">Nombre</span>
						</div>
						<input type="text" aria-label="First name" class="form-control" placeholder="Nombre de empleado" name="idNombre">
						<div class="input-group-prepend">
						<span class="input-group-text">Numero</span>
						</div>
						<input type="text" aria-label="Last name" class="form-control" placeholder="Numero de empleado" name="idNumero">
						<div class="input-group-append">
		    				<button class="btn btn-outline-success" type="submit" name="buscar">Filtrar</button>
		  				</div>
					</div>
				</form>
			</div>
		  	<br>
		  	<div class="row justify-content-center align-items-center minh-100">
		    	<h5 class="page-header text-white">Empleados registrados</h5>
		    </div>
	    </div>
	    <!-- Se crea la tabla con las columnas necesarias-->
		<div class="table-responsive">
			<table class="table table-hover">
				<thead class="thead-dark">
					<tr>
						<th scope="col">ID Empleado</th>
						<th scope="col">Nombre</th>
						<th scope="col">Numero</th>
						
					</tr>
				</thead>
				<?php	
				//Mientras se encuentre un registro seguira el ciclo
				while ($columna = mysqli_fetch_array( $resultado ))
				{?>
					<!-- Se crea una fila por cada ciclo con los datos de la consulta-->
					<tbody>
					<th scope="row"><?php echo $columna["EmpleadoID"] ?> </th>
					<td> <?php echo $columna["Nombre"] ?></td>
					<td> <?php echo $columna["NumEmpleado"] ?></td>
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