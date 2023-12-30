import React, { Component } from 'react';
import { useParams } from 'react-router-dom';

export const ViewContent = () => {
    // Accessing URL parameters using useParams hook from react-router-dom
    const { id } = useParams(); // Assuming the parameter name is 'id'

    return (
        <div>
            <h1>Parameter Value: {id}</h1>
        </div>
    );
};
// class ViewContent extends Component {
//     constructor() {
//         super();
//         this.state = {
//         };
//     }

//     render() {
//         return (
//             <>
//                 {console.log(this.props)}
//                 <h1>{this.props.match}</h1>
//             </>
//         );
//     }
// }

// export default ViewContent;