import React,{Component} from 'react'
import {connect} from 'react-redux'
import classes from './getPasswordResult.module.css'
import * as actions from '../store/actions'

const mapStateToProps=state=>{
  return {
    reduxState: state
  }
}


const mapDispatchToProps=(dispatch)=>{
  return {
     onPasswordHander:(pwd)=>dispatch(actions.passwordhandler(pwd))
  }
}



class result extends Component{

  componentDidMount(){
    const password = Math.floor(Math.random()*100000000000)
    if (this.props.onPasswordHander){
      this.props.onPasswordHander(password)
    }
  }


  render(){
    return (
      <div className={classes.result}>
              <h1>学要认真，玩要放开，今天做的很好，继续保持，加油！！！</h1>
              <p>现在时间是{new Date().getHours()}点</p>
              <p>今天的密码是： {new Date().getHours()>=23?this.props.reduxState.password:"时间还未到23点"}</p>
              <p>游戏完记得来重置密码</p>

            </div>
    )
  }

}

export default connect(mapStateToProps, mapDispatchToProps)(result)
