define(['jquery'], function($){

    // Represents the data required to render a small tree view
    var tree_draw_info = {
        person : null,
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
        },

        // Builds draw info
        build_draw_info: function(tree_data) {
            this.person = tree_data.people_by_id[tree_data.person_id];

            this.undrawn_relations_by_person_id = {};
            this.upper = {};
            this.same_level = {};
            this.lower = {};
            this.relations_by_id = {};
            this._all_drawn_relatives = null;

            this.add_relatives_from_from_relations(tree_data);
            this.add_relatives_from_to_relations(tree_data);
            this.add_partner_relations_of_parents(tree_data);
            this.mark_undrawn_relations(tree_data);
        },

        // add in relatives from the relations from lookup
        add_relatives_from_from_relations: function(tree_data) {


            if (this.person.id in tree_data.relations_by_from_person_id) {
                var to_relations = tree_data.relations_by_from_person_id[this.person.id];

                for (var i = 0; i < to_relations.length; i++) {
                    var relation = to_relations[i];
                    var relative = tree_data.people_by_id[relation.to_person_id]

                    this.relations_by_id[relation.id] = relation;

                    // if partnered
                    if (relation.relation_type == 1) {
                        this.same_level[relative.id] = relative;
                    } else {
                        //raised
                        this.lower[relative.id] = relative;
                    }
                }
            }
        },

        // add in relatives for the relations to lookup
        add_relatives_from_to_relations: function(tree_data) {

            if (this.person.id in tree_data.relations_by_to_person_id) {
                var from_relations = tree_data.relations_by_to_person_id[this.person.id];

                for (var i = 0; i < from_relations.length; i++) {
                    var relation = from_relations[i];
                    var relative = tree_data.people_by_id[relation.from_person_id]

                    this.relations_by_id[relation.id] = relation;

                    // if partnered
                    if (relation.relation_type == 1) {
                        this.same_level[relative.id] = relative;
                    } else {
                        //raised
                        this.upper[relative.id] = relative;
                    }
                }
            }
        },

        // Add in partnered relations of upper level
        add_partner_relations_of_parents: function(tree_data) {

            for (var upper_person_id in this.upper) {

                if (upper_person_id in tree_data.relations_by_to_person_id) {
                    var to_relations = tree_data.relations_by_to_person_id[upper_person_id];

                    for (var j = 0; j < to_relations.length; j++) {
                        var relation = to_relations[j];

                        if (relation.relation_type == 1 && relation.from_person_id in this.upper) {
                            this.relations_by_id[relation.id] = relation;
                        }
                    }
                }
            }
        },

        // Mark if any have any undrawn relations not already included
        // Allows us to show an arrow for further exploration
        mark_undrawn_relations: function(tree_data) {

             for (var relation_id in tree_data.relations_by_id) {

                if (!(relation_id in this.relations_by_id)) {
                    var relation = tree_data.relations_by_id[relation_id];

                    if(relation.from_person_id in this.all_drawn_relatives()) {
                        this.undrawn_relations_by_person_id[relation.from_person_id] = true;
                    }

                    if(relation.to_person_id in this.all_drawn_relatives()) {
                        this.undrawn_relations_by_person_id[relation.to_person_id] = true;
                    }
                }
            }

        }
    };

    return tree_draw_info;
});