import React, { Component } from 'react';
import Navbar from './component/Navbar';
import RecordsManagement from './pages/RecordsManagement';
import {
    BrowserRouter as Router,
    Routes,
    Route
} from "react-router-dom";
import ComparisonManagement from './pages/ComparisonManagement';
import WebInspector from './pages/WebInspector';
import InspectContent from './component/InspectContent';
import LoginPage from './pages/LoginPage';
import Logout from './pages/Logout';

class App extends Component {
    constructor(props) {
        super(props);

    }
    NotFoundRedirect() {
        window.location.href = '/login'
        return
    }
    render() {
        return (
            <Router>
                <>
                    <Routes>
                        <Route path='/home' element={<Navbar />} />
                        <Route path='/login' element={<LoginPage />} />
                        <Route path='/web-inspector' element={<><Navbar /><WebInspector /></>} />
                        <Route path='/records' element={<><Navbar /><RecordsManagement /></>} />
                        {/* <Route path='/comparison/:id' element={<><Navbar /><ComparisonManagement /></>} /> */}
                        <Route path='/comparison/:id' element={<><ComparisonManagement /></>} />
                        <Route path='/inspect/:id' element={<InspectContent />} />
                        <Route path='/logout' element={<Logout />} />
                        <Route path='*' element={this.NotFoundRedirect} />  {/*IF ROUTES NOT MATCHED */}
                    </Routes>
                </>
            </Router>


        );
    }
}

export default App;
