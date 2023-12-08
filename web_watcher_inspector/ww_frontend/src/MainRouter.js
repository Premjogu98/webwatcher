import React, { Component } from 'react';
import Navbar from './component/Navbar';
import RecordsManagement from './pages/RecordsManagement';
import {
    BrowserRouter as Router,
    Routes,
    Route,
    NavLink
} from "react-router-dom";
import ComparisonManagement from './pages/ComparisonManagement';
import WebInspector from './pages/WebInspector';

class App extends Component {
    constructor(props) {
        super(props);
    }
    render() {

        return (
            <Router>
                <>
                    <Navbar />
                    <div className='content'>
                        <Routes>
                            <Route index element="" />
                            <Route path='/web-inspector' element={<WebInspector />} />
                            <Route path='/records' element={<RecordsManagement />} />
                            <Route path='/comparison' element={<ComparisonManagement />} />
                            <Route path='*' element={<div>NOT FOUND</div>} />  {/* IF ROUTES NOT MATCHED */}
                        </Routes>
                    </div>
                </>
            </Router>
        );
    }
}

export default App;
