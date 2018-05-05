define(function(require){

    var $ = require('jquery');
    var jsPlumb = require('jsPlumb');
    var Mustache = require('mustache');
    var TreeData =  require('./tree_data.js');
    var DrawInfo = require('./tree_draw_info.js');

    // Run on page load
    $(document).ready(function() {

        // Grab person ID from url
        if (TreeData.person_id == null) {
            TreeData.person_id = parseInt(window.location.pathname.split('/')[2]);
        }

        $('.loading').show();

        //Ajax request to get tree data
        $.ajax({
                url: "/tree/data/",

        }).done(function(data) {
            TreeData.populate_lookups(data);
            draw_tree();
            $('.loading').hide();
        });
    });

    $(window).resize(function () {
        draw_tree();
    });


    // Draws the tree
    function draw_tree() {
        DrawInfo.build_draw_info(TreeData);
        var draw_info = DrawInfo;
        html = layout_people_html(draw_info);
        render_tree(html, draw_info);
    }


    // Creates the html
    function layout_people_html (draw_info) {
        var pixel_width = $('#container').width() - 16;
        var node_width;
        var height_change;

        if ($('#container').width() < 768) {
            node_width = 90;
            height_change = 140;
        }
        else {
            node_width = 120;
            height_change = 190;
        }

        var template = $('#relative_person').html();
        var template_more_up = $('#relative_person_more_up').html();
        var template_more_down = $('#relative_person_more_down').html();
        var template_more_left = $('#relative_person_more_left').html();
        var template_more_right = $('#relative_person_more_right').html();

        var html = [];
        var top = 0

        // Draw ancestors
        var num_ancestors = Object.keys(draw_info.upper).length;
        if (num_ancestors > 1) {
            var left = 0;
            var gap = (pixel_width - num_ancestors * node_width) / (num_ancestors - 1)

            for (var key in draw_info.upper) {
                var relative = draw_info.upper[key];

                if (relative.id in draw_info.undrawn_relations_by_person_id) {
                    html.push(draw_relative(relative, left, top, template_more_up));
                } else {
                    html.push(draw_relative(relative, left, top, template));
                }
                left = left + node_width + gap
            }
        }

        if (num_ancestors == 1) {
            var relative = draw_info.upper[Object.keys(draw_info.upper)[0]];
            var left = (pixel_width - node_width) / 2;

            if (relative.id in draw_info.undrawn_relations_by_person_id) {
                html.push(draw_relative(relative, left, top, template_more_up));
            } else {
                html.push(draw_relative(relative, left, top, template));
            }
        }

        top = height_change;

        // Draw partners
        var num_partners = Object.keys(draw_info.same_level).length;
        if (num_partners > 0) {
            var left = 0;
            var gap = (pixel_width - num_partners * node_width) / (num_partners - 1)
            var count = 1

            var threshold = (num_partners + 1) / 2;

            for (var key in draw_info.same_level) {
                var relative = draw_info.same_level[key];

                if (relative.id in draw_info.undrawn_relations_by_person_id) {
                    if (count <= threshold) {
                        html.push(draw_relative(relative, left, top, template_more_left));
                    }
                    else {
                        html.push(draw_relative(relative, left, top, template_more_right));
                    }
                } else {
                    html.push(draw_relative(relative, left, top, template));
                }

                count++;

                if (count <= threshold) {
                    left = left + gap;
                } else {
                    left = left + node_width + gap;
                }
            }
        }

        // add centred person
        html.push(draw_centred_person(pixel_width, node_width, top, draw_info.person));
        top = top + height_change + 60; //Include button height

        // Draw descendants
        var num_descendants = Object.keys(draw_info.lower).length;
        if (num_descendants > 1) {
            var left = 0;
            var gap = (pixel_width - num_descendants * node_width) / (num_descendants - 1)

            for (var key in draw_info.lower) {
                var relative = draw_info.lower[key];

                if (relative.id in draw_info.undrawn_relations_by_person_id) {
                    html.push(draw_relative(relative, left, top, template_more_down));
                } else {
                    html.push(draw_relative(relative, left, top, template));
                }

                left = left + node_width + gap
            }
        }

        if (num_descendants == 1) {
            var left = (pixel_width - node_width) / 2;
             var relative = draw_info.lower[Object.keys(draw_info.lower)[0]];

            if (relative.id in draw_info.undrawn_relations_by_person_id) {
                html.push(draw_relative(relative, left, top, template_more_down));
            } else {
                html.push(draw_relative(relative, left, top, template));
            }
        }

        return html.join('');
    }


    // Renders a relative to the centred person
    function draw_relative(relative, left, top, template) {
        relative.left = left;
        relative.top = top;
        var output = Mustache.render(template, relative);

        return output;
    }


    // Renders the person at the centre of the tree
    function draw_centred_person(pixel_width, node_width, top, person) {

        var position_left = Math.round((pixel_width - node_width) / 2)

        var template = $('#centre_person').html();
        person.left = position_left;
        person.top = top;
        var output = Mustache.render(template, person);

        return output;
    }

    function render_tree(html, draw_info) {
        // Clear tree
        jsPlumb.deleteEveryConnection();
        $('#family_tree_container').html('');

        // Draw new ones
        $('#family_tree_container').append(html);
        draw_relations(draw_info)
    }

    function draw_relations (draw_info) {

            // Gets translations of relation types
            var raised = $('#localization').data('raised');
            var partnered = $('#localization').data('partnered');

        	// setup some defaults for jsPlumb.
        	var instance = jsPlumb.getInstance({
        		Endpoint : ["Dot", {radius:2}],
        		Connector:"StateMachine",
        		HoverPaintStyle : {strokeStyle:"#1e8151", strokeWidth:2 },
        		Container:"family_tree_container"
        	});

            window.jsp = instance;

        	var windows = jsPlumb.getSelector(".family_tree_container .w");

            // Batch draw all relations for speed
            instance.batch(function () {

                // Initialise the connector styles
                instance.makeSource(windows, {
                    filter: ".ep",
                    connector: [ "StateMachine", { curviness: 20 } ],
                    connectorStyle: { stroke: "#5c96bc", strokeWidth: 2, outlineColor: "transparent", outlineWidth: 4 },
                    anchors: "AutoDefault",
                    maxConnections: 15,
                    onMaxConnections: function (info, e) {
                        alert("Maximum connections (" + info.maxConnections + ") reached");
                    }
                });

                // initialise all '.w' elements as connection targets.
                instance.makeTarget(windows, {
                    dropOptions: { hoverClass: "dragHover" },
                    anchors: "AutoDefault",
                    allowLoopback: true
                });

                // Add each relation as a connection
                for (var key in draw_info.relations_by_id) {
                    var relation = draw_info.relations_by_id[key];

                    var arrow_id = "arrow" + relation.id.toString();
                    var label_id = "label" + relation.id.toString();

                    // Partnered relation
                    if (relation.relation_type == 1) {

                        var inverse_arrow_id = "inverse_arrow" + relation.id.toString();

                        instance.connect({
                            source: relation.from_person_id.toString(),
                            target: relation.to_person_id.toString(),
                            overlays:[
                                    [ "Arrow", { location:1, direction:1, id:arrow_id } ],
                                    [ "Arrow", { location:0, direction: -1, id:inverse_arrow_id } ],
                                    [ "Label", { label:partnered, id:label_id, cssClass:"aLabel" } ]
                                ]
                        });

                    // Raised relation
                    } else {
                        instance.connect({
                            source: relation.from_person_id.toString(),
                            target: relation.to_person_id.toString(),
                            overlays:[
                                    [ "Arrow", { location:1, direction:1, id:arrow_id } ],
                                    [ "Label", { label:raised, id:label_id, cssClass:"aLabel"} ]
                                ]
                        });
                    }
                }
            });

            // Add click handlers
            for (var key in draw_info.all_drawn_relatives()) {

                var id = draw_info.all_drawn_relatives()[key].id.toString();

                var that = this;
                jsPlumb.on(document.getElementById(id), "click", function (e, that) {
                    var new_person_id = $('#' + this.id).data('person_id');

                    $old_person = $('#' + TreeData.person_id.toString());
                    $new_person = $('#' + new_person_id);

                    // The person_id becomes the new person we have just clicked on
            	    var person_id = parseInt(new_person_id);

            	    // Animate clicked person into centre
            	    var left = $old_person.offset().left - $new_person.offset().left;
            	    var top = $old_person.offset().top - $new_person.offset().top;

            	    $('#family_tree_container').find('*').not('#' + new_person_id + ',#' + new_person_id + ' *').remove();

            	    var html;
            	    var animation_finished = false;
            	    var build_tree_finished = false;

                    var new_draw_info = DrawInfo;

            	    $new_person.animate({left : "+=" + left.toString(), top : "+=" + top.toString()}, 400, function() {
            	        animation_finished = true;
            	        check_done();
            	    });

                    // Build new tree
                    TreeData.person_id = person_id;
                    new_draw_info.build_draw_info(TreeData);
                    html = layout_people_html(new_draw_info);
                    build_tree_finished = true;
            	    check_done();

                    // Only once animation has finished and tree built, do we we display new tree
            	    function check_done () {
            	        if (build_tree_finished && animation_finished) {
            	            render_tree(html, new_draw_info)
            	        }
            	    }
                });
            }
        }
});

