define(['jquery', 'jsPlumb', 'mustache'], function($, jsPlumb, Mustache){

    // global object Container
    var TreeApp = {
        person_id : 0,
        people_hierarchy_order : [],
        person_by_id : {},
        relations_by_id : {},
        from_relations : {},
        to_relations : {},

        //Ajax request to get tree data
        load_tree_data : function() {
            $('.loading').show();

            $.ajax({
                context: this,
                url: "/tree/data/",

            }).done(function(data) {
                    this.populate_lookups(data);
                    this.redraw_tree();
                    $('.loading').hide();
            });
        },

        // Populates lookups of people and relations
        populate_lookups : function(data) {
            //People
            var arrayLength = data.people.length;
            for (var i = 0; i < arrayLength; i++) {

                var person = {
                    id : data.people[i][0],
                    name : data.people[i][1],
                    image : this.get_image_url(data.media_url, data.people[i][2]),
                    hierarchy_score: data.people[i][3],
                    relations: []
                };

                this.person_by_id[data.people[i][0]] = person;
                this.people_hierarchy_order.push(person);
            }



            // Relations
            var data_relations = data.relations;
            var data_relations_length = data_relations.length;

            for (var i = 0; i < data_relations_length; i++) {

                var data_relation = data_relations[i];

                var id = data_relation[0];
                var from_id = data_relation[1];
                var to_id = data_relation[2];
                var relation_type = data_relation[3];

                var relation = {
                    id : id,
                    from_person_id : from_id,
                    to_person_id : to_id,
                    relation_type : relation_type
                };

                this.person_by_id[from_id].relations.push(relation);
                this.person_by_id[to_id].relations.push(relation);

                this.relations_by_id[id] = relation;

                if (!(from_id in this.from_relations)) {
                    this.from_relations[from_id] = {};
                }
                this.from_relations[from_id][to_id] = relation;

                if (!(to_id in this.to_relations)) {
                    this.to_relations[to_id] = {};
                }
                this.to_relations[to_id][from_id] = relation;
            }
        },

        redraw_tree : function() {
            var relatives = this.get_related_people();
            html = this.build_tree(relatives);
            this.render_tree(html, relatives);
        },

        render_tree : function (html, relatives) {
            // Clear tree
            jsPlumb.deleteEveryConnection();
            $('#family_tree_container').html('');

            // Draw new ones
            $('#family_tree_container').append(html);
            this.draw_relations(relatives)
        },

        build_tree : function (relatives) {

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
            if (relatives.upper.length > 1) {
                var left = 0;
                var gap = (pixel_width - relatives.upper.length * node_width) / (relatives.upper.length - 1)

                for (var i = 0; i < relatives.upper.length; i++) {
                    var relative = relatives.upper[i];

                    if (relatives.relations_by_member_id[relative.id].length < this.person_by_id[relative.id].relations.length) {
                        html.push(this.draw_relative(relative, left, top, template_more_up));
                    } else {
                        html.push(this.draw_relative(relative, left, top, template));
                    }

                    left = left + node_width + gap
                }
            }

            if (relatives.upper.length == 1) {
                var relative = relatives.upper[0];
                var left = (pixel_width - node_width) / 2;

                if (relatives.relations_by_member_id[relative.id].length < this.person_by_id[relative.id].relations.length) {
                    html.push(this.draw_relative(relative, left, top, template_more_up));
                } else {
                    html.push(this.draw_relative(relative, left, top, template));
                }
            }

            top = height_change;

            // Draw partners
            if (relatives.same_level.length > 0)
            {
                var left = 0;
                var gap = (pixel_width - relatives.same_level.length * node_width) / (relatives.same_level.length - 1)
                var count = 1

                var threshold = (relatives.same_level.length + 1) / 2;

                for (var i = 0; i < relatives.same_level.length; i++) {
                    var relative = relatives.same_level[i];

                    if (relatives.relations_by_member_id[relative.id].length < this.person_by_id[relative.id].relations.length) {
                        if (count <= threshold) {
                            html.push(this.draw_relative(relative, left, top, template_more_left));
                        }
                        else {
                            html.push(this.draw_relative(relative, left, top, template_more_right));
                        }
                    } else {
                        html.push(this.draw_relative(relative, left, top, template));
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
            html.push(this.draw_centred_person(pixel_width, node_width, top));
            top = top + height_change + 60; //Include button height

            // Draw descendants
            if (relatives.lower.length > 1) {
                var left = 0;
                var gap = (pixel_width - relatives.lower.length * node_width) / (relatives.lower.length - 1)

                for (var i = 0; i < relatives.lower.length; i++) {
                    var relative = relatives.lower[i];

                    if (relatives.relations_by_member_id[relative.id].length < this.person_by_id[relative.id].relations.length) {
                        html.push(this.draw_relative(relative, left, top, template_more_down));
                    } else {
                        html.push(this.draw_relative(relative, left, top, template));
                    }

                    left = left + node_width + gap
                }
            }

            if (relatives.lower.length == 1) {
                var left = (pixel_width - node_width) / 2;
                var relative = relatives.lower[0];

                if (relatives.relations_by_member_id[relative.id].length < this.person_by_id[relative.id].relations.length) {
                    html.push(this.draw_relative(relative, left, top, template_more_down));
                } else {
                    html.push(this.draw_relative(relative, left, top, template));
                }
            }

            return html.join('');
        },

        get_related_people: function() {

            var hierarchy = this.person_by_id[person_id].hierarchy_score;

            var related_people = {
                all_members: [],
                upper: [],
                same_level: [],
                lower: [],
                relations_by_id: {},
                members_by_id: {},
                relations_by_member_id : {},
                drawn_relations_by_id: {},

                add_relative : function(relative) {
                    this.all_members.push(relative);
                    this.members_by_id[relative.id] = relative;
                    this.relations_by_member_id[relative.id] = [];
                },
            };

            // Iterate through people
            var people_hierarchy_order_length = this.people_hierarchy_order.length;
            for (var i = 0; i < people_hierarchy_order_length; i++) {
                var relative = this.people_hierarchy_order[i];

                if (relative.id in this.from_relations && person_id in this.from_relations[relative.id]) {
                    this.add_relative(related_people, relative, hierarchy);
                    related_people.add_relative(relative);
                }

                if (relative.id in this.to_relations &&  person_id in this.to_relations[relative.id]) {
                    this.add_relative(related_people, relative, hierarchy);
                    related_people.add_relative(relative);
                }
            }

            // Get all associated relations
            for (var key in this.relations_by_id) {
                var relation = this.relations_by_id[key];

                if (relation.from_person_id in related_people.members_by_id && relation.to_person_id == person_id) {
                    related_people.relations_by_member_id[relation.from_person_id].push(relation);
                    related_people.relations_by_id[relation.id] = relation;
                    related_people.drawn_relations_by_id[relation.id] = relation;
                }

                if (relation.to_person_id in related_people.members_by_id && relation.from_person_id == person_id) {
                    related_people.relations_by_member_id[relation.to_person_id].push(relation);
                    related_people.relations_by_id[relation.id] = relation;
                    related_people.drawn_relations_by_id[relation.id] = relation;
                }

                if (relation.from_person_id in related_people.members_by_id && relation.to_person_id in related_people.members_by_id) {
                    related_people.relations_by_member_id[relation.to_person_id].push(relation);
                    related_people.relations_by_member_id[relation.from_person_id].push(relation);
                    related_people.relations_by_id[relation.id] = relation;

                    // Show partnered relations
                    if (relation.relation_type == 1) {
                        related_people.drawn_relations_by_id[relation.id] = relation;
                    }
                }
            }

            return related_people;
        },

        add_relative : function(related_people, relative, hierarchy) {

            if (relative.hierarchy_score < hierarchy) {
                related_people.upper.push(relative);

            } else if (relative.hierarchy_score > hierarchy) {
                related_people.lower.push(relative);

            } else {
                related_people.same_level.push(relative);

            }
        },


        // Renders the person at the centre of the tree
        draw_centred_person : function(pixel_width, node_width, top) {

            var person = this.person_by_id[person_id];
            var position_left = Math.round((pixel_width - node_width) / 2)

            var template = $('#centre_person').html();
            person.left = position_left;
            person.top = top;
            var output = Mustache.render(template, person);

            return output;
        },

        // Renders a relative to the centred person
        draw_relative : function(relative, left, top, template) {
            relative.left = left;
            relative.top = top;
            var output = Mustache.render(template, relative);

            return output;
        },

        // Returns the url of the profile picture
        get_image_url : function(media_url, image) {

            if (image) {
                return media_url + image;
            }
            else {
                return "/static/img/portrait_80.png";
            }
        },

        draw_relations : function(related_people) {

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

            instance.batch(function () {

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

                for (var key in related_people.drawn_relations_by_id) {
                    var relation = related_people.drawn_relations_by_id[key];

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
            for (var i = 0; i < related_people.all_members.length; i++) {

                var id = related_people.all_members[i].id.toString();

                var that = this;
                jsPlumb.on(document.getElementById(id), "click", function (e, that) {
                    var new_person_id = $('#' + this.id).data('person_id');

                    $old_person = $('#' + person_id.toString());
                    $new_person = $('#' + new_person_id);

            	    person_id = parseInt(new_person_id);

            	    // Animate clicked person into centre
            	    var left = $old_person.offset().left - $new_person.offset().left;
            	    var top = $old_person.offset().top - $new_person.offset().top;

            	    $('#family_tree_container').find('*').not('#' + new_person_id + ',#' + new_person_id + ' *').remove();

            	    var html;
            	    var animation_finished = false;
            	    var build_tree_finished = false;

            	    $new_person.animate({left : "+=" + left.toString(), top : "+=" + top.toString()}, 400, function() {
            	        animation_finished = true;
            	        check_done();
            	    });

                    // Build new tree
        	        var relatives = TreeApp.get_related_people();
                    html = TreeApp.build_tree(relatives);
                    build_tree_finished = true;
            	    check_done();

                    // Only once animation has finished and tree built, do we we display new tree
            	    function check_done () {
            	        if (build_tree_finished && animation_finished) {
            	            TreeApp.render_tree(html, relatives)
            	        }
            	    }
                });
            }
        }

    };



    $(document).ready(function() {

        person_id = parseInt(window.location.pathname.split('/')[2]);
        TreeApp.load_tree_data();
    });

    $(window).resize(function () {
        if (TreeApp.people_hierarchy_order.length > 0) {
            TreeApp.redraw_tree();
        }
    });
});









