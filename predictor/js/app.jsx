import React from 'react';
import Query from './query';
import ParticlesBg from 'particles-bg';


class App extends Component {
    constructor() {
      super();
      this.state = {
        name: "React"
      };
    }
  
    render() {
      return (
        <div>
          <Query/>
          <ParticlesBg type="cobweb" bg={true}/>
        </div>
      );
    }
  }

  export default App;