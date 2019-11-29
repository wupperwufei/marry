//搜索功能
function T_search(page,ord){
    var $opt = $('#text_s').val();
    var $op_gender = $('#op_g').val();
    var $op_birth = $('#op_b').val();
    console.log($opt)
    console.log($op_gender)
    console.log($op_birth)
    //如果用户没有输入文本信息查询，则弹框提醒
    if($opt.length==0 && $op_gender.length!=0){
        window.location.href = "http://127.0.0.1:5000/search/";
    }
    else{
//        var list_template = "<ul class='list-group'><li>查询条件</li><li>"+$opt+"</li><li>"+$op_gender+"</li><li>"+$op_birth+"</li></ul>";
//        $("#show").css("display","block");
//        $('#show').html(list_template);
        console.log(ord)
        post_data = {'option':$opt,'op_gender':$op_gender,'op_birth':$op_birth,'page':page,'order':ord};
        console.log(post_data);
        var data = { data:JSON.stringify(post_data),};
        $.ajax({
            type:'post',
            url:'http://127.0.0.1:5000/search/',
            data:data,
            dataType:'json',
            //是否用异步
            async: false,
            success:function(result){
                    if(result.code==200){
//                        console.log(result.data[0])

                        html_body = ''
                        html_body += '<ul class="main-member">'
                            for(i in result.data){
                            console.log(i)
                            html_body += '<li>'
                            html_body += '<a href="">'
                            html_body += '<img src="/static/media/'
                            html_body += result.data[i].image
                            html_body += '"width="150px" height="140px"><p class="mem-num">昵称：'
                            html_body += result.data[i].nickname
                            html_body += '</p>'
                            html_body += '<p class="mem-text">'
                            html_body += result.data[i].age
                            html_body += '  |  '
                            html_body += result.data[i].education
                            html_body += '  |  '
                            html_body += result.data[i].high
                            html_body += '<br>'
                            html_body += result.data[i].profession
                            html_body +=   ' | '
                            html_body += result.data[i].property
                            html_body += '</p>'
                            html_body += '</a>'
                            html_body += '</li>'
                            }
                        html_body += '</ul>'
                        $('.main-member').html(html_body)

                        if (result.data[0].total){
                            console.log("total:",result.data[0].total)
                            pages = Math.ceil(result.data[0].total/2)
                            order = result.data[0].order

                            console.log("pages:",pages)
                            console.log("order:",order)
                            html_body2 = ''
                            html_body2 += '<div class="page" id="page1">'
                            if(result.data[0].page>1){
                                html_body2 += '<a href="javascript:void(0);" onclick="T_search('
                                html_body2 += result.data[0].page-1
                                html_body2 += ','
                                html_body2 += order
                                html_body2 += ';">上一页</a>'
                                }
                            for(i=1;i<=pages;i++){
                                html_body2 += '<a href="javascript:void(0);" onclick="T_search('
                                html_body2 += i
                                html_body2 += ','
                                html_body2 += order
                                html_body2 += ');">'
                                html_body2 += i
                                html_body2 += '</a>'
                            }
                            if(result.data[0].page<pages){
                                html_body2 += '<a href="javascript:void(0);" onclick="T_search('
                                html_body2 += result.data[0].page+1
                                html_body2 += ','
                                html_body2 += order
                                html_body2 += ');">下一页</a>'
                                }
                            html_body2 += '当前页数：['
                            html_body2 += result.data[0].page
                            html_body2 += '/'
                            html_body2 += pages
                            html_body2 += ']&nbsp'
                        html_body2 += '</div>'
                        $('.page').html(html_body2)
                        }
                    }else{
                        alert(result.data['error'])
                    }
                },
            error:function(){
                alert("输入信息错误，请重新查询")
            }
    })
        }
    }