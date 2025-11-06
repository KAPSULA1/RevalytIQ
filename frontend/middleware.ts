import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

const API_PREFIX = "/api/";
const BACKEND_ORIGIN = "https://revalytiq-backend.onrender.com";

export function middleware(request: NextRequest) {
  if (request.nextUrl.pathname.startsWith(API_PREFIX)) {
    const backendUrl = new URL(
      request.nextUrl.pathname,
      BACKEND_ORIGIN
    );
    backendUrl.search = request.nextUrl.search;
    return NextResponse.rewrite(backendUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/api/:path*"],
};
