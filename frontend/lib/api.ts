export const money = (value: number | string = 0) => new Intl.NumberFormat('en-CN', {style:'currency',currency:'CNY',maximumFractionDigits:0}).format(Number(value));
export const exactMoney = (value: number | string = 0) => new Intl.NumberFormat('en-CN', {style:'currency',currency:'CNY',minimumFractionDigits:2,maximumFractionDigits:2}).format(Number(value));
export const dateLabel = (value: string) => new Date(value+'T12:00:00').toLocaleDateString('en-GB',{day:'numeric',month:'short'});
export async function api<T>(path:string,identity:string,method='GET',body?:unknown):Promise<T> {const response=await fetch('/api'+path,{method,headers:{'Content-Type':'application/json','X-Demo-User':identity},...(body!==undefined?{body:JSON.stringify(body)}:{})});const data=await response.json();if(!response.ok)throw new Error(typeof data.detail==='string'?data.detail:JSON.stringify(data.detail||data));return data;}
export type Business={id:string;name:string;sector:string;scenario:string};
export type Invoice={id:string;customer:string;recipient:string;amount:number;paid:number;due_date:string;status:string;description:string};
export type Expense={id:string;vendor:string;amount:number;date:string;category:string;flexible:boolean};
export type Proposal={id:string;business_id:string;type:string;target_id:string;recipient?:string;new_date?:string;amount:number;reason:string;message:string;status:string;execution?:unknown};
export type Dashboard={business:Business;current_cash:number;minimum_balance:number;shortfall_date:string|null;shortfall_amount:number;overdue_total:number;forecast:{date:string;inflow:number;outflow:number;balance:number;conservative_balance:number}[];invoices:Invoice[];expenses:Expense[];verification:{status:string;message:string};proposals:Proposal[]};
