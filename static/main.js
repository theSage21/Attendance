$( document ).ready(function() {
    console.log( "ready!" );
    document.user_token = null;
    // -----------------------------------------------------------------------
    function currentuser(token){
        var url = '/user';
        var data = JSON.stringify({'token': token});
        postit(url, data, function(data) {
            console.log(data); 
            $("#username").html(data['name'] + ' ' + data['kind']);
        });
    }
    function showinputform()
    { $("#inputform").fadeIn();
      $("#inputform").css({"visibility":"visible","display":"block"});
      $("#name").focus();
    }

    function hideinputform()
    { $("#inputform").fadeOut();
      $("#inputform").css({"visibility":"hidden","display":"none"});
    }
    function getformdata(){
        var name = $("#name").val();
        var pwd = $("#password").val();
        var kind = $("#kind").val();
        return {'user': name, 'password': pwd, 'kind': kind};
    }
    function postit(url, data, success) {
        $.ajax({type: 'POST',
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
            var data = JSON.stringify(getformdata());
            postit(url, data, function(data) {
                console.log(data); 
                alert("Signup Successful. You can login now.");
            });
            hideinputform();
        });
        showinputform();
    });
    $("#login").click(function (){
        var url = '/user/login';
        $("#go_button").html('Login');
        $("#go_button").click(function (){
            var data = JSON.stringify(getformdata());
            postit(url, data, function(data) {
                console.log(data); 
                document.user_token = data.token;
                currentuser(data.token);
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
