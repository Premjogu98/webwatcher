import React, { Component } from 'react';
import "./Loader.css"
class Loader extends Component {
    constructor(props) {
        super(props);
        this.state = {
            load: 0
        };
    }
    componentDidMount() {
        this.interval = setInterval(() => {
            const { load } = this.state;
            if (load < 100) {
                this.setState({ load: load + 1 });
            } else {
                // Just to make it repeat, reset load to 0 after 2 seconds
                setTimeout(() => {
                    this.setState({ load: 0 });
                }, 2000);
            }
        }, 50);
    }
    componentWillUnmount() {
        clearInterval(this.interval);
    }

    render() {
        const { load } = this.state;
        return (
            <div id="loader-d">
                <span id="loader-s">{load} %</span>
            </div>
        );
    }
}

export default Loader;
