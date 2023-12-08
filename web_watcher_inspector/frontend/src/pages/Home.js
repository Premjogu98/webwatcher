import React, { Component } from 'react'

import ClickHandler from '../component/ClickHandler';
import './Home.css';
import Navbar from '../component/Navbar';
import ReactTable6 from '../component/TableManagement';
class Home extends Component {
    constructor(props) {
        super(props);
        this.state = {
            highlightedElement: null        
        };
    }
    render() {
        return (
        <div id='content'>
            <h3 id="main-xpath"></h3>
            {/* <ClickHandler /> */}
            <ReactTable6 />
        </div>
        )
    }
}
export default Home;