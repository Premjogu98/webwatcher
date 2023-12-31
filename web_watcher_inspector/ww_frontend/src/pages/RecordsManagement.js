import React, { Component } from 'react';
import ReactTable6 from '../component/ReactTable';
import { QueryClientProvider, QueryClient } from 'react-query';
import { ReactQueryDevtools } from 'react-query/devtools';
import WeakMap from '../component/WebWTable';

const queryClient = new QueryClient();

class RecordsManagement extends Component {
    constructor(props) {
        super(props);
    }

    render() {

        return (
            <div className="records-management">
                {/* <ReactTable6 /> */}
                <QueryClientProvider client={queryClient} >
                    <WeakMap />
                    <ReactQueryDevtools initialIsClose position={"bottom-right"} />
                </QueryClientProvider>
            </div>
        );
    }
}

export default RecordsManagement;
