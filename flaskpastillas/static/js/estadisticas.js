var chart;

$(document).ready(function() {
   var datos = eval($("#container_data").text());

   chart = new Highcharts.Chart({
      chart: {
         renderTo: 'container',
         plotBackgroundColor: null,
         plotBorderWidth: null,
         plotShadow: false
      },
      title: {
         text: 'Llamadas realizadas una o mas veces',
      },
      tooltip: {
         formatter: function() {
            return '<b>'+ this.point.name +'</b>: '+ this.percentage +' %';
         }
      },
      plotOptions: {
         pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
               enabled: true,
               formatter: function() {
                  return '<b>'+ this.point.name +'</b>: '+ this.percentage +' %';
               }
            }
         }
      },
       series: [{
         type: 'pie',
         name: 'Browser share',
         data: datos,
      }]
   });
});
