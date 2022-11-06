import type { AppProps } from "next/app"
import Head from "next/head"
import Footer from "../components/footer"
import Navbar from "../components/navbar"
import "../styles/globals.css"

export default function App({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <title>Jogaar Admins</title>
        <meta name="description" content="Dashboard for mods and admins." />
      </Head>

      <Navbar />

      <main>
        <Component {...pageProps} />
      </main>

      <Footer />
    </>
  )
}
