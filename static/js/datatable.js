$(document).ready(function() {
        $('#llamadas').dataTable({
            "bLengthChange": false,
            "bInfo": true,
            "bPaginate": true,
            "bSortable": false,

            "bSort": true,
            "bServerSide": true,
            "sAjaxSource": "/obtener_llamadas",
    });
});
