import React, {Component}from 'react';
import logo from './logo.svg';
import './App.css';
import {BrowserRouter} from 'react-router-dom'
import { Route, NavLink, Switch} from 'react-router-dom'
import getPwdQuestion from './containers/getPasswordQuestion'
import getPwdResult from './containers/getPasswordResult'
import {connect} from 'react-redux'



const mapStateToProps=state=>{
  return {
    reduxState: state
  }
}


const mapDispatchToProps=(dispatch)=>{
  return {

  }
}

class App extends Component {


  render(){
    return (
      <BrowserRouter>
      <div className="App">
      <Switch>
        <Route  path='/' exact component={getPwdQuestion} />
        {this.props.reduxState &&this.props.reduxState.questionAnswered &&this.props.reduxState.questionResult ?
          <Route path='/password' exact component={getPwdResult} />:null}
      <Route render={()=> <h1>404, Not Found</h1>} />
      </Switch>
      </div>
      </BrowserRouter>
    );

  }

}

export default connect(mapStateToProps, mapDispatchToProps)(App);
