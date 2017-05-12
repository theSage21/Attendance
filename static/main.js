$( document ).ready(function() {
    console.log( "ready!" );
    // -----------------------------------------------------------------------
    function deltoken(){
        document.cookie = "usertoken=; expires=Thu, 01 Jan 1970 00:00:00 UTC;";

    }
    function gettoken(){
        var cookies = document.cookie.split('; ');
        for(cook of cookies){
            if(cook.includes('usertoken=')){
                return cook.replace('usertoken=', '');
            }
        }
        return null;
    }
    function addtogallery(path){
        console.log(path);
        $("#gallery").append('<img src="/'+path+'">');

    }
    function currentuser(token){
        var url = '/user';
        var data = JSON.stringify({'token': token});
        postit(url, data, function(data) {
            console.log(data); 
            if(data['status']){
                $("#username").html(data['name'] + ' ' + data['kind']);
                console.log('adding images');
                for(image of data['images']){
                    addtogallery(image);
                }
            }
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
            } else if($('#go_button').html() == 'Login'){
                deltoken();
                $("#usertoken").val(data.token);
                document.cookie = "usertoken="+data.token;
                currentuser(data.token);
            }
        });
        hideinputform();
    });
    $("#signup").click(function (){
        $("#posturl").val('/user/signup');
        $("#kind").css({"visibility":"visible","display":"block"});
        $("#go_button").html('Sign Up');
        hideimageform();
        showinputform();
    });
    $("#login").click(function (){
        $("#posturl").val('/user/login');
        $("#kind").css({"visibility":"hidden","display":"none"});
        $("#go_button").html('Login');
        hideimageform();
        showinputform();
    });
    $("#logout").click(function (){
        var token = gettoken();
        console.log(token);
        var data = JSON.stringify({'token': token});
        var url = '/user/logout';
        postit(url, data, function(data) { console.log(data); });
        $("#username").html('|Anon User|');
        deltoken();
        document.location.reload();
    });
    $("#imageupload").click(function (){
        hideinputform();
        showimageform();
    });
    var token = gettoken();
    if(token != null){
        currentuser(token);
    }
});
