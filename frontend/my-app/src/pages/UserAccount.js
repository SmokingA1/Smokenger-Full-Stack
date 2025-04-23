import React, { useEffect, useState, useCallback} from "react";
import { useParams } from "react-router-dom";
// import { Link } from "react-router-dom";
import "../styles/pages/UserAccount.css"
import api from "../api";
import default_icon from "../images/user-icons/default_icon.jpg"

const UserAccount = () => {
    const { user_id } = useParams(); // Получаем user_id из URL
    const [userData, setUserData] = useState({});

    const getUser = useCallback(async () => {
        try {
            console.log(`ID IS HERE :  ${user_id}`)
            const response = await api.get(`/users/${user_id}`);
            setUserData(response.data);
        } catch (error) {
            console.error("Some error during displaying user occurred: ", error);
        }
    }, [user_id]);

    useEffect(() => {
        getUser();
    }, [getUser])

    return(
        <div className="user-account-app">
            <div className="user-account-container">
                <div className="user-account-main-data">
                    <img className="user-icon" src={default_icon} alt="user icon"></img>
                    {userData.full_name}
                </div>
                
            </div>
        </div>
        
    )


}

export default UserAccount;