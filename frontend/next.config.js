/** @type {import('next').NextConfig} */
const nextConfig = {
  trailingSlash: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://revalytiq-backend.onrender.com/api/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
