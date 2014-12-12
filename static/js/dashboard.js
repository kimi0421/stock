/**
 * Created by kimi on 12/10/14.
 */

// Toggle side bar
$(document)
    .ready(function () {

        $('.ui.sidebar')
            .sidebar('attach events', '.launch.button');

        $('.ui.modal')
            .modal('attach events', '#card_modal_trigger', 'show');

    })
;