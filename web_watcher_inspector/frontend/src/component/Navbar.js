import React, { Component } from 'react'
import "./Navbar.css"
import {
    BrowserRouter,
    Routes,
    Route,
    NavLink
} from "react-router-dom";
import Home from '../pages/Home';
import App from '../App';
import { globalVariables } from '../global';
class Navbar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isNavExpanded: false
        };
        this.handleNavClick = this.handleNavClick.bind(this);
    }
    handleNavClick() {
        this.setState(prevState => ({
            isNavExpanded: !prevState.isNavExpanded
        }));
    }
    render() {
        const { isNavExpanded } = this.state;
        return (
            <BrowserRouter>
                <nav className="navigation" id="navigation">
                    <a href="/" className="brand-name">
                        SAMPLE TEXT HERE
                    </a>
                    <button className="hamburger" onClick={this.handleNavClick}></button>
                    <div className={isNavExpanded ? "navigation-menu expanded" : "navigation-menu"}>
                        <ul>
                            <li>
                                <NavLink to={'/'}>Home</NavLink>
                            </li>
                            <li>
                                <NavLink to={'/about'}>About</NavLink>
                            </li>
                            <li>
                                <NavLink to={'/contact'}>Contact</NavLink>
                            </li>
                        </ul>
                    </div>
                </nav>
                <Routes>
                    <Route index element={<Home />} />
                    <Route path='/about' element={<App />} /> 
                    <Route path='*' element={<div>NOT FOUND</div>} /> IF ROUTES NOT MATCHED
                </Routes>
            </BrowserRouter>
                
        )
    }
}
export default Navbar;