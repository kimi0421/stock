/**
 * Created by kimi on 12/10/14.
 */

// Toggle side bar
$(document)
    .ready(function () {

        $('.ui.sidebar')
            .sidebar('attach events', '.launch.button');

        $('.ui .modal').each(function() {
            var modal_id = this.id;
            var button_id = '#button_' + modal_id.split('_')[1];
            $('#' + modal_id)
                .modal('attach events', button_id, 'show');
        });

//        $('#modal0')
//            .modal('attach events', '#button0', 'show');
//
//        $('#modal1')
//            .modal('attach events', '#button1', 'show');
//
//        $('#modal2')
//            .modal('attach events', '#button2', 'show');
//
//        $('#modal3')
//            .modal('attach events', '#button3', 'show');
//
//        $('#modal4')
//            .modal('attach events', '#button4', 'show');
//
//        $('#modal5')
//            .modal('attach events', '#button5', 'show');

        $('.ui.ribbon.label')
            .popup({
                hoverable: true,
                position: 'bottom right',
                delay: {
                    show: 100,
                    hide: 100
                }
            })
        ;

    })
;