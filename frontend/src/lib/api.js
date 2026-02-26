import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

export const agentApi = {
    invoke: async (message, context = {}) => {
        try {
            const res = await axios.post(`${API_BASE}/agent/invoke`, {
                message,
                ...context
            });
            return res.data;
        } catch (error) {
            console.error("Agent Error:", error);
            return { response: "Sorry, I am having trouble connecting to the Trip Spirit." };
        }
    },
    searchPlaces: async (query) => {
        try {
            const res = await axios.post(`${API_BASE}/search`, { query });
            return res.data;
        } catch (error) {
            console.error("Search Error:", error);
            return [];
        }
    }
};
