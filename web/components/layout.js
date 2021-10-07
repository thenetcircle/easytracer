import Head from 'next/head'
import Image from 'next/image'
import styles from './layout.module.css'
import utilStyles from '../styles/utils.module.css'
import Link from 'next/link'

export const siteTitle = 'EasyTracer'

export default function Layout({ children, home }) {
  return (
    <div className={styles.container}>
      <Head>
        <link rel="icon" href="/favicon.ico" />
        <meta
          name="description"
          content="EasyTracer"
        />
        <meta name="og:title" content={siteTitle} />
      </Head>
      <header className={styles.header}>
      </header>

      <main>{children}</main>

    </div>
  )
}