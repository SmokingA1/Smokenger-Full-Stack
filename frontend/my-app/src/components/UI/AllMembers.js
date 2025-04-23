import React, { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api";
import "../../styles/components/AllMembers.css"
import default_icon from "../../images/user-icons/default_icon.jpg"

const AllMembers = ( { chatId, toggleList, chatName, toggleInfo }) => {
    const [members, setMembers] = useState([]);
    const [isVisibleADD, setIsVisibleADD] = useState(false);
    const [currentUser, setCurrentUser] = useState(null);
    const [isVisibleAddForm, setIsVisibleAddForm] = useState(false);
    const [userByPhone, setUserByPhone] = useState();
    const [phoneMember, setPhoneNumber] = useState("");

    const navigate = useNavigate();

    const getUserMe = useCallback(async () => {
        try { 
            const response = await api.get('/users/me');
            setCurrentUser(response.data);
            console.log(response.data.id)
        } catch (error) {
            console.error("Some error occured while receiving current user: ", error);
        }
    }, [chatId])

    const getUser = async () => {
        try {
            const response = await api.get("/users/phone", {
                params: { user_phone: phoneMember }
            });
            setUserByPhone(response.data)
        } catch (error) {
            console.error("Error during find data by phone: ", error);
        }
    }

    const joinToChat = async () => {
        try {
            const response = await api.post(`/chat-members/create`, 
                {
                "chat_id": chatId,
                "user_id": currentUser.id
                }
            );
            console.log(response.data);
        } catch (error) {
            console.error("Error during adding new member to chat: ", error);
        }
    }


    const getMembers = useCallback(async () => {
        try {
            console.log(chatId)
            const response = await api.get(`/chat-members/${chatId}/members`);
            setMembers(response.data)
        
        } catch (error) {
            console.error("Display members was unsuccessfully with erro: ", error)
        }
    }, [chatId])


    const removeMember = async () => {
        try {
            const response = await api.delete(`/chat-members/remove-me/${chatId}`, {}, {
                withCredentials: true,
            });
            console.log(response.data);
            navigate(0);
        } catch (error) {
            console.error("Some type of error occured: ", error);
        }
    }


    const addMember = async () => {
        try {
            const response = await api.post(`/chat-members/create`, 
                {
                "chat_id": chatId,
                "user_id": userByPhone.id
                }
            );
            console.log(response.data);
        } catch (error) {
            console.error("Error during adding new member to chat: ", error);
        }
    }


    const deleteChat = async () => {
        try {
            const response = await api.delete(`/chats/delete/${chatId}`);
            if (response.data) {
                navigate(0);    
            }

        } catch (error) {
            console.error("Some type of error occured while deleting a chat: ", error);
        }
    }

    const handleGetUser = async (e) => {
        e.preventDefault();
        await getUser();
    }

    const handleNavigate = ({memberId}) => {
        console.log(memberId)
        navigate(`/user-account/${memberId}`)
    }
    
    useEffect(() => {
        getMembers();
        getUserMe();
    }, [chatId, getMembers, getUserMe]);


    return(
        <div>
            {isVisibleAddForm ? (
                <div className="cnt2 container-chat-info">
                    <form className="input-search-user-form" onSubmit={handleGetUser}>
                        <input 
                        className="input-search-user-field"
                        type="text"
                        value={phoneMember}
                        onChange={(e) => setPhoneNumber(e.target.value)}
                        placeholder="Enter the phone number here..."
                        />

                        <button className="search-user-button"
                        type="submit">Search</button>
                    </form>

                        
                    {userByPhone ? (
                        <div className="input-search-user-user" >
                            <div className="input-search-user-user-info" onClick={() => handleNavigate({memberId: userByPhone.id})}>
                                <img  src={default_icon} alt="user-icon" style={{width: 40 + "px", borderRadius: 50 + "%", marginRight: 10 + "px"}}></img>
                                {userByPhone.full_name}
                            </div >
                           
                            <button className="input-search-user-button-add"
                            onClick={() => addMember()}
                            >
                                Add
                            </button>

                        </div>) : ""
                    }
                        
                    
                    <button className="button-close-search-form" onClick={() => setIsVisibleAddForm(!isVisibleAddForm)}>Cancel</button>
                </div>) 
                
                
                : (
                <div className="container-chat-info">
                    <div className="chat-info-header">
                    <span id="chat-info-name">{chatName}</span>
                    
                    {!toggleInfo ? 
                        (<div id="chat-container-additional-actions">
                            <button onClick={() => setIsVisibleADD(!isVisibleADD)} id="chat-info-additionaly"><i className="bi bi-three-dots-vertical"></i></button>
                            {isVisibleADD && (
                                <div id="chat-info-additionaly-form">
                                    <button className="chat-butt chat-leave-button" onClick={() => removeMember()}>Leave group</button>
                                    <button className="chat-butt chat-add-button" onClick={() => setIsVisibleAddForm(!isVisibleAddForm)}>Add member</button>
                                    <button className="chat-butt chat-delete-button" onClick={() => deleteChat()}>Delete chat</button>
                                </div>
                            )}
                        </div>
                        ) : ""                  
                
                    }
                    </div>
                    
                    <span id="chat-info-members">Members</span>
                    <div className="container-chat-members">
                    {members ? (
                        members.map((member) => (
                            <div className="chat-member" key={member.id} onClick={() => handleNavigate({memberId: member.user.id})}>
                                <img style={{width: 40 + "px", borderRadius: 50 + "%", marginRight: 10 + "px"}} src={default_icon} alt="user-icon"></img>
                                {member.user.full_name}
                            </div>
                        ))

                    ) : ""}
                    </div>

                    {toggleList ? (
                                <button onClick={() => toggleList()} className="cinfobtns chat-info-cancel-button">Cancel</button>
                            )   :

                            (
                                <div className="chat-info-cj-buttons">

                                {/* if currentUser was received CurrentUser = true, if in members is currentUser = true converts to false and button doesn't display!!!     */}
                                {currentUser && !members.some(member => member.user.id === currentUser.id) &&
                                             (<button onClick={() => joinToChat()} className="cinfobtns chat-info-join-button">Join</button>)}
                                <button onClick={() => toggleInfo()} className="cinfobtns chat-info-cancel-button">Cancel</button>
                                </div>
                            )
                           
                    }

                </div>)
            }
            
        </div>
        
    )
}


export default AllMembers;