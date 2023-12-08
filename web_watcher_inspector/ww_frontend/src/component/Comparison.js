import React, { useEffect, useState } from "react";
import ReactDiffViewer, { DiffMethod } from "react-diff-viewer";
import { html } from "js-beautify";
import ToggleButton from "react-toggle-button";
import "./Comparison.css";
import { fromHTML,toHTML } from "../globalVariables/global";

const htmlStylingOptions = {
    indent_size: 4,
    html: {
        end_with_newline: true
    }
};

function formatHTMLForDiff(htmlStr, textOnly) {
    const formattedHTML = html(htmlStr, htmlStylingOptions);
    if (textOnly) {
        return new DOMParser().parseFromString(formattedHTML, "text/html").body
            .innerText;
    }

    return formattedHTML;
}

export default function Comparison() {
    const [textOnly, setTextOnly] = useState(true);

    const compareStyles = {
        variables: {
            light: {
                codeFoldGutterBackground: "#6F767E",
                codeFoldBackground: "#E2E4E5"
            }
        }
    };

    useEffect(() => {
        window.addEventListener("click", (e) => console.log(e.target));
    }, []);

    return (
        <div className="Comparison">
            <div>
                Text only
                <ToggleButton
                    onToggle={(value) => {
                        setTextOnly(!value);
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
                leftTitle="Initial version"
                rightTitle="Adjusted solution"
                onLineNumberClick={(lineId) => console.log(lineId)}
                renderContent={(source) => {
                    return source;
                }}
            />
        </div>
    );
}
