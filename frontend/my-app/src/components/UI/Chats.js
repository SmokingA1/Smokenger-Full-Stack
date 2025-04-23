import React, { useEffect, useState, useCallback} from "react";
import api from "../../api";
import "../../styles/components/Chats/Chats.css"

import smoke_chat_icon from "../../images/smoke_chat_icon_ph.jpg"

const Chats = ( { setChatId }) => {
    const [chats, setChats] = useState([]);
    const [isAddChat, setIsAddChat] = useState(false);
    const [addChatForm, setAddChatForm] = useState(
        {
            "name": "",
            "is_private": false
        }
    )
    const [chatIdForMember, setChatIdForMember] = useState(0);


    const getChats = async () => {
        try {
            const response = await api.get(`/chats/my/`,
                {
                    withCredentials: true,                  
                }
            )

            setChats(response.data)
        } catch (error) {
            console.error("Some kind of error ooccured: ", error)
        }
    }


    const addChat = async () => {
        try {
            const response = await api.post('/chats/create', addChatForm)
            setChatIdForMember(response.data.id)
            setChats(prevChats => [...prevChats, response.data]); //
            setIsAddChat(false); // закрываем форму
            setAddChatForm({ name: "", is_private: false }); // сбрасываем форму
        } catch (error) {
            console.error("Some kind of error occured: ", error)
        }
    }
    

    const addMember = useCallback(async () => {
        if (chatIdForMember) {
            try {
                const response = await api.post(
                    `/chat-members/create/${chatIdForMember}`,
                    {},
                    { withCredentials: true }
                );
                console.log(response.data);
                console.log("Member was added successfully");
                setChatIdForMember(null);
            } catch (error) {
                console.error("Some error occurred: ", error);
            }
        }
    }, [chatIdForMember]); 

    useEffect(() => {
        if (chatIdForMember) {
          addMember();
        }
      }, [chatIdForMember, addMember]); // Будет вызываться каждый раз, когда chatIdForMember изменится
    

    const handleSubmit = async (event) => {
        event.preventDefault();
        await addChat();

    }

    useEffect(() => {
        const fetchChatsData = async () => {
            await getChats();
        }
        fetchChatsData()
    }, [])


    return (
        <div className="chats-container">
            {isAddChat ?(
                <div className="chat-add-container">
                    <div className="close-chat-add-container"> 
                        <button className="close-container-button"
                                onClick={() => setIsAddChat(!isAddChat)}
                        ><i className="bi bi-x"></i></button>
                    </div>
                    <form className="chat-add-form" onSubmit={handleSubmit}>
                        <label>Name</label>
                        <input
                                className="chat-add-form-name-input"
                                type="text"
                                value={addChatForm.name}
                                placeholder="Enter a name of the chat"
                                onChange={(e) => 
                                    setAddChatForm(prev => ({ ...prev, name: e.target.value }))
                                }
                            />
                        <label>Private?</label>
                        <input 
                            id="chkbx"
                            type="checkbox" 
                            checked={addChatForm.is_private} 
                            onChange={(e) => 
                                setAddChatForm(prev => ({ ...prev, is_private: e.target.checked }))
                            }
                        />

                        <button className="confirm-add-chat-button" type="submit">
                            ADD CHAT
                        </button>
                    </form>
                </div>

                
            ) : ""}

            <button onClick={()=> setIsAddChat(!isAddChat)} className="add-chat-button">ADD CHAT<i className="bi bi-plus"></i></button>
            
            {chats.map((chat) => (
                <div 
                    className="chat-own-item" key={chat.id}
                    onClick={() => setChatId(chat.id)}>
                    <div className="marquee-wrapper">
                        <span className="chats-own-name">
                                {chat.name}
                        </span>
                    </div>

                    <img src={smoke_chat_icon} alt="chat-icon" className="chat-icon-default"></img>

                </div>
            ))
            }

        </div>
    )
}

export default Chats;