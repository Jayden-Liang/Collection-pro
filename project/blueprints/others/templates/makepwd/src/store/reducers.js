const initialState={
  questionAnswered: false,
  questionResult: false,
  password: null,
  resetedPwd: false,
  PwdReceived: false
}

const reducer =(state=initialState, action)=>{
  switch(action.type){
    case 'YESCLICKED':
      return{
        ...state,
        questionAnswered: true,
        questionResult: true
      }
    case 'NOCLICKED':
      return{
        ...state,
        questionAnswered: true,
        questionResult: false
      }
    case 'PASSWORDHANDLER':
       return{
         ...state,
         password: state.password?state.password:action.pwd,
         PwdReceived: true
       }
  }
}

export default reducer
