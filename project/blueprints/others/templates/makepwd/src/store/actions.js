
import axios from 'axios'

export const pwdhandler=(pwd)=>{
  return {
    type: "PASSWORDHANDLER",
    pwd: pwd
  }
}


export const passwordhandler=(pwd)=>{
  return (dispatch)=>{
    // localStorage.setItem('mypwd',pwd)
    dispatch(pwdhandler(pwd))
  }
}



// ----------------------


export const yeshandler=()=>{
  return {
    type:'YESCLICKED'
  }
}
export const yesclicked =()=>{
  return (dispatch)=>{
    axios.get('http://hit-the-road.cc/burger/set_pwd')
    .then(result=>{
      console.log(result)
      dispatch(yeshandler())
    })

  }
}
