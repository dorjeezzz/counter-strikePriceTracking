import React, { useState, useEffect } from "react";
import SearchTextLists from "./components/SearchTextList";
import axios from "axios";
import PriceHistoryTable from "./components/PriceHistoryTable";
import TrackedProductList from "./components/TrackedProductList";

const URL = "http://localhost:5000";

function App(){
    const [showPriceHistory, setShowPriceHistory] = useState(false);
    const [PriceHistory, setPriceHistory] = useState([]);
    const [searchTexts, setSearchTexts] = useState([]);
    const [newSearchText, setNewSearchText] = useState("");

    useEffect(() =>{
        fetchUniqueSearchTexts();
    }, []);

    const fetchUniqueSearchTexts = async () =>{
        try{
            const response =  await axios.get(`${URL}/unique_search_texts`);
            const data = response.data;
            setSearchTexts(data);
        }
        catch (error){
            console.error("Failed to fetch search text: ", error);
        }
    };

    const handleSearchTextClick = async (searchText) => {
        try{
            const response = await axios.get(
                `${URL}/results?search_text=${searchText}`
            );
            const data = response.data;
            setPriceHistory(data);
            setShowPriceHistory(true);
        }
        catch(error){
            console.error("Error Fetching Price History, Try Again.", error);
        }
    };

    const handlePriceHistoryClose = () =>{
        setShowPriceHistory(false);
        setPriceHistory([]);
    };

    const handleNewSearchTextChange = (event) => {
        setNewSearchText(event.target.value);
    };

    const handleNewSearchTextSubmit = async (event) => {
        event.preventDefault();
        try{
            await axios.post(`${URL}/start-scraper`,{
                search_text: newSearchText,
                url: "https://cs.float",
            });
            alert("Successfully Started");
            setSearchTexts([...searchTexts, newSearchText]);
            setNewSearchText("");
        }
        catch(error){
            console.error("Error starting...", error);
        }
    };
    return(
        <div className = "main">
            <h1>Product Search Tool</h1>
            <form onSubmit={handleNewSearchTextSubmit}>
                <label>Search for New Item:</label>
                <input
                
                />
            </form>
        </div>
    );
}

export default App;