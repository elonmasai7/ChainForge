import "./globals.css";

export const metadata = {
  title: "CreatorChain",
  description: "Initia-powered monetization platform for creators"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
