domSelector = function(target){
  return document.querySelector(target)
}


var ui =(function(){
    var updateSpan = function(value){
      var newHtml =`<button type="button" class="btn tag-btn  btn-info">
                  ${value} <span class="badge badge-light">×</span>
                  </button>`
       domSelector('.myInput').insertAdjacentHTML('afterBegin', newHtml);
    }


    return {
      updateSpan: updateSpan
    }
})()




var controller = (function(){
   var setupEventListeners = function(){
     //点击外部的框，input框focus
        domSelector('.myInput').addEventListener('click', function(){
          domSelector('.input-inner').focus()
        })
        //输入值，然后在外部框下面增加可以删除的button
        get_input = domSelector('.input-inner')
        get_input.addEventListener('keypress', function(event){
          if (event.keyCode ===13 || event.which ===13){
            var value = get_input.value
            if (value !=''){
              ui.updateSpan(value)
              get_input.value=''
              get_input.focus()
              badge=domSelector('.myInput').addEventListener('click', function(event){
                my_target= event.target.parentNode
                if (my_target.classList.contains('btn')){
                  my_target.remove()
                }
              })
            }

          }
        })

        //添加ingredient和删除
        domSelector('.ingre-btn').addEventListener('click', function(){
          value = domSelector('.ingredients').value
          if (value !== ''){
            var newHtml=`<li>${value} <span class="badge badge-transparent">×</span></li>`
            document.querySelector('.ingre ul').insertAdjacentHTML('afterBegin', newHtml);
            domSelector('.ingredients').value=''
          }
          domSelector('.badge-transparent').addEventListener('click', function(event){
            my_target= event.target.parentNode
            my_target.remove()

          })
        })



        //添加steps
        domSelector('.steps-btn').addEventListener('click', function(){
           value = domSelector('.form-steps').value
           if (value !== ''){
             var newHtml=`<li>${value}</li>`
             document.querySelector('.steps ul').insertAdjacentHTML('beforeEnd', newHtml);
             domSelector('.form-steps').value=''
           }

        })

        //验证和提交
        domSelector('.submit_btn').addEventListener('click', function(){
           title= domSelector('.form-title').value
           if (title.length >125){
             alert('菜名超出125字')
           }else{
             category = domSelector('.form-select').value
             tagNode= document.querySelectorAll('.tag-btn')
             tagArr= Array.prototype.slice.call(tagNode)
             var tags = tagArr.map(function(item){
                 return item.innerText.split(' ')[0]
               })
             if (tags.length >10){
               alert('标签超出10个')
             }else{
               ingre = document.querySelectorAll('.ingre ul li')
               ingredients = Array.from(ingre).map(function(item){
                 return item.innerText
               })
               //得到所有steps
               stepsNode= document.querySelectorAll('.steps ul li')
               steps = Array.from(stepsNode).map(function(item){
                     return item.innerText
                   })
                if (title !=''){
                    var form ={
                          title: title,
                          category: category,
                          tags: tags,
                          ingredients: ingredients,
                          steps: steps,
                          files: []
                         }
                    send_form(form, function(r){
                      var data = JSON.parse(r)
                      if (data ==='saved'){
                            domSelector('.first-f').style.display='none'
                            domSelector('.upload').style.display='block'
                            domSelector('.hidden-input').value= title
                            }else{
                                console.log('you')
                              }

                    })


              }

             }
           }


        })
            // title= domSelector('.form-title').value
            // console.log('go')
            // if (title.length >125){
            //   alert('菜名超出125字')
            // }else{
            //   category = domSelector('.form-select').value
            //   //得到所有tags
            //   tagNode= document.querySelectorAll('.tag-btn')
            //   tagArr= Array.prototype.slice.call(tagNode)
            //   var tags = tagArr.map(function(item){
            //     return item.innerText.split(' ')[0]
            //   })
            //   if (tags.length >10){
            //     alert('标签超出10个')
            //   }else{
            //     //得到所有ingredients
            //     ingre = document.querySelectorAll('.ingre ul li')
            //     ingredients = Array.from(ingre).map(function(item){
            //       return item.innerText
            //     })
            //     //得到所有steps
            //     stepsNode= document.querySelectorAll('.steps ul li')
            //     steps = Array.from(stepsNode).map(function(item){
            //       return item.innerText
            //     })
            //     if (title !=''){
            //       var form ={
            //          title: title,
            //          category: category,
            //          tags: tags,
            //          ingredients: ingredients,
            //          steps: steps,
            //          files: []
            //       }
            //       console.log(form)
            //       send_form(form, function(r){
            //         console.log('hi')
            //         var data = JSON.parse(r)
            //         if (data ==='saved'){
            //           domSelector('.first-f').style.display='none'
            //           domSelector('.upload').style.display='block'
            //           domSelector('.hidden-input').value= title
            //         }else{
            //           console.log('you')
            //         }
            //       })
            //
            //     }
            //   }
            //
            // }





   }

   return { init:function(){
       setupEventListeners();
   }}
})()


controller.init()
