import React, { Component } from 'react';
import { UpdateXpathToDB, loadHtmlUsingID } from '../apiManagement/apiService.js';
import { NotificationContainer } from 'react-notifications';
import { Notifications } from './Notifications.js';
import { clearSessionData, getSessionData, globalVariables, setSessionData, specificDivRef } from "../globalVariables/global.js";
import "./InspectContent.css";
import axios from 'axios';
class InspectContent extends Component {
    constructor(props) {
        super(props);
        this.state = {
            content: <h3>Loading.....</h3>,
            highlightedElement: null,
            isHighlighting: false,
            inspect: "Start Inspect",
            xpath: null,
            showDialog: false,
            tlid: null
        };
    }

    componentDidMount() {
        this.handleButtonClick();
        this.setState({ isHighlighting: true, inspect: "Press Escape" });
        clearSessionData()
        this.startListener()
    }
    startListener() {
        document.addEventListener('mousemove', this.handleMouseMove);
        document.addEventListener('keyup', this.handleKeyUp);
        document.addEventListener('click', this.handleClick);
    }

    endListener() {
        document.removeEventListener('mousemove', this.handleMouseMove);
        document.removeEventListener('keyup', this.handleKeyUp);
        document.removeEventListener('click', this.handleClick);
    }

    handleButtonClick = () => {
        const url = window.location.pathname.replace("/inspect/", "")
        this.setState({ tlid: url })
        loadHtmlUsingID(url)
            .then((result) => {
                const element = document.getElementById("contentbox");
                if (element) {
                    element.innerHTML = result;
                }
            })
            .catch((error) => {
                const element = document.getElementById("contentbox");
                if (element) {
                    Notifications("error", error.response.data, "error", 3000)();
                    console.log(error.response.data)
                }
            });
    };
    updateXpathOnYes = () => {
        const { xpath, tlid } = this.state;
        const requestData = {
            xpath,
            tlid,
        };
        console.log(requestData)
        axios.patch(`${globalVariables.apiUrl}/update/xpath`, requestData)
            .then(response => {
                console.log(response.data); // Log the response data
                Notifications("success", "XPATH Updated Successfully", "error", 3000)();
            })
            .catch(error => {
                console.error('Error:', error);
                Notifications("error", "Failed To Update XAPTH", "error", 3000)();
            }).finally(re => {
                this.handleCancel()
            });
        
    }


    handleMouseMove = (event) => {
        // console.log(event)
        if (
            specificDivRef.current &&
            specificDivRef.current.contains(event.target) === true && this.state.isHighlighting === true
        ) {
            const element = this.getElementUnderCursor(event);
            if (element !== this.state.highlightedElement) {
                if (this.state.highlightedElement) {
                    this.state.highlightedElement.style.backgroundColor = null;
                    this.state.highlightedElement.style.transition = null;
                }
                if (element) {
                    element.style.backgroundColor = '#95d3ffdb';
                    element.style.transition = 'background-color 0.1s ease';
                }
                this.setState({ highlightedElement: element });
            }
        }

    };

    getElementUnderCursor(event) {
        const elementsFromPoint = document.elementsFromPoint(event.clientX, event.clientY);
        const target = 'target' in event ? event.target : event.srcElement;
        const path = this.getPathTo(target);
        this.setState({ xpath: path });
        document.getElementById('copy-input').value = path;

        return elementsFromPoint.find(
            (el) => el !== this.state.highlightedElement
        );
    }
    getPathTo(element) {
        if (element.id !== '') return "//*[@id='" + element.id + "']";
        // if (element.className !== '') return "//*[@class='" + element.className + "']";
        if (element === document.body) return element.tagName.toLowerCase();

        let ix = 0;
        const siblings = element.parentNode.childNodes;
        for (let i = 0; i < siblings.length; i++) {
            const sibling = siblings[i];
            if (sibling === element)
                return (this.getPathTo(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + (ix + 1) + ']');
            if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
                ix++;
            }
        }
    }

    handleKeyUp = (event) => {
        if (event.key === 'Escape') {
            this.endListener()
            this.clearHighlights();
            this.setState({ inspect: "Start Inspect" });
            document.getElementById('copy-input').value = this.inpuText;
        }
    };
    copyToClipboard = () => {
        if (getSessionData('xpath') !== this.inpuText) {
            navigator.clipboard.writeText(getSessionData('xpath')).then(
                () => {
                    // Notifications("success", 'Xpath Copied', '', 1000)();
                    setSessionData("xpath", this.inpuText)
                    this.setState({ value: this.inpuText })
                },
                () => {
                    Notifications("error", 'Copying failed', '', 4000)();
                }
            )
        } else {
            Notifications("info", 'Nothing to copy', '', 3000)();
        }

    };
    handleClick = (event) => {
        if (
            specificDivRef.current &&
            specificDivRef.current.contains(event.target) && this.state.isHighlighting === true
        ) {
            setSessionData("xpath", this.state.xpath)
            this.copyToClipboard()
            this.setState({ showDialog: true });
            this.endListener()
            this.clearHighlights();

        }
    };

    clearHighlights() {
        if (this.state.highlightedElement) {
            this.state.highlightedElement.style.backgroundColor = null;
            this.state.highlightedElement.style.transition = null;
            this.setState({ isHighlighting: false });
        }
    }
    handleConfirm = () => {
        // Handle confirmation logic when user clicks "OK"
        // alert('Confirmed!');
        Notifications("info", 'Wait Until Xpath Update', '', 5000)();
        this.updateXpathOnYes()
        this.setState({ showDialog: false });
    };

    handleCancel = () => {
        this.setState({ isHighlighting: true, inspect: "Press Escape" });
        clearSessionData()
        this.startListener()
        this.setState({ showDialog: false });
    };
    render() {
        return (
            <>
                {this.state.showDialog && (
                    <div className="confirmation-dialog">
                        <div>
                            <h6 className='alert-header'>Update Xpath <strong>{this.state.xpath}</strong></h6>
                            <p className='alert-content'>Are you sure you want to update XPath with the previous one?</p>
                            <button className='alert-button' onClick={this.handleConfirm}>Yes</button>
                            <button className='alert-button' onClick={this.handleCancel}>No</button>
                        </div>
                    </div>
                )}
                <input
                    id="copy-input"
                    className="copy-input"
                    defaultValue={this.state.value}
                    onChange={this.state.value}
                />
                <div id="contentbox" ref={specificDivRef}>
                </div>
                <NotificationContainer />
            </>
        );
    }
}

export default InspectContent;
