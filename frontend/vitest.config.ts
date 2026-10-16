import {defineConfig} from 'vitest/config';
import path from 'node:path';
export default defineConfig({resolve:{alias:{'@':path.resolve(__dirname,'.')}},oxc:{jsx:{runtime:'automatic'}},test:{environment:'jsdom',setupFiles:['./test-setup.ts'],exclude:['node_modules/**','.next/**','.npm-cache/**']}});
