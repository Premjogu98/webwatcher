import React, { Component } from 'react';
import "../component/GridHandler.css"
import "./WebInspector.css"
import Clipboard from '../component/Clipboard';
import { specificDivRef } from "../globalVariables/global.js";
import { loadHtml } from '../apiManagement/apiService.js';
import { NotificationContainer } from 'react-notifications';
import { Notifications } from '../component/Notifications';

class WebInspector extends Component {
    constructor() {
        super();
        this.state = {
            test_api_data: "",
            input_value: "null"
        };
    }
    handleInputChange = (event) => {
        this.setState({ input_value: event.target.value });
    };
    handleButtonClick = () => {
        loadHtml(this.state.input_value)
            .then((result) => {
                const element = document.getElementById("contentbox");
                if (element) {
                    element.innerHTML = result;
                }
            })
            .catch((error) => {
                const element = document.getElementById("contentbox");
                if (element) {
                    Notifications("error",error.response.data,"error",3000)();
                    console.log(error.response.data)
                }
            });
    };
    render() {

        return (
            <>
            <div className="grid web-inspector-d">
                <div className='grid-col-5 insider-left'>
                    <div className='insider-left-input'>
                        <input type="text" className="input-area" required id="inputName" placeholder='https://www.example.com/' onChange={this.handleInputChange} />
                    </div>
                </div>
                <div className='grid-col-2 insider-left'>
                    <button className="go-btn" onClick={this.handleButtonClick} ><span >Goo.. </span></button>
                </div>
                {/* <div className='grid-col-5 insider-left'>
                    <Clipboard />
                </div> */}
                
                <NotificationContainer/> 
            </div>
            <div>
                <div id="contentbox" ref={specificDivRef}>
                    {/* <h1>L</h1> */}
                </div>
            </div>
            </>
        );
    }
}

export default WebInspector;
