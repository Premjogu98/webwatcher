import React, { Component } from 'react';
import "../component/GridHandler.css"
import "./WebInspector.css"
import Clipboard from '../component/Clipboard';
class WebInspector extends Component {
    constructor(props) {
        super(props);
    }
    render() {

        return (
            <div className="grid web-inspector-d">
                <div className='grid-col-5 insider-left'>
                    <div className='insider-left-input'>
                        <input type="text" className="input-area" required id="inputName" placeholder='https://www.example.com/' onChange={this.handleInputChange} />
                    </div>
                </div>
                <div className='grid-col-5 insider-left'>
                <button className="go-btn" onClick={this.handleButtonClick} ><span >Goo.. </span></button>
                </div>
                {/* <div className='grid-col-3 insider-left'>
                    <div className='insider-left-input'><input type="text" className="input-area" required id="inputName" placeholder='https://www.example.com/' onChange={this.handleInputChange} /></div>

                    <div><Clipboard /></div>
                    <div><h3>1</h3></div>
                    <div><h3>1</h3></div>
                </div>
                <div className='grid-col-9'>
                    <div><button className="go-btn" onClick={this.handleButtonClick} ><span >Goo.. </span></button></div>
                </div> */}
                {/* <div className='grid-col-10 insider-right'>
                    <div><h3>1</h3></div>
                    <div><h3>1</h3></div>
                    <div><h3>1</h3></div>
                    <div><h3>1</h3></div>
                    <div><h3>1</h3></div>
                </div> */}
            </div>
        );
    }
}

export default WebInspector;
