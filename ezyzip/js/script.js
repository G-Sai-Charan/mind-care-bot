$(document).ready(function() {
    $('#chat-form').submit(function(event) {
        event.preventDefault();
        var message = $('#message-input').val();
        if (!message) {
            console.error('Message is empty');
            return;
        }
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5000',
            data: {'message': message},
            success: function(response) {
                if (!response || !response.response) {
                    console.error('Invalid response:', response);
                    return;
                }
                console.log(response);
                $('#chat-box').append('<p><strong>You:</strong> ' + message + '</p>');
                $('#chat-box').append('<p><strong>Bot:</strong> ' + response.response + '</p>');
                $('#message-input').val('');
                $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
            },
            error: function(xhr, status, error) {
                console.error('Ajax error:', xhr, status, error);
            }
        });
    });
});
