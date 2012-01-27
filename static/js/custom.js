
$(document).ready(function (){

    // Se marca como activo el link al tab que se esta viendo
    seccion = '/' +  window.location.pathname.split('/')[1];
    $('ul.tabs li').has('a[href="'+seccion+'"]').addClass('active');

})
