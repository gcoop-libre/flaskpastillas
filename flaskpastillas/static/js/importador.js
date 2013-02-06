function mostrar_boton_procesar() {
    $("#procesar").fadeIn();
    $(".box img").attr("src", "/static/ok.png");
}

function mostrar_boton_errores() {
    $("#boton_error").fadeIn();
    $("#mensaje_de_error").fadeIn();
}

function monitorizar_tarea(tarea_id) {
    global_tarea_id = tarea_id;
    $.get('/importar/obtener_estado/' + tarea_id, agregar_resultado_o_pulling);
}

function agregar_resultado_o_pulling(data) {
    console.log(data);
    if (data['resultado']) {
        mostrar_boton_procesar();
        mostrar_barra_de_progreso_terminada();
        $('.box #status #mensaje').html("Terminado");
        actualizar_contadores_de_progreso(data.resultado);

        if (data.resultado.incorrectos > 0) {
            mostrar_boton_errores();
        }
    } else {

        if (data['procesados']) {
            actualizar_barra_de_progreso(data);
            actualizar_contadores_de_progreso(data);
            $('.box #status #mensaje').html("En curso");
        }
        else {
            $('.box #status #mensaje').html(data['status']);
        }

        setTimeout("monitorizar_tarea('" + global_tarea_id + "')", 100);
    }
}

function actualizar_contadores_de_progreso(data) {
    $('.box #status #procesados').html(data['procesados']);
    $('.box #status #total').html(data['total']);
    $('.box #status #correctos').html(data['correctos']);
    $('.box #status #incorrectos').html(data['incorrectos']);
    $('#cantidad_errores').html(data['incorrectos']);
}

function actualizar_barra_de_progreso(data) {
    var total = data['total'];
    var procesados = data['procesados'];
    var porcentaje = (procesados / total) * 100;

    definir_progreso_de_la_barra(porcentaje);
}

function mostrar_barra_de_progreso_terminada() {
    definir_progreso_de_la_barra(100);
}

function definir_progreso_de_la_barra(porcentaje) {
    $('.bar').attr('style', 'width: ' + porcentaje + '%');
}
