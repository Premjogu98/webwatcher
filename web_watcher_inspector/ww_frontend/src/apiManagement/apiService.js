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