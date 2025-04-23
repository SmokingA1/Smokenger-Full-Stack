import logo from "../../images/logo.jpg"
import React from 'react';
import { Link } from "react-router-dom";
import "../../styles/components/Header.css"

const Header = ({toggleIsChatVisible}) => {
    return(
        <header>
            <span className='header-name-content'>
                <img src={logo} alt='logo' className='header-logo'></img>
                <h3>Smokenger</h3>
            </span>
            <nav className='header-nav-menu'>
                <button className="button-all-chats" onClick={toggleIsChatVisible}>All Chats</button>
                <p>
                    <Link className="link-account" to="/me">My Accont</Link>    
                </p>    
            </nav>
        </header>
    )
}

export default Header;
