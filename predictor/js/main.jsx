import React from 'react';
import ReactDOM from 'react-dom';
import ParticlesBg from 'particles-bg'

// This method is only called once
ReactDOM.render(
    <React.Fragment>
      <h1>Enter the stock symbol (i.e. AAPL, GOOGL, etc.) to view future predictions! </h1>
      <form>
        <label>
            Stock:
            <input type="text" name="stock" />
        </label>
        <input type="submit" value="Submit" />
      </form>
      <ParticlesBg type="cobweb" bg={true} />
    </React.Fragment>,
    document.getElementById('reactEntry')
  );