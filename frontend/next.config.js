/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    unoptimized: true,
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://127.0.0.1:8000/api/:path*',
      },
      {
        source: '/panels/:path*',
        destination: 'http://127.0.0.1:8000/panels/:path*',
      },
      {
        source: '/audio/:path*',
        destination: 'http://127.0.0.1:8000/audio/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
