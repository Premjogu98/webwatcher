import React, { Component } from "react";
import { CopyIcon } from '../assets/icons/find_icon.js';
import { NotificationContainer } from 'react-notifications';
import { Notifications } from './Notifications.js';
import { getSessionData, setSessionData } from "../global.js";

class Clipboard extends Component {
    constructor(props) {
        super(props);

        this.state = {
            url: null,
            value: "Copy Xpath Here",
        };
    }
    copyToClipboard = () => {
        if (getSessionData('xpath') !== this.state.value) {
            navigator.clipboard.writeText(getSessionData('xpath')).then(
                () => {
                    Notifications("success", 'Xpath Copied', '', 2000)();
                    setSessionData("xpath", this.state.value)
                    this.setState({ value: this.state.value })
                },
                () => {
                    Notifications("error", 'Copying failed', '', 2000)();
                }
            )
        } else {
            Notifications("info", 'Nothing to copy', '', 2000)();
        }

    };

    otherCopy = () => {
        console.log(getSessionData("xpath"))
        Notifications("success", 'Xpath Copied', '', 3000)();
    }

    render() {
        return (
            <div className="grid-col-11">
                <div className="xpath-input-box">
                    <input
                        id="copy-input"
                        className="copy-input"
                        defaultValue={this.state.value}
                        onChange={this.state.value}
                    />
                    <button
                        className="copy-btn"
                        onClick={this.copyToClipboard}
                    >
                        <CopyIcon {...{
                            style: {
                                width: "1.6vw",
                                height: "unset"
                            }
                        }} />
                    </button>
                    <NotificationContainer />

                </div>
            </div>
        );

    }
}
export default Clipboard;