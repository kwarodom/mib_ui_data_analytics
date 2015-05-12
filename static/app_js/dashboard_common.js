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

$( document ).ready(function() {
    $.csrftoken();

    //var nick_re = /^[A-Za-z0-9_ ]*[A-Za-z0-9 ][A-Za-z0-9_ ]{5,10}$/;
    var nick_re = /^[A-Za-z0-9]{6,10}$/;

    /*$(".thermo_gauge").each(function(index) {

			var opts = {
					  lines: 12, // The number of lines to draw
					  angle: 0.20, // The length of each line
					  lineWidth: 0.15, // The line thickness
					  pointer: {
					    length: 0.9, // The radius of the inner circle
					    strokeWidth: 0.035, // The rotation offset
					    color: '#000000' // Fill color
					  },
					  limitMax: 'true',   // If true, the pointer will not go past the end of the gauge
					  //colorStart: '#6F6EA0',   // Colors
					  //colorStop: '#C0C0DB',    // just experiment with them
					  strokeColor: '#EEEEEE',   // to see which ones work best for you
					  generateGradient: true,
	      			  animationSpeed: 20,
	      			  fontSize: 15
					};
					var donut_target = document.getElementById(this.id); // your canvas element
					var donut = new Donut(donut_target).setOptions(opts); // create sexy gauge!
					//donut.maxValue = 3000; // set max gauge value
					donut.animationSpeed = 32; // set animation speed (32 is default value)
					//donut.set(1250);

					var power_id = this.id.split("_");
	      			text_field = power_id[1]+"-textfield";
	      			donut.setTextField(document.getElementById(text_field));
	      			var temp_value_id = power_id[1] + "_chvalue";
	      			temp_value = parseInt(document.getElementById(temp_value_id).innerHTML);
	      			$("#"+temp_value_id).hide();
	      			mode_value_id = power_id[1]+"_tmode";
	      			//$("#"+power_id[1]+"_tmode").hide();
	      			donut.maxValue = 100;
	      			if (document.getElementById(mode_value_id).innerHTML == "HEAT"){
	      				//donut.colorStart = '#F09022';
	      				//donut.colorStop = '#DB2602';
	      				var opts = {
	      					  lines: 12, // The number of lines to draw
	      					  angle: 0.20, // The length of each line
	      					  lineWidth: 0.15, // The line thickness
	      					  pointer: {
	      					    length: 0.9, // The radius of the inner circle
	      					    strokeWidth: 0.035, // The rotation offset
	      					    color: '#000000' // Fill color
	      					  },
	      					  limitMax: 'true',   // If true, the pointer will not go past the end of the gauge
	      					  colorStart: '#F09022',   // Colors
	      					  colorStop: '#DB2602',    // just experiment with them
	      					  strokeColor: '#EEEEEE',   // to see which ones work best for you
	      					  generateGradient: true,
	      	      			  animationSpeed: 20,
	      	      			  fontSize: 15
	      					};
	      			}
	      			if (document.getElementById(mode_value_id).innerHTML == "COOL"){
	      				//donut.colorStart = '#2EC3F0';
	      				//donut.colorStop = '#69DBD3';
	      				var opts = {
		      					  lines: 12, // The number of lines to draw
		      					  angle: 0.20, // The length of each line
		      					  lineWidth: 0.15, // The line thickness
		      					  pointer: {
		      					    length: 0.9, // The radius of the inner circle
		      					    strokeWidth: 0.035, // The rotation offset
		      					    color: '#000000' // Fill color
		      					  },
		      					  limitMax: 'true',   // If true, the pointer will not go past the end of the gauge
		      					  colorStart: '#2082A0',   // Colors
		      					  colorStop: '#65DBCF',    // just experiment with them
		      					  strokeColor: '#EEEEEE',   // to see which ones work best for you
		      					  generateGradient: true,
		      	      			  animationSpeed: 20,
		      	      			  fontSize: 15
		      					};
	      			}
	      			if (document.getElementById(mode_value_id).innerHTML == "AUTO"){
	      				//donut.colorStart = '#219E13';
	      				//donut.colorStop = '#2CDB32';
	      				var opts = {
		      					  lines: 12, // The number of lines to draw
		      					  angle: 0.20, // The length of each line
		      					  lineWidth: 0.15, // The line thickness
		      					  pointer: {
		      					    length: 0.9, // The radius of the inner circle
		      					    strokeWidth: 0.035, // The rotation offset
		      					    color: '#000000' // Fill color
		      					  },
		      					  limitMax: 'true',   // If true, the pointer will not go past the end of the gauge
		      					  colorStart: '#35E635',   // Colors
		      					  colorStop: '#275C21',    // just experiment with them
		      					  strokeColor: '#EEEEEE',   // to see which ones work best for you
		      					  generateGradient: true,
		      	      			  animationSpeed: 20,
		      	      			  fontSize: 15
		      					};
	      			}
	      			if (document.getElementById(mode_value_id).innerHTML == "OFF"){
	      				//donut.colorStart = '#737270';
	      				//donut.colorStop = '#DADBD9';
	      				var opts = {
		      					  lines: 12, // The number of lines to draw
		      					  angle: 0.20, // The length of each line
		      					  lineWidth: 0.15, // The line thickness
		      					  pointer: {
		      					    length: 0.9, // The radius of the inner circle
		      					    strokeWidth: 0.035, // The rotation offset
		      					    color: '#000000' // Fill color
		      					  },
		      					  limitMax: 'true',   // If true, the pointer will not go past the end of the gauge
		      					  colorStart: '#737270',   // Colors
		      					  colorStop: '#DADBD9',    // just experiment with them
		      					  strokeColor: '#EEEEEE',   // to see which ones work best for you
		      					  generateGradient: true,
		      	      			  animationSpeed: 20,
		      	      			  fontSize: 15
		      					};
	      			}

	      			//var gvalue = {{element.current_status.power}};
	      			if (temp_value == 0)
	      				temp_value = temp_value + 0.1;
	      			//power_value = 800;
	      			//alert(temp_value);
	      			donut.set(temp_value);
	      			donut.setOptions(opts);

			});
	 });
	 */


    $( ".save_changes" ).click(function(evt) {
		evt.preventDefault();
		values = this.id.split('-');
		device_id = values[1];
        device_type = values[2];
		values = values[1]+"_nickname";
		var value_er = values;
		nickname = $("#"+values).val();
		var error_id = "viewediterror_" + device_id;
		if (!nick_re.test(nickname)) {
			document.getElementById(error_id).innerHTML = "Nickname error. Please try again.";
			document.getElementById(values).value = "";
		} else {
		values = {
			    "id": device_id,
			    "nickname": nickname,
                "device_type": device_type
			    };
		document.getElementById(error_id).innerHTML = "";
	    var jsonText = JSON.stringify(values);
		$.ajax({
			  url : '/save_view_edit_changes_dashboard/',
			  type: 'POST',
			  data: jsonText,
			  contentType: "application/json; charset=utf-8",
			  dataType: 'json',
			  success : function(data) {
				if (data == "invalid") {
					document.getElementById(error_id).innerHTML = "Nickname error. Please try again.";
					document.getElementById(value_er).value = "";
				} else {
				req_value_modal = data.device_id+"_nick"
				req_val_stats = data.device_id + "_nickname_header";
              	var newtest = document.getElementById(req_value_modal);
              	document.getElementById(req_val_stats).innerHTML = nickname.charAt(0).toUpperCase()+nickname.slice(1);
            	newtest.innerHTML = nickname.charAt(0).toUpperCase()+nickname.slice(1);
			  	$('.bottom-right').notify({
			  	    message: { text: 'Heads up! The device nickname change was successful.' },
			  	    type: 'blackgloss',
                    fadeOut: { enabled: true, delay: 5000 }
			  	  }).show();
				}
			  },
			  error: function(data) {
				  $('.bottom-right').notify({
				  	    message: { text: 'Error! Use close button to exit / Click on edit button to change nickname. ' },
				  	    type: 'blackgloss',
                      fadeOut: { enabled: true, delay: 5000 }
				  	}).show();
			  }
			 });
	}
	});

    $(".identify").click(function (evt) {
        evt.preventDefault();
        var identifier = (this).id;
        identify_id = identifier.split("-");
        identify_id = identify_id[1];
        //alert(identify_id);
        values = {
            "id": identify_id,
            "zone_id": this_id
        };
        var jsonText = JSON.stringify(values);
        $.ajax({
            url: '/identify_device/',
            type: 'POST',
            data: jsonText,
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            success: function (data) {
                //alert(data);

                if (data.indexOf("success") > -1) {
                    $('#' + identify_id + "-spin").addClass('fa fa-spinner fa-spin').removeClass('icon-search');
                    //$('#'+identify_id+"-spin").removeClass('icon-search');
                    $("#" + identifier).removeClass('btn-warning').addClass('btn-success disabled');
                    //$("#"+identifier).addClass('btn-success');
                    /*var setTimeOut_identifier = setTimeout(function() {
                     $('#'+identify_id+"-spin").removeClass('fa fa-spinner fa-spin').addClass('icon-search');
                     //$('#'+identify_id+"-spin").addClass('icon-search');
                     $("#"+identifier).removeClass('btn-success').addClass('btn-warning');
                     //$("#"+identifier).addClass('btn-warning');
                     }, 10000);*/
                    identify_status(identify_id, identifier);
                    $('.bottom-right').notify({
                        message: { text: 'Communicating with the device for identification...' },
                        type: 'blackgloss',
                        fadeOut: { enabled: true, delay: 5000 }
                    }).show();
                    //clearInterval(setTimeOut_identifier);
                }
            },
            error: function (data) {
                $('.bottom-right').notify({
                    message: { text: 'Oh snap! Try again. ' },
                    type: 'blackgloss',
                    fadeOut: { enabled: true, delay: 5000 }
                }).show();
            }
        });
    });


    function identify_status(identify_id, identifier) {
        var setTimeOut_identifier = setTimeout(function () {
            $.ajax({
                url: '/identify_status/',
                type: 'POST',
                data: identify_id,
                //dataType : 'text',
                success: function (data) {
                    update_status = data.status;
                    console.log(update_status);
                    if (update_status.indexOf("success") > -1) {
                        $('#' + identify_id + "-spin").removeClass('fa fa-spinner fa-spin').addClass('icon-search');
                        $("#" + identifier).removeClass('btn-success disabled').addClass('btn-warning');
                        stopTimer('setTimeOut_identifier');
                    }
                    else {
                        $('#' + identify_id + "-spin").removeClass('fa fa-spinner fa-spin').addClass('icon-search');
                        $("#" + identifier).removeClass('btn-success disabled').addClass('btn-warning');
                        stopTimer('setTimeOut_identifier');
                        $('.bottom-right').notify({
                            message: { text: data.status},
                            type: 'blackgloss',
                            fadeOut: { enabled: true, delay: 5000 }
                        }).show();
                    }
                },
                error: function (data) {
                    identify_status(identify_id, identifier);
                    //$('#'+identify_id+"-spin").removeClass('fa fa-spinner fa-spin').addClass('icon-search');
                    //$("#"+identifier).removeClass('btn-success').addClass('btn-warning');
                    /*$('.bottom-right').notify({
                     message: { text: 'Could not communicate with the device for identification. Please try again! ' },
                     type: 'blackgloss'
                     }).show();*/
                }
            });
        }, 3000);
    }


    function stopTimer(setTimeOut_identifier) {
        clearInterval(setTimeOut_identifier);
    }

    $(function () {

            $("#sortable1").sortable({
                connectWith: ".connectedSortable"
            }).disableSelection();

        });

        $(".panel").mousemove(function (e) {
            if (e.which == 1) {
                if ($(".panel-collapse").hasClass("collapse")) {
                    $(".panel-collapse").removeClass("collapse");
                    $(".panel-collapse").addClass("in");
                    $(".panel-body").show();
                    //alert("testing");
                }

            } else {

                $(".panel-body").mouseenter(function (e) {
                    if (e.which == 1) {
                        $(".panel-body").show();
                    }
                });
            }
        });

});