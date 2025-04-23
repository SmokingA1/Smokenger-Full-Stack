import React, { useState, useEffect, useCallback } from "react";
import api from "../../api";
import "../../styles/components/Chats/AllChats.css"
import {debounce} from "lodash";
import AllMembers from "./AllMembers";

const AllChats = ({ toggleIsChatVisible}) => {
    const [chats, setChats] = useState([]);
    const [chatName, setChatName] = useState("");
    const [isInfoList, setIsInfoList] = useState(false);
    const [infoData, setInfoData] = useState({
        id: null,
        chatName: "",
    })

    const getChats = useCallback(async (searchQuery) => {
        try {
            const response = await api.get(`/chats/?search=${searchQuery}`)
            setChats(response.data)
        } catch (error) {
            console.error("Some error occurred: ", error)
        }
    }, []);
    

    const debouncedFetchChats = useCallback(
        debounce((searchQuery) => getChats(searchQuery), 500),
        [getChats]
    );


    useEffect(() => {
        debouncedFetchChats(chatName);
    }, [chatName, debouncedFetchChats])


    return(
        <div className="all-chat-container">
            <div onClick={toggleIsChatVisible} className="close-container"> 
                <button><i className="bi bi-x"></i></button>
            </div>
            <div className="all-chats-input-container">
                <input 
                    className="all-chats-input-field"
                    type="text"
                    value={chatName}
                    onChange={(e) => setChatName(e.target.value)}
                    placeholder="Find by chat name..."
                />

            </div>
            <div className="all-chats-items">
                {chats.map((chat) => (
                    chat.is_private === false && (
                        <div className="chat-item" key={chat.id} onClick={() => { setInfoData({id: chat.id, chatNameData: chat.name}); setIsInfoList(!isInfoList); }}>
                            <p>{chat.name}</p>
                        </div>
                    )
                ))}
            </div>
            

            {isInfoList ? <AllMembers chatId={infoData.id} chatName={infoData.chatNameData} toggleInfo={() => setIsInfoList(!isInfoList)} /> : ""}
        </div>
    )
}

export default AllChats;