import React, { useEffect, useState, useCallback, useRef} from "react";
import "../../styles/components/Chats/Chat.css";
import api from "../../api";
import AllMembers from "./AllMembers";
import default_icon from "../../images/user-icons/default_icon.jpg"
  

const Chat = ( {chatId}) => {
    const [chat, setChat] = useState({});
    const [messages, setMessages] = useState([]);
    const [message, setMessage] = useState("");
    const [isMembersList, setIsMemberList] = useState(false);
    const [isActionsMessage, setIsActionsMessage] = useState(null);
    const [ws, setWs] = useState(null); // Состояние для WebSocket
    const [offset, setOffset] = useState(0);
    const chatContainerRef = useRef(null);  // реф на контейнер сообщений
    const isInitialLoad = useRef(true);




    const getChat = useCallback(async () => {
        if (!chatId) return;
        try {
            const response = await api.get(`/chats/${chatId}`);
            console.log(response.data)
            setChat(response.data);


        } catch (error) {
            console.error("Ошибка при загрузке чата:", error);
        }
    }, [chatId]); // Теперь getChat зависит от chatId

    const sendMessage = () => {
        if (!message || !ws || ws.readyState !== WebSocket.OPEN) return; // Если WebSocket не открыт, не отправляем

        ws.send(JSON.stringify(message)); // Отправляем сообщение через WebSocket
        setMessage(""); // Сбрасываем поле ввода
    };


    
    const fetchMessages = useCallback(async () => {
        try {
            console.log("PAGEEE NUM : ", offset);
            const response = await api.get(`/chat-messages/${chatId}?offset=${offset}`);
            console.log(response.data);
            setMessages((prev) => [...prev, ...response.data]);

        } catch (error) {
            console.error("Some error occured while fetching messages: ", error);
        }
    }, [offset, chatId]);


    const deleteMessage = async ({messageId}) => {
        try {
            const response = await api.delete(`/chat-messages/delete/${messageId}`)
            console.log(response.data)
            setMessages((prevMessages) => prevMessages.filter((msg) => msg.id !== messageId));
        } catch (error) {
            console.error("Some error occured: ", error)
        }
    }

    const handleScroll = () => {
        const container = chatContainerRef.current;
        console.log("Scroll Top" , container.scrollTop);      // Текущая прокрученная высота
        console.log("Scrool Height", container.scrollHeight);  // Общая высота контента
        console.log("Client Height", container.clientHeight);  // Высота видимой области
        console.log("Solution", container.scrollHeight - container.clientHeight - 1)
        console.log(Math.abs(container.scrollTop) === container.scrollHeight - container.clientHeight- 1)
        if (Math.abs(container.scrollTop) >= container.scrollHeight - container.clientHeight - 1) {
            
            setOffset((prev) => prev + 20);
            console.log("Offset:", offset);
        }
        
        
    };
    

    const handleMouseDown = (e, messageId) => {
        if (e.button === 2) {

            if (messageId !== isActionsMessage) {
                setIsActionsMessage(messageId);
            } else {
                setIsActionsMessage(null);
            }
        } else {
            setIsActionsMessage(null);
        }
    };
    


    useEffect(() => {
        setMessages([]);
        setOffset(0);
        if (chatId) {
            getChat();
         }
    }, [chatId, getChat]);
    


    useEffect(() => {
        if (isInitialLoad.current) {
            isInitialLoad.current = false;
            return;
        }

        fetchMessages();
    }, [offset, fetchMessages]);
        


    function getCookie(name) {
        const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return match ? decodeURIComponent(match[2]) : null;
    }


    useEffect(() => {
        if (!chatId) return;
      
        const token = getCookie("access_token"); // или как называется твоя кука
        const ws = new WebSocket(`ws://localhost:8000/ws/${chatId}?token=${token}`);
        setWs(ws)

        ws.onopen = () => {
          console.log("✅ WebSocket соединение установлено");
        };
      
        ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data); // предполагаем, что ты шлёшь JSON
            setMessages((prev) => [data, ...prev]); // добавляем сообщение в начало
          } catch (error) {
            console.error("Ошибка при получении WS-сообщения:", error);
          }
        };
      
        ws.onerror = (err) => {
          console.error("❌ WebSocket ошибка:", err);
        };
      
        ws.onclose = () => {
          console.log("🔌 WebSocket соединение закрыто");
        };
      
        return () => {
          ws.close(); // Закрываем соединение при размонтировании
        };
      }, [chatId]);
      

    return (
        <div className="chat-container">
            {isMembersList ? (
                <div className="container-members">
                    <AllMembers chatId={chatId} toggleList={() => setIsMemberList(false)} chatName={chat.name}/>
                    <div className="shadow-background"></div>
                    
                </div>
            ) : ""}
            <div className="chat-name" key={chat.id} onClick={() => setIsMemberList(!isMembersList)}>
                {chat.name} 
            </div>

            <div className="chat-message-container" onScroll={handleScroll} ref={chatContainerRef}>
                {/* <div className="messages-container">  */}
                    {messages.length > 0 ? (
                        messages.map((msg) => {
                            
                            const date = new Date(msg.created_at);
                            const formattedTime = date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
                    
                            return (
                                <div className="message-container"  key={msg.id}>
                                    <div className="message-icon">
                                        <img className="chat-user-icon" src={default_icon} alt="user-icon"></img>
                                    </div>

                                    <span className="chat-message" onMouseDown={(e) => handleMouseDown(e, msg.id)}
                                        onContextMenu={(e) => e.preventDefault()}
                                    >
                                        <span id="chat-message-sender-name">{msg.sender.full_name}</span>
                                        <span className="chat-message-content">
                                            {msg.content} <small>{formattedTime}</small>
                                        </span>
                                        
                                       
                                    </span>
                                    {isActionsMessage === msg.id && (
                                            <div className="message-actions">
                                                <button onClick={() => {deleteMessage({messageId: msg.id})}} className="message-delete-button"><i className="bi bi-trash"></i></button>
                                            </div>
                                    )}
                                </div>
                                
                            );
                        })
                    ) : (
                    <span className="chat-emptiness">Start Messaging . . .</span>
                    )}
                            
                {/* </div> */}
            </div>

            <div className="chat-input-container">
                <input 
                    type="text"
                    placeholder="Write a message...."
                    value={message}
                    onChange={(e) => 
                        setMessage(e.target.value)
                    }
                />
                <button onClick={sendMessage} >Send</button>
            </div>
        </div>
    );
}

export default Chat;