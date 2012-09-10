$(document).ready(function() {
    $('#datepicker').datepicker({
	        format: 'yyyy-mm-dd'
		});
    configurar_formulario_filtro();
});


function configurar_formulario_filtro() {
    $("#form").bind('submit',function(){
        var $datepicker = $('#datepicker');
        limpiar_filtros();
        if ($.trim($datepicker.val()).length != 0) {
            actualizar_filtros($datepicker.val());
        }
        return false;
    });
}


function conectar_indicador_actividad() {
    $(document).ajaxStart(function() {
        $('#keyword').addClass('working');
    });
    $(document).ajaxStop(function() {
        $('#keyword').removeClass('working');
    });
}


function limpiar_filtros() {
    $('#regex_table tbody').html('');
    $('#xquery_table tbody').html('');
}


function actualizar_filtros(keyword) {
    actualizar_filtro_regex(keyword);
}


function actualizar_filtro_regex(keyword) {
    $.getJSON('/query3/?', {'q':keyword}, function(data) {
        var items = [];
        var titles = data.titles
        $.each(titles, function(index) {
            items.push('<tr><td>' + titles[index] + '</td></tr>');
        });
        $('#regex_table tbody').html(items.join(''));
    });
}


function actualizar_filtro_xquery(keyword) {
    $.get('/filtro_xquery/?', {'q':keyword}, function(data) {
        $('#xquery_table tbody').html(data);
    });
}
