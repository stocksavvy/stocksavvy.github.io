import React from 'react';
import ReactDOM from 'react-dom';
import App from './app'
import "../static/css/style.css";



// This method is only called once
ReactDOM.render(
    <div>
        <App />
    </div>,
    document.getElementById('reactEntry')
  );