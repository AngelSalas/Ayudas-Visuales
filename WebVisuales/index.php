<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="utf-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <meta name="description" content="" />
        <meta name="author" content="" />
        <title>Dashboard</title>
        <link href="css/styles.css" rel="stylesheet" />
        <link href="https://cdn.datatables.net/1.10.20/css/dataTables.bootstrap4.min.css" rel="stylesheet" crossorigin="anonymous" />
        <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/js/all.min.js" crossorigin="anonymous"></script>
    </head>
    <body class="sb-nav-fixed">
        <nav class="sb-topnav navbar navbar-expand navbar-dark bg-dark">
            <a class="navbar-brand" href="index.php">Ayudas Visuales</a>
            <button class="btn btn-link btn-sm order-1 order-lg-0" id="sidebarToggle" href="#"><i class="fas fa-bars"></i></button>
            <!-- Navbar-->
            
        </nav>
        <div id="layoutSidenav">
            <div id="layoutSidenav_nav">
                <nav class="sb-sidenav accordion sb-sidenav-dark" id="sidenavAccordion">
                    <div class="sb-sidenav-menu">
                        <div class="nav">
                            <!-- Menu de navegacion del dashboard-->
                            <div class="sb-sidenav-menu-heading">Navegación</div>
                            <a class="nav-link" href="index.php">
                                <div class="sb-nav-link-icon"><i class="fas fa-tachometer-alt"></i></div>
                                Dashboard
                            </a>
                             <a class="nav-link" href="php/Empleados.php">
                                <div class="sb-nav-link-icon"><i class="fas fa-tachometer-alt"></i></div>
                                Empleados
                            </a>
                             <a class="nav-link" href="php/Log.php">
                                <div class="sb-nav-link-icon"><i class="fas fa-tachometer-alt"></i></div>
                                Log
                            </a>
                             <a class="nav-link" href="php/Diagramas.php">
                                <div class="sb-nav-link-icon"><i class="fas fa-tachometer-alt"></i></div>
                                Diagramas
                            </a>
                        </div>
                    </div>
                    <!-- Footer del side menu-->
                    <div class="sb-sidenav-footer">
                        <div class="small">Proyecto:</div>
                        Ayudas Visuales
                    </div>
                </nav>
            </div>
            <div id="layoutSidenav_content">
                <main>
                    <div class="container-fluid">
                        <h1 class="mt-4">Dashboard</h1>
                        <div class="row">
                            <!-- Card de las piezas aceptadas asignadole idAceptadas-->
                            <div class="col-xl-3 col-md-6">
                                <div class="card bg-success text-white mb-4">
                                    <div class="card-header">Piezas Aceptadas
                                    </div>
                                    <div class="card-body">
                                        <h5 class="card-title"><span id="idAceptadas">0</span></h5>
                                        <p class="card-text">Total de piezas aceptadas</p>
                                    </div>
                                    
                                </div>
                            </div>
                            <!-- Card de las piezas rechazadas asignadole idRechazadas-->
                            <div class="col-xl-3 col-md-6">
                                <div class="card bg-danger text-white mb-4">
                                    <div class="card-header">Piezas Rechazadas
                                    </div>
                                    <div class="card-body">
                                        <h5 class="card-title"><span id="idRechazadas">0</span></h5>
                                        <p class="card-text">Total de piezas rechazadas</p>
                                    </div>
                                    
                                </div>
                            </div>
                            <!-- Card de las piezas totales asignadole idTotales-->
                            <div class="col-xl-3 col-md-6">
                                <div class="card bg-primary text-white mb-4">
                                    <div class="card-header">Piezas Totales
                                    </div>
                                    <div class="card-body">
                                        <h5 class="card-title"><span id="idTotales">0</span></h5>
                                        <p class="card-text">Total de piezas producidas</p>
                                    </div>
                                    
                                </div>
                            </div>
                            <!-- Card del yield asignadole idYield-->
                            <div class="col-xl-3 col-md-6">
                                <div class="card bg-warning text-white mb-4">
                                    <div class="card-header">Yield
                                    </div>
                                    <div class="card-body">
                                        <h5 class="card-title"><span id="idYield">0</span></h5>
                                        <p class="card-text">Yield promedio en total</p>
                                    </div>
                                    
                                </div>
                            </div>           
                        </div>
                    <!-- Creacion del Canvas para dibujar la grafica asignandole idGrafica-->
                    <div class="row my-3">
                        <div class="col-md-12 text-center">
                            <h2>Reporte de piezas</h2>
                            <canvas id="idGrafica" class="grafica" width="100%" height="35"></canvas>
                        </div>
                    </div>
                </main>
            </div>
        </div>
        <script src="js/jquery.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js" crossorigin="anonymous"></script>
        <script src="js/scripts.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.min.js" crossorigin="anonymous"></script>
        <script src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js" crossorigin="anonymous"></script>
        <script src="https://cdn.datatables.net/1.10.20/js/dataTables.bootstrap4.min.js" crossorigin="anonymous"></script>
        <script src="js/index.js"></script>
    </body>
</html>
