
$(document).ready(function (){

    // Se marca como activo el link al tab que se esta viendo
    seccion = '/' +  window.location.pathname.split('/')[1];
    $('ul.tabs li').has('a[href="'+seccion+'"]').addClass('active');

    $("#fum").datepicker();
    $("a.close").click(function(){$("a.close").closest("div").fadeOut()});

    $('.plegable .cuerpo').hide();
    $('.plegable .titulo').click(function() {
        alternar_fondo($('.titulo'));


     
        $(this).next(".cuerpo").slideToggle(600);
    });
})

function alternar_fondo(elemento)
{
    var imagen = elemento.css('background-image');

    if (/expand/.test(imagen))
        imagen = imagen.replace('expand', 'collapse');
    else
        imagen = imagen.replace('collapse', 'expand');

    elemento.css('background-image', imagen);
    console.log(imagen);
}
