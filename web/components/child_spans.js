import { Component } from 'react'
import styles from './search.module.css'

class ChildSpans extends Component {
    render() {
        return (
            <>
                {this.props.children.length > 0 && (
                    <>
                        {this.props.children.map((child, id) => (
                            <div className={styles.container} key={id}>
                                <div
                                    style={{
                                        width: 1000 * (child.event.elapsed / this.props.root_event.elapsed),
                                        left: 1000 * (child.event.created_at - this.props.root_event.created_at) / this.props.root_event.elapsed
                                    }}
                                    className="relative bg-blue-200 border-solid border-2 border-gray-600 p-2 m-1"
                                >
                                    <p className="mt-1 text-sm text-gray-900">
                                        {child.event.service_name}: {child.event.name} ({child.event.elapsed} ms)
                                    </p>
                                </div>

                                <ChildSpans children={child.children} root_event={this.props.root_event} />
                            </div>
                        ))}
                    </>
                )}
            </>
        )
    }
}

export default ChildSpans;
