var person_id;
var people_hierarchy_order = [];
var person_by_id = {};
var relations_by_id = {};
var from_relations = {};
var to_relations = {};

$(document).ready(function() {

    person_id = parseInt(window.location.pathname.split('/')[2]);
    load_tree_data();


});

$(window).resize(function () {
    if (people_hierarchy_order.length > 0) {
        redraw_tree();
    }
});



//Ajax request to get tree data
function load_tree_data() {
    $.ajax({
        url: "/tree/data",
        success: function(data) {
            populate_lookups(data);
            redraw_tree();
        }

    });
}

// Populates lookups of people and relations
function populate_lookups(data) {

    //People
    var arrayLength = data.people.length;
    for (var i = 0; i < arrayLength; i++) {

        var person = {
            id : data.people[i][0],
            name : data.people[i][1],
            image : get_image_url(data.people[i][2]),
            hierarchy_score: data.people[i][3],
            relations: [],
        };

        person_by_id[data.people[i][0]] = person;
        people_hierarchy_order.push(person);
    }

    // Relations
    for (var i = 0; i < data.relations.length; i++) {

        var id = data.relations[i][0];
        var from_id = data.relations[i][1];
        var to_id = data.relations[i][2];
        var relation_type = data.relations[i][3];

        var relation = {
            id : id,
            from_person_id : from_id,
            to_person_id : to_id,
            relation_type : relation_type,
        };

        person_by_id[from_id].relations.push(relation);
        person_by_id[to_id].relations.push(relation);

        relations_by_id[id] = relation;

        if (!(from_id in from_relations)) {
            from_relations[from_id] = {};
        }
        from_relations[from_id][to_id] = relation;

        if (!(to_id in to_relations)) {
            to_relations[to_id] = {};
        }
        to_relations[to_id][from_id] = relation;
    }
}

function redraw_tree() {
    var relatives = get_related_people();
    html = build_tree(relatives);
    render_tree(html, relatives);
}

function render_tree(html, relatives) {
    // Clear tree
    jsPlumb.detachEveryConnection();
    $('#family_tree_container').html('');

    // Draw new ones
    $('#family_tree_container').append(html);
    draw_relations(relatives)
}

function build_tree(relatives) {

    var pixel_width = $('#container').width() - 16;
    var node_width;
    var height_change;

    if ($('#container').width() < 768) {
        node_width = 90;
        height_change = 150;
    }
    else {
        node_width = 120;
        height_change = 200;
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

            if (relatives.relations_by_member_id[relative.id].length < person_by_id[relative.id].relations.length) {
                html.push(draw_relative(relative, left, top, template_more_up));
            } else {
                html.push(draw_relative(relative, left, top, template));
            }

            left = left + node_width + gap
        }

        top = height_change;
    }

    if (relatives.upper.length == 1) {
        var relative = relatives.upper[0];
        var left = (pixel_width - node_width) / 2;

        if (relatives.relations_by_member_id[relative.id].length < person_by_id[relative.id].relations.length) {
            html.push(draw_relative(relative, left, top, template_more_up));
        } else {
            html.push(draw_relative(relative, left, top, template));
        }

        top = height_change;
    }

    // Draw partners
    if (relatives.same_level.length > 0)
    {
        var left = 0;
        var gap = (pixel_width - relatives.same_level.length * node_width) / (relatives.same_level.length - 1)
        var count = 1

        var threshold = (relatives.same_level.length + 1) / 2;

        for (var i = 0; i < relatives.same_level.length; i++) {
            var relative = relatives.same_level[i];

            if (relatives.relations_by_member_id[relative.id].length < person_by_id[relative.id].relations.length) {
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
    html.push(draw_centred_person(pixel_width, node_width, top));
    top = top + height_change + 70; //Include button height

    // Draw descendants
    if (relatives.lower.length > 1) {
        var left = 0;
        var gap = (pixel_width - relatives.lower.length * node_width) / (relatives.lower.length - 1)

        for (var i = 0; i < relatives.lower.length; i++) {
            var relative = relatives.lower[i];

            if (relatives.relations_by_member_id[relative.id].length < person_by_id[relative.id].relations.length) {
                html.push(draw_relative(relative, left, top, template_more_down));
            } else {
                html.push(draw_relative(relative, left, top, template));
            }

            left = left + node_width + gap
        }
    }

    if (relatives.lower.length == 1) {
        var left = (pixel_width - node_width) / 2;
        var relative = relatives.lower[0];

        if (relatives.relations_by_member_id[relative.id].length < person_by_id[relative.id].relations.length) {
            html.push(draw_relative(relative, left, top, template_more_down));
        } else {
            html.push(draw_relative(relative, left, top, template));
        }
    }

    return html.join('');
}



function get_related_people() {

    var hierarchy = person_by_id[person_id].hierarchy_score;

    var related_people = {
        all_members: [],
        upper: [],
        same_level: [],
        lower: [],
        relations_by_id: {},
        members_by_id: {},
        relations_by_member_id : {},
        drawn_relations_by_id: {},
    };

    // Iterate through people
    for (var i = 0; i < people_hierarchy_order.length; i++) {
        var relative = people_hierarchy_order[i];

        if (relative.id in from_relations && person_id in from_relations[relative.id]) {
            add_relative(related_people, relative, hierarchy);
            related_people.all_members.push(relative);
            related_people.members_by_id[relative.id] = relative;
            related_people.relations_by_member_id[relative.id] = [];
        }

        if (relative.id in to_relations &&  person_id in to_relations[relative.id]) {
            add_relative(related_people, relative, hierarchy);
            related_people.all_members.push(relative);
            related_people.members_by_id[relative.id] = relative;
            related_people.relations_by_member_id[relative.id] = [];
        }
    }

    // Get all associated relations
    for (var key in relations_by_id) {
        var relation = relations_by_id[key];

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
}

function add_relative(related_people, relative, hierarchy) {

    if (relative.hierarchy_score < hierarchy) {
        related_people.upper.push(relative);

    } else if (relative.hierarchy_score > hierarchy) {
        related_people.lower.push(relative);

    } else {
        related_people.same_level.push(relative);

    }
}


// Renders the person at the centre of the tree
function draw_centred_person(pixel_width, node_width, top) {

    var person = person_by_id[person_id];
    var position_left = Math.round((pixel_width - node_width) / 2)

    var template = $('#centre_person').html();
    person.left = position_left;
    person.top = top;
    var output = Mustache.render(template, person);

    return output;
}

// Renders a relative to the centred person
function draw_relative(relative, left, top, template) {
    relative.left = left;
    relative.top = top;
    var output = Mustache.render(template, relative);

    return output;
}

// Returns the url of the profile picture
function get_image_url(image) {

    if (image) {
        return "/media/" + image;
    }
    else {
        return "/static/img/portrait_80.png";
    }
}

function draw_relations(related_people) {

    // Gets translations of relation types
    var raised = $('#localization').data('raised');
    var partnered = $('#localization').data('partnered');

	// setup some defaults for jsPlumb.
	var instance = jsPlumb.getInstance({
		Endpoint : ["Dot", {radius:2}],
		HoverPaintStyle : {strokeStyle:"#1e8151", lineWidth:2 },
		Container:"family_tree_container"
	});

    window.jsp = instance;

	var windows = jsPlumb.getSelector(".family_tree_container .w");

    instance.batch(function () {

        instance.makeSource(windows, {
            filter: ".ep",
            anchor: "Continuous",
            connector: [ "StateMachine", { curviness: 20 } ],
            connectorStyle: { strokeStyle: "#5c96bc", lineWidth: 2, outlineColor: "transparent", outlineWidth: 4 },
            maxConnections: 5,
            onMaxConnections: function (info, e) {
                alert("Maximum connections (" + info.maxConnections + ") reached");
            }
        });

        // initialise all '.w' elements as connection targets.
        instance.makeTarget(windows, {
            dropOptions: { hoverClass: "dragHover" },
            anchor: "Continuous",
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
                            [ "Label", { label:partnered, id:label_id, cssClass:"aLabel" } ],
                        ]
                });

            // Raised relation
            } else {
                instance.connect({
                    source: relation.from_person_id.toString(),
                    target: relation.to_person_id.toString(),
                    overlays:[
                            [ "Arrow", { location:1, direction:1, id:arrow_id } ],
                            [ "Label", { label:raised, id:label_id, cssClass:"aLabel"} ],
                        ]
                });
            }
        }

        jsPlumb.fire("jsPlumbDemoLoaded", instance);
    });

    // Add click handlers
    for (var i = 0; i < related_people.all_members.length; i++) {

        var id = related_people.all_members[i].id.toString();

        jsPlumb.on(document.getElementById(id), "click", function (e) {
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
	        var relatives = get_related_people();
            html = build_tree(relatives);
            build_tree_finished = true;
    	    check_done();

            // Only once animation has finished and tree built, do we we display new tree
    	    function check_done () {
    	        if (build_tree_finished && animation_finished) {
    	            render_tree(html, relatives)
    	        }
    	    }
        });
    }
}
