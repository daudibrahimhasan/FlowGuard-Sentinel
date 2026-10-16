const {defineConfig}=require('@playwright/test');
module.exports=defineConfig({testDir:'.',testMatch:'workflow.spec.cjs',timeout:60000,workers:1,reporter:[['list'],['json',{outputFile:'../../submission/browser-results.json'}]],use:{baseURL:'http://127.0.0.1:3000',viewport:{width:1440,height:1050},trace:'retain-on-failure'},outputDir:'test-results'});
