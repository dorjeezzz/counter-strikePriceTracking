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

    // const handleSearchTextClick = async (searchText) => {
        
    // };

    const handlePriceHistoryClose = () =>{
        setShowPriceHistory(false);
        setPriceHistory([]);
    };

    const handleNewSearchTextChange = (event) => {
        setNewSearchText(event.target.value);
    };

    return(
        <div className = "main">
            <h1>Product Search Tool</h1>

        </div>
    );
}