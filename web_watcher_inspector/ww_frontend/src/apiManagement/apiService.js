import axios from 'axios';
import { globalVariables } from "../globalVariables/global.js";
export const loadHtml = async (url) => {
    try {
        const main_url = `${globalVariables.apiUrl}/get/html?url=${url}`
        const response = await axios.get(main_url);
        console.log(response)
        return response.data;
    } catch (error) {
        console.error("Error fetching data:", error);
        throw error;
    }
}
export const loadHtmlUsingID = async (id) => {
    try {
        const main_url = `${globalVariables.apiUrl}/get/html?id=${id}`
        const response = await axios.get(main_url);
        console.log(response)
        return response.data;
    } catch (error) {
        console.error("Error fetching data:", error);
        throw error;
    }
}
export const UpdateXpathToDB = async (data) => {
    try {
        const main_url = `${globalVariables.apiUrl}/update/xpath`
        const response = await axios.patch(main_url,data);
        console.log(response)
        return response.data;
    } catch (error) {
        console.error("Error fetching data:", error);
        throw error;
    }
}
export const FetchAdditionalInfo = async (id) => {
    try {
        const main_url = `${globalVariables.apiUrl}/addition/data?id=${id}`
        const response = await axios.get(main_url);
        console.log(response.data)
        return response.data;
    } catch (error) {
        console.error("Error fetching data:", error);
        throw error;
    } finally{
        return id;
    }
}