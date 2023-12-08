import React, { Component } from 'react'
import "./Navbar.css"
import {
    NavLink
} from "react-router-dom";

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
                            <NavLink to={'/web-inspector'}>Web Inspector</NavLink>
                        </li>
                        <li>
                            <NavLink to={'/comparison'}>Comparison</NavLink>
                        </li>
                        <li>
                            <NavLink to={'/records'}>Check Records</NavLink>
                        </li>
                    </ul>
                </div>
            </nav>


        )
    }
}
export default Navbar;