import React from 'react';
import { globalVariables } from '../globalVariables/global';

class Logout extends React.Component {
    constructor(props) {
        super(props);
    }
    componentDidMount () {
        sessionStorage.removeItem(globalVariables.authKey);
        window.location.href = '/login'
    }
    
    render() {
        return (
            <></>
        );
    }
}

export default Logout;
