var ajax = function(method, path, data, responseCallback) {
    var r = new XMLHttpRequest()           // 设置请求方法和请求地址
    r.open(method, path, true)              //true开启异步
    csrf_token = document.querySelector('#csrf_token')            //csrf 防护
    r.setRequestHeader("X-CSRFToken", csrf_token.value)
    r.setRequestHeader('Content-Type', 'application/json')
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            responseCallback(r.response)                                // r.response 存的就是服务器发过来的放在 HTTP BODY 中的数据
        }
    }
    data = JSON.stringify(data)
    r.send(data)
}

var apiAdd = function(form, callback) {
  var path = '/todo/add'
  ajax('POST', path, form, callback)
}


var apiDelete = function(form, callback){
  var path ='/todo/delete'
  ajax('POST', path, form, callback)
}

var apiFinish = function(form, callback){
  var path ='/todo/finish'
  ajax('POST', path, form, callback)
}
// ------------------------------------------------------------------------------------------------------------

var bindAdd = function(){
  todo = document.querySelector('.mytodo')
  todo.addEventListener('keydown', function(event){
     if (event.keyCode == 13){
       if (todo.value){
         htmlString  =`<li class='list-group-item items mark-1 '>
           <div class="row">
              <div class="col col-sm-10">
                <i class="far fa-square"></i> ${todo.value}
              </div>
              <div class="del col col-sm-2 mark-2">
                删除
              </div>
           </div>

         </li>`
         document.querySelector('.todos').insertAdjacentHTML('beforeend', htmlString)
         form ={'todo': todo.value}
         apiAdd(form, function(r){
           r =JSON.parse(r)
           listId = 'list-'+r['id']
           delId = 'del-'+r['id']
           document.querySelector('.mark-1').classList.add(listId)
           document.querySelector('.mark-2').classList.add(delId)
           document.querySelector('.mark-1').classList.remove('mark-1')
           document.querySelector('.mark-2').classList.remove('mark-2')
           console.log('complete')
         })
         todo.value=''
         todo.focus()
       }

     }
   })
}

// var delete = function(node1, node2){
//
// }


var bindDelete = function(){
  // 删除和完成
  t = document.querySelector('.todos')
  t.addEventListener('click', function(event){
    e = event.target
    if (e){
      clsName = e.classList
      if (clsName.contains('del')){
        parent= e.parentElement.parentElement;
        topNode = e.parentElement.parentElement.parentElement;
        topNode.removeChild(parent)
        dataId = parent.classList['2'].split('-')[1]
        form ={'todo': dataId}
        apiDelete(form, function(r){
          console.log(r)
        })
      }
      if (clsName.contains('col')){
        if (e.children[0]){
          e.children[0].classList.remove('fa-square')
          e.children[0].classList.add('fa-check-square')
          parent= e.parentElement.parentElement;
          topNode = e.parentElement.parentElement.parentElement;
          setTimeout(function(){
            topNode.removeChild(parent)
          }, 500)
          dataId = parent.classList['2'].split('-')[1]
          form ={'todo': dataId}
          apiFinish(form, function(r){
            console.log(r)
          })

        }
      }
    }
  })

}

bindAdd()
bindDelete()
