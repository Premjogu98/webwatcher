import React, { Component } from 'react';
import { useParams } from 'react-router-dom';
import { loadHtmlUsingID } from '../apiManagement/apiService';
import { specificDivRef } from "../globalVariables/global.js";
import { NotificationContainer } from 'react-notifications';
import { Notifications } from '../component/Notifications';
export function handleButtonClick (id) {
    loadHtmlUsingID(id)
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
export const InspectContent = () => {
    const { id } = useParams();
    handleButtonClick(id)
    return (
        <>
        <NotificationContainer/> 
        <div id="contentbox" ref={specificDivRef}>
            <h3>Loading.....</h3>
        </div>
        </>
    )
}
