import './globals.css';
import '@fontsource/inter/400.css';
import '@fontsource/inter/500.css';
import '@fontsource/inter/600.css';
import '@fontsource/poppins/400.css';
import '@fontsource/poppins/500.css';
import '@fontsource/poppins/600.css';
import '@fontsource/ibm-plex-mono/400.css';
import './typography.css';
import type { Metadata } from 'next';
export const metadata: Metadata = {title:'FlowGuard Sentinel | Financial workspace',description:'Human-supervised financial recovery, with verifiable authorization. Synthetic competition sandbox.'};
export default function RootLayout({children}:{children:React.ReactNode}) {return <html lang="en"><body>{children}</body></html>}
