import { Component } from 'react'
import styles from './search.module.css'

function colorByHashCode(value) {
    return "<span style='color:" + value.getHashCode().intToHSL() + "'>" + value + "</span>";
}

function getHashCode(value) {
    var hash = 0;
    if (value.length == 0) return hash;
    for (var i = 0; i < value.length; i++) {
        hash = value.charCodeAt(i) + ((hash << 5) - hash);
        hash = hash & hash; // Convert to 32bit integer
    }
    return hash;
};

const intToHSL = function (value) {
    var shortened = value % 360;
    return "hsl(" + shortened + ",85%,90%)";
};

/* bg-blue-200 */

class ChildSpans extends Component {
    render() {
        return (
            <>
                {this.props.children.length > 0 && (
                    <>
                        {this.props.children.map((child, id) => (
                            <>
                                <div style={{ width: 1420 }} className="flex flex-row">
                                    <div style={{ width: 80 }} className="text-right">
                                        <p style={{ display: "inline-block" }} className="text-sm text-gray-600">
                                            {Math.floor(child.event.elapsed)} ms
                                        </p>
                                    </div>

                                    <div style={{ width: 20 }}></div>

                                    <div style={{ width: 300 }} className="hover:bg-blue-100">
                                        <p style={{ display: "inline-block" }} className="text-sm text-gray-500">
                                            {child.event.name}
                                        </p>
                                    </div>
                                    
                                    <div style={{ width: 20 }} className="border-l-2"></div>

                                    <div style={{ width: 1000 }} className="hover:bg-blue-100" key={id}>
                                        <div
                                            style={{
                                                /* 980 instead of 1000 to account for paddings and margins */
                                                width: 980 * ((child.event.elapsed / 1000) / (this.props.root_event.elapsed / 1000)),
                                                left: 980 * (child.event.created_at - this.props.root_event.created_at) / (this.props.root_event.elapsed / 1000),

                                                /* generate a light color based on the name, to group spans visually */
                                                backgroundColor: intToHSL(getHashCode(child.event.name))
                                            }}
                                            className="relative border-solid border-2 border-gray-600 p-2 m-1"
                                        >
                                        </div>
                                    </div>
                                </div>

                                <ChildSpans children={child.children} root_event={this.props.root_event} parent_left={
                                    980 * (child.event.created_at - this.props.root_event.created_at) / (this.props.root_event.elapsed / 1000) - this.props.parent_left
                                } />
                            </>
                        ))}
                    </>
                )}
            </>
        )
    }
}

export default ChildSpans;
