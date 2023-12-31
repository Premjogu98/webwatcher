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
import { InspectContent } from './component/ViewContent';

class App extends Component {
    constructor(props) {
        super(props);
    }
    render() {

        return (
            <Router>
                <>
                    {/* <Navbar /> */}
                    {/* <> */}
                        <Routes>
                            <Route index element={<Navbar />} />
                            <Route path='/web-inspector' element={<><Navbar /><WebInspector /></>} />
                            <Route path='/records' element={<><Navbar /><RecordsManagement /></>} />
                            <Route path='/comparison' element={<><Navbar /><ComparisonManagement /></>} />
                            <Route path='/inspect/:id' element={<InspectContent />} />
                            <Route path='*' element={<div>PAGE NOT FOUND</div>} />  {/*IF ROUTES NOT MATCHED */}
                        </Routes>
                    {/* </> */}
                </>
            </Router>


        );
    }
}

export default App;
