import { Component, useCallback, useRef, useState } from 'react'
import Link from 'next/link'
import styles from './search.module.css'

class Search extends Component {
    state = {
        result: undefined
    }

    searchEndpoint = (query) => `/api/search?q=${query}`

    handleSubmit = (event) => {
        event.preventDefault();

        if (event.target.eventId.value.length) {
            fetch(this.searchEndpoint(event.target.eventId.value))
                .then(res => res.json())
                .then(res => {
                    console.log('got res:', res[0])
                    this.setState({
                        result: res[0]
                    });
                })
        } else {
            this.setState({
                result: undefined
            });
        }
    }

    render() {
        return (
            <div className={styles.container}>
                <form onSubmit={this.handleSubmit}>
                    <label htmlFor="eventId">Event ID</label>
                    <input
                        id="eventId"
                        className={styles.search}
                        type='text'
                    />
                    <button type="submit" className="btn btn-green">Search</button>
                </form>

                {this.state.result && (
                    <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                        <div className="px-4 py-5 sm:px-6">
                            <h3 className="text-lg leading-6 font-medium text-gray-900">
                                Trace for event
                            </h3>
                            <p className="mt-1 max-w-2xl text-sm text-gray-500">
                                {this.state.result.event.event_id}
                            </p>
                        </div>
                        <div className="border-t border-gray-200">
                            <dl>
                                <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                    <dt className="text-sm font-medium text-gray-500">
                                        Trace ID
                                    </dt>
                                    <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                        {this.state.result.event.trace_id}
                                    </dd>
                                </div>
                                <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                    <dt className="text-sm font-medium text-gray-500">
                                        Span ID
                                    </dt>
                                    <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                        {this.state.result.event.span_id}
                                    </dd>
                                </div>
                                <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                    <dt className="text-sm font-medium text-gray-500">
                                        Trace started at
                                    </dt>
                                    <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                        {this.state.result.event.created_at}
                                    </dd>
                                </div>
                            </dl>
                        </div>
                    </div>
                )}

                {this.state.result && this.state.result.children.length > 0 && (
                    <div>
                        {this.state.result.children.map((child, id) => (
                            <div key={id}>{child.event.event_id}</div>
                        ))}
                    </div>
                )}
            </div>
        )
    }
}

export default Search;
