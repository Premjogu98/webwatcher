import React from 'react';
// import ReactDOM from 'react-dom';
import ReactDOM from 'react-dom';
import './index.css';
import Filters from './component/Filters';
import ShowContent from './component/ShowContent';
import App from './Main';
import Home from './pages/Home';
import Navbar from './component/Navbar';
// const root = ReactDOM.createRoot(document.getElementById('root'));
// root.render(
//   <React.StrictMode>
//     {/* <App /> */}
//     <Home />
//   </React.StrictMode>
// );
// ReactDOM.render(<Home />, document.getElementById('root'));

ReactDOM.render(
    <React.StrictMode>
      <Navbar />
    </React.StrictMode>,
    document.getElementById('root')
  );
  