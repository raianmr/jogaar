import type { AppProps } from "next/app"
import Head from "next/head"
import { SWRConfig } from "swr"
import Footer from "../components/footer"
import Navbar from "../components/navbar"
import { fetchJson } from "../data/fetching"

import "../styles/globals.css"

export default function App({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <title>Jogaar Moderation</title>
        <meta name="description" content="Dashboard for mods and admins." />
      </Head>

      <SWRConfig
        value={{
          fetcher: fetchJson,
          onError: err => {
            console.error(err)
          },
        }}>
        <Navbar />

        <Component {...pageProps} />

        <Footer />
      </SWRConfig>
    </>
  )
}
