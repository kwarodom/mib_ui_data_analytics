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
			      labels:["Real Power","Power Factor"]
			    },
                series:[{
                    label: 'Power (W)',
                    neighborThreshold: -1,
                    yaxis: 'yaxis'
                }, {
                    label: 'Power Factor',
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
		            min : _real_power[0][0],
		            max: _real_power[_real_power.length-1][0]
			      },
			      yaxis: {
			        min:0,
			        max:100,
			        label: "Power (W)"
			      },
                  y2axis: {
                    min:0,
			        max:1,
			        label: "Power Factor"
                  }
			    }
	  };

    var options_energy = {
			    legend: {
			      show: true,
			      labels:["Power Factor"]
			    },
                series:{
                    label: "Power Factor",
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
		            min : _power_factor[0][0],
		            max: _power_factor[_power_factor.length-1][0]
			      },
			      yaxis: {
			        min:0,
			        max:1,
			        label: "Power Factor"
			      }
			    }
	  };



	  //Initialize plot for lighting
      var data_points = [_real_power, _power_factor];
	  var plot1 = $.jqplot('chart100', data_points ,options);
      $("#real_power").attr('checked','checked');
      $("#pfactor").attr('checked','checked');

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
              var _real_power = _data.real_power;
              var _power_factor = _data.power_factor;
              var new_data = [];

              $.each($('input:checked'), function(index, value){
                   //new_data.push(outdoor_temp);
                   if (this.id == 'real_power') {
                       new_data.push(_real_power);
                   } else if (this.id == 'pfactor') {
                       new_data.push(_power_factor);
                   }
                   options.legend.labels.push(this.value);
                   options.axes.xaxis.min = _real_power[0][0];
                   options.axes.xaxis.max = _real_power[_real_power.length-1][0];
              });
              if ($('input:checked').length == 1 && $('input:checked')[0].id == 'pfactor') {
                  options_energy.legend.labels.push('Power Factor');
                  options_energy.axes.yaxis.min = 0;
                  options_energy.axes.yaxis.max = 1;
                  options_energy.axes.xaxis.min = _power_factor[0][0];
                  options_energy.axes.xaxis.max = _power_factor[_power_factor.length-1][0];

                  if (plot1) {
                        plot1.destroy();
                   }

                  var plot2 = $.jqplot('chart100', new_data ,options_energy);
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
				  url : '/pmtr_smap_update/',
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
                   if (this.id == 'real_power') {
                       new_data.push(_real_power);
                   } else if (this.id == 'pfactor') {
                       new_data.push(_power_factor);
                   }
                   options.legend.labels.push(this.value);
                   options.axes.xaxis.min = _real_power[0][0];
                   options.axes.xaxis.max = _real_power[_real_power.length-1][0];
              });
              if ($('input:checked').length == 1 && $('input:checked')[0].id == 'pfactor') {
                  options_energy.legend.labels.push('Power Factor');
                  options_energy.axes.yaxis.min = 0;
                  options_energy.axes.yaxis.max = 1;
                  options_energy.axes.xaxis.min = _power_factor[0][0];
                  options_energy.axes.xaxis.max = _power_factor[_power_factor.length-1][0];

                  if (plot1) {
                        plot1.destroy();
                   }

                  var plot2 = $.jqplot('chart100', new_data ,options_energy);
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


      }



});