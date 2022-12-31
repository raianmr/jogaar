import { ChakraProvider } from "@chakra-ui/react"
import type { AppProps } from "next/app"
import Head from "next/head"
import { SWRConfig } from "swr"
import Footer from "../components/footer"
import Navbar from "../components/navbar"

import "bootstrap/dist/css/bootstrap.min.css"
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
          onError: err => {
            console.error(err)
          },
        }}>
        <ChakraProvider>
          <Navbar />

          <Component {...pageProps} />

          <Footer />
        </ChakraProvider>
      </SWRConfig>
    </>
  )
}
