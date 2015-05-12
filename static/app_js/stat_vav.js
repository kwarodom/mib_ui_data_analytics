/**

 *  Authors: Kruthika Rathinavel
 *  Version: 2.0
 *  Email: kruthika@vt.edu
 *  Created: "2014-10-13 18:45:40"
 *  Updated: "2015-02-13 15:06:41"


 * Copyright © 2014 by Virginia Polytechnic Institute and State University
 * All rights reserved

 * Virginia Polytechnic Institute and State University (Virginia Tech) owns the copyright for the BEMOSS software and its
 * associated documentation ("Software") and retains rights to grant research rights under patents related to
 * the BEMOSS software to other academic institutions or non-profit research institutions.
 * You should carefully read the following terms and conditions before using this software.
 * Your use of this Software indicates your acceptance of this license agreement and all terms and conditions.

 * You are hereby licensed to use the Software for Non-Commercial Purpose only.  Non-Commercial Purpose means the
 * use of the Software solely for research.  Non-Commercial Purpose excludes, without limitation, any use of
 * the Software, as part of, or in any way in connection with a product or service which is sold, offered for sale,
 * licensed, leased, loaned, or rented.  Permission to use, copy, modify, and distribute this compilation
 * for Non-Commercial Purpose to other academic institutions or non-profit research institutions is hereby granted
 * without fee, subject to the following terms of this license.

 * Commercial Use: If you desire to use the software for profit-making or commercial purposes,
 * you agree to negotiate in good faith a license with Virginia Tech prior to such profit-making or commercial use.
 * Virginia Tech shall have no obligation to grant such license to you, and may grant exclusive or non-exclusive
 * licenses to others. You may contact the following by email to discuss commercial use:: vtippatents@vtip.org

 * Limitation of Liability: IN NO EVENT WILL VIRGINIA TECH, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR REDISTRIBUTE
 * THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR
 * CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO
 * LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE
 * OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF VIRGINIA TECH OR OTHER PARTY HAS BEEN ADVISED
 * OF THE POSSIBILITY OF SUCH DAMAGES.

 * For full terms and conditions, please visit https://bitbucket.org/bemoss/bemoss_os.

 * Address all correspondence regarding this license to Virginia Tech's electronic mail address:: vtippatents@vtip.org

**/

$(document).ready(function(){
    $.csrftoken();
	  //Plot options
	  var options = {
			    legend: {
			      show: true,
			      labels:["Temperature","Supply Temperature", "Heat Set Point", "Cool Set Point", "Flap Position"]
			    },
                series:[{
                    label: 'Temperature °F',
                    neighborThreshold: -1,
                    yaxis: 'yaxis'
                }, {
                    label: 'Flap Position (%)',
                    yaxis: 'y2axis'
                }],
			    cursor: {
			           show: true,
			           zoom: true
			    },
			    seriesDefaults: {
                  show: true,
			      showMarker:false,
			      pointLabels: {show:false},
			      rendererOption:{smooth: true}
			    },
			    axesDefaults: {
			      labelRenderer: $.jqplot.CanvasAxisLabelRenderer
			    },
			    axes: {
			      xaxis: {
			        label: "Time",
			        renderer: $.jqplot.DateAxisRenderer,
			        tickOptions:{formatString:'%I:%M:%S %p'},
			        numberTicks: 10,
		            min : _temperature[0][0],
		            max: _temperature[_temperature.length-1][0]
			      },
			      yaxis: {
			        min:0,
			        max:100,
			        label: "Temperature °F"
			      },
                  y2axis: {
                    min:0,
			        max:100,
			        label: "Flap Position (%)"
                  }
			    }
	  };

    var options_flap_position = {
			    legend: {
			      show: true,
			      labels:["Flap Position"]
			    },
                series:{
                    label: "Flap Position (%)",
                    neighborThreshold: -1,
                    yaxis: 'yaxis'
                },
			    cursor: {
			           show: true,
			           zoom: true
			    },
			    seriesDefaults: {
                  show: true,
			      showMarker:false,
			      pointLabels: {show:false},
			      rendererOption:{smooth: true}
			    },
			    axesDefaults: {
			      labelRenderer: $.jqplot.CanvasAxisLabelRenderer
			    },
			    axes: {
			      xaxis: {
			        label: "Time",
			        renderer: $.jqplot.DateAxisRenderer,
			        tickOptions:{formatString:'%I:%M:%S %p'},
			        numberTicks: 10,
		            min : _flap_position[0][0],
		            max: _flap_position[_flap_position.length-1][0]
			      },
			      yaxis: {
			        min:0,
			        max:100,
			        label: "Flap Position (%)"
			      }
			    }
	  };



	  //Initialize plot for lighting
      var data_points = [_temperature, _supply_temperature, _heat_setpoint, _cool_setpoint, _flap_position];
	  var plot1 = $.jqplot('chart100', data_points ,options);
      $("#temperature").attr('checked','checked');
      $("#supply_temp").attr('checked','checked');
      $("#heat_set_point").attr('checked','checked');
      $("#cool_set_point").attr('checked','checked');
      $("#flap_position").attr('checked','checked');

      temp = {
            seriesStyles: {
                seriesColors: ['red', 'orange', 'yellow', 'green', 'blue', 'indigo'],
                highlightColors: ['lightpink', 'lightsalmon', 'lightyellow', 'lightgreen', 'lightblue', 'mediumslateblue']
            },
            grid: {
                //backgroundColor: 'rgb(211, 233, 195)'
            },
            axesStyles: {
               borderWidth: 0,
               label: {
                   fontFamily: 'Sans',
                   textColor: 'white',
                   fontSize: '9pt'
               }
            }
        };


        plot1.themeEngine.newTheme('uma', temp);
        plot1.activateTheme('uma');

        var timeOut;

        function update_plot(_data) {
              _temperature = _data.temperature;
              _supply_temperature = _data.supply_temperature;
              _heat_setpoint = _data.heat_setpoint;
              _cool_setpoint = _data.cool_setpoint;
              _flap_position = _data.flap_position;
              var new_data = [];

              $.each($('input:checked'), function(index, value){
                   //new_data.push(outdoor_temp);
                   if (this.id == 'temperature') {
                       new_data.push(_temperature);
                   } else if (this.id == 'supply_temp') {
                       new_data.push(_supply_temperature);
                   } else if (this.id == 'heat_set_point') {
                       new_data.push(_heat_setpoint);
                   } else if (this.id == 'cool_set_point') {
                       new_data.push(_cool_setpoint);
                   } else if (this.id == 'flap_position') {
                       new_data.push(_flap_position);
                   }
                   options.legend.labels.push(this.value);
                   options.axes.xaxis.min = _temperature[0][0];
                   options.axes.xaxis.max = _temperature[_temperature.length-1][0];
              });
              if ($('input:checked').length == 1 && $('input:checked')[0].id == 'flap_position') {
                  options_flap_position.legend.labels.push('Flap Position');
                  options_flap_position.axes.yaxis.min = 0;
                  options_flap_position.axes.yaxis.max = 100;
                  options_flap_position.axes.xaxis.min = _flap_position[0][0];
                  options_flap_position.axes.xaxis.max = _flap_position[_flap_position.length-1][0];

                  if (plot1) {
                        plot1.destroy();
                   }

                  var plot2 = $.jqplot('chart100', new_data ,options_flap_position);
                  plot2.themeEngine.newTheme('uma', temp);
                  plot2.activateTheme('uma');

              } else {

                   if (plot1) {
                        plot1.destroy();
                    }

              //var plot2 = $('#chart100').jqplot(new_data, options);
                  plot2 = $.jqplot('chart100', new_data ,options);
                  plot2.themeEngine.newTheme('uma', temp);
                  plot2.activateTheme('uma');
              }



              console.log('nowww');
              $("#auto_update").attr('disabled','disabled');
              $("#stop_auto_update").removeAttr('disabled');
        }


        function do_update() {
            var values = {
		        "device_info": device_info
		    };
	        var jsonText = JSON.stringify(values);
            console.log(jsonText);
			//setTimeout(function() {
				$.ajax({
				  url : '/vav_smap_update/',
				  //url : 'http://38.68.237.143/backend/api/data/uuid/97699b93-9d6d-5e31-b4ef-7ac78fdc985a',
				  type: 'POST',
                  data: jsonText,
                  dataType: 'json',
				  //dataType: 'jsonp',
				  success : function(data) {
					//update_status = $.parseJSON(data.status);
					  console.log ("testing");
					  console.log (data);
                      update_plot(data);
    			  	  //stopTimer('setTimeOut_chartUpdate');
				  },
				  error: function(data) {

                      clearTimeout(timeOut);
                      $('.bottom-right').notify({
					  	    message: { text: 'Communication Error. Try again later!'},
					  	    type: 'blackgloss',
                          fadeOut: { enabled: true, delay: 5000 }
					  	  }).show();
				  }
				 });
                timeOut = setTimeout(do_update, 30000);
			//},5000);
	}

    	  //Auto update the chart
	  $('#auto_update').click( function(evt){
          evt.preventDefault();
	      do_update();
	   });

      $('#stop_auto_update').click(function(){
          clearTimeout(timeOut);
          $('#stop_auto_update').attr('disabled', 'disabled');
          $('#auto_update').removeAttr('disabled');
      });

        $('#stack_chart').click( function(evt){
            evt.preventDefault();
	        stackCharts();
	   });

	  function stackCharts(){
        if (timeOut) {
          clearTimeout(timeOut);
          $('#stop_auto_update').attr('disabled', 'disabled');
          $('#auto_update').removeAttr('disabled');
        }
        options.legend.labels = [];
        var new_data = [];
        $.each($('input:checked'), function(index, value){
           //new_data.push(outdoor_temp);
           if (this.id == 'temperature') {
               new_data.push(_temperature);
           } else if (this.id == 'supply_temp') {
               new_data.push(_supply_temperature);
           } else if (this.id == 'heat_set_point') {
               new_data.push(_heat_setpoint);
           } else if (this.id == 'cool_set_point') {
               new_data.push(_cool_setpoint);
           } else if (this.id == 'flap_position') {
               new_data.push(_flap_position);
           }
           options.legend.labels.push(this.value);
           options.axes.xaxis.min = _temperature[0][0];
           options.axes.xaxis.max = _temperature[_temperature.length-1][0];
        });

          if ($('input:checked').length == 1 && $('input:checked')[0].id == 'flap_position') {
                  options_flap_position.legend.labels.push('Flap Position');
                  options_flap_position.axes.yaxis.min = 0;
                  options_flap_position.axes.yaxis.max = 100;
                  options_flap_position.axes.xaxis.min = _flap_position[0][0];
                  options_flap_position.axes.xaxis.max = _flap_position[_flap_position.length-1][0];

                  if (plot1) {
                        plot1.destroy();
                   }

                  var plot2 = $.jqplot('chart100', new_data ,options_flap_position);
                  plot2.themeEngine.newTheme('uma', temp);
                  plot2.activateTheme('uma');

              } else {

                   if (plot1) {
                        plot1.destroy();
                    }

                  plot2 = $.jqplot('chart100', new_data ,options);
                  plot2.themeEngine.newTheme('uma', temp);
                  plot2.activateTheme('uma');
              }

      }



});