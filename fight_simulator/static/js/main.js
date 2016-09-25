$(document).ready(function(){

        $("body").on('change','.dynamic-select',function(e){
            var url_params = '?' + $(this).attr('name') + '=' + $(this).val() + '&sid=' + $(this).attr('id');
            $.getJSON('ajax' + url_params,function(data) {

                $("#"+ data.element_id).replaceWith(data.data);




    });

        });
    });
