import { useEffect, useContext } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { UserContext } from './UserContext';

const useUserIdCheck = () => {
  const { userId } = useContext(UserContext);
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    if (!userId && location.pathname !== '/login') {
      navigate('/login'); // Navigate to the page where userId can be set
    }
  }, [userId, location, navigate]);
};

export default useUserIdCheck;







// // =====
// /** @jsx React.DOM */

// var ReactCSSTransitionGroup = React.addons.CSSTransitionGroup;
// var SelectBox = React.createClass({
//   getInitialState: function() {
//       return {
//           input_value: "",
//           placeholder: "Select Option...",
//           show_list: false,
//           show_input: true
//       };
//   },
//   render: function() {
//     return (   
//       <div className="selectbox">
//           <HiddenInput onChange={this.handleOptionClick} value={this.state.input_value} />
//           {this.state.show_input ?<SelectInput onClick={this.handlePlaceholderClick} placeholder={this.state.placeholder} /> : null }
//           {this.state.show_list ? <SelectList onClick={this.handleOptionClick} data={this.props.data} /> : null }       
//       </div>
//     );
//   },
//   handleOptionClick: function() {
//     this.setState({placeholder: event.target.dataset.tag});
//     this.setState({input_value: event.target.dataset.tag});
//     this.setState({show_list: false});
//     this.setState({show_input: true});
  
//    var node = document.getElementById('select_input_id');
//     var event2 = new Event('input', { bubbles: true });
//     node.dispatchEvent(event2);

//   },
//   handlePlaceholderClick: function() {
//       this.setState({show_list: true});
//       this.setState({show_input: false});
//   }   
// });


// var SelectList = React.createClass({

//   render: function() {
//     var $this = this;
//     var optionNodes = this.props.data.map(function(option) {
//       return (  
//         <Option onClick={$this.props.onClick} text={option.text} ></Option>
//       );
//     });
 
    
//     return (
//       <ReactCSSTransitionGroup transitionEnterTimeout={500} transitionAppear={true} transitionName="example">
//           <div className="select_list">          
//                   {optionNodes}   
//           </div>
//       </ReactCSSTransitionGroup>
//     );
//   }
// });
    
// var Option = React.createClass({
//   render: function() {
//     return (
//       <div onClick={this.props.onClick} className="option" data-tag={this.props.text}>
//         <p>
//             {this.props.text}
//         </p>
//       </div>
//     );
//   }
// });


// var SelectInput = React.createClass({
//   render: function() {
//     return ( 
//       <div onClick={this.props.onClick} className="select_input">
//           <p>
//               {this.props.placeholder}
//           </p>
//       </div>
//     );
//   }
// });

// var HiddenInput = React.createClass({
//   getInitialState: function() {
//     return {value: this.props.value};
//   },
//   handleChange: function(event) {
//     this.setState({value: this.props.value});
//   },
//   render: function() {
//     var value = this.state.value;
//     return (   
//    <input type="hidden"  id="select_input_id" value={this.props.value}  />
      
//     );
//   }
// });    
    
// var options_data = [
//   {id: 1,text: "Aaa"},
//   {id: 2,text: "Baa"},
//   {id: 3,text: "Caa"}
// ];    
    
// React.render(
//   <SelectBox data={options_data} />,
//   document.getElementById("select_container")
// );


