import React from 'react';
import Head from 'next/head';
import '../styles/globals.css';

export default function App({ Component, pageProps }) {
  return (
    <>
      <Head>
        <title>AI Kamishibai • Indo-Japanese Cross-Cultural Visual Storytelling</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="description" content="An automated generative AI pipeline and interactive web application adapting ancient Indian folk tales into Japanese Kamishibai format with trilingual neural audio." />
        <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🎭</text></svg>" />
      </Head>
      <Component {...pageProps} />
    </>
  );
}
