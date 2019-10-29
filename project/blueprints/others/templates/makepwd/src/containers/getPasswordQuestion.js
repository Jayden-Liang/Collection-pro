import React, {Component} from 'react'
import classes from './getPasswordQuestion.module.css'
import {Route} from 'react-router-dom'
import {connect} from 'react-redux'
import * as actions from '../store/actions'
import FUCK from '../components/setPwd/setPwd'

const mapStateToProps=state=>{
  return {
    reduxState: state
  }
}


const mapDispatchToProps=(dispatch)=>{
  return {
    onYesClicked: ()=> dispatch(actions.yesclicked()),
    onNoClicked: ()=> dispatch({type:'NOCLICKED'})
  }
}



class GetPwd extends Component{

  componentDidUpdate(){
    if(this.props.reduxState &&this.props.reduxState.questionResult){
      this.props.history.push('/password')
    }

  }



  render(){
    console.log(this.props)
    return <div className={classes.question}>
            <h1>今天做了什么？离目标更近了吗？</h1>
            <div className={classes.buttonGroup}>
                <button onClick={this.props.onYesClicked} type='button'>是的</button>
                <button onClick={this.props.onNoClicked} type='button'>很惭愧，没有</button>
            </div>

            <FUCK />

            <Route path={'/go_pwd'} component={FUCK}></Route>

          </div>
  }
}


export default connect(mapStateToProps, mapDispatchToProps)(GetPwd)
