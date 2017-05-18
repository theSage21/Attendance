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
        var elem = $('<img src="/'+path+'" width=150px height=150px class="userimage">');
        $("#gallery").append(elem);
        elem.click(function (){
            if($(this).hasClass('marked_for_removal')){
                console.log('Removed for removal');
                $(this).removeClass('marked_for_removal');
            }else{
                console.log('Added for removal');
                $(this).addClass('marked_for_removal');
            }
        });
    }
    function get_class_joining_requests(){
        var url = '/user/request/approval';
        var data = JSON.stringify({'token': gettoken()});
        postit(url, data, function (data){
            console.log(data);

            if(data['status'] == true){
                var lecture_tables = $("<div class='row'></div>");
                lecture_tables.append('<div class="container"><h2>Lectures Under Your Supervision</h2><sub>People in gray are pending requests. Click on them to accept them. Requests are flushed every week.</sub></div>');
                $("#class_joining_requests").html('');
                $("#class_joining_requests").append(lecture_tables);
                // For each lecture
                for (var lecture in data['lectures']) {
                    if (data['lectures'].hasOwnProperty(lecture)) {
                        var table = $('<table class="two columns container"></table>');
                        var thead = $("<thead><tr><th>"+lecture+"</th></tr></thead>");
                        var tbody = $("<tbody></tbody>");
                        table.append(thead);
                        table.append(tbody);
                        // For each request
                        for(name of data['lectures'][lecture]['req']){
                            var name = $("<tr class='mem_req' parent='"+lecture+"'><td>"+
                                         name+"</td></tr>");
                            name.click(function (){
                                var name = $(this).html().replace('<td>', '').replace('</td>', '');
                                var lec = $(this).attr('parent');
                                var data = JSON.stringify({'token': gettoken(),
                                    'user': name,
                                    'lecture': lec});
                                var url = '/user/request/approved';
                                postit(url, data, function (data){
                                    console.log(data);
                                    if(data['status'] == true){
                                        get_class_joining_requests();
                                    }
                                });
                            });
                            tbody.append(name);
                        }
                        // For each member
                        for(name of data['lectures'][lecture]['mem']){
                            var name = $("<tr class='mem_approved'><td>"+
                                         name+"</td></tr>");
                            tbody.append(name);
                        }
                        console.log(lecture + " -> " + data['lectures'][lecture]);
                        lecture_tables.append(table);
                    }
                }
            }
        });
    }
    function studentview(data){
        console.log('adding images');
        for(image of data['images']){
            addtogallery(image);
        }
      $("#StudentImageGallery").fadeIn();
      $("#StudentImageGallery").css({"visibility":"visible","display":"block"});
      $("#request_classform").fadeIn();
      $("#request_classform").css({"visibility":"visible","display":"block"});
    }
    function teacherview(data){
      $("#TeacherGallery").fadeIn();
      $("#TeacherGallery").css({"visibility":"visible","display":"block"});
      $("#class_joining_requests").fadeIn();
      $("#class_joining_requests").css({"visibility":"visible","display":"block"});
      get_class_joining_requests();
    // TODO
    }
    function currentuser(token){
        var url = '/user';
        var data = JSON.stringify({'token': token});
        $("#usertoken").val(token);
        $("#usertoken_teacher").val(token);
        postit(url, data, function(data) {
            console.log(data); 
            if(data['status']){
                    $("#username").html(data['name'] + ' ' + data['kind']);
                    if(data['kind'] == 'Student'){
                        studentview(data);
                    } else {
                        teacherview(data);
                        console.log('Teacher');
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
    $("#gallery_button").click(function (){
        console.log($(".marked_for_removal"));  // TODO
        var to_remove = [];
        $('.marked_for_removal').map(function (index){
            to_remove.push($(this).attr('src').slice(1)//removes the leading '/'
            );
        });
        console.log(to_remove);
        var data = JSON.stringify({'images_to_remove': to_remove, 'token': gettoken()});
        var url = '/image/delete';
        postit(url, data, function (data) {
            console.log(data);
            if(data['status']){
                $('.marked_for_removal').remove();
            }
        });
    });
    $("#class_attendance_button").click(function (){
        var data = JSON.stringify({'token': gettoken(),
            'teacher': $('#teachername_for_req').val(),
            'lecture': $('#lecturename_for_req').val()
        });
        console.log(data);
        var url = '/user/request/class';
        postit(url, data, function (data){
            if(data['status'] == true){
                alert('Your request was successful. The teacher needs to accept your request');
            }else{
                alert(data['message']);
            }
        });
    });
    $("#generate_excel").click(function (){
        var lecture = $("#lecture_name_for_report_generation").val();
        var data = JSON.stringify({'token': gettoken(), 'lecture': lecture});
        console.log(data);
        var url = '/user/excelgen';
        postit(url, data, function(data){
            console.log(data);
            if (data['status'] == true){
                console.log('status is true');
                $("#download_link_for_excel").html('');
                var link = $("<a href='/static/"+ data['message'] + "'>Download "+data['message']+"</a>");
                $("#download_link_for_excel").append(link);

            }
        });
    });
});
