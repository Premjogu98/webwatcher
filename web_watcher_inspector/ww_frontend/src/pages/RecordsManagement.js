import React, { Component } from 'react';
import ReactTable6 from '../component/ReactTable';


class RecordsManagement extends Component {
    constructor(props) {
        super(props);
    }
    render() {

        return (
            <div className="records-management">
                <ReactTable6 />
            </div>
        );
    }
}

export default RecordsManagement;
