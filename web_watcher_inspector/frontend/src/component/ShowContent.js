import React, { Component } from 'react'
import "./ShowContent.css"
import { specificDivRef } from '../global';
import HomeInfoCard from './InfoCard';
class ShowContent extends Component {
    render() {
        return (
            <div id="contentbox" ref={specificDivRef}>
                <HomeInfoCard />
            </div>
        );
    }
}
export default ShowContent;