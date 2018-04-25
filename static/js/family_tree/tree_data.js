// Helper for drawing the tree

define(['jquery'], function($){

    var tree_data = {
        person_id : null,
        people_by_id : {},
        relations_by_id : {},
        relations_by_from_person_id : {},
        relations_by_to_person_id : {},

        // Returns the url of the profile picture
        get_image_url : function(media_url, image) {
            if (image) {
                return media_url + image;
            }
            else {
                return "/static/img/portrait_80.png";
            }
        },

        // Gets people as a dictionary by id
        populate_people_by_id: function(data) {
            var people_by_id = {};

            for (var i = 0; i < data.people.length; i++) {
                var row = data.people[i];

                var person = {
                    id : row[0],
                    name : row[1],
                    image : this.get_image_url(data.media_url, row[2]),
                };

                this.people_by_id[person.id] = person;
            }
        },

        // Relation lookups
        populate_relation_lookups: function(data) {

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

        populate_lookups: function (data) {
            this.populate_people_by_id(data);
            this.populate_relation_lookups(data);
        },

    };

    return tree_data;

});