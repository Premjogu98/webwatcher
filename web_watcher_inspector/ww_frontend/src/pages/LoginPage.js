import React from 'react';
import './LoginPage.css'; // Import your CSS file
import { globalVariables } from '../globalVariables/global';

class LoginPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
        };
    }
    componentDidMount () {
        const AUTH = localStorage.getItem(globalVariables.authKey);
        if (AUTH === globalVariables.authStatus){
            window.location.href = '/home'
            console.log(AUTH)
        }
    }
    handleUsernameChange = (e) => {
        this.setState({ username: e.target.value });
    };

    handlePasswordChange = (e) => {
        this.setState({ password: e.target.value });
    };

    handleLogin = (e) => {
        e.preventDefault();
        const { username, password } = this.state;
        const main_username = globalVariables.loginUsername;
        const main_password = globalVariables.loginPassword;
        if (username === main_username && password === main_password) {
            localStorage.setItem(globalVariables.authKey, globalVariables.authStatus);
            window.location.href = '/home'
        } else {
            alert('Invalid credentials. Please try again.');
        }
    };

    render() {
        return (
            <div className="login-container">
                <form className="login-form" onSubmit={this.handleLogin}>
                    <h2>
                        <strong className='strong1'>TOT</strong>&nbsp;
                        <strong className='strong2'>WebWatcher</strong>
                    </h2>
                    <div className="input-group">
                        <label>Username:</label>
                        <input
                            type="text"
                            value={this.state.username}
                            onChange={this.handleUsernameChange}
                            required
                        />
                    </div>
                    <div className="input-group">
                        <label>Password:</label>
                        <input
                            type="password"
                            value={this.state.password}
                            onChange={this.handlePasswordChange}
                            required
                        />
                    </div>
                    <button className='login-btn' type="submit">Login</button>
                </form>
            </div>
        );
    }
}

export default LoginPage;
