import { Component } from 'react'
import styles from './trace_header.module.css'

class TraceHeader extends Component {
    render() {
        return (
            <>
                <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                    <div className="px-4 py-5 sm:px-6">
                        <h3 className="text-lg leading-6 font-medium text-gray-900">
                            Trace for event
                        </h3>
                        <p className="mt-1 max-w-2xl text-sm text-gray-500">
                            {this.props.result.event.event_id}
                        </p>
                    </div>
                    <div className="border-t border-gray-200">
                        <dl>
                            <div className={styles.row_gray}>
                                <dt className={styles.column_key}>
                                    Context ID
                                </dt>
                                <dd className={styles.column_value}>
                                    {this.props.result.event.context_id}
                                </dd>
                            </div>
                            
                            <div className={styles.row_white}>
                                <dt className={styles.column_key}>
                                    Trace ID
                                </dt>
                                <dd className={styles.column_value}>
                                    {this.props.result.event.trace_id}
                                </dd>
                            </div>

                            <div className={styles.row_gray}>
                                <dt className={styles.column_key}>
                                    Span ID
                                </dt>
                                <dd className={styles.column_value}>
                                    {this.props.result.event.span_id}
                                </dd>
                            </div>

                            <div className={styles.row_white}>
                                <dt className={styles.column_key}>
                                    Trace started at
                                </dt>
                                <dd className={styles.column_value}>
                                    {new Intl.DateTimeFormat(
                                        'sv-SE',
                                        {
                                            year: 'numeric',
                                            month: '2-digit',
                                            day: '2-digit',
                                            hour: '2-digit',
                                            minute: '2-digit',
                                            second: '2-digit'
                                        }).format(
                                            this.props.result.event.created_at * 1000
                                        )
                                    }
                                </dd>
                            </div>

                            <div className={styles.row_gray}>
                                <dt className={styles.column_key}>
                                    Runtime
                                </dt>
                                <dd className={styles.column_value}>
                                    {this.props.result.event.elapsed} ms
                                </dd>
                            </div>
                        </dl>
                    </div>
                </div>
            </>
        )
    }
}

export default TraceHeader;
