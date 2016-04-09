require(["jsPlumb"], function (jsPlumb) {

    jsPlumb.ready(function() {

    	// setup some defaults for jsPlumb.
    	var instance = jsPlumb.getInstance({
    		Endpoint : ["Dot", {radius:2}],
    		HoverPaintStyle : {strokeStyle:"#1e8151", lineWidth:2 },
    		Container:"family_tree_container"
    	});


         window.jsp = instance;

    	var windows = jsPlumb.getSelector(".family_tree_container .boxed_chained");


        instance.batch(function () {

            instance.makeSource(windows, {
                filter: ".ep",
                anchor: "AutoDefault",
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
                anchor: "AutoDefault",
                allowLoopback: true
            });


            for (var i = 0; i < OKKINDRED_HOW_RELATED.relations.length; i++) {

                var relation = OKKINDRED_HOW_RELATED.relations[i];

                instance.connect({
                    source:"person" + relation.from_person_id,
                    target:"person" + relation.to_person_id,
                    overlays:[
                        [ "Arrow", { location:1, direction: 1, id:"arrow" + relation.id } ],
                        [ "Label", { label:relation.desc, id:"label" + relation.id , cssClass:"aLabel"} ]
                        ],
                });
            }
        });
    });
});