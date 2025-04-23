import React, {useState} from "react";

import Header from "../components/UI/Header";
import Chats from "../components/UI/Chats";
import Chat from "../components/UI/Chat";
import AllChats from "../components/UI/AllChats"

import "../styles/components/Home.css"

function Home() {
  const [isChatVisible, setIsChatVisible] = useState(false)
  const [chatId, setChatId] = useState(null);

  return (
    <div className='App'>
      <Header toggleIsChatVisible={() => setIsChatVisible(!isChatVisible)}/>
      <div className='main-container'>
        <Chats setChatId={setChatId}/>
        {chatId ? (<Chat chatId={chatId} />) : 
          (<div className="chat-container"></div>)
        }
        {isChatVisible ? (
          <div className="modal-overlay">
            <AllChats toggleIsChatVisible={() => setIsChatVisible((!isChatVisible))}/> 
          </div>
          ) : ""}
      </div>
    </div>
  );
}


export default Home;
