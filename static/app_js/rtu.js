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

    var _values_on_submit = {};
    var update_time;

    var ws = new WebSocket("ws://" + window.location.host + "/socket_rtu");
     ws.onopen = function () {
         ws.send("WS opened from html page");
     };
     ws.onmessage = function (event) {
         var _data = event.data;
         _data = $.parseJSON(_data);
         var topic = _data['topic'];
         // ["", "ui", "web", "rtu", "999", "Wifithermostat1", "device_status", "response"]
         if (topic) {
             topic = topic.split('/');
             console.log(topic);
             if (topic[5] == device_id && topic[6] == 'device_status') {
                 if ($.type( _data['message'] ) === "string"){
                     var _message = $.parseJSON(_data['message']);
                     change_rtu_values(_message);
                 } else if ($.type( _data['message'] ) === "object"){
                     change_rtu_values(_data['message']);
                 }

             }
             if (topic[5] == device_id && topic[6] == 'update') {
                 var message_upd = _data['message'];
                 if (message_upd.indexOf('success') > -1) {
                     change_rtu_values_on_submit_success(_values_on_submit);
                     $('.bottom-right').notify({
                        message: { text: 'The changes made at '+update_time+" are now updated in the device!"},
                        type: 'blackgloss',
                         fadeOut: { enabled: true, delay: 5000 }
                      }).show();
                 }
             }
         }
     };

    function change_rtu_values_on_submit_success(_data) {
        /*  "heat_setpoint": heat_setpoint,
            "cool_setpoint": cool_setpoint,
            "fan_status": fan_status,
            "cooling_status": cooling_status,
            "cooling_mode": cooling_mode,
            "heating": heating,
            "outside_damper_position": outside_damper,
            "bypass_damper_position": bypass_damper,
            "device_info": device_info */
        if (_data.fan_status == 'ON') {
            if ($("#on_fan").hasClass('btn-default')) {
                $("#on_fan").removeClass('btn-default').addClass('btn-success');
                $("#off_fan").removeClass('btn-success').addClass('btn-default');
            }
        }

        if (_data.cooling_status == 'ON') {
            if ($("#on_cool").hasClass('btn-default')) {
                $("#on_cool").removeClass('btn-default').addClass('btn-success');
                $("#off_cool").removeClass('btn-success').addClass('btn-default');
            }
        }

        $('#heating').slider({ value: _data.heating });
        $("#heating_level").text(_data.heating);

        $('#outside_damper').slider({ value: _data.outside_damper_position });
        $("#outside_damper_val").text(_data.outside_damper_position);

        $('#bypass_damper').slider({ value: _data.bypass_damper_position });
        $("#bypass_damper_val").text(_data.bypass_damper_position);

        $("#heat_setpoint").text(_data.heat_setpoint);
        $("#cool_setpoint").text(_data.cool_setpoint);

        if (_data.cooling_mode == 'None') {
            $("#coolmode").text("None");
        } else if (_data.cooling_mode == 'STG1') {
            $("#coolmode").text("Stage 1 Cooling");
        } else if (_data.cooling_mode == 'STG2') {
            $("#coolmode").text("Stage 2 Cooling");
        } else if (_data.cooling_mode == 'STG3') {
            $("#coolmode").text("Stage 3 Cooling");
        } else if (_data.cooling_mode == 'STG4') {
            $("#coolmode").text("Stage 4 Cooling");
        }

        //$("#coolmode").text(_data.cooling_mode);
    }

    function change_rtu_values(_data) {
        /*  "heat_setpoint": heat_setpoint,
            "cool_setpoint": cool_setpoint,
            "fan_status": fan_status,
            "cooling_status": cooling_status,
            "cooling_mode": cooling_mode,
            "heating": heating,
            "outside_damper_position": outside_damper,
            "bypass_damper_position": bypass_damper,
            "device_info": device_info */
        if (_data.fan_status == 'ON') {
            if ($("#on_fan").hasClass('btn-default')) {
                $("#on_fan").removeClass('btn-default').addClass('btn-success');
                $("#off_fan").removeClass('btn-success').addClass('btn-default');
            }
        }

        if (_data.cooling_status == 'ON') {
            if ($("#on_cool").hasClass('btn-default')) {
                $("#on_cool").removeClass('btn-default').addClass('btn-success');
                $("#off_cool").removeClass('btn-success').addClass('btn-default');
            }
        }

        $('#heating').slider({ value: _data.heating });
        $("#heating_level").text(_data.heating);

        $('#outside_damper').slider({ value: _data.outside_damper_position });
        $("#outside_damper_val").text(_data.outside_damper_position);

        $('#bypass_damper').slider({ value: _data.bypass_damper_position });
        $("#bypass_damper_val").text(_data.bypass_damper_position);

        $("#heat_setpoint").text(_data.heat_setpoint);
        $("#cool_setpoint").text(_data.cool_setpoint);

        $("#outside_temp").text(_data.outdoor_temperature);
        //$("#return_temp").text(_data.return_temperature);
        //$("#supply_temp").text(_data.supply_temperature);
        //$("#pressure").text(_data.pressure);
        $("#return_temp").text("--");
        $("#supply_temp").text("--");
        $("#pressure").text("--");

        if (_data.cooling_mode == 'None') {
            $("#coolmode").text("None");
        } else if (_data.cooling_mode == 'STG1') {
            $("#coolmode").text("Stage 1 Cooling");
        } else if (_data.cooling_mode == 'STG2') {
            $("#coolmode").text("Stage 2 Cooling");
        } else if (_data.cooling_mode == 'STG3') {
            $("#coolmode").text("Stage 3 Cooling");
        } else if (_data.cooling_mode == 'STG4') {
            $("#coolmode").text("Stage 4 Cooling");
        }

        //$("#coolmode").text(_data.cooling_mode);
    }

    //Dropdown value append
    $('.dropdown-menu li').click(function(event) {
      var $target = $( event.currentTarget );
      $target.closest( '.btn-group' )
         .find( '[data-bind="label"]' ).text( $target.text() )
            .end()
         .children( '.dropdown-toggle' ).dropdown( 'toggle' );

      return false;
    });

    var setHeight = $("#actt").height();
    $("#dispp").height(setHeight+'px');

    $("button[id^='off_']").click(function(e) {
        e.preventDefault();
        var off = this.id.split("_");
        var on = "on_" + off[1];
        if ($(this).hasClass('btn-success')) {
            $(this).removeClass('btn-success').addClass('btn-default');
            $('#' + on).removeClass('btn-default').addClass('btn-success');
        } else {
            $(this).removeClass('btn-default').addClass('btn-success');
            $('#' + on).removeClass('btn-success').addClass('btn-default');
        }
    });

    $("button[id^='on_']").click(function(e) {
        e.preventDefault();
        var on = this.id.split("_");
        var off = "off_" + on[1];
        if ($(this).hasClass('btn-success')) {
            $(this).removeClass('btn-success').addClass('btn-default');
            $('#' + off).removeClass('btn-default').addClass('btn-success');
        } else {
            $(this).removeClass('btn-default').addClass('btn-success');
            $('#' + off).removeClass('btn-success').addClass('btn-default');
        }
    });

    $("#heating").slider({
        value: heating,
        orientation: "horizontal",
        range: "min",
        animate: true,
        min: 0,
        max: 100,
        step: 1,
        slide: function (event, ui) {
            $("#heating_level").html(ui.value);
        }
    });

    $("#outside_damper").slider({
        value: outside_damper,
        orientation: "horizontal",
        range: "min",
        animate: true,
        min: 0,
        max: 100,
        step: 1,
        slide: function (event, ui) {
            $("#outside_damper_val").html(ui.value);
        }
    });

    $("#bypass_damper").slider({
        value: bypass_damper,
        orientation: "horizontal",
        range: "min",
        animate: true,
        min: 0,
        max: 100,
        step: 1,
        slide: function (event, ui) {
            $("#bypass_damper_val").html(ui.value);
        }
    });
    $(".slider").slider("float");

    if (role != 'admin' && uzone != zone) {
         $('#heating').slider("disable");
        $('#outside_damper').slider("disable");
        $('#bypass_damper').slider("disable");
    }

    $('#heatplus').click(function(e){
        e.preventDefault();
        var currentVal = parseInt($("#heat_setpoint").text());
        if (!isNaN(currentVal) && currentVal < 95) {
            $('#heat_setpoint').text(currentVal + 1);
        } else {
            $('#heat_setpoint').text(95);
        }
    });

    $("#heatminus").click(function(e) {
            e.preventDefault();
            var currentVal = parseInt($("#heat_setpoint").text());
            if (!isNaN(currentVal) && currentVal > 35) {
                $('#heat_setpoint').text(currentVal - 1);
            } else {
                $('#heat_setpoint').text(35);
            }
        });

    $('#coolplus').click(function(e){
            e.preventDefault();
            var currentVal = parseInt($("#cool_setpoint").text());
            if (!isNaN(currentVal) && currentVal < 95) {
                $('#cool_setpoint').text(currentVal + 1);
            } else {
                $('#cool_setpoint').text(95);
            }
        });

    $("#coolminus").click(function(e) {
            e.preventDefault();
            var currentVal = parseInt($("#cool_setpoint").text());
            if (!isNaN(currentVal) && currentVal > 35) {
                $('#cool_setpoint').text(currentVal - 1);
            } else {
                $('#cool_setpoint').text(35);
            }
        });


    $("#submit_rtu_data").click(function(e){
        e.preventDefault();
        update_time = new Date();
	    update_time = update_time.toLocaleTimeString();
        var heat_setpoint = $("#heat_setpoint").text();
        var cool_setpoint = $("#cool_setpoint").text();
        var fan_status = 'OFF';
        if ($("#on_fan").hasClass("btn-success")){
            fan_status = 'ON';
        }
        var cooling_status = 'OFF';
        if ($("#on_cool").hasClass("btn-success")){
            cooling_status = 'ON';
        }
        var cooling_mode = $("#coolmode").text();

        if (cooling_mode == 'None') {
            cooling_mode = 'NONE';
        } else if (cooling_mode == 'Stage 1 Cooling') {
            cooling_mode = 'STG1';
        } else if (cooling_mode == 'Stage 2 Cooling') {
            cooling_mode = 'STG2';
        } else if (cooling_mode == 'Stage 3 Cooling') {
            cooling_mode = 'STG3';
        } else if (cooling_mode == 'Stage 4 Cooling') {
            cooling_mode = 'STG4';
        }

        var heating = $("#heating_level").text();
        var outside_damper = $("#outside_damper_val").text();
        var bypass_damper = $("#bypass_damper_val").text();

        var values = {
            "heat_setpoint": parseFloat(heat_setpoint),
            "cool_setpoint": parseFloat(cool_setpoint),
            "fan_status": fan_status,
            "cooling_status": cooling_status,
            "cooling_mode": cooling_mode,
            "heating": parseInt(heating),
            "outside_damper_position": parseInt(outside_damper),
            "bypass_damper_position": parseInt(bypass_damper),
            "device_info": device_info
        };
        _values_on_submit = values;
        var jsonText = JSON.stringify(values);
        console.log(jsonText);
        $.ajax({
              url : '/submit_rtu_data/',
              type: 'POST',
              data: jsonText,
              dataType: 'json',
              success : function(data) {
                console.log("Data submitted");
                /*wifi_3m50_data_updated(wifi3m50_update);
                $('.bottom-right').notify({
                    message: { text: 'Your thermostat settings will be updated shortly' },
                    type: 'blackgloss'
                  }).show(); */
              },
              error: function(data) {
                  //submit_thermostat_data(values);
                  $('.bottom-right').notify({
                        message: { text: 'Something went wrong when submitting RTU data. Please try again.' },
                        type: 'blackgloss',
                      fadeOut: { enabled: true, delay: 5000 }
                    }).show();
              }
		 });

    });

});