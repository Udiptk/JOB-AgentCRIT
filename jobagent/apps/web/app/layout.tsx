import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "OBSIDIAN.INTEL | HYBRID_DASHBOARD",
  description: "Autonomous multi-agent career concierge",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark h-full antialiased">
      <head>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Space+Grotesk:wght@300;400;500;700&display=swap" rel="stylesheet" />
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
      </head>
      <body className="min-h-full flex flex-col bg-background text-on-surface font-body selection:bg-primary selection:text-on-primary">
        {children}
      </body>
    </html>
  );
}
