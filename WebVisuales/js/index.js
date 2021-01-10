function index() {
    //Funcion principal que se ejecutara en el index
    this.ini = function () {
        console.log("Iniciando...");
        this.getInidicadores();
        this.getDatosGraficas();
    }

    //Funcion que envia los datos que requiere servidor.php
    this.getInidicadores = function () {
        //Piezas aceptadas
        $.ajax({
            statusCode: {
                404: function () {
                    console.log("Esta página no existe");
                }
            },
            url: 'php/servidor.php',
            method: 'POST',
            data: {
                rq: "1"
            }
            //Una vez que se hace todo el proceso, guarda los resultados que se obtuvo de la funcion getAceptadas de mysql.php en datos
        }).done(function (datos) {
            //Muestra el resultado en el Card con idAceptadas de index.php y transforma los datos a tipo float local
            $("#idAceptadas").text(parseFloat(datos).toLocaleString());
        });

        //Piezas rechazadas
        $.ajax({
            statusCode: {
                404: function () {
                    console.log("Esta página no existe");
                }
            },
            url: 'php/servidor.php',
            method: 'POST',
            data: {
                rq: "2"
            }
            //Una vez que se hace todo el proceso, guarda los resultados que se obtuvo de la funcion getRechazadas de mysql.php en datos
        }).done(function (datos) {
            //Muestra el resultado en el Card con idRechazadas de index.php y transforma los datos a tipo float local
            $("#idRechazadas").text(parseFloat(datos).toLocaleString());
        });

        //Piezas totales
        $.ajax({
            statusCode: {
                404: function () {
                    console.log("Esta página no existe");
                }
            },
            url: 'php/servidor.php',
            method: 'POST',
            data: {
                rq: "3"
            }
            //Una vez que se hace todo el proceso, guarda los resultados que se obtuvo de la funcion getTotales de mysql.php en datos
        }).done(function (datos) {
            //Muestra el resultado en el Card con idTotales de index.php y transforma los datos a tipo float local
            $("#idTotales").text(parseFloat(datos).toLocaleString());
        });

        //Yield
        $.ajax({
            statusCode: {
                404: function () {
                    console.log("Esta página no existe");
                }
            },
            url: 'php/servidor.php',
            method: 'POST',
            data: {
                rq: "5"
            }
            //Una vez que se hace todo el proceso, guarda los resultados que se obtuvo de la funcion getYield de mysql.php en datos
        }).done(function (datos) {
            //Muestra el resultado en el Card con idYield de index.php y transforma los datos a tipo float local
            $("#idYield").text(parseFloat(datos).toLocaleString());
        });
    }

    //Funcion para crear la grafica con los datos obtenidos del query
    this.getDatosGraficas = function () {
        $.ajax({
            statusCode: {
                404: function () {
                    console.log("Esta página no existe");
                }
            },
            url: 'php/servidor.php',
            method: 'POST',
            data: {
                rq: "4"
            }
        }).done(function (datos) {  
            if (datos != '') {
                 //Creando los arreglos necesarios para crear la grafica
                let etiquetas = new Array();
                let tAceptadas = new Array();
                let tRechazadas = new Array();
                let tYield = new Array(); 
                let coloresV = new Array();
                let coloresP = new Array();
                let coloresY = new Array();
                var jDatos = JSON.parse(datos);

                //Guardando todos los datos que se generaron del query de getGrafica en mysql.php
                for (let i in jDatos) {
                    //En este caso la etiqueta de cada barra sera su numero de orden
                    etiquetas.push(jDatos[i].noOrden);
                    tAceptadas.push(jDatos[i].totalAceptadas);
                    tRechazadas.push(jDatos[i].totalRechazadas);
                    tYield.push(jDatos[i].yield);
                    coloresV.push("#12F72B");
                    coloresP.push("#C70039");
                    coloresY.push("#3498DB");

                }

                //Se toma el id del Canvas creado para la grafica y se inicializa de tipo bar en este caso para una
                //grafica de barras.
                var ctx = document.getElementById('idGrafica').getContext('2d');
                var myChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        //Se asigna la etiqueta de cada barra utilizando el arreglo etiquetas creado anteriormente
                        labels: etiquetas,
                        datasets: [
                            {
                                //Se asigna la etiqueta Aceptadas que se mostrara al pasar el puntero por encima de la barra
                                //ademas de asignarle tAceptadas en los que se basara para crear la grafica y el color de la misma
                                label: 'Aceptadas',
                                data: tAceptadas,
                                backgroundColor: coloresV
                            },
                            {
                                //Se asigna la etiqueta Rechazadas que se mostrara al pasar el puntero por encima de la barra
                                //ademas de asignarle tRechazadas en los que se basara para crear la grafica y el color de la misma
                                label: 'Rechazadas',
                                data: tRechazadas,
                                backgroundColor: coloresP
                            },
                            {
                                //Se asigna la etiqueta Yield que se mostrara al pasar el puntero por encima de la barra
                                //ademas de asignarle tYield en los que se basara para crear la grafica y el color de la misma
                                label: 'Yield',
                                data: tYield,
                                backgroundColor: coloresY
                            }
                        ]
                    }
                });
            }
        });
    }
}

//Se instancia la clase index y la funcion ini se ejecuta cada 10 segundos
var oIndex = new index();
setTimeout(function () { oIndex.ini(); }, 100);
setInterval(function () { oIndex.ini(); }, 30000);