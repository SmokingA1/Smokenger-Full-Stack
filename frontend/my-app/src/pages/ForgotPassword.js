import React, { useState } from "react";
import "../styles/pages/ForgotPassword.css"
import { useNavigate } from "react-router-dom";


const ForgotPassword = () => {
    const [email, setEmail] = useState("");
    const [error, setError] = useState("");

    let navigate = useNavigate();

    const sendEmail = async () => {
        let newError = '';

        if (!email) {
            newError = 'Field cannot be empty!';
        } else if  (!email.includes("@")) {
            newError = 'Email must contain  \'@\' '
        } 

        setError(newError);
        
        if(!newError) { // condition работает когда true но к нам приходит true и конвертируется в false, значит нам должно прийти false или ""
            try {
                // axios.post()
                console.log(email);
                navigate("/login");
            } catch (error) {
                console.error("Some error occured: ", error); 
            }
        }
        
    }

    return (
        <div className="forgot-password-page">
            <div className="forgot-password-container">
                <div className="forgot-password-input-data">
                    <label style={{marginLeft: 2 + "px"}}>
                        Email:
                    </label>
                    <input 
                        className={error ? "error-input" : ""}
                        id="forgot-password-input"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Enter your email..."                
                    />
                    {error && <p className="error-message">{error}</p>}

                </div>
               

                <button className="forgot-password-button" onClick={() => sendEmail()}>
                    SEND EMAIL
                </button>
            </div>
        </div>
    )
}

export default ForgotPassword;