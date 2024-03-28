import React, { Component } from 'react'
import "./Filters.css"
import Clipboard from './Clipboard';
import ClickHandler from './ClickHandler';
// import axios from 'axios';
// import { globalVariables } from '../global';
import { loadHtml } from '../apiManagement/apiService';
import { Notifications } from './Notifications';
import {NotificationContainer} from 'react-notifications';

class Filters extends Component {
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
            <div className="sticky">
                <div className="grid">
                    <div className="grid-col-6 header">
                        <div className="input-group">
                            <input type="text" className="input-area" required id="inputName" placeholder='https://www.example.com/' onChange={this.handleInputChange} />
                            <button className="go-btn" onClick={this.handleButtonClick} ><span >Goo... </span></button>
                            <NotificationContainer/> 
                        </div>
                    </div>
                    <div className="grid-col-6 filters-d">
                        <div className="grid">
                            <Clipboard />
                            <ClickHandler />
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}
export default Filters;