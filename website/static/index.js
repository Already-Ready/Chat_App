$(function() {
    $('#sendBtn').bind('click', function() {
        var value = document.getElementById("msg").value
        $.getJSON('/send_message',
            {val:value},
            function(data) {

            });

});

window.addEventListener("load", function(){
    var update_loop = setInterval(update, 100);
    update()
});


function update() {
    fetch('/get_messages')
            .then(function (response) {
                return response.text();
            }).then(function (text) {
                console.log('GET response text:');
                document.getElementById("test").innerHTML = text; // Print the greeting as text
            });
            return false;
        });
}


