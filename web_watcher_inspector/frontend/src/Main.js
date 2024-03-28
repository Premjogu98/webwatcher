import React, { Component } from 'react';
import Loader from './component/Loader';
import Filters from './component/Filters';
import ShowContent from './component/ShowContent';
import TextComparison from './pages/comparison';
import Navbar from './component/Navbar';
import Home from './pages/Home';

class App extends Component {
    constructor(props) {
        super(props);
    }

    render() {

        return (
            <div className="App">
                {/* <Loader /> */}
                {/* <Home /> */}
                {/* <TextComparison /> */}
                {/* <Filters />
                <ShowContent /> */}
                <Navbar />
            </div>
        );
    }
}

export default App;
