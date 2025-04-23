import React, { useEffect, useState } from "react";
import api from "../api";
import "../styles/components/MyAccount/MyAccount.css"
import default_icon from "../images/user-icons/default_icon.jpg"
import { useNavigate } from "react-router-dom";

const MyAccount = () => {
    const [error, setError] = useState("");
    const [errorName, setErrorName] = useState("");
    const [userData, setUserData] = useState(null);
    const [newName, setNewName] = useState("");
    const [isVisibleEditForm, setIsVisibleEditForm] = useState(false);


    const navigate = useNavigate();

    const deleteCookie = async () => {
        try {
            const response = await api.get("/clear-cookie")
            console.log(response.data)
        } catch (error) {
            console.error("Some type of error occured: ", error)
        }
    }

    const updateName = async () => {
        let newError = "";

        if (newName.length <= 1 || newName.length > 40) {
            newError = "New name must be between 2 and 40 characters.";
        }

        setErrorName(newError);
        if (errorName.length === 0) {
            try {
                const response = await api.put("/users/me/update/name", {new_name: newName }, );
                console.log(response.data);
                setIsVisibleEditForm(false);
                setNewName("");
                await fetchUserData();
            } catch (error) {
                console.error("Some error occured while editing user name: ", error);
            }
        }
        
    }

    const fetchUserData = async () => {
        try {
            const response = await api.get('/users/me')
            console.log(response.data)
            setUserData(response.data)
        } catch (err) {
            console.error("Error receiving user data:", err);
            setError("Uploading data was unsuccessfully!")
        }
    }
    
    useEffect(() => {
        fetchUserData();
    }, []);
    
    return(
        <div className="profile-page">
            {error ? (
                <p style={{ color: "red" }}>{error}</p>
            ) : userData ? (
                <div className="profile-container">

                    <div id="navigate-to-home" onClick={() => navigate("/")}> 
                        <i style={{fontSize: 22 + "px"}} className="bi bi-arrow-left"></i>
                    </div>

                    {isVisibleEditForm ? 
                        (
                            <div className="main-data">
                                <img src={default_icon} alt="User icon" className='user-icon'></img>
                                <span>
                                    <strong>Name: </strong> 
                                    <input 
                                        className="user-update-field"
                                        type="text" 
                                        value={newName}
                                        onChange={(e) => setNewName(e.target.value)}
                                        placeholder={userData.full_name}
                                    />
                                </span>
                                
                                <button className="btn-acc-u confirm-btn-acc" onClick={() => updateName()}><i className="bi bi-check2"></i></button>
                                <button className="btn-acc-u edit-btn-acc" onClick={() => setIsVisibleEditForm(!isVisibleEditForm)}><i className="bi bi-pencil-square"></i></button>

                            </div>
                        ) : (
                            <div className="main-data">
                        
                                <img src={default_icon} alt="User icon" className='user-icon'></img>
                                <span><strong>Name:</strong> {userData.full_name}</span>
                                <button className="btn-acc-u edit-btn-acc" onClick={() => setIsVisibleEditForm(!isVisibleEditForm)}><i className="bi bi-pencil-square"></i></button>
                            </div>
                        )
                    }
                    
                    
                    <div className="second-data">
                        <p><strong>Email:</strong> {userData.email}</p>
                        <p><strong>Phone number:</strong> {userData.phone_number}</p>
                    </div>


                    <div className="account-buttons-actions">
                        <button className="log-out-button" onClick={() => {deleteCookie(); navigate("/login");} }>Log out</button>
                    </div>
                </div>
            ) : (
                <p>Загрузка...</p>
            )}
        </div>
    )
}

export default MyAccount;