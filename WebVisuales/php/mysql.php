<?php
include '../Conexion.php';
class MySQL{
	private $oConBD = null;

	//Datos de la BD para la conexion con PDO
    public function __construct()
    {
        global $usuarioBD, $passBD, $ipBD, $nombreBD;
        $this->usuarioBD = $usuarioBD;
        $this->passBD = $passBD;
        $this->ipBD = $ipBD;
        $this->nombreBD = $nombreBD;
    }

    //Funcion para la conexion con la BD utilizando PDO
    public function conBDPDO()
	{
        try {
            $this->oConBD = new PDO("mysql:host=" . $this->ipBD . ";dbname=" . $this->nombreBD, $this->usuarioBD, $this->passBD);
            return true;
        } catch (PDOException $e) {
            echo "Error al conectar a la base de datos: " . $e->getMessage() . "\n";
            return false;
        }
	}

	//Funcion que obtiene las piezas que fueron rechazadas mediante un Query a la BD
	public function getRechazadas()
	{
		$rechazadas=0;
		try {
			$strQuery="SELECT SUM(PartesRe) as Prechazadas FROM Log";
			if($this->conBDPDO()){
				$pQuery = $this->oConBD->prepare($strQuery);
				$pQuery->execute();
				$rechazadas = $pQuery->fetchColumn();
			}
		} catch (PDOException $e) {
			echo "MySQL.getRechazadas: " . $e->getMessage() . "\n";
			return -1;
		} 
		return $rechazadas;
	}

	//Funcion que obtiene las piezas que fueron aceptadas mediante un Query a la BD
	public function getAceptadas()
	{
		$aceptadas=0;
		try {
			$strQuery="SELECT SUM(PartesAc) as Paceptadas FROM Log";
			if($this->conBDPDO()){
				$pQuery = $this->oConBD->prepare($strQuery);
				$pQuery->execute();
				$aceptadas = $pQuery->fetchColumn();
			}
		} catch (PDOException $e) {
			echo "MySQL.getAceptadas: " . $e->getMessage() . "\n";
			return -1;
		} 
		return $aceptadas;
	}

	//Funcion que obtiene las piezas totales producidas mediante un Query a la BD
	public function getTotales()
	{
		$totales=0;
		try {
			$strQuery="SELECT SUM(Partes) as Ptotales FROM Log";
			if($this->conBDPDO()){
				$pQuery = $this->oConBD->prepare($strQuery);
				$pQuery->execute();
				$totales = $pQuery->fetchColumn();
			}
		} catch (PDOException $e) {
			echo "MySQL.getTotales: " . $e->getMessage() . "\n";
			return -1;
		} 
		return $totales;
	}

	//Funcion que obtiene las piezas que fueron rechazadas mediante un Query a la BD
	public function getYield()
	{
		$yieldt=0;
		try {
			//La formula para obtener el Yield es (1-(Piezas rechazadas/Piezas totales)*100) dando un porcentaje en base a 100%
			$strQuery="SELECT (1-(SUM(PartesRe)/SUM(Partes)))*100 as YieldP FROM Log";
			if($this->conBDPDO()){
				$pQuery = $this->oConBD->prepare($strQuery);
				$pQuery->execute();
				$yieldt = $pQuery->fetchColumn();
			}
		} catch (PDOException $e) {
			echo "MySQL.getYield: " . $e->getMessage() . "\n";
			return -1;
		} 
		return $yieldt;
	}

	//Funcion que obtiene los datos que se requieren para crear la grafica de barras
	public function getDatosGrafica()
    {
        $jDatos = '';
        $rawdata = array();
        $i = 0;
        try {
            $strQuery = "SELECT SUM(PartesRe) as tRechazadas, SUM(PartesAc) as tAceptadas
            ,NumOrden as Orden, SUM(Partes) as tPartes FROM Log GROUP BY LogID";
            
            if ($this->conBDPDO()) {
                $pQuery = $this->oConBD->prepare($strQuery);
                $pQuery->execute();
                $pQuery->setFetchMode(PDO::FETCH_ASSOC);
                //Mientras siga encontrando registros seguira el ciclo
                while($producto = $pQuery->fetch()) {
                	//Se instancia la clase Grafica para guardar los datos de la grafica
                    $oGrafica = new Grafica();
                    //Se guardan los datos de la BD en las respectivas variables de la clase Grafica
                    $oGrafica->totalRechazadas = $producto['tRechazadas'];
                    $oGrafica->totalAceptadas = $producto['tAceptadas'];
                    $oGrafica->noOrden = $producto['Orden'];
                    $oGrafica->yield = (1-($producto['tRechazadas']/$producto['tPartes']))*100;
                    $rawdata[$i] = $oGrafica;
                    $i++;
                }
                $jDatos = json_encode( $rawdata);
            }
        } catch (PDOException $e) {
            echo "MySQL.getDatosGrafica: " . $e->getMessage() . "\n";
            return -1;
        }
        return $jDatos;
    }
}

//Datos de acceso publico que serviran para crear la grafica de barras
class Grafica{
    public $totalRechazadas = 0;
    public $totalAceptadas = 0;
    public $noOrden = 0; 
    public $yield = 0;
}
?>