/** @type {import('next').NextConfig} */
const nextConfig = {
  trailingSlash: true,
  skipTrailingSlashRedirect: true,
  async rewrites() {
    return {
      beforeFiles: [
        {
          source: '/api/:path*',
          destination: 'https://revalytiq-backend.onrender.com/api/:path*',
        },
      ],
    };
  },
};

module.exports = nextConfig;
