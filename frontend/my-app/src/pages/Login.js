    import React, { useState } from "react";
    import "../styles/components/Login.css"
    import { Link } from "react-router-dom";
    import { useNavigate } from "react-router-dom";
    import api from "../api";

    const Login = () => {
        const [email, setEmail] = useState("");
        const [password, setPassword] = useState("");
        const navigate = useNavigate();

        const handleLogin = async (e) => {
            e.preventDefault(); // Предотвращаем перезагрузку страницы при сабмите формы
            console.log({
                "username": email,
                "password": password
            })
            try {
                const formData = new URLSearchParams();
                formData.append("username", email);
                formData.append("password", password);

                const response = await api.post("/login/access-token", formData, {
                    headers: { "Content-Type": "application/x-www-form-urlencoded"}
                });

                alert(response.data.data)

                console.log("Login successful!")
                navigate('/')
            } catch (error) {
                console.error("Ошибка при входе:", error);
                alert("Ошибка: " + error.response?.data?.detail);
            }
        }

        return(
            <div className="login-app">
                <div className="login-container">
                <h2>Login</h2>
                <form onSubmit={handleLogin} className="login-form">
                    <label>Email</label>
                    <input 
                        type="text"
                        placeholder="Enter email here"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)} 
                        autoComplete="username"
                    />
                    <label>Password</label>
                    <input 
                        type="password" 
                        placeholder="Enter password here"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        autoComplete="current-password"
                    />
                    <button className="login-button" type="submit">LOG IN</button>
                </form>

                <span className="nav-links">
                    <p>
                        <Link className="link-lf link-register" to="/register">Don't have an account? Register</Link>    
                    </p>        
                    <p>
                        <Link className="link-lf link-forgot-password" to='/forgot-password'> 
                            Forgot password?
                        </Link>
                    </p>        
                </span>
            </div>
            </div>
            
        )
    }

    export default Login;