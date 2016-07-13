$( window ).scroll(function() {
    var top = $(this).scrollTop();
            var shrinkOn = 300;
        if (top > shrinkOn) {
            $("#mainNav").switchClass( "expandedNav", "suspendedNav", 300, "easeInOutQuad" );
            $("#slogan").hide();
        } else {
            $("#mainNav").switchClass( "suspendedNav", "expandedNav", 300, "easeInOutQuad" );
            $("#slogan").show();
        }
    });
