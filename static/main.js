$( document ).ready(function() {
    console.log( "ready!" );
    document.user_token = null;
    // -----------------------------------------------------------------------
    function showinputform()
    {
         $("#inputform").fadeIn();
         $("#inputform").css({"visibility":"visible","display":"block"});
    }

    function hideinputform()
    {
         $("#inputform").fadeOut();
         $("#inputform").css({"visibility":"hidden","display":"none"});
    }
    function postit(url, data, success) {
        $.ajax({
                type: 'POST',
                url: url,
                data: data,
                success: success,
                contentType: "application/json",
                dataType: 'json'
        });
    };
    // -----------------------------------------------------------------------
    $("#signup").click(function (){
        var url = '/user/signup';
        $("#go_button").html('Sign Up');
        $("#go_button").click(function (){
            var name = $("#name").val();
            var pwd = $("#password").val();
            var data = JSON.stringify({'user': name, 'password': pwd});
            postit(url, data, function(data) {
                console.log(data); 
            });
            hideinputform();
        });
        showinputform();
    });
    $("#login").click(function (){
        var url = '/user/login';
        $("#go_button").html('Login');
        $("#go_button").click(function (){
            var name = $("#name").val();
            var pwd = $("#password").val();
            var data = JSON.stringify({'user': name, 'password': pwd});
            postit(url, data, function(data) {
                console.log(data); 
                document.user_token = data.token;
            });
            hideinputform();
        });
        showinputform();
    });
    $("#logout").click(function (){
        var url = '/user/logout';
        var data = JSON.stringify({'token': document.user_token});
        postit(url, data, function(data) { console.log(data); });
    });
});
