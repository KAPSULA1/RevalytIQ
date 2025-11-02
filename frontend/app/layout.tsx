import "./../styles/globals.css";
import { ReactNode } from "react";
import { Toaster } from "react-hot-toast";
import Providers from "../lib/Providers";

export const metadata = {
  title: "RevalytIQ Dashboard",
  description: "SaaS analytics admin panel",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900">
        <Providers>
          {children}
          <Toaster position="top-right" />
        </Providers>
      </body>
    </html>
  );
}
