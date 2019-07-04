var ajax = function(method, path, data, responseCallback){
  var r= new XMLHttpRequest()
  r.open(method, path, true)
  csrf_token = document.querySelector('#csrf_token')
  r.setRequestHeader('X-CSRFToken', csrf_token.value)
  r.setRequestHeader('Content-Type', 'application/json')
  r.onreadystatechange = function(){
    if (r.readyState === 4){
        responseCallback(r.response)
    }
  }
  data = JSON.stringify(data)
  r.send(data)
}


var send_form = function(form, callback){
   var path ='/new_recipe'
   ajax('POST', path, form, callback)
}
