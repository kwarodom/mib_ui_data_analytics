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

    $(function ($) {
        /*
         $(".powermeter").each(function(index) {
         //alert(this.id);
         var popts = {
         lines: 12, // The number of lines to draw
         angle: 0.0, // The length of each line
         lineWidth: 0.2, // The line thickness2
         pointer: {
         length: 0.8, // The radius of the inner circle
         strokeWidth: 0.03, // The rotation offset
         color: '#00000' // Fill color
         },
         limitMax: 'true',   // If true, the pointer will not go past the end of the gauge
         colorStart: '#6FADCF',   // Colors
         colorStop: '#8FC0DA',    // just experiment with them
         strokeColor: '#E0E0E0',   // to see which ones work best for you
         generateGradient: true,
         percentColors: [[0.0, "#a9d70b" ], [0.50, "#f9c802"], [1.0, "#ff0000"]],
         animationSpeed: 20,
         fontSize: 15
         };
         var gauge_target = document.getElementById(this.id);
         var gauge = new Gauge(gauge_target);
         var power_id = this.id.split("_");
         text_field = power_id[1]+"-textfield";
         gauge.setTextField(document.getElementById(text_field));
         var power_value_id = power_id[1] + "_chvalue";
         power_value = parseFloat(document.getElementById(power_value_id).innerHTML);
         //alert(power_value);
         $("#"+power_value_id).hide();
         gauge.setOptions(popts);
         gauge.maxValue = 18;
         gauge.set(power_value);

         //var gvalue = {{element.current_status.power}};
         //if (power_value == 0)
         //power_value = power_value + 0.1;
         //power_value = 800;
         //alert(power_value);


         });


         $(".thsens_gauge").each(function(index) {
         var sensor_element = document.getElementById(this.id);
         var element_id = sensor_element.id.split('_');
         element_id = element_id[1];
         //element_id = document.getElementById(this.id);
         divid = element_id + "_divopen";
         var class_name = document.getElementById(divid);
         class_name = class_name.className;
         $("#"+divid).attr("class", "col-md-5 col-xs-12 col-sm-6");
         var thopts = {
         lines: 12, // The number of lines to draw
         angle: 0.20, // The length of each line
         lineWidth: 0.15, // The line thickness
         pointer: {
         length: 0.9, // The radius of the inner circle
         strokeWidth: 0.035, // The rotation offset
         color: '#000000' // Fill color
         },
         limitMax: 'true',   // If true, the pointer will not go past the end of the gauge
         colorStart: '#6F6EA0',   // Colors
         colorStop: '#C0C0DB',    // just experiment with them
         strokeColor: '#EEEEEE',   // to see which ones work best for you
         generateGradient: true,
         animationSpeed: 20,
         fontSize: 15
         };
         var donut_target = document.getElementById(this.id); // your canvas element
         var donut = new Donut(donut_target).setOptions(thopts); // create sexy gauge!
         donut.animationSpeed = 32; // set animation speed (32 is default value)

         var power_id = this.id.split("_");
         text_field = power_id[1]+"-ttextfield";
         donut.setTextField(document.getElementById(text_field));
         var temp_value_id = power_id[1] + "_tvalue";
         temp_value = parseFloat(document.getElementById(temp_value_id).innerHTML);
         $("#"+temp_value_id).hide();
         //mode_value_id = power_id[1]+"_tmode";
         //$("#"+power_id[1]+"_tmode").hide();
         donut.maxValue = 100;
         //var gvalue = {{element.current_status.power}};
         if (temp_value == 0)
         temp_value = temp_value + 0.1;
         //power_value = 800;
         //alert(temp_value);
         donut.set(temp_value);
         donut.setOptions(thopts);
         });

         $(".humidsens_gauge").each(function(index) {
         //alert(this.id);
         var hopts = {
         lines: 1, // The number of lines to draw
         angle: 0.0, // The length of each line
         lineWidth: 0.2, // The line thickness
         pointer: {
         length: 0.7, // The radius of the inner circle
         strokeWidth: 0.035, // The rotation offset
         color: '#00000' // Fill color
         },
         limitMax: 'true',   // If true, the pointer will not go past the end of the gauge
         colorStart: '#6FADCF',   // Colors
         colorStop: '#8FC0DA',    // just experiment with them
         strokeColor: '#E0E0E0',   // to see which ones work best for you
         generateGradient: true,
         percentColors: [[0.0, "#a9d70b" ], [0.50, "#f9c802"], [1.0, "#ff0000"]],
         animationSpeed: 20,
         fontSize: 15
         };
         var hgauge_target = document.getElementById(this.id);
         var humid_gauge = new Gauge(hgauge_target);
         var h_id = this.id.split("_");
         htext_field = h_id[1]+"-htextfield";
         humid_gauge.setTextField(document.getElementById(htext_field));
         var h_value_id = h_id[1] + "_hvalue";
         h_value = parseFloat(document.getElementById(h_value_id).innerHTML);
         $("#"+h_value_id).hide();
         humid_gauge.maxValue = 100;

         //var gvalue = {{element.current_status.power}};
         //if (power_value == 0)
         //power_value = power_value + 0.1;
         //power_value = 800;
         //alert(power_value);
         humid_gauge.set(h_value);
         humid_gauge.setOptions(hopts);

         });

         $(".lightsens_gauge").each(function(index) {
         //alert(this.id);
         var lopts = {
         lines: 1, // The number of lines to draw
         angle: 0.0	, // The length of each line
         lineWidth: 0.2, // The line thickness
         pointer: {
         length: 0.7, // The radius of the inner circle
         strokeWidth: 0.035, // The rotation offset
         color: '#00000' // Fill color
         },
         limitMax: 'true',   // If true, the pointer will not go past the end of the gauge
         colorStart: '#6FADCF',   // Colors
         colorStop: '#8FC0DA',    // just experiment with them
         strokeColor: '#E0E0E0',   // to see which ones work best for you
         generateGradient: true,
         percentColors: [[0.0, "#a9d70b" ], [0.50, "#f9c802"], [1.0, "#ff0000"]],
         animationSpeed: 20,
         fontSize: 15
         };
         var lgauge_target = document.getElementById(this.id);
         var light_gauge = new Gauge(lgauge_target);
         var l_id = this.id.split("_");
         ltext_field = l_id[1]+"-ltextfield";
         light_gauge.setTextField(document.getElementById(ltext_field));
         var light_value_id = l_id[1] + "_lvalue";
         light_value = parseFloat(document.getElementById(light_value_id).innerHTML);
         $("#"+light_value_id).hide();
         light_gauge.maxValue = 1000;

         //var gvalue = {{element.current_status.power}};
         //if (power_value == 0)
         //power_value = power_value + 0.1;
         //power_value = 800;
         //alert(power_value);
         light_gauge.set(light_value);
         light_gauge.setOptions(lopts);

         });*/


        /*$(".hue").each(function(index) {
         //alert(this.id);
         var hue_element = document.getElementById(this.id);
         var element_id = hue_element.id.split('_');
         element_id = element_id[0];
         var no_of_lights = hue_element.innerHTML;
         no_of_lights = no_of_lights.split('');
         if (no_of_lights.length > 4 && no_of_lights.length < 10) {
         divid = element_id + "_divopen";
         var class_name = document.getElementById(divid);
         class_name = class_name.className;
         $("#"+divid).attr("class", "col-md-5 col-xs-12 col-sm-6");
         }
         if (no_of_lights.length > 9) {
         divid = element_id + "_divopen";
         var class_name = document.getElementById(divid);
         //class_name = class_name.className;
         class_name.className = 'col-md-9 col-xs-12 col-sm-6'
         $("#"+divid).attr("class", "col-md-9 col-xs-12 col-sm-6");
         }
         $.each( no_of_lights, function( i, val ) {
         current_innerHTML = $( "#huelights_" + element_id ).html();
         if (val==1)
         $( "#huelights_" + element_id ).html(current_innerHTML + '<img src="/static/images/bulbon.png" width="45" height="70" alt="ON" style="-webkit-filter:brightness(1.5);">');
         if (val==0)
         $( "#huelights_" + element_id ).html(current_innerHTML + '<img src="/static/images/bulbon.png" width="45" height="70" alt="OFF" style="-webkit-filter:grayscale(100%);">');
         });

         $(".hue").hide();

         });*/

        /*$(".vthem").each(function (index) {
            var vth_element = document.getElementById(this.id);
            var element_id = vth_element.id.split('_');
            element_id = element_id[0];
            var no_of_plugs = vth_element.innerHTML;
            no_of_plugs = no_of_plugs.split('');

            $.each(no_of_plugs, function (i, val) {
                current_innerHTML = $("#vth_" + element_id).html();
                if (val == 1)
                    $("#vth_" + element_id).html(current_innerHTML + '<img src="/static/images/plugon.png" width="50" height="70" alt="ON">');
                if (val == 0)
                    $("#vth_" + element_id).html(current_innerHTML + '<img src="/static/images/plugoff.png" width="50" height="70" alt="OFF">');
            });

            $(".vthem").hide();

        });*/

        /*
         $(".thermo_gauge").each(function(index) {

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

        $("#add_new_zone_submit").click(function (evt) {
            evt.preventDefault();
            values = $("#add_new_zone").val();
            if (!nick_re.test(values)) {
                document.getElementById("newzoneerror").innerHTML = "Nickname can only contain letters and numbers. Please try again.";
                document.getElementById(values).value = "";
            } else {
                $.ajax({
                    url: '/add_new_zone/',
                    type: 'POST',
                    data: values,
                    success: function (data) {
                        if (data == "invalid") {
                            document.getElementById("newzoneerror").innerHTML = "Your nickname was not accepted by BEMOSS. Please try again.";
                        } else {
                            $("#accordion2").append('<div class="panel" id="sortable_' + data + '"><div class="panel-heading"><p> <a href="#collapse_' + data + '" data-toggle="collapse" class="accordion-toggle collapsed" id="' + data + '_nick_dp">' + values.charAt(0).toUpperCase() + values.slice(1) + '</a>&nbsp;&nbsp;&nbsp;<i id="' + data + '_znedit" class="icon-pencil" data-backdrop="false" data-target="#' + data + '_znmodal" data-toggle="modal"></i></p> </div><div style="display: none;" aria-hidden="true" aria-labelledby="myModalLabel" role="dialog" tabindex="-1" class="modal fade" id="' + data + '_znmodal"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><button aria-hidden="true" data-dismiss="modal" class="close" type="button">x</button><h4 id="myModalLabel" class="modal-title">Edit Zone Information</h4></div><div class="modal-body"><table class="table table-condensed"><thead><tr><th></th><th></th><th></th></tr></thead><tbody><tr><td>Zone Nickname</td><td id="' + data + '_znick">' + values.charAt(0).toUpperCase() + values.slice(1) + '</td><td><a href="javascript:;" class="znickname_edit" ><i class="icon-small icon-edit" id="' + data + '_znick_edit"></i></a></td><script>$( "#' + data + '_znick_edit" ).click(function() {var newtest = document.getElementById(this.id.replace("_edit",""));newtest.innerHTML = \'<input type="text" id="' + data + '_znickname" placeholder="' + values + '"></input>\'});</script></tr></tbody></table></div><div class="modal-footer"><button data-dismiss="modal" class="btn btn-default" type="button">Close</button><button class="btn btn-primary save_changes_zn" id="#savechanges-' + data + '" type="button">Save changes</button><script>$( ".save_changes_zn" ).click(function(evt) {evt.preventDefault();var save_this = new Common();save_this.Save_Zone_Changes(this.id);});</script></div></div><!-- /.modal-content --></div><!-- /.modal-dialog --></div><div style="height: 0px;" class="panel-collapse collapse" id="collapse_' + data + '"><ul class="panel-body connectedSortable" id="panelbody_' + data + '"><script>$(".panel-body").droppable().sortable({dropOnEmpty: true,connectWith: ".connectedSortable"}).disableSelection();</script></ul></div></div>');
                            $('.bottom-right').notify({
                                message: { text: 'A new zone was added.' },
                                type: 'blackgloss',
                                fadeOut: { enabled: true, delay: 5000 }
                            }).show();

                            $(".panel").mousemove(function (e) {
                                if (e.which == 1) {
                                    if ($(".panel-collapse").hasClass("collapse")) {
                                        $(".panel-collapse").removeClass("collapse");
                                        $(".panel-collapse").addClass("in");
                                        $(".panel-body").show();
                                    }

                                } else {

                                    $(".panel-body").mouseenter(function (e) {
                                        if (e.which == 1) {
                                            $(".panel-body").show();
                                            //$(".panel-body").css("background","rgba(17, 19, 4, 0.35)");
                                        }
                                    });
                                }
                            });

                        }
                    },
                    error: function (data) {
                        $('.bottom-right').notify({
                            message: { text: 'Oh snap! Try submitting again. ' },
                            type: 'blackgloss',
                            fadeOut: { enabled: true, delay: 5000 }
                        }).show();
                    }
                });
            }
        });

        //'<div style="display: none;" aria-hidden="true" aria-labelledby="myModalLabel" role="dialog" tabindex="-1" class="modal fade" id="'+data+'_znmodal"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><button aria-hidden="true" data-dismiss="modal" class="close" type="button">x</button><h4 id="myModalLabel" class="modal-title">Edit Zone Information</h4></div><div class="modal-body"><table class="table table-condensed"><thead><tr><th></th><th></th><th></th></tr></thead><tbody><tr><td>Zone Nickname</td><td id="'+data+'_znick">'+values+'</td><td><a href="javascript:;" class="znickname_edit" ><i class="icon-small icon-edit" id="'+data+'_znick_edit"></i></a></td><script>$( "#'+data+'_znick_edit" ).click(function() {var newtest = document.getElementById(this.id.replace("_edit",""));newtest.innerHTML = \'<input type="text" id="'+data+'_znickname" placeholder="'+values+'"></input>\'});</script></tr></tbody></table></div><div class="modal-footer"><button data-dismiss="modal" class="btn btn-default" type="button">Close</button><button class="btn btn-primary save_changes_zn" id="#savechanges-'+data+'" type="button">Save changes</button></div></div><!-- /.modal-content --></div><!-- /.modal-dialog --></div>'
        /*
         $( ".save_changes" ).click(function(evt) {
         evt.preventDefault();
         values = this.id.split('-');
         device_id = values[1];
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
         "nickname": nickname
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
         type: 'blackgloss'
         }).show();
         }
         },
         error: function(data) {
         $('.bottom-right').notify({
         message: { text: 'Error! Use close button to exit / Click on edit button to change nickname. ' },
         type: 'blackgloss'
         }).show();
         }
         });
         }
         });
         */

        $(".save_changes_zn").click(function (evt) {
            evt.preventDefault();
            values = this.id.split('-');
            zone_id = values[1];
            values = values[1] + "_znickname";
            var value_er = values;
            znickname = $("#" + values).val();
            var error_id = "zonenickname_" + zone_id;
            if (!nick_re.test(znickname)) {
                document.getElementById(error_id).innerHTML = "Nickname error. Please try again.";
                document.getElementById(values).value = "";
            } else {
                values = {
                    "id": zone_id,
                    "nickname": znickname
                };
                var jsonText = JSON.stringify(values);
                $.ajax({
                    url: '/save_zone_nickname_change/',
                    type: 'POST',
                    data: jsonText,
                    contentType: "application/json; charset=utf-8",
                    dataType: 'json',
                    success: function (data) {
                        if (data == "invalid") {
                            document.getElementById(error_id).innerHTML = "Nickname error. Please try again.";
                            document.getElementById(value_er).value = "";
                        } else {
                            //$('#zoned_device_listing').load(' #zoned_device_listing'/*, function(){$(this).children().unwrap()}*/);
                            //$('#zoned_device_listing').html(data);
                            req_value_modal = data.zone_id + "_znick";
                            req_val_stats = data.zone_id + "_nick_dp";
                            modal_zone_nickname = data.zone_id + "_ztdnick";
                            var newtest = document.getElementById(req_value_modal);
                            document.getElementById(req_val_stats).innerHTML = znickname.charAt(0).toUpperCase() + znickname.slice(1);
                            if (document.getElementById(modal_zone_nickname) != null)
                                document.getElementById(modal_zone_nickname).innerHTML = znickname.charAt(0).toUpperCase() + znickname.slice(1);
                            newtest.innerHTML = znickname.charAt(0).toUpperCase() + znickname.slice(1);
                            $('.bottom-right').notify({
                                message: { text: 'Heads up! The zone nickname change was successful.' },
                                type: 'blackgloss',
                                fadeOut: { enabled: true, delay: 5000 }
                            }).show();
                        }
                    },
                    error: function (data) {
                        $('.bottom-right').notify({
                            message: { text: 'Oh snap! Try submitting again. ' },
                            type: 'blackgloss',
                            fadeOut: { enabled: true, delay: 5000 }
                        }).show();
                    }
                });
            }
        });
        /*
         $( ".identify" ).click(function(evt) {
         evt.preventDefault();
         var identifier = (this).id;
         identify_id = identifier.split("-");
         identify_id = identify_id[1];
         //alert(identify_id);
         values = {
         "id": identify_id
         };
         var jsonText = JSON.stringify(values);
         $.ajax({
         url : '/identify_device/',
         type: 'POST',
         data: jsonText,
         contentType: "application/json; charset=utf-8",
         dataType: 'json',
         success : function(data) {
         //alert(data);

         if (data.indexOf("success")>-1) {
         $('#'+identify_id+"-spin").addClass('fa fa-spinner fa-spin').removeClass('icon-search');
         //$('#'+identify_id+"-spin").removeClass('icon-search');
         $("#"+identifier).removeClass('btn-warning').addClass('btn-success disabled');
         //$("#"+identifier).addClass('btn-success');

         identify_status(identify_id, identifier);
         $('.bottom-right').notify({
         message: { text: 'Communicating with the device for identification...' },
         type: 'blackgloss'
         }).show();
         //clearInterval(setTimeOut_identifier);
         }
         },
         error: function(data) {
         $('.bottom-right').notify({
         message: { text: 'Oh snap! Try again. ' },
         type: 'blackgloss'
         }).show();
         }
         });
         });


         function identify_status(identify_id, identifier){
         var setTimeOut_identifier = setTimeout(function()
         {
         $.ajax({
         url : '/identify_status/',
         type: 'POST',
         data : identify_id,
         //dataType : 'text',
         success : function(data) {
         update_status = data.status;
         console.log(update_status);
         if (update_status.indexOf("success") > -1){
         $('#'+identify_id+"-spin").removeClass('fa fa-spinner fa-spin').addClass('icon-search');
         $("#"+identifier).removeClass('btn-success disabled').addClass('btn-warning');
         stopTimer('setTimeOut_identifier');
         }
         else {
         $('#'+identify_id+"-spin").removeClass('fa fa-spinner fa-spin').addClass('icon-search');
         $("#"+identifier).removeClass('btn-success disabled').addClass('btn-warning');
         stopTimer('setTimeOut_identifier');
         $('.bottom-right').notify({
         message: { text: data.status},
         type: 'blackgloss'
         }).show();
         }
         },
         error: function(data) {
         identify_status(identify_id,identifier);
         //$('#'+identify_id+"-spin").removeClass('fa fa-spinner fa-spin').addClass('icon-search');
         //$("#"+identifier).removeClass('btn-success').addClass('btn-warning');

         }
         });
         },3000);
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
*/

    });
});