import type { NextConfig } from "next";

const backendInternalUrl = process.env.BACKEND_INTERNAL_URL ?? "http://127.0.0.1:8000";

const nextConfig: NextConfig = {
  output: "standalone",
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${backendInternalUrl}/api/:path*`,
      },
      {
        source: "/uploads/:path*",
        destination: `${backendInternalUrl}/uploads/:path*`,
      },
      {
        source: "/healthz",
        destination: `${backendInternalUrl}/healthz`,
      },
    ];
  },
};

export default nextConfig;
