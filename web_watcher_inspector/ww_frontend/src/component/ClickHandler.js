import React, { Component } from 'react';
import { clearSessionData, getSessionData, setSessionData, specificDivRef } from "../globalVariables/global.js";
import { Notifications } from './Notifications';
import { NotificationContainer } from 'react-notifications';
import "./ClickHandler.css";

class ClickHandler extends Component {
    constructor(props) {
        super(props);
        this.state = {
            highlightedElement: null,
            isHighlighting: false,
            inspect: "Start Inspect",
            xpath: null
        };
        this.inpuText = "Copy Xpath Here";
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

    handleMouseMove = (event) => {
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
                    element.style.backgroundColor = 'pink';
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
                    Notifications("success", 'Xpath Copied', '', 1000)();
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
        }
    };

    clearHighlights() {
        if (this.state.highlightedElement) {
            this.state.highlightedElement.style.backgroundColor = null;
            this.state.highlightedElement.style.transition = null;
            this.setState({ isHighlighting: false });
        }
    }

    handleButtonClick = () => {
        this.setState({ isHighlighting: true, inspect: "Press Escape" });
        clearSessionData()
        this.startListener()
    };
    render() {
        return (
            <>
                <button id='inspect-btn' onClick={this.handleButtonClick}>{this.state.inspect}</button>
                <NotificationContainer />
            </>

        )
    }
}

export default ClickHandler;
