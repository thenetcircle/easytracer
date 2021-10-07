import { useCallback, useRef, useState } from 'react'
import Link from 'next/link'
import styles from './search.module.css'

export default function Search() {
    const searchRef = useRef(null)
    const [active, setActive] = useState(false)
    const [results, setResults] = useState([])

    const searchEndpoint = (query) => `/api/search?q=${query}`

    const onSubmit = useCallback((event) => {
        event.preventDefault();

        console.log('onSubmit, eventId:', event.target.eventId.value)

        if (event.target.eventId.value.length) {
            fetch(searchEndpoint(event.target.eventId.value))
                .then(res => res.json())
                .then(res => {
                    setResults(res.results)
                })
        } else {
            setResults([])
        }
    }, [])

    return (
        <div
            className={styles.container}
            ref={searchRef}
        >
            <form onSubmit={onSubmit}>
                <label htmlFor="eventId">Event ID</label>
                <input
                    id="eventId"
                    className={styles.search}
                    type='text'
                />
                <button type="submit">Search</button>
            </form>

            {active && results.length > 0 && (
                <ul className={styles.results}>
                    {results.map(({ id, title }) => (
                        <li className={styles.result} key={id}>
                            <Link href="/posts/[id]" as={`/posts/${id}`}>
                                <a>{title}</a>
                            </Link>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    )
}