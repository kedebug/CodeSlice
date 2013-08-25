$(document).ready(function() {
    document.session = $('#session').val();
    setTimeout(request_inventory, 100);
    
    $('#add-button').click(function(event) {
        jQuery.ajax({
            url: '//localhost:8000/cart',
            type: 'POST'
            data: {
                session: document.session,
                action: 'add'
            },
            dataType: 'json',
            beforeSend: function(xhr, setting) {
                $(event.target).attr('disabled', 'disabled'); 
            },
            success: function(data, status, xhr) {
                $('#add-to-cart').hide();
                $('#remove-from-cart').show();
                $(event.target).removeAttr('disabled');
            }
        });
    });

    $('#remove-button').click(function(event) {
        jQuery.ajax({
            url: '//localhost:8000/cart',
            type: 'POST'
            data: {
                session: document.session,
                action: 'remove'
            },
            dataType: 'json',
            beforeSend: function(xhr, setting) {
                $(event.target).attr('disabled', 'disabled'); 
            },
            success: function(data, status, xhr) {
                $('#add-to-cart').show();
                $('#remove-from-cart').hide();
                $(event.target).removeAttr('disabled');
            }
        });
    });
});

function request_inventory() {
    jQuery.getJSON('//localhost:8000/cart/status', {session: document.session},
        function(data, status, xhr) {
            $('#count').html(data['inventory_count']);
            setTimeout(request_inventory, 0);
        }
    );
}
