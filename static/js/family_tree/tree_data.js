// Helper for drawing the tree

define(['jquery'], function($){

    tree_data = {
        person_id : null,
        people_by_id : {},
        relations_by_id : {},
        relations_by_from_person_id : {},
        relations_by_to_person_id : {},

        populate_lookups: function (data) {

            // Returns the url of the profile picture
            function get_image_url(media_url, image) {
                if (image) {
                    return media_url + image;
                }
                else {
                    return "/static/img/portrait_80.png";
                }
            }

            //People
            for (var i = 0; i < data.people.length; i++) {
                var row = data.people[i];

                var person = {
                    id : row[0],
                    name : row[1],
                    image : get_image_url(data.media_url, row[2]),
                };

                this.people_by_id[person.id] = person;
            }

            // Relation lookups
            for (var i = 0; i < data.relations.length; i++) {
                var row = data.relations[i];

                var relation = {
                    id : row[0],
                    from_person_id : row[1],
                    to_person_id : row[2],
                    relation_type : row[3],
                };

                // Add relation to relation by id lookup
                this.relations_by_id[relation.id] = relation;

                // Add relation to relation by from person id lookup
                if (!(relation.from_person_id in this.relations_by_from_person_id)) {
                        this.relations_by_from_person_id[relation.from_person_id] = [];
                }
                this.relations_by_from_person_id[relation.from_person_id].push(relation);

                if (!(relation.to_person_id in this.relations_by_to_person_id)) {
                    this.relations_by_to_person_id[relation.to_person_id] = [];
                }
                this.relations_by_to_person_id[relation.to_person_id].push(relation);
            }
        },



         // Gets all the information required to draw screen
        get_draw_info: function() {

            var draw_info = {
                person : this.people_by_id[this.person_id],
                undrawn_relations_by_person_id : {},
                upper : {},
                same_level : {},
                lower : {},
                relations_by_id: {},

                // Returns lookup of all drawn relatives
                _all_drawn_relatives : null,
                all_drawn_relatives : function() {
                    if (this._all_drawn_relatives == null) {
                        this._all_drawn_relatives = $.extend({}, this.upper, this.same_level, this.lower);
                    }
                    return this._all_drawn_relatives;
                }
            };

            // add in relatives from the relations from lookup
            if (this.person_id in this.relations_by_from_person_id) {
                var to_relations = this.relations_by_from_person_id[this.person_id];

                for (var i = 0; i < to_relations.length; i++) {
                    var relation = to_relations[i];
                    var relative = this.people_by_id[relation.to_person_id]

                    draw_info.relations_by_id[relation.id] = relation;

                    // if partnered
                    if (relation.relation_type == 1) {
                        draw_info.same_level[relative.id] = relative;
                    } else {
                        //raised
                        draw_info.lower[relative.id] = relative;
                    }
                }
            }

            // add in relatives for the relations to lookup
            if (this.person_id in this.relations_by_to_person_id) {
                var from_relations = this.relations_by_to_person_id[this.person_id];

                for (var i = 0; i < from_relations.length; i++) {
                    var relation = from_relations[i];
                    var relative = this.people_by_id[relation.from_person_id]

                    draw_info.relations_by_id[relation.id] = relation;

                    // if partnered
                    if (relation.relation_type == 1) {
                        draw_info.same_level[relative.id] = relative;
                    } else {
                        //raised
                        draw_info.upper[relative.id] = relative;
                    }
                }
            }

            // Add in partnered relations of upper level
            for (var upper_person_id in draw_info.upper) {

                if (upper_person_id in this.relations_by_to_person_id) {
                    var to_relations = this.relations_by_to_person_id[upper_person_id];

                    for (var j = 0; j < to_relations.length; j++) {
                        var relation = to_relations[j];

                        if (relation.relation_type == 1 && relation.from_person_id in draw_info.upper) {
                            draw_info.relations_by_id[relation.id] = relation;
                        }
                    }
                }
            }

            // Mark if any have any undrawn relations no already included
             for (var relation_id in this.relations_by_id) {
                 var relation = this.relations_by_id[relation_id];

                if (!(relation.id in draw_info.relations_by_id)) {

                    if(relation.from_person_id in draw_info.all_drawn_relatives()) {
                        draw_info.undrawn_relations_by_person_id[relation.from_person_id] = true;
                    }

                    if(relation.to_person_id in draw_info.all_drawn_relatives()) {
                        draw_info.undrawn_relations_by_person_id[relation.to_person_id] = true;
                    }
                }
             }

            return draw_info;
        },
    }

    return tree_data;

});