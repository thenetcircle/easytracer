import Head from 'next/head'
import Layout, { siteTitle } from '../components/layout'
import Search from '../components/search'
import utilStyles from '../styles/utils.module.css'

export default function Home() {
  return (
    <Layout home>
      <Head>
        <title>{siteTitle}</title>
      </Head>
      <section className={utilStyles.heading2Xl}>
        <p>
          {siteTitle}
        </p>
      </section>
      <section className={utilStyles.headingMd}>
        <p>
          Find traces for either event ID or context ID
        </p>
      </section>

      <Search />
    </Layout>
  )
}