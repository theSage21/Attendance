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
    function showimageform(){
      $("#imageform").fadeIn();
      $("#imageform").css({"visibility":"visible","display":"block"});
    }
    function hideimageform(){
      $("#imageform").fadeOut();
      $("#imageform").css({"visibility":"hidden","display":"none"});
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
        console.log(url);
        $.ajax({type: 'POST',
                url: url,
                data: data,
                success: success,
                contentType: "application/json",
                dataType: 'json'
        });
    };
    // -----------------------------------------------------------------------
    $("#go_button").click(function (){
        var data = JSON.stringify(getformdata());
        var url = $("#posturl").val();
        postit(url, data, function(data) {
            console.log(data); 
            if($('#go_button').html() == 'Sign Up'){
                alert("Signup Successful. You can login now.");
            } else {
                document.user_token = data.token;
                currentuser(data.token);
            }
        });
        hideinputform();
    });
    $("#signup").click(function (){
        $("#posturl").val('/user/signup');
        $("#kind").css({"visibility":"visible","display":"block"});
        $("#go_button").html('Sign Up');
        showinputform();
    });
    $("#login").click(function (){
        $("#posturl").val('/user/login');
        $("#kind").css({"visibility":"hidden","display":"none"});
        $("#go_button").html('Login');
        showinputform();
    });
    $("#logout").click(function (){
        $("#posturl").val('/user/logout');
        console.log(document.user_token);
        var data = JSON.stringify({'token': document.user_token});
        var url = $("#posturl").val();
        postit(url, data, function(data) { console.log(data); });
        $("#username").html('ANON');
    });
});
