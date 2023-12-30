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
import { ViewContent } from './component/ViewContent';

class App extends Component {
    constructor(props) {
        super(props);
    }
    render() {

        return (
            <Router>
                <>
                    <Navbar />
                    <>
                        <Routes>

                            <Route index element="" />
                            <Route path='/web-inspector' element={<WebInspector />} />
                            <Route path='/records' element={<RecordsManagement />} />
                            <Route path='/comparison' element={<ComparisonManagement />} />
                            {/* <Route path='*' element={<div>PAGE NOT FOUND</div>} />  IF ROUTES NOT MATCHED */}
                        </Routes>
                    </>
                </>
                <Routes>
                    <Route path='/page/:id' element={<ViewContent />} />
                </Routes>
            </Router>


        );
    }
}

export default App;
