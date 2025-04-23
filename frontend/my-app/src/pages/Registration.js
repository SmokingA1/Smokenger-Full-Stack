import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import "../styles/components/Registration.css"
import { Link } from "react-router-dom"; // Импорт компонента Link для создания ссылок
import api from "../api";

const Register = () => {
    const [fullName, setFullName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [repeatPassword, setRepeatPassword] = useState("");
    const [phoneNumber, setPhoneNumber] = useState("");

    const navigate = useNavigate();

    const registerUser = async (user_create) => {
        try {
            const response = await api.post("/users/signup", user_create);
            console.log(response.data);
            setFullName("");
            setEmail("");
            setPassword("");
            setRepeatPassword("");
            setPhoneNumber("");
            navigate("/login")
        } catch (error) {
            if (error.response) {
                console.error("Error during registration:", error.response.data.detail);
                alert("Error during registration: " + error.response.data.detail);
            } else {
                console.error("Ошибка сети или другие проблемы:", error.message);
            }
        }
    }

    const [errors, setErrors] = useState({});

    const handleRegister = async (e) => {
        e.preventDefault();
        
        let newErrors = {};
        
        if (!email) newErrors.email = "Email is required";
        if (!password) newErrors.password = "Password is required";
        if (password !== repeatPassword) newErrors.repeatPassword = "Passwords do not match";

        setErrors(newErrors); // Обновляем ошибки

        // Если нет ошибок, логируем данные
        if (Object.keys(newErrors).length === 0) {
            await registerUser(
                {
                    "full_name": fullName,
                    "email": email,
                    "password": password,
                    "phone_number": phoneNumber
                }
            )
        }
    };


    return(
        <div className="register-app">
            <div className="register-container">
                <h2>Register Account</h2>
                <form onSubmit={handleRegister} className="register-form">
                    <label>Name</label>
                    <input 
                        type="text"
                        value={fullName}
                        onChange={(e) => setFullName(e.target.value)}
                    />
                    <label>Email</label>
                    <input 
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        
                    />
                    {errors.email &&<p className="error-message">{errors.email}</p>}
                    <label>Password</label>
                    <input 
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className={errors.password ? "error-input" : ""}
                    />
                    {errors.password && <p className="error-message">{errors.password}</p>}
                    <label>Repeat password</label>
                    <input 
                        type="password"
                        value={repeatPassword}
                        onChange={(e) => setRepeatPassword(e.target.value)}
                        className={errors.repeatPassword ? "error-input" : ""}
                    />
                    {errors.repeatPassword && <p className="error-message">{errors.repeatPassword}</p>}
                    <label>Phone number</label>
                    <input 
                        type="text"
                        value={phoneNumber}
                        onChange={(e) => setPhoneNumber(e.target.value)}
                    />
                    <button className="register-button" type="submit">Register</button>
                </form>
                <span className="nav-register">
                    <p>
                        <Link to='/login' className="link-login">Already have an account? Login</Link>
                    </p>
                </span>
            </div>
        </div>


    )
}

export default Register;