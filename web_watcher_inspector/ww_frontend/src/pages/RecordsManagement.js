import React, { Component } from 'react';
import ReactTable6 from '../component/ReactTable';
import { QueryClientProvider, QueryClient } from 'react-query';
import { ReactQueryDevtools } from 'react-query/devtools';
import WeakMap from '../component/WebWTable';
import { globalVariables } from '../globalVariables/global';

const queryClient = new QueryClient();

class RecordsManagement extends Component {
    constructor(props) {
        super(props);
    }
    componentDidMount () {
        const AUTH = localStorage.getItem(globalVariables.authKey);
        if (AUTH === globalVariables.authStatus){
            console.log("succsess")
        }else{
            window.location.href = '/login'
        }
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
