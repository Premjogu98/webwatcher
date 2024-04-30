import React, { Component } from "react";
import ReactDiffViewer, { DiffMethod } from "react-diff-viewer";
import { html } from "js-beautify";
import ToggleButton from "react-toggle-button";
import "./Comparison.css";
import axios from "axios";
import { globalVariables } from "../globalVariables/global.js";

const htmlStylingOptions = {
    indent_size: 4,
    html: {
        end_with_newline: true,
    },
};

function formatHTMLForDiff(htmlStr, textOnly) {
    const formattedHTML = html(htmlStr, htmlStylingOptions);
    if (textOnly) {
        return new DOMParser().parseFromString(formattedHTML, "text/html").body
            .innerText;
    }

    return formattedHTML;
}

class Comparison extends Component {
    constructor(props) {
        super(props);
        this.state = {
            textOnly: false,
            fromHTML: "",
            toHTML: "",
        };
    }

    componentDidMount() {
        // this.checkAuth();
        this.renderHtmlData();

    }
    renderHtmlData() {
        const id = window.location.pathname.replace("/comparison/", "").replace("/compare/", "")
        axios.get(`${globalVariables.apiUrl}/compared/html?id=${id}`)
            .then((response) => {
                this.setState({ fromHTML: response.data });
            })
            .catch((error) => {
                console.error("Error fetching fromHTML:", error);
            });

        axios.get(`${globalVariables.apiUrl}/compared/html?id=${id}&old=True`)
            .then((response) => {
                this.setState({ toHTML: response.data });
            })
            .catch((error) => {
                console.error("Error fetching toHTML:", error);
            });

        // window.addEventListener("click", (e) => console.log(e.target));
    }
    checkAuth() {
        console.error("Error fetching toHTML:");
        const AUTH = localStorage.getItem(globalVariables.authKey);
        if (AUTH === globalVariables.authStatus) {
            console.log("succsess")
        } else {
            window.location.href = '/login'
        }
    }
    render() {
        const { textOnly, fromHTML, toHTML } = this.state;

        const compareStyles = {
            variables: {
                light: {
                    codeFoldGutterBackground: "#6F767E",
                    codeFoldBackground: "#E2E4E5",
                },
            },
        };

        return (
            <div className="comparison-content">
                <div>
                    Text only
                    <ToggleButton
                        onToggle={(value) => {
                            this.setState({ textOnly: !value });
                        }}
                        value={textOnly}
                    />
                </div>
                <ReactDiffViewer
                    oldValue={formatHTMLForDiff(fromHTML, textOnly)}
                    newValue={formatHTMLForDiff(toHTML, textOnly)}
                    splitView={true}
                    compareMethod={DiffMethod.WORDS}
                    styles={compareStyles}
                    leftTitle="OLD HTML / TEXT"
                    rightTitle="NEW HTML / TEXT"
                    onLineNumberClick={(lineId) => console.log(lineId)}
                    renderContent={(source) => {
                        return source;
                    }}
                // useDarkTheme={true}
                />
            </div>
        );
    }
}

export default Comparison;