import { Component, useCallback, useRef, useState } from 'react'
import ChildSpans from './child_spans'
import Link from 'next/link'
import styles from './search.module.css'
import TraceHeader from './trace_header'

class Search extends Component {
    state = {
        results: []
    }

    searchEndpoint = (eventId, contextId) => `/api/search?e=${eventId}&c=${contextId}`

    handleSubmit = (event) => {
        event.preventDefault();

        if (event.target.eventId.value.length || event.target.contextId.value.length) {
            fetch(this.searchEndpoint(event.target.eventId.value, event.target.contextId.value))
                .then(res => res.json())
                .then(res => {
                    console.log('got res:', res)
                    this.setState({
                        results: res
                    });
                })
        } else {
            this.setState({
                results: []
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
                    <label htmlFor="eventId">Context ID</label>
                    <input
                        id="contextId"
                        className={styles.search}
                        type='text'
                    />
                    <button type="submit" className="btn btn-green">Search</button>
                </form>

                {this.state.results.length > 0 && this.state.results.map((result, id) => (
                    <div className={styles.container} key={id}>
                        <TraceHeader result={result} />

                        <div className={styles.container}>
                            <div className="m-4 border-solid border-2 border gray-400 p-4">
                                <div
                                    style={{ width: 500 }}
                                    className="bg-blue-200 border-solid border-2 border-gray-600 p-2 m-1"
                                >
                                    {result.event.service_name}: {result.event.name} ({result.event.elapsed} ms)
                                </div>

                                <ChildSpans children={result.children} root_event={result.event} />
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        )
    }
}

export default Search;
